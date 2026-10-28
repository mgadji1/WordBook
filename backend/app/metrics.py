from prometheus_client import Counter, Gauge, Histogram


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


# SLI metrics

wordbook_requests_total = Counter(
    "wordbook_requests_total",
    "Total number of HTTP requests",
    ["status"]
)

wordbook_request_duration_seconds = Histogram(
    "wordbook_request_duration_seconds",
    "HTTP request duration in seconds",
    buckets=(0.05, 0.1, 0.2, 0.3, 0.5, 1.0, 2.0, 3.0, 5.0) # seconds for x-axis
)