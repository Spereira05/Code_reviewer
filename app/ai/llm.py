from langchain_openai import ChatOpenAI
import os

os.environ['OPENAI_API_KEY'] = "not-used-for-ollama"

llama3 = ChatOpenAI(
  model='ollama/llama3.1',
  base_url="http://localhost:11434"
)