import os
import requests
import time
from prometheus_client import Counter, start_http_server


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://backend-service:8080/"
)

PROBE_TIMEOUT = 5
PROBE_INTERVAL = 10


# SLI metric
wordbook_availability_checks_total = Counter(
    "wordbook_availability_checks_total",
    "Total availability probe checks",
    ["result"]
)

start_http_server(9101)

while True:
    try:
        response = requests.get(
            BACKEND_URL,
            timeout=PROBE_TIMEOUT
        )

        if response.status_code >= 200 and response.status_code < 300:
            wordbook_availability_checks_total.labels(result="success").inc()
        else:
            wordbook_availability_checks_total.labels(result="failure").inc()
    except Exception:
        wordbook_availability_checks_total.labels(result="failure").inc()

    time.sleep(PROBE_INTERVAL)
