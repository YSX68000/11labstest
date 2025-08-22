from fastapi import FastAPI, Query
from fastapi.responses import Response, HTMLResponse
import requests
import os

app = FastAPI()

# 環境変数から APIキーを取得
API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = "YyBHEgIAvkDGlHvbSe5A"

@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <!DOCTYPE html>
    <html lang="ja">
    <head><meta charset="UTF-8"><title>11Labs TTS</title></head>
    <body>
        <h1>11Labs 音声合成</h1>
        <input type="text" id="text" placeholder="テキストを入力">
        <button onclick="playTTS()">再生</button>
        <audio id="audio" controls></audio>

        <script>
        async function playTTS() {
            const text = document.getElementById("text").value;
            const audio = document.getElementById("audio");
            audio.src = "/tts?text=" + encodeURIComponent(text);
            audio.play();
        }
        </script>
    </body>
    </html>
    """

@app.get("/tts")
def tts(text: str = Query(..., min_length=1)):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {"xi-api-key": API_KEY, "Content-Type": "application/json"}
    payload = {
        "text": text,
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        return Response(
            content=f"Error from ElevenLabs: {response.text}",
            media_type="text/plain",
            status_code=response.status_code
        )

    # 音声データを直接返す
    return Response(content=response.content, media_type="audio/mpeg")
