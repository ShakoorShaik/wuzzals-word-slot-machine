#!/usr/bin/env python3
"""
build_data.py -- build words.db from the supplied word list + WordNet + curated lists.

The vocabulary is read from `wordbase.txt` (one word per line). That file is the
~5,000-word list provided for this project; the build uses ONLY those words --
no words are added from any other source.

Pipeline:
  1. Read every word from wordbase.txt.
  2. For each word, ask WordNet which open classes it can be (noun/verb/adj/adverb).
  3. Layer in the curated closed classes and subcategory lists from curated.py.
  4. Derive noun subtypes (common/proper, concrete/abstract, countable/uncountable,
     collective), adjective subtypes, and adverb subtypes.
  5. Write the normalized SQLite database.

Re-run any time to rebuild from scratch:  python3 build_data.py
"""

import os
import sqlite3

import nltk
from nltk.corpus import wordnet as wn

import curated
from scoring import point_value

HERE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(HERE, "words.db")
SCHEMA_PATH = os.path.join(HERE, "schema.sql")
WORDBASE_PATH = os.path.join(HERE, "wordbase.txt")

CONCRETE_LEXNAMES = {
    "noun.animal", "noun.artifact", "noun.body", "noun.food",
    "noun.object", "noun.person", "noun.plant", "noun.substance",
    "noun.location", "noun.shape",
}

CLOSED_CLASS_WORDS = (
    curated.PRONOUNS | curated.PREPOSITIONS | curated.CONJUNCTIONS
    | curated.DETERMINERS | curated.INTERJECTIONS
)


CATEGORY_DEFS = [
    ("noun", "Nouns", None,
     "A person, place, thing, or idea (teacher, city, apple, courage)."),
    ("common_noun", "Common Nouns", "noun",
     "General, non-specific items, people, or places (city, dog, teacher)."),
    ("proper_noun", "Proper Nouns", "noun",
     "Specific, unique names; always capitalised (Niagara Falls, Sarah, Canada)."),
    ("concrete_noun", "Concrete Nouns", "noun",
     "Tangible things you can experience with your five senses (apple, ocean)."),
    ("abstract_noun", "Abstract Nouns", "noun",
     "Intangible concepts, ideas, emotions, or states (freedom, love, courage)."),
    ("countable_noun", "Countable Nouns", "noun",
     "Items that can be counted; have singular and plural forms (book/books)."),
    ("uncountable_noun", "Uncountable Nouns", "noun",
     "Masses or concepts that are not counted; usually no plural (water, advice)."),
    ("collective_noun", "Collective Nouns", "noun",
     "A group of people, animals, or things as one unit (team, flock, jury)."),

    ("pronoun", "Pronouns", None,
     "Replace nouns to avoid repetition (he, she, they, it)."),

    ("adjective", "Adjectives", None,
     "Describe or modify nouns (blue, tall, loud)."),
    ("descriptive_adjective", "Descriptive Adjectives", "adjective",
     "Describe size, shape, colour, or other qualities (big, blue, haunted)."),
    ("quantitative_adjective", "Quantitative Adjectives", "adjective",
     "Describe quantity or amount (three, several, much)."),
    ("demonstrative_adjective", "Demonstrative Adjectives", "adjective",
     "Indicate which specific noun is meant (this, that, these)."),
    ("proper_adjective", "Proper Adjectives", "adjective",
     "Formed from proper nouns; capitalised (Victorian, Canadian)."),

    ("adverb", "Adverbs", None,
     "Modify verbs, adjectives, or other adverbs (quickly, very, softly)."),
    ("manner_adverb", "Adverbs of Manner", "adverb",
     "Describe how an action is done (She spoke quietly)."),
    ("time_adverb", "Adverbs of Time", "adverb",
     "Indicate when something happens (We are leaving today)."),
    ("place_adverb", "Adverbs of Place", "adverb",
     "Specify where an action takes place (Put the books there)."),
    ("frequency_adverb", "Adverbs of Frequency", "adverb",
     "Tell how often an event occurs (They always arrive on time)."),
    ("degree_adverb", "Adverbs of Degree", "adverb",
     "Show intensity or level (The coffee is very hot)."),

    ("verb", "Verbs", None,
     "An action or state of being (run, is, think)."),
    ("preposition", "Prepositions", None,
     "Show relationships of time, space, or direction (in, on, at, under)."),
    ("conjunction", "Conjunctions", None,
     "Connect words, phrases, or clauses (and, but, because, although)."),
    ("determiner", "Determiners", None,
     "Introduce a noun and give context about quantity or possession (the, a, some)."),
    ("interjection", "Interjections", None,
     "Express sudden emotions or exclamations (wow, oh, ouch)."),
]


def get_base_words():
    """Read the supplied vocabulary from wordbase.txt (lower-cased, de-duped)."""
    if not os.path.exists(WORDBASE_PATH):
        raise RuntimeError(f"{WORDBASE_PATH} not found.")
    words, seen = [], set()
    with open(WORDBASE_PATH, encoding="utf-8-sig") as f:
        for line in f:
            w = line.strip().lower()
            if w and w not in seen:
                seen.add(w)
                words.append(w)
    return words


def wordnet_pos(word):
    """Set of open-class POS tags WordNet knows for `word`: n / v / a / r."""
    pos = set()
    for syn in wn.synsets(word):
        p = syn.pos()
        pos.add("a" if p == "s" else p)
    return pos


