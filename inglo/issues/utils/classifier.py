import torch
from transformers import AlbertTokenizer, pipeline
from .predict import get_overlapped_chunks, summarize_text, load_model, predict

def classify_news(content):
    """
    뉴스 기사의 내용을 바탕으로
    SDGs를 분류하는 모델
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    summarizer = pipeline('summarization', model='facebook/bart-large-cnn', device=0)
    model_path = "issues/utils/best_model_state.pt"
    tokenizer = AlbertTokenizer.from_pretrained('albert-base-v2')
    model = load_model(model_path, device)

    text = content
    
    final_summary = summarize_text(text, summarizer, tokenizer)

    predictions = predict(model, tokenizer, final_summary, max_len=512, device=device)
    return (predictions.item()+1)