from transformers import pipeline

# 사전 학습된 요약 모델 불러오기 
tokenizer = "t5-small"
model = "t5-small"
summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)

def summarize_text(text, max_length=100, min_length=30):
    # 입력 제한 대비 잘라내고 요약 prefix 붙임
    text = "summarize: " + text[:512]
    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
    return summary[0]['summary_text']

if __name__ == "__main__":
    sample_text = """
    We introduce a novel approach for optimizing transformer-based models by applying a layer-wise pruning
    technique that maintains performance while reducing model size. Our method is evaluated on benchmark datasets...
    """
    print(summarize_text(sample_text))