def categorize(word):
    """
    Return the set of category slugs that apply to `word` (lower-case).
    Returns an empty set if the word can't be confidently classified.
    """
    cats = set()
    pos = wordnet_pos(word)

    is_noun = "n" in pos
    is_verb = "v" in pos
    is_adj = "a" in pos
    is_adv = "r" in pos

    if word in curated.PRONOUNS:
        cats.add("pronoun")
    if word in curated.PREPOSITIONS:
        cats.add("preposition")
    if word in curated.CONJUNCTIONS:
        cats.add("conjunction")
    if word in curated.DETERMINERS:
        cats.add("determiner")
    if word in curated.INTERJECTIONS:
        cats.add("interjection")

    if is_noun:
        cats.add("noun")

        noun_syns = wn.synsets(word, pos=wn.NOUN)
        first = noun_syns[0] if noun_syns else None

        is_proper_noun = (
            not (is_verb or is_adj or is_adv)
            and word not in CLOSED_CLASS_WORDS
            and bool(noun_syns)
            and all(s.instance_hypernyms() for s in noun_syns)
        )

        if is_proper_noun:
            cats.add("proper_noun")
        else:
            cats.add("common_noun")

        lexname = first.lexname() if first else None
        if lexname in CONCRETE_LEXNAMES:
            cats.add("concrete_noun")
        else:
            cats.add("abstract_noun")

        if not is_proper_noun:
            if word in curated.UNCOUNTABLE_NOUNS:
                cats.add("uncountable_noun")
            else:
                cats.add("countable_noun")
            if word in curated.COLLECTIVE_NOUNS:
                cats.add("collective_noun")

    if is_verb or word in curated.MODAL_VERBS:
        cats.add("verb")

    adj_special = False
    if word in curated.QUANTITATIVE_ADJECTIVES:
        cats.add("adjective"); cats.add("quantitative_adjective"); adj_special = True
    if word in curated.DEMONSTRATIVE_ADJECTIVES:
        cats.add("adjective"); cats.add("demonstrative_adjective"); adj_special = True
    if word in curated.PROPER_ADJECTIVES:
        cats.add("adjective"); cats.add("proper_adjective"); adj_special = True
    if is_adj:
        cats.add("adjective")
        if not adj_special:
            cats.add("descriptive_adjective")

    adv_special = False
    if word in curated.TIME_ADVERBS:
        cats.add("adverb"); cats.add("time_adverb"); adv_special = True
    if word in curated.PLACE_ADVERBS:
        cats.add("adverb"); cats.add("place_adverb"); adv_special = True
    if word in curated.FREQUENCY_ADVERBS:
        cats.add("adverb"); cats.add("frequency_adverb"); adv_special = True
    if word in curated.DEGREE_ADVERBS:
        cats.add("adverb"); cats.add("degree_adverb"); adv_special = True
    if word in curated.MANNER_ADVERBS_EXTRA:
        cats.add("adverb"); cats.add("manner_adverb"); adv_special = True
    if is_adv:
        cats.add("adverb")
        if word.endswith("ly") or not adv_special:
            cats.add("manner_adverb")

    return cats


def build():
    print("Loading WordNet...")
    nltk.download("wordnet", quiet=True)
    nltk.download("omw-1.4", quiet=True)
    wn.ensure_loaded()

    base = get_base_words()
    print(f"Word base (from wordbase.txt): {len(base)} words")

    entries = {}
    unclassified = []
    for w in base:
        cats = categorize(w)
        if "proper_noun" in cats:
            entries[w.capitalize()] = (cats, True)
        else:
            entries[w] = (cats, False)
            if not cats:
                unclassified.append(w)

    print(f"Final vocabulary: {len(entries)} words "
          f"({len(unclassified)} could not be categorised: {', '.join(unclassified) or 'none'})")

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    with open(SCHEMA_PATH) as f:
        conn.executescript(f.read())

    cat_id = {}
    for sort_order, (name, display, parent, desc) in enumerate(CATEGORY_DEFS):
        parent_id = cat_id.get(parent) if parent else None
        cur = conn.execute(
            "INSERT INTO categories (name, display_name, parent_id, description, sort_order)"
            " VALUES (?,?,?,?,?)",
            (name, display, parent_id, desc, sort_order),
        )
        cat_id[name] = cur.lastrowid

    for text, (cats, is_proper) in entries.items():
        display = text.capitalize() if is_proper else text
        cur = conn.execute(
            "INSERT INTO words (text, display_text, is_proper, points) VALUES (?,?,?,?)",
            (text, display, 1 if is_proper else 0, point_value(display)),
        )
        wid = cur.lastrowid
        for c in cats:
            if c in cat_id:
                conn.execute(
                    "INSERT OR IGNORE INTO word_categories (word_id, category_id) VALUES (?,?)",
                    (wid, cat_id[c]),
                )
    conn.commit()

    print("\nWords per category:")
    rows = conn.execute(
        "SELECT c.display_name, COUNT(wc.word_id) n "
        "FROM categories c LEFT JOIN word_categories wc ON wc.category_id = c.id "
        "GROUP BY c.id ORDER BY c.sort_order"
    ).fetchall()
    for display, n in rows:
        print(f"  {display:<28} {n}")
    conn.close()
    print(f"\nDone -> {DB_PATH}")


if __name__ == "__main__":
    build()
