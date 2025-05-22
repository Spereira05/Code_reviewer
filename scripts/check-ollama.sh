#!/bin/bash
# Script to check Ollama status and test models
# Usage: ./check-ollama.sh [host] [port] [model]
#   host: Ollama host (default: localhost or ollama in container)
#   port: Ollama port (default: 11434)
#   model: Model to check/test (default: llama3)

# Set default values
if [ -z "$1" ]; then
  # Check if we're in a container by looking for cgroup
  if grep -q docker /proc/1/cgroup 2>/dev/null; then
    HOST="ollama"
  else
    HOST="localhost"
  fi
else
  HOST="$1"
fi

PORT="${2:-11434}"
MODEL="${3:-tinyllama}"
BASE_URL="http://${HOST}:${PORT}"

echo "=== Ollama Status Check ==="
echo "Checking Ollama at ${BASE_URL}..."

# Function to check if a command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Ensure curl is available
if ! command_exists curl; then
  echo "Error: curl is not installed. Please install curl to use this script."
  exit 1
fi

# Check if Ollama is running
check_version() {
  echo -n "Checking Ollama service... "
  VERSION_RESPONSE=$(curl -s -w "%{http_code}" -o /tmp/ollama_version ${BASE_URL}/api/version)
  
  if [ "$VERSION_RESPONSE" = "200" ]; then
    VERSION=$(grep -o '"version":"[^"]*' /tmp/ollama_version | cut -d '"' -f 4)
    echo "✅ ONLINE (version: ${VERSION})"
    return 0
  else
    echo "❌ OFFLINE (HTTP status: ${VERSION_RESPONSE})"
    return 1
  fi
}

# List all available models
list_models() {
  echo -n "Fetching available models... "
  MODELS_RESPONSE=$(curl -s -w "%{http_code}" -o /tmp/ollama_models ${BASE_URL}/api/tags)
  
  if [ "$MODELS_RESPONSE" = "200" ]; then
    echo "✅ SUCCESS"
    echo "Available models:"
    
    # Parse models from JSON (use grep/sed for maximum compatibility)
    grep -o '"name":"[^"]*' /tmp/ollama_models | cut -d '"' -f 4 | while read -r model_name; do
      echo "  - ${model_name}"
      if [ "${model_name}" = "${MODEL}" ]; then
        MODEL_EXISTS="true"
      fi
    done
    
    return 0
  else
    echo "❌ FAILED (HTTP status: ${MODELS_RESPONSE})"
    return 1
  fi
}

# Pull a model
pull_model() {
  local model="$1"
  echo -n "Pulling model '${model}'... "
  
  # Use a longer timeout for model pulling
  PULL_RESPONSE=$(curl -s -m 600 -w "%{http_code}" -o /tmp/ollama_pull \
    -X POST "${BASE_URL}/api/pull" \
    -H "Content-Type: application/json" \
    -d "{\"name\":\"${model}\"}")
  
  if [ "$PULL_RESPONSE" = "200" ]; then
    echo "✅ SUCCESS"
    return 0
  else
    echo "❌ FAILED (HTTP status: ${PULL_RESPONSE})"
    cat /tmp/ollama_pull
    return 1
  fi
}

# Test a model with a simple prompt
test_model() {
  local model="$1"
  echo -n "Testing model '${model}'... "
  
  GENERATE_RESPONSE=$(curl -s -m 60 -w "%{http_code}" -o /tmp/ollama_generate \
    -X POST "${BASE_URL}/api/generate" \
    -H "Content-Type: application/json" \
    -d "{\"model\":\"${model}\",\"prompt\":\"Explain what code review is in one sentence.\",\"stream\":false}")
  
  if [ "$GENERATE_RESPONSE" = "200" ]; then
    echo "✅ SUCCESS"
    MODEL_OUTPUT=$(grep -o '"response":"[^"]*' /tmp/ollama_generate | sed 's/"response":"//' | head -1)
    echo "Model response: ${MODEL_OUTPUT}"
    return 0
  else
    echo "❌ FAILED (HTTP status: ${GENERATE_RESPONSE})"
    if [ "$GENERATE_RESPONSE" = "404" ]; then
      echo "Model not found. You may need to pull it first."
    fi
    cat /tmp/ollama_generate
    return 1
  fi
}

# Check if model exists in the list
model_exists() {
  local model="$1"
  curl -s "${BASE_URL}/api/tags" | grep -q "\"name\":\"${model}\""
  return $?
}

# Main execution
if check_version; then
  echo ""
  list_models
  echo ""
  
  # Check if our target model exists
  if model_exists "${MODEL}"; then
    echo "Model '${MODEL}' is available ✅"
    echo ""
    test_model "${MODEL}"
  else
    echo "Model '${MODEL}' is not available ❌"
    echo ""
    
    # Ask if we should pull the model
    read -p "Do you want to pull the model '${MODEL}'? (y/n): " PULL_DECISION
    if [ "$PULL_DECISION" = "y" ] || [ "$PULL_DECISION" = "Y" ]; then
      echo ""
      pull_model "${MODEL}"
      if [ $? -eq 0 ]; then
        echo ""
        test_model "${MODEL}"
      fi
    fi
  fi
else
  echo ""
  echo "Ollama service is not available at ${BASE_URL}."
  echo "Please make sure:"
  echo "1. Ollama is installed and running"
  echo "2. You're using the correct host and port"
  echo "3. There are no firewall issues blocking access"
  
  if [ "$HOST" = "ollama" ]; then
    echo ""
    echo "You seem to be trying to connect to an Ollama service named 'ollama'."
    echo "If you're running this script outside Docker, try:"
    echo "  ./check-ollama.sh localhost"
  fi
  
  exit 1
fi

# Clean up temporary files
rm -f /tmp/ollama_version /tmp/ollama_models /tmp/ollama_pull /tmp/ollama_generate

echo ""
echo "Check complete."