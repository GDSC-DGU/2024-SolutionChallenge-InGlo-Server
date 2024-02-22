import torch
from transformers import BertTokenizer, pipeline
from .predict import get_overlapped_chunks, load_model, predict

def classify_news(content):
    """
    뉴스 기사의 내용을 바탕으로
    SDGs를 분류하는 모델
    """
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    summarizer = pipeline('summarization', model='facebook/bart-large-cnn', device=0)
    model_path = "issues/utils/output_multi_class/best_model_state.pt"
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = load_model(model_path, device)

    text = content

    # Summarize each chunk
    outs = []
    for chunk in get_overlapped_chunks(text, 1024, 32):
        out = summarizer(chunk, max_length=128, min_length=32)
        outs.append(out[0]['summary_text'])

    # Combine the chunk summaries into a single text
    text = ' '.join(outs)

    if len(tokenizer.tokenize(text)) > 512:
        summary = summarizer(text, max_length=512)[0]['summary_text']
    else:
        summary = text

    predictions = predict(model, tokenizer, summary, max_len=256, device=device)

    return (predictions.item()+1)