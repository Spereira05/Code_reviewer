#!/bin/bash
set -e

# Wait for Ollama service to be ready
echo "Waiting for Ollama service to be ready..."
until curl -s -f -o /dev/null "http://ollama:11434/api/version" || [ $? -eq 7 ]; do
    echo "Ollama not ready yet, waiting..."
    sleep 2
done

echo "Ollama service is ready!"

# Pull required models
echo "Pulling Llama 3.1 model..."
curl -X POST http://ollama:11434/api/pull -d '{"name": "llama3.1"}'

echo "Models are ready for use"