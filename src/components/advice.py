# src/components/advice.py
import streamlit as st
from openai import OpenAI

def get_advice(location: str, plant: str) -> str:
    client = OpenAI(api_key=st.secrets["general"]["OPENAI_API_KEY"])
    prompt = f"場所: {location}\n植物: {plant}\nこの条件での栽培アドバイスを教えてください。"
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"アドバイス取得エラー: {str(e)}"