import io
import os
import json
import modal
import requests
from pydub import AudioSegment

app = modal.App("speech-emotion-analyzer")

image = (
    modal.Image.debian_slim()
    .apt_install("ffmpeg")
    .pip_install("pydub", "requests")
)

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")

@app.function(image=image, secrets=[modal.Secret.from_name("openrouter")], gpu="any")
def analyze_confidence(text):
    prompt = f"""
    Analyze the confidence of the inputted text: "{text}". 
    Consider the word choice of the user and the use of filler words. Additionally, generate a score from 1-10. Put this score at the very end.
    Be a hard grader. NO MARKDOWN PLEASE. Keep to 500 tokens max."""

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": "anthropic/claude-sonnet-4.5",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 1000
        })
    )
    response.raise_for_status()
    confidence_analysis = response.json()["choices"][0]["message"]["content"]

    return {
        "response": response,
        "confidence_analysis": confidence_analysis
    }

@app.function(image=image, secrets=[modal.Secret.from_name("openrouter")], gpu="any")
def analyze_word_choice(text):
    prompt = f"""
    Analyze the word choice of the inputted text: "{text}". 
    Consider how professional the wording is. Additionally, generate a score from 1-10. Put this score at the very end.
    Be a hard grader. NO MARKDOWN PLEASE. Keep to 500 tokens max."""

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": "anthropic/claude-sonnet-4.5",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 1000
        })
    )
    response.raise_for_status()
    word_analysis = response.json()["choices"][0]["message"]["content"]

    return {
        "response": response,
        "word_analysis": word_analysis
    }

@app.local_entrypoint()
def main():
    text = "It might be best to hire me."
    result_confidence = analyze_confidence.remote(text)
    result_word = analyze_word_choice.remote(text)

    print("\n*** --- CONFIDENCE ANALYSIS --- ***\n")
    print(result_confidence["confidence_analysis"])
    print("\n*** --- WORD CHOICE ANALYSIS --- ***\n")
    print(result_word["word_analysis"])