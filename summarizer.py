import os
import requests
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline

load_dotenv()
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")

MODEL_ID = "google/pegasus-cnn_dailymail"
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID, use_fast=False)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_ID)

summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

def chunk_text(text, max_tokens=512):
    if not isinstance(text, str):
        text = str(text)
    
    tokens = tokenizer.encode(text, truncation=False, add_special_tokens=True)
    chunks = []
    
    for i in range(0, len(tokens), max_tokens):
        chunk_tokens = tokens[i:i+max_tokens]
        chunk_text = tokenizer.decode(chunk_tokens, skip_special_tokens=True)
        chunks.append(chunk_text)
    
    return chunks
    
def summarize_text(text, max_length=100, min_length=30):
    if not text or not isinstance(text, str):
        return "No summary available"

    if len(text.split()) < min_length:
        return text
    
    try:
        chunks = chunk_text(text, max_tokens=512)
        summaries = []
        
        for chunk in chunks:
            chunk_words = len(chunk.split())
            if chunk_words < 10:
                continue

            adjusted_max = min(max_length, max(chunk_words // 2, min_length + 5))
            adjusted_min = min(min_length, adjusted_max - 5)
            
            try:
                out = summarizer(
                    chunk,
                    max_length=adjusted_max,
                    min_length=adjusted_min,
                    no_repeat_ngram_size=3,
                    do_sample=False,
                    truncation=True,
                )
                summaries.append(out[0]["summary_text"])
            except Exception as e:
                print(f"[경고] 청크 요약 실패: {e}")
                # 실패한 청크는 첫 문장만 추출
                first_sentence = chunk.split('.')[0] + '.'
                summaries.append(first_sentence)
        
        return " ".join(summaries) if summaries else text[:200] + "..."
        
    except Exception as e:
        print(f"[오류] 요약 생성 실패: {e}")
        # 폴백: 첫 200자 반환
        return text[:200] + "..." if len(text) > 200 else text

def translate_text(text, source_lang="EN", target_lang="KO"):
    if not text or not isinstance(text, str):
        return "Translation not available"
    
    if not DEEPL_API_KEY:
        print("[경고] DeepL API 키가 설정되지 않았습니다.")
        return text
    
    try:
        url = "https://api-free.deepl.com/v2/translate"
        
        # 1. 인증을 위해 헤더(Header)를 추가합니다.
        headers = {
            "Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}"
        }
        
        # 2. 본문 데이터에서는 auth_key를 제거합니다.
        data = {
            "text": text,
            "source_lang": source_lang,
            "target_lang": target_lang
        }
        
        # 3. headers 파라미터를 추가하여 요청을 보냅니다.
        response = requests.post(url, headers=headers, data=data, timeout=30)
        
        if response.status_code == 200:
            return response.json()["translations"][0]["text"]
        else:
            print(f"[경고] DeepL API 오류: {response.status_code}")
            return text
            
    except Exception as e:
        print(f"[오류] 번역 실패: {e}")
        return text

# def translate_text(text, source_lang="EN", target_lang="KO"):
#     if not text or not isinstance(text, str):
#         return "Translation not available"
    
#     if not DEEPL_API_KEY:
#         print("[경고] DeepL API 키가 설정되지 않았습니다.")
#         return text
    
#     try:
#         url = "https://api-free.deepl.com/v2/translate"
#         params = {
#             "auth_key": DEEPL_API_KEY,
#             "text": text,
#             "source_lang": source_lang,
#             "target_lang": target_lang
#         }
#         response = requests.post(url, data=params, timeout=30)
        
#         if response.status_code == 200:
#             return response.json()["translations"][0]["text"]
#         else:
#             print(f"[경고] DeepL API 오류: {response.status_code}")
#             return text
            
#     except Exception as e:
#         print(f"[오류] 번역 실패: {e}")
#         return text




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
