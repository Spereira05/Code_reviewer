#!/usr/bin/env python3
import requests
import sys
import json
import time
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Check Ollama status and test models")
    parser.add_argument("--host", default="ollama", help="Ollama host (default: ollama)")
    parser.add_argument("--port", default=11434, type=int, help="Ollama port (default: 11434)")
    parser.add_argument("--model", default="tinyllama", help="Model to check/test (default: tinyllama)")
    parser.add_argument("--pull", action="store_true", help="Pull model if not found")
    return parser.parse_args()

def check_ollama_status(base_url):
    """Check if Ollama is running"""
    try:
        response = requests.get(f"{base_url}/api/version", timeout=5)
        if response.status_code == 200:
            version = response.json().get("version", "unknown")
            print(f"✅ Ollama is running (version: {version})")
            return True
        else:
            print(f"❌ Ollama returned status code {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Ollama is not available: {str(e)}")
        return False

def list_models(base_url):
    """List available models in Ollama"""
    try:
        response = requests.get(f"{base_url}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json().get("models", [])
            if models:
                print(f"Found {len(models)} models:")
                for model in models:
                    model_name = model.get("name", "unknown")
                    model_size = model.get("size", 0) // (1024 * 1024)  # MB
                    print(f"  - {model_name} ({model_size} MB)")
                return [model.get("name") for model in models]
            else:
                print("No models found")
                return []
        else:
            print(f"❌ Failed to list models: HTTP {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"❌ Error listing models: {str(e)}")
        return []

def pull_model(base_url, model_name):
    """Pull a model from Ollama"""
    print(f"Pulling model '{model_name}'... This may take a while.")
    try:
        response = requests.post(
            f"{base_url}/api/pull",
            json={"name": model_name},
            timeout=600  # 10 minutes timeout for large models
        )
        if response.status_code == 200:
            print(f"✅ Successfully pulled model '{model_name}'")
            return True
        else:
            print(f"❌ Failed to pull model: HTTP {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error pulling model: {str(e)}")
        return False

def test_model(base_url, model_name):
    """Test a model with a simple prompt"""
    print(f"Testing model '{model_name}' with a simple prompt...")
    try:
        prompt = "Explain what code review is in one sentence."
        response = requests.post(
            f"{base_url}/api/generate",
            json={"model": model_name, "prompt": prompt, "stream": False},
            timeout=30
        )
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Model response: {result.get('response')}")
            return True
        else:
            print(f"❌ Failed to test model: HTTP {response.status_code}")
            if response.status_code == 404:
                print(f"Model '{model_name}' not found. Try pulling it first.")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error testing model: {str(e)}")
        return False

def main():
    args = parse_args()
    base_url = f"http://{args.host}:{args.port}"
    
    print(f"\n=== Ollama Status Check ===")
    print(f"Checking Ollama at {base_url}...")
    
    if not check_ollama_status(base_url):
        print("\nTroubleshooting tips:")
        print("1. Make sure Ollama is running")
        print("2. If running locally, use --host localhost")
        print("3. If in Docker, make sure the ollama service is running")
        sys.exit(1)
    
    print("\n=== Available Models ===")
    available_models = list_models(base_url)
    
    model_exists = args.model in available_models
    
    if not model_exists:
        print(f"\nThe requested model '{args.model}' is not available.")
        if args.pull or input(f"Do you want to pull the '{args.model}' model? (y/n): ").lower() == 'y':
            print()  # Empty line
            if pull_model(base_url, args.model):
                model_exists = True
    
    if model_exists:
        print(f"\n=== Testing Model ===")
        test_model(base_url, args.model)
    
    print("\nCheck complete!")

if __name__ == "__main__":
    main()