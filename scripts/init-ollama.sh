#!/bin/bash
set -e

# Define variables
OLLAMA_HOST=${1:-"ollama"}
OLLAMA_PORT=${2:-"11434"}
OLLAMA_URL="http://${OLLAMA_HOST}:${OLLAMA_PORT}"
MODEL_NAME=${3:-"tinyllama"}
MAX_RETRIES=30
RETRY_INTERVAL=5

echo "=== Ollama Initialization Script ==="
echo "Ollama URL: ${OLLAMA_URL}"
echo "Model to initialize: ${MODEL_NAME}"

# Wait for Ollama service to be ready
echo "Waiting for Ollama service to be ready..."
for i in $(seq 1 $MAX_RETRIES); do
    if curl -s -f "${OLLAMA_URL}/api/version" > /dev/null; then
        VERSION=$(curl -s "${OLLAMA_URL}/api/version" | grep -o '"version":"[^"]*' | sed 's/"version":"//')
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
    PULL_RESPONSE=$(curl -s -X POST "${OLLAMA_URL}/api/pull" -d "{\"name\":\"${MODEL_NAME}\"}")
    
    if echo "$PULL_RESPONSE" | grep -q "error"; then
        echo "❌ Failed to pull model: $PULL_RESPONSE"
        exit 1
    else
        echo "✅ Successfully pulled model '${MODEL_NAME}'"
    fi
fi

# Verify model works
echo "Testing model with a simple prompt..."
TEST_RESPONSE=$(curl -s -m 60 -X POST "${OLLAMA_URL}/api/generate" \
  -d "{\"model\":\"${MODEL_NAME}\",\"prompt\":\"Say hello\",\"stream\":false}")

if echo "$TEST_RESPONSE" | grep -q "response"; then
    RESPONSE_TEXT=$(echo "$TEST_RESPONSE" | grep -o '"response":"[^"]*' | sed 's/"response":"//')
    echo "✅ Model test successful. Response: ${RESPONSE_TEXT}"
else
    echo "⚠️ Model test returned unexpected response: $TEST_RESPONSE"
    # Don't fail on this - the model might still work for the application
fi

echo "=== Ollama Initialization Complete ==="
exit 0