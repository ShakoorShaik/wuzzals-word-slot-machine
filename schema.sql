-- ===========================================================================
-- Word Slot Machine -- database schema
--
-- Design goal: represent each vocabulary word and the (many) grammatical
-- categories it belongs to, in a normalized relational structure.
--
-- A word is rarely just one thing. "apple" is a noun AND a common noun AND a
-- concrete noun AND a countable noun. "run" is a noun AND a verb. Modelling
-- this as columns/flags would not scale and would not let us add categories
-- later, so we use a classic many-to-many design:
--
--     words  <--  word_categories  -->  categories
--
-- Categories are themselves hierarchical (Noun -> Concrete Noun) via a
-- self-referencing parent_id, so the UI can group subcategories under their
-- parent part of speech.
-- ===========================================================================

PRAGMA foreign_keys = ON;

CREATE TABLE categories (
    id           INTEGER PRIMARY KEY,
    name         TEXT    NOT NULL UNIQUE,
    display_name TEXT    NOT NULL,
    parent_id    INTEGER REFERENCES categories(id) ON DELETE SET NULL,
    description  TEXT,
    sort_order   INTEGER NOT NULL DEFAULT 0
);

-- The vocabulary.
CREATE TABLE words (
    id           INTEGER PRIMARY KEY,
    text         TEXT    NOT NULL UNIQUE,
    display_text TEXT    NOT NULL,
    is_proper    INTEGER NOT NULL DEFAULT 0,
    points       INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE word_categories (
    word_id     INTEGER NOT NULL REFERENCES words(id)      ON DELETE CASCADE,
    category_id INTEGER NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
    PRIMARY KEY (word_id, category_id)
);

CREATE INDEX idx_wc_category ON word_categories(category_id);
CREATE INDEX idx_wc_word     ON word_categories(word_id);
CREATE INDEX idx_cat_parent  ON categories(parent_id);
