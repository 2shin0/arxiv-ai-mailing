from transformers import pipeline

# 사전 학습된 요약 및 번역 모델 불러오기
tokenizer = "t5-small"
model = "t5-small"
summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

# 영어 → 한국어 번역기 불러오기
translator = pipeline("translation_en_to_ko", model="facebook/nllb-200-distilled-1.3B")

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

def translate_text(text):
    translated = translator(text[:512])  # 길이 제한
    return translated[0]['translation_text']

if __name__ == "__main__":
    sample_text = """
    We introduce a novel approach for optimizing transformer-based models by applying a layer-wise pruning
    technique that maintains performance while reducing model size. Our method is evaluated on benchmark datasets...
    """
    print(summarize_text(sample_text))
    print(translate_text(sample_text))