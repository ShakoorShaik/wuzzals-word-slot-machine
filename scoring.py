"""Word Slot point calculation rules."""

from dataclasses import dataclass


VOWELS = set("aeiou")


@dataclass(frozen=True)
class RuleMatch:
    label: str
    points: int
    start: int
    end: int
    text: str


CV_PATTERN_POINTS = {
    "VC": 2,
    "CVC": 2,
    "VCC": 2,
    "CVCC": 3,
    "CVCCVC": 5,
}

SILENT_E_GROUPS = {
    ("abe", "ade", "ake", "ale", "ame", "ane", "ase", "ate", "ave", "aze"): 2,
    ("ide", "ime", "ine", "ire", "ive", "ipe", "ize"): 2,
    ("ode", "oke", "ole", "one", "ote", "ope", "ove", "obe", "ome"): 2,
}

LITERAL_RULES = [
    ("ther", "THER", 4),
    ("tch", "TCH", 2),
    ("eigh", "EIGH", 3),
    ("igh", "IGH", 3),
    ("eer", "EER", 3),
    ("oor", "OOR", 3),
    ("ook", "OOK", 3),
    ("ear", "EAR", 3),
    ("ead", "EAD", 3),
    ("ain", "AIN", 3),
    ("air", "AIR", 3),
    ("oar", "OAR", 3),
    ("ion", "ION", 3),
    ("age", "AGE", 3),
    ("ary", "ARY", 3),
    ("are", "ARE", 3),
    ("arr", "ARR", 3),
    ("war", "WAR", 3),
    ("all", "ALL", 2),
    ("ull", "ULL", 2),
    ("oll", "OLL", 2),
    ("ank", "ANK", 3),
    ("ink", "INK", 3),
    ("onk", "ONK", 3),
    ("unk", "UNK", 3),
    ("ing", "ING", 3),
    ("ong", "ONG", 3),
    ("ang", "ANG", 3),
    ("ung", "UNG", 3),
    ("old", "OLD", 3),
    ("ice", "ICE", 3),
    ("ild", "ILD", 3),
    ("ind", "IND", 3),
    ("ace", "ACE", 3),
    ("th", "TH", 2),
    ("ch", "CH", 2),
    ("sh", "SH", 2),
    ("wh", "WH", 2),
    ("or", "OR", 2),
    ("ir", "IR", 2),
    ("er", "ER", 2),
    ("ay", "AY", 2),
    ("ee", "EE", 2),
    ("ow", "OW", 3),
    ("ew", "EW", 3),
    ("ue", "UE", 3),
    ("ar", "AR", 2),
    ("ur", "UR", 3),
    ("aw", "AW", 3),
    ("au", "AU", 3),
    ("oo", "OO", 3),
    ("ea", "EA", 3),
    ("oi", "OI", 3),
    ("oy", "OY", 3),
    ("ai", "AI", 3),
    ("oa", "OA", 3),
]

SUFFIX_RULES = [
    ("ore", "ORE", 2),
    ("le", "-LE", 2),
    ("ed", "ED", 2),
    ("ly", "LY (E sound)", 3),
    ("ar", "Ends in AR", 3),
    ("ge", "-GE (end of a word)", 3),
    ("ce", "-CE", 3),
    ("ure", "URE", 3),
]

LONG_I_Y_WORDS = {
    "by", "cry", "dry", "fly", "fry", "my", "ply", "pry", "shy",
    "sky", "sly", "spy", "try", "why", "wry",
}

AR_EXCEPTION_PREFIXES = ("war", "wor", "quar")


def letters_only(word):
    return "".join(ch.lower() for ch in word if ch.isalpha())


def base_points(word):
    return len(letters_only(word))


def cv_shape(word):
    return "".join("V" if ch in VOWELS else "C" for ch in word)


def add_literal_matches(matches, word, pattern, label, points):
    start = word.find(pattern)
    while start != -1:
        end = start + len(pattern)
        matches.append(RuleMatch(label, points, start, end, word[start:end]))
        start = word.find(pattern, start + 1)


def add_suffix_match(matches, word, suffix, label, points):
    if word.endswith(suffix):
        start = len(word) - len(suffix)
        matches.append(RuleMatch(label, points, start, len(word), word[start:]))


def raw_rule_matches(word):
    word = letters_only(word)
    matches = []
    if not word:
        return matches

    shape = cv_shape(word)
    if shape in CV_PATTERN_POINTS:
        matches.append(RuleMatch(shape, CV_PATTERN_POINTS[shape], 0, len(word), word))

    if word.endswith("ey"):
        add_suffix_match(matches, word, "ey", "Ends in EY (long E)", 2)
    elif word.endswith("y"):
        label = "Ends in Y (Long I)" if word in LONG_I_Y_WORDS else "Ends in Y (Long E)"
        add_suffix_match(matches, word, "y", label, 2)

    for endings, points in SILENT_E_GROUPS.items():
        for ending in endings:
            if word.endswith(ending):
                add_suffix_match(matches, word, ending, f"Silent E (-{ending.upper()})", points)

    for prefix in AR_EXCEPTION_PREFIXES:
        start = word.find(prefix)
        while start != -1:
            end = start + len(prefix)
            matches.append(RuleMatch("AR Exceptions", 5, start, end, word[start:end]))
            start = word.find(prefix, start + 1)

    for pattern, label, points in LITERAL_RULES:
        add_literal_matches(matches, word, pattern, label, points)

    for suffix, label, points in SUFFIX_RULES:
        add_suffix_match(matches, word, suffix, label, points)

    return matches


def non_overlapping_matches(matches):
    chosen = []
    occupied = set()
    for match in sorted(matches, key=lambda m: (-m.points, -(m.end - m.start), m.start, m.label)):
        span = set(range(match.start, match.end))
        if span and not occupied.intersection(span):
            chosen.append(match)
            occupied.update(span)
    return sorted(chosen, key=lambda m: (m.start, m.end, m.label))


def score_word(word):
    clean = letters_only(word)
    base = base_points(word)
    rules = non_overlapping_matches(raw_rule_matches(word))
    total = base + sum(rule.points for rule in rules)
    return {
        "total": total,
        "base": {
            "label": f"{base} {'letter' if base == 1 else 'letters'}",
            "points": base,
            "match": clean,
        },
        "rules": [
            {
                "label": rule.label,
                "points": rule.points,
                "match": rule.text,
            }
            for rule in rules
        ],
    }


def point_value(word):
    return score_word(word)["total"]
