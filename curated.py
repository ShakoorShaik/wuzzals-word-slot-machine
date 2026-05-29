"""
Curated word lists.

WordNet reliably tags the open word classes (noun / verb / adjective / adverb)
and gives a usable concrete-vs-abstract signal via its lexicographer files.
It does NOT reliably handle:

  * closed word classes (pronouns, prepositions, conjunctions, determiners,
    interjections) -- these are small, finite sets, so we list them in full;
  * fine noun subtypes (countable / uncountable / collective);
  * adjective subtypes (quantitative / demonstrative / proper);
  * adverb subtypes (manner / time / place / frequency / degree).

So those are curated here. Everything is lower-cased; the build script
matches against these sets. This is deliberately a maintainable data file:
to fix a miscategorised word later, edit a list here and re-run build_data.py.
"""

PRONOUNS = {
    "i", "you", "he", "she", "it", "we", "they",
    "me", "him", "her", "us", "them",
    "mine", "yours", "hers", "ours", "theirs",
    "myself", "yourself", "himself", "herself", "itself",
    "ourselves", "yourselves", "themselves", "oneself",
    "this", "that", "these", "those",
    "who", "whom", "whose", "which", "what", "whoever", "whomever",
    "whatever", "whichever",
    "anyone", "everyone", "someone", "no one", "nobody", "somebody",
    "anybody", "everybody", "anything", "everything", "something",
    "nothing", "none", "one", "ones", "another", "other", "others",
    "each", "either", "neither", "both", "all", "any", "some", "few",
    "many", "several", "such",
}

PREPOSITIONS = {
    "about", "above", "across", "after", "against", "along", "amid",
    "among", "amongst", "around", "as", "at", "atop", "before", "behind",
    "below", "beneath", "beside", "besides", "between", "beyond", "by",
    "concerning", "despite", "down", "during", "except", "for", "from",
    "in", "inside", "into", "like", "near", "of", "off", "on", "onto",
    "opposite", "out", "outside", "over", "past", "per", "regarding",
    "round", "since", "than", "through", "throughout", "till", "to",
    "toward", "towards", "under", "underneath", "until", "unto", "up",
    "upon", "via", "versus", "with", "within", "without",
}

CONJUNCTIONS = {
    "and", "but", "or", "nor", "for", "yet", "so",
    "after", "although", "as", "because", "before", "if", "once",
    "since", "than", "that", "though", "unless", "until", "when",
    "whenever", "where", "whereas", "wherever", "whether", "while",
    "why", "how", "lest", "provided", "supposing", "albeit", "whereby",
    "however", "moreover", "therefore", "thus", "hence", "otherwise",
    "nevertheless", "nonetheless", "consequently", "furthermore",
    "meanwhile", "instead", "accordingly", "likewise",
}

DETERMINERS = {
    "the", "a", "an",
    "this", "that", "these", "those",
    "my", "your", "his", "her", "its", "our", "their", "whose",
    "all", "any", "both", "each", "either", "enough", "every", "few",
    "fewer", "less", "little", "many", "more", "most", "much", "neither",
    "no", "several", "some",
    "what", "which", "another", "other",
}

INTERJECTIONS = {
    "wow", "oh", "ouch", "hey", "hi", "hello", "hmm", "oops", "yay",
    "ugh", "ah", "aha", "alas", "bravo", "hooray", "hurray", "eh",
    "phew", "yikes", "gosh", "darn", "whoa", "oof", "yeah", "yep",
    "nope", "nah", "huh", "ow", "ooh", "aw", "eek", "gee", "golly",
    "jeez", "psst", "shh", "tsk", "um", "uh", "well", "yes", "no",
    "bye", "goodbye", "congratulations", "please", "thanks", "cheers",
    "boo", "ha", "hmph", "meh", "gah", "blah", "yuck", "ick", "hush",
    "behold", "amen", "encore", "indeed", "absolutely", "exactly", "aye",
}

MODAL_VERBS = {
    "can", "could", "shall", "should", "will", "would",
    "may", "might", "must", "ought",
}

