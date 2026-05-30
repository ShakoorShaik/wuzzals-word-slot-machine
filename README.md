# Word Slot Machine

Word Slot Machine is a classroom-friendly vocabulary game that helps students practice sentence building. Students choose one, two, or three word slots, select a grammatical category for each active slot, spin for random words, and then use those words in a sentence.

The app is intentionally simple for students, but the implementation has a real data pipeline behind it: a 5,000-word vocabulary list is categorized with WordNet plus curated grammar rules, stored in a normalized SQLite database, and served through a small Flask API.

## What It Does

- Lets students choose 1, 2, or 3 active word slots.
- Gives each active slot its own category dropdown.
- Supports broad categories such as nouns, verbs, adjectives, adverbs, pronouns, prepositions, conjunctions, determiners, and interjections.
- Supports subcategories such as concrete nouns, abstract nouns, countable nouns, descriptive adjectives, time adverbs, frequency adverbs, and more.
- Spins random words from the selected category for each slot.
- Lets students mark words they used in a sentence.
- Scores each used word by its letter count plus phonics-pattern bonuses.
- Displays each word's point value and an expandable scoring calculation below the "Used in sentence" button.
- Keeps the UI focused and student-friendly by hiding technical category metadata after the spin.

## Why This Project Is Interesting

This project combines a playful learning interface with a structured language-processing backend. It is not just a static random-word picker. It uses:

- a normalized relational database,
- many-to-many word/category relationships,
- hierarchical grammar categories,
- a rebuildable data pipeline,
- API-driven frontend state,
- per-slot category selection,
- SQLite random selection,
- and a responsive classroom-oriented UI.

It is designed to be understandable for young learners while still demonstrating thoughtful engineering decisions.

## Tech Stack

### Backend

- Python 3
- Flask
- SQLite
- NLTK
- WordNet

### Frontend

- HTML
- CSS
- Vanilla JavaScript
- Flask templates
- SVG branding asset

### Data

- `wordbase.txt`: source vocabulary list
- `curated.py`: curated grammar lists for categories WordNet does not handle well
- `build_data.py`: database build script
- `schema.sql`: SQLite schema
- `words.db`: generated SQLite database

## How It Works

### 1. Vocabulary Source

The project starts with `wordbase.txt`, a supplied vocabulary list of roughly 5,000 words. The build script reads this file, lowercases entries, removes duplicates, and keeps the vocabulary limited to the provided list.

### 2. Categorization Pipeline

The categorization logic lives in `build_data.py`.

For each word, the script asks WordNet which open-class parts of speech the word can be:

- noun
- verb
- adjective
- adverb

Then it layers in curated grammar lists from `curated.py` for categories WordNet does not reliably classify:

- pronouns
- prepositions
- conjunctions
- determiners
- interjections
- modal verbs
- uncountable nouns
- collective nouns
- quantitative adjectives
- demonstrative adjectives
- proper adjectives
- time/place/frequency/degree/manner adverbs

This means a word can belong to multiple categories. For example, a word may be both a noun and a verb.

### 3. Database Design

The database uses a normalized many-to-many structure:

```text
words  <-- word_categories --> categories
```

Important tables:

- `words`: vocabulary entries and display text
- `categories`: grammar categories and subcategories
- `word_categories`: joins words to all categories they belong to

Categories can also have parents. For example:

```text
Nouns
  Concrete Nouns
  Abstract Nouns
  Countable Nouns
  Uncountable Nouns
```

This makes the UI easier to organize and keeps the data model flexible.

### 4. Flask API

The Flask app exposes three main routes:

```text
GET /
```

Serves the main Word Slot UI.

```text
GET /api/categories
```

Returns all categories, parent relationships, descriptions, sort order, and live word counts.

```text
GET /api/spin
```

Returns random words for the selected slot categories.

Example:

```text
/api/spin?category=noun&category=verb&category=adjective&count=3
```

This asks the backend for one noun, one verb, and one adjective.

### 5. Point Calculation

Each word starts with one point per letter. The app then applies phonics-pattern bonuses such as CVC, CVCC, silent-e endings, vowel teams, r-controlled patterns, and ending patterns.

When multiple rules match without overlapping, their points are added together. When rules overlap, the scorer keeps the higher-value or more specific match. This prevents a smaller rule from double-counting inside a larger rule, such as `CH` inside `TCH`.

The API returns both the final point total and a scoring breakdown so the frontend can show students exactly how the value was calculated.

### 6. Random Word Selection

Random selection happens in SQLite using:

```sql
ORDER BY RANDOM()
```

For multi-slot spins, the frontend sends one `category` parameter per active slot. The backend returns words in slot order. It also tries to avoid duplicate word IDs within a spin when possible.

### 7. Frontend Flow

The frontend is contained mainly in `templates/index.html`.

On page load:

1. The browser requests `/api/categories`.
2. JavaScript builds category dropdowns for each slot.
3. The user selects 1, 2, or 3 active slots.
4. The user picks categories for the active slots.
5. Pressing `SPIN!` calls `/api/spin`.
6. Returned words are displayed in the reel cards.
7. Students mark words as used in a sentence.
8. The score updates.

## Project Structure

```text
.
├── app.py                  # Flask app and API routes
├── build_data.py           # Builds words.db from wordbase + WordNet + curated lists
├── curated.py              # Hand-curated grammar lists
├── scoring.py              # Letter-count and phonics-rule point calculation
├── requirements.txt        # Python dependencies
├── schema.sql              # SQLite schema
├── wordbase.txt            # Source vocabulary list
├── words.db                # Generated SQLite database
├── static/
│   └── wuzzals-logo.svg    # Branding asset
└── templates/
    └── index.html          # Frontend UI, CSS, and JavaScript
```

## How To Run Locally

### 1. Clone The Repo

```bash
git clone https://github.com/YOUR_USERNAME/wuzzals-word-slot-machine.git
cd wuzzals-word-slot-machine
```

### 2. Create A Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Build The Database

The repo can include `words.db`, but if you want to rebuild it from source:

```bash
python3 build_data.py
```

This downloads the required NLTK WordNet data if needed and regenerates `words.db`.

### 5. Start The App

```bash
python3 app.py
```

Then open:

```text
http://127.0.0.1:5000
```

## API Examples

Get categories:

```bash
curl http://127.0.0.1:5000/api/categories
```

Spin three words from different categories:

```bash
curl "http://127.0.0.1:5000/api/spin?category=noun&category=verb&category=adjective&count=3"
```

Spin from all words:

```bash
curl "http://127.0.0.1:5000/api/spin?category=all&count=3"
```

## Implementation Highlights

- Rebuildable data pipeline from raw word list to categorized SQLite database.
- Hybrid categorization system using WordNet plus curated grammar lists.
- Normalized schema for words, categories, and many-to-many category membership.
- Hierarchical categories with parent-child relationships.
- Per-slot category selection in the frontend.
- API supports repeated `category` query parameters for multi-category spins.
- Responsive UI designed for classroom use on laptops, tablets, and projectors.
- Student-facing interface avoids overwhelming category metadata.
- Word scores are transparent: students can expand a calculation showing letter points and matched phonics rules.

## Potential Future Improvements

- Add a teacher dashboard for custom word lists.
- Add difficulty levels by grade or reading level.
- Add sentence submission and validation.
- Add multiplayer or classroom group mode.
- Add exportable score/session history.
- Add automated tests for the categorization pipeline and API routes.
