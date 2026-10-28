#!/bin/bash

THREADS=100

run_batch() {
    curl -s -o /dev/null http://localhost:8080/api/words

    curl -s -o /dev/null http://localhost:8080/api/words/hello

    curl -s -o /dev/null -X POST http://localhost:8080/api/words \
     -H "Content-Type: application/json" \
     -d '{"word": "hello", "translation": "привет"}'

    curl -s -o /dev/null -X PUT http://localhost:8080/api/words/hello \
     -H "Content-Type: application/json" \
     -d '{"translation": "привет"}'

    curl -s -o /dev/null -X DELETE http://localhost:8080/api/words/hello
}

export -f run_batch

yes | xargs -P "$THREADS" -I {} bash -c run_batch