UNCOUNTABLE_NOUNS = {
    "water", "air", "oxygen", "hydrogen", "nitrogen", "helium", "gas",
    "steam", "smoke", "fog", "mist", "rain", "snow", "ice", "hail",
    "sand", "dust", "dirt", "mud", "soil", "gravel", "salt", "sugar",
    "pepper", "flour", "rice", "pasta", "bread", "butter", "cheese",
    "milk", "cream", "yogurt", "honey", "jam", "oil", "vinegar", "sauce",
    "soup", "cereal", "meat", "beef", "pork", "fruit", "juice", "coffee",
    "tea", "wine", "beer", "alcohol", "liquor", "soda", "lemonade",
    "chocolate", "candy", "gum", "corn", "wheat", "grain", "hay", "grass",
    "wood", "timber", "metal", "gold", "silver", "iron", "steel",
    "copper", "aluminum", "plastic", "rubber", "glass", "cardboard",
    "cloth", "fabric", "cotton", "wool", "silk", "leather", "fur", "ink",
    "paint", "glue", "soap", "shampoo", "toothpaste", "lotion", "perfume",
    "makeup", "jewelry", "clothing", "furniture", "equipment",
    "machinery", "luggage", "baggage", "garbage", "trash", "rubbish",
    "junk", "stuff", "money", "cash", "currency", "wealth", "income",
    "traffic", "transportation", "electricity", "energy", "fuel",
    "gasoline", "heat", "music", "noise", "silence", "information",
    "knowledge", "wisdom", "intelligence", "education", "research",
    "evidence", "proof", "advice", "news", "gossip", "feedback",
    "homework", "housework", "work", "employment", "business", "progress",
    "help", "assistance", "support", "fun", "entertainment", "leisure",
    "recreation", "sleep", "rest", "relaxation", "health", "fitness",
    "hygiene", "nutrition", "weather", "climate", "nature", "scenery",
    "pollution", "waste", "recycling", "agriculture", "vocabulary",
    "grammar", "spelling", "punctuation", "literature", "poetry",
    "drama", "comedy", "history", "geography", "mathematics", "math",
    "arithmetic", "algebra", "geometry", "physics", "chemistry",
    "biology", "economics", "philosophy", "psychology", "technology",
    "software", "hardware", "courage", "bravery", "honesty", "loyalty",
    "patience", "kindness", "generosity", "creativity", "imagination",
    "curiosity", "confidence", "pride", "dignity", "respect", "trust",
    "faith", "hope", "love", "hatred", "anger", "fear", "joy",
    "happiness", "sadness", "grief", "sorrow", "despair", "loneliness",
    "jealousy", "envy", "guilt", "shame", "freedom", "liberty",
    "justice", "equality", "democracy", "peace", "violence", "safety",
    "security", "luck", "fortune", "beauty", "truth", "reality", "magic",
    "gravity", "friction", "pressure", "humidity", "warmth",
}

COLLECTIVE_NOUNS = {
    "team", "flock", "herd", "jury", "family", "committee", "crew",
    "staff", "board", "panel", "audience", "crowd", "mob", "gang",
    "band", "choir", "orchestra", "cast", "troupe", "company",
    "association", "club", "society", "union", "league", "group",
    "batch", "bunch", "cluster", "pack", "pride", "swarm", "colony",
    "litter", "brood", "pod", "army", "navy", "fleet", "squad",
    "platoon", "regiment", "battalion", "congregation", "class",
    "faculty", "department", "government", "parliament", "congress",
    "senate", "council", "cabinet", "tribe", "clan", "population",
    "public", "household", "party", "series", "set", "collection",
    "range", "array", "assortment", "bundle", "heap", "pile", "stack",
    "library", "anthology", "fellowship", "membership", "staff",
}


QUANTITATIVE_ADJECTIVES = {
    "one", "two", "three", "four", "five", "six", "seven", "eight",
    "nine", "ten", "eleven", "twelve", "twenty", "thirty", "forty",
    "fifty", "sixty", "seventy", "eighty", "ninety", "hundred",
    "thousand", "million", "billion", "first", "second", "third",
    "many", "few", "fewer", "several", "some", "much", "little", "all",
    "both", "half", "enough", "numerous", "various", "double", "triple",
    "single", "multiple", "countless", "no", "whole", "ample", "scarce",
    "abundant", "plenty", "more", "most", "less", "least",
}

DEMONSTRATIVE_ADJECTIVES = {"this", "that", "these", "those", "such"}

PROPER_ADJECTIVES = {
    "canadian", "american", "english", "french", "spanish", "german",
    "italian", "chinese", "japanese", "russian", "mexican", "british",
    "european", "african", "asian", "australian", "indian", "irish",
    "scottish", "greek", "roman", "victorian", "shakespearean",
    "christian", "muslim", "jewish", "buddhist", "islamic", "catholic",
    "arabic", "hispanic", "latin", "nordic", "persian", "egyptian",
    "brazilian", "korean", "dutch", "polish", "swedish", "norwegian",
    "turkish", "thai", "vietnamese", "cuban", "portuguese", "danish",
    "finnish", "icelandic", "kenyan", "moroccan", "argentine",
}

