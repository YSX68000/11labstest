# streamlit_app.py
import streamlit as st
import requests
import io
from pathlib import Path
import base64
import os

# --- 環境変数から APIキー取得 ---
API_KEY = os.getenv("ELEVENLABS_API_KEY")  # Streamlit Secrets でも可
VOICE_ID = "YyBHEgIAvkDGlHvbSe5A"

st.title("11Labs 音声合成 (TTS)")

text_input = st.text_area("テキストを入力してください", "こんにちは、11Labsの音声合成APIを試しています！")

if st.button("再生") and text_input.strip():
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {"xi-api-key": API_KEY, "Content-Type": "application/json"}
    payload = {
        "text": text_input,
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
    }

    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        # 音声データを BytesIO に読み込み
        audio_bytes = io.BytesIO(response.content)

        # HTML5 audio タグで再生するため base64 に変換
        audio_base64 = base64.b64encode(audio_bytes.read()).decode("utf-8")
        audio_html = f"""
        <audio controls autoplay>
            <source src="data:audio/mpeg;base64,{audio_base64}" type="audio/mpeg">
        </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
    else:
        st.error(f"ElevenLabs API エラー: {response.status_code} {response.text}")
