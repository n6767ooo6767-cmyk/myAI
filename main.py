import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Твой ключ должен быть добавлен в переменные среды на Railway
API_KEY = os.getenv("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")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Словарь наших агентов (моделей)
AGENTS = {
    "coder": "poolside/laguna-xs-2.1",
    "analyzer": "qwen/qwen-3-next-80b",
    "visionary": "google/gemma-4-31b",
    "searcher": "nvidia/llama-nemotron-rerank-1b-v2"
}

@app.route('/')
def index():
    return "Командный центр проекта Олимп активен. Система готова к работе."

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    prompt = data.get("prompt")
    role = data.get("role", "analyzer")  # По умолчанию Аналитик (Qwen)
    
    model = AGENTS.get(role, AGENTS["analyzer"])
    
    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