TIME_ADVERBS = {
    "now", "then", "today", "yesterday", "tomorrow", "tonight", "soon",
    "later", "early", "earlier", "late", "already", "yet", "still",
    "recently", "lately", "formerly", "previously", "afterward",
    "afterwards", "beforehand", "eventually", "finally", "immediately",
    "instantly", "presently", "shortly", "ago", "henceforth",
    "meanwhile", "nowadays", "simultaneously", "momentarily",
    "currently", "initially", "originally", "subsequently", "since",
}

PLACE_ADVERBS = {
    "here", "there", "everywhere", "somewhere", "anywhere", "nowhere",
    "elsewhere", "inside", "outside", "indoors", "outdoors", "upstairs",
    "downstairs", "abroad", "away", "back", "backward", "backwards",
    "forward", "forwards", "downward", "upward", "ahead", "nearby",
    "near", "far", "off", "overhead", "underground", "apart", "aside",
    "around", "everywhere", "nearby", "yonder",
}

FREQUENCY_ADVERBS = {
    "always", "never", "often", "sometimes", "usually", "normally",
    "generally", "frequently", "occasionally", "rarely", "seldom",
    "regularly", "constantly", "continually", "repeatedly",
    "periodically", "daily", "weekly", "monthly", "yearly", "hourly",
    "annually", "twice", "once", "again", "ever", "sometime",
    "infrequently", "routinely",
}

DEGREE_ADVERBS = {
    "very", "too", "quite", "almost", "rather", "fairly", "extremely",
    "totally", "completely", "entirely", "absolutely", "perfectly",
    "utterly", "highly", "deeply", "greatly", "enormously", "incredibly",
    "remarkably", "particularly", "especially", "slightly", "somewhat",
    "partly", "partially", "nearly", "barely", "hardly", "scarcely",
    "merely", "just", "only", "so", "more", "most", "less", "least",
    "much", "enough", "fully", "purely", "simply", "truly", "really",
    "terribly", "awfully", "pretty", "mostly", "altogether", "virtually",
}

MANNER_ADVERBS_EXTRA = {
    "well", "fast", "hard", "together", "alone", "aloud", "straight",
    "tight", "loud", "low", "high", "deep", "wrong", "right", "slow",
    "quick",
}

PROPER_NOUNS = [
    "Canada", "America", "Mexico", "Brazil", "Argentina", "England",
    "France", "Germany", "Italy", "Spain", "Portugal", "Greece",
    "Ireland", "Scotland", "Norway", "Sweden", "Finland", "Denmark",
    "Iceland", "Poland", "Russia", "Ukraine", "China", "Japan", "Korea",
    "India", "Pakistan", "Thailand", "Vietnam", "Indonesia", "Australia",
    "Egypt", "Kenya", "Nigeria", "Morocco", "Turkey", "Israel", "Iran",
    "Iraq", "Cuba", "Chile", "Peru", "Colombia", "Switzerland",
    "Austria", "Belgium", "Netherlands",
    "Toronto", "Ottawa", "Vancouver", "Montreal", "London", "Paris",
    "Berlin", "Madrid", "Rome", "Tokyo", "Beijing", "Moscow", "Cairo",
    "Sydney", "Chicago", "Boston", "Seattle", "Miami", "Hollywood",
    "Manhattan", "Brooklyn", "Niagara",
    "Everest", "Amazon", "Sahara", "Pacific", "Atlantic", "Arctic",
    "Antarctica", "Himalayas", "Andes", "Nile", "Danube", "Thames",
    "Sarah", "Emma", "Olivia", "Sophia", "Isabella", "Mia", "Charlotte",
    "Amelia", "Harper", "Evelyn", "Liam", "Noah", "Oliver", "James",
    "William", "Benjamin", "Lucas", "Henry", "Alexander", "Michael",
    "Daniel", "Matthew", "David", "Joseph", "John", "Maria", "Anna",
    "Grace", "Lily", "Ethan",
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday",
    "Sunday", "January", "February", "March", "April", "June", "July",
    "August", "September", "October", "November", "December",
    "Google", "Apple", "Microsoft", "Amazon", "Netflix", "Disney",
    "Nintendo", "Toyota", "Tesla", "Nike", "Pepsi", "Shakespeare",
    "Einstein", "Newton", "Darwin", "Mozart", "Picasso", "Beethoven",
]
