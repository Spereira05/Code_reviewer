#!/bin/bash
set -e

echo "=== Ollama Initialization Script ==="
echo "Starting..."

# Constants
MODEL_NAME="tinyllama"
OLLAMA_HOST="ollama"
OLLAMA_PORT="11434"
OLLAMA_URL="http://${OLLAMA_HOST}:${OLLAMA_PORT}"
MAX_RETRIES=30
RETRY_INTERVAL=5

# Wait for Ollama service to be ready
echo "Waiting for Ollama service to be ready at ${OLLAMA_URL}..."
for i in $(seq 1 $MAX_RETRIES); do
    if curl -s -f "${OLLAMA_URL}/api/version" > /dev/null; then
        VERSION=$(curl -s "${OLLAMA_URL}/api/version" | grep -o '"version":"[^"]*' | cut -d'"' -f4)
        echo "✅ Ollama service is running (version: ${VERSION})"
        break
    fi
    
    if [ $i -eq $MAX_RETRIES ]; then
        echo "❌ Ollama service did not become available after $MAX_RETRIES attempts"
        exit 1
    fi
    
    echo "Attempt $i/$MAX_RETRIES: Ollama not ready yet, waiting ${RETRY_INTERVAL}s..."
    sleep $RETRY_INTERVAL
done

# Check for models
echo "Checking available models..."
MODELS_RESPONSE=$(curl -s "${OLLAMA_URL}/api/tags")
echo "Response: $MODELS_RESPONSE"

# Check if our model exists
if echo "$MODELS_RESPONSE" | grep -q "\"name\":\"${MODEL_NAME}\""; then
    echo "✅ Model '${MODEL_NAME}' is already available"
else
    echo "⏳ Model '${MODEL_NAME}' not found, pulling it now..."
    curl -X POST "${OLLAMA_URL}/api/pull" -d "{\"name\":\"${MODEL_NAME}\"}"
    echo "✅ Successfully pulled model '${MODEL_NAME}'"
fi

echo "=== Ollama Initialization Complete ==="
exit 0