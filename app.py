import os
import streamlit as st
import requests
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

st.title("📚 AI Study Helper (OpenRouter)")

mode = st.sidebar.selectbox(
    "Выбери режим",
    ["Объяснить", "Упростить", "Сделать вопросы"]
)

text = st.text_area("Вставь текст для обработки:")

if st.button("Обработать") and text:
    if mode == "Объяснить":
        prompt = f"Объясни этот текст простыми словами:\n{text}"
    elif mode == "Упростить":
        prompt = f"Сделай текст максимально простым для новичка:\n{text}"
    else:
        prompt = f"Сгенерируй 5 вопросов по тексту:\n{text}"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        st.subheader("Ответ AI:")
        st.write(result["choices"][0]["message"]["content"])
    except requests.exceptions.HTTPError as e:
        st.error(f"Ошибка AI: {e} | {response.text}")