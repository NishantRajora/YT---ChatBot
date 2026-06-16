from langchain_ollama import OllamaLLM

model = OllamaLLM(model="qwen2.5-coder:3b")

response = model.invoke("What is machine learning? in 1 line ")

print(response)

