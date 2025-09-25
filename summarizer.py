import os
import requests
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

# 환경 변수 로드
load_dotenv()
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")

# Pegasus 모델 로드 (slow 토크나이저 강제)
MODEL_ID = "google/pegasus-cnn_dailymail"
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, use_fast=False)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_ID)

# 여기서 'model'과 'tokenizer' 객체를 그대로 사용
summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

# 텍스트를 모델 입력 크기에 맞게 분할 (문자 기준: 간단 버전)
def chunk_text(text, max_chunk_size=512):
    return [text[i:i + max_chunk_size] for i in range(0, len(text), max_chunk_size)]

def summarize_text(text, max_length=100, min_length=30):
    chunks = chunk_text(text, max_chunk_size=512)
    summaries = []
    for chunk in chunks:
        # 아주 짧은 청크에서 min_length > max_length 되는 문제 방지
        input_len = max(len(chunk), 1)
        adjusted_max = max(min(max_length, input_len // 2), min_length + 1)

        out = summarizer(
            chunk,
            max_length=adjusted_max,
            min_length=min_length,
            do_sample=False,
            truncation=True,     # 입력 초과 방지
        )
        summaries.append(out[0]["summary_text"])
    return " ".join(summaries)

def translate_text(text, source_lang="EN", target_lang="KO"):
    url = "https://api-free.deepl.com/v2/translate"
    params = {
        "auth_key": DEEPL_API_KEY,
        "text": text,
        "source_lang": source_lang,
        "target_lang_





# import requests
# from transformers import pipeline, AutoTokenizer
# from dotenv import load_dotenv
# import os

# # 환경 변수 로드
# load_dotenv()
# DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")

# # Pegasus 모델 로드
# tokenizer_name = "google/pegasus-cnn_dailymail"
# model_name = "google/pegasus-cnn_dailymail"
# summarizer = pipeline("summarization", model=model_name, tokenizer=tokenizer_name)

# # 텍스트를 모델 입력 크기에 맞게 분할
# def chunk_text(text, max_chunk_size=512):
#     """
#     긴 텍스트를 모델 입력 한도에 맞춰 청크 단위로 분할
#     """
#     return [text[i:i + max_chunk_size] for i in range(0, len(text), max_chunk_size)]

# # 요약 함수
# def summarize_text(text, max_length=100, min_length=30):
#     """
#     텍스트가 너무 길면 자동으로 분할하여 요약 후 결과를 합침
#     """
#     # 텍스트 길이가 너무 길면 분할
#     chunks = chunk_text(text, max_chunk_size=512)
#     summaries = []

#     for chunk in chunks:
#         input_length = len(chunk)
#         adjusted_max_length = min(max_length, input_length // 2)

#         summary = summarizer(
#             chunk,
#             max_length=adjusted_max_length,
#             min_length=min_length,
#             do_sample=False
#         )
#         summaries.append(summary[0]['summary_text'])

#     # 여러 청크 요약 결과를 다시 하나로 합침
#     return " ".join(summaries)

# # 번역 함수
# def translate_text(text, source_lang="EN", target_lang="KO"):
#     """
#     DeepL API를 이용하여 번역
#     """
#     url = "https://api-free.deepl.com/v2/translate"
#     params = {
#         "auth_key": DEEPL_API_KEY,
#         "text": text,  # 자르지 않고 전체 번역
#         "source_lang": source_lang,
#         "target_lang": target_lang
#     }
#     response = requests.post(url, data=params)
#     if response.status_code == 200:
#         return response.json()["translations"][0]["text"]
#     else:
#         raise Exception(f"DeepL API 오류: {response.status_code} - {response.text}")
