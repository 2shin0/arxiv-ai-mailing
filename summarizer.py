import requests
from transformers import pipeline
from dotenv import load_dotenv
import os

# .env 파일에서 API 키 로딩
load_dotenv()
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")

# 사전 학습된 요약 모델
tokenizer = "t5-small"
model = "t5-small"
summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

def summarize_text(text, max_length=100, min_length=30):
    text = "summarize: " + text[:512]
    input_length = len(text)
    adjusted_max_length = min(max_length, input_length // 2)

    summary = summarizer(
        text,
        max_length=adjusted_max_length,
        min_length=min_length,
        do_sample=False
    )
    return summary[0]['summary_text']

# 번역기 : DeepL 활용, 월 500,000자 제공 (영어 기준)
def translate_text(text, source_lang="EN", target_lang="KO"):
    url = "https://api-free.deepl.com/v2/translate"
    params = {
        "auth_key": DEEPL_API_KEY,
        "text": text[:512],  # 요청당 길이 제한
        "source_lang": source_lang,
        "target_lang": target_lang
    }
    response = requests.post(url, data=params)
    if response.status_code == 200:
        return response.json()["translations"][0]["text"]
    else:
        raise Exception(f"DeepL API 오류: {response.status_code} - {response.text}")

if __name__ == "__main__":
    sample_text = """
    We introduce a novel approach for optimizing transformer-based models by applying a layer-wise pruning
    technique that maintains performance while reducing model size. Our method is evaluated on benchmark datasets...
    """
    print("요약 결과:", summarize_text(sample_text))
    print("번역 결과:", translate_text(sample_text))
