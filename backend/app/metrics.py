from prometheus_client import Counter, Gauge


wordbook_operations_total = Counter(
    "wordbook_operations_total",
    "Total number of successful word operations",
    ["operation"]
)

wordbook_searches_total = Counter(
    "wordbook_searches_total",
    "Total number of word searches"
)

wordbook_word_updates_total = Counter(
    "wordbook_word_updates_total",
    "Total number of successful word translation updates"
)

wordbook_words_total = Gauge(
    "wordbook_words_total",
    "Current number of words in user dictionary"
)