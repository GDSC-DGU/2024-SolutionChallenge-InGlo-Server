import torch
from issues.utils.model import ALBERTClass

def get_overlapped_chunks(text, chunk, overlap):
    return [text[i:i+chunk] for i in range(0, len(text), chunk-overlap)]

def summarize_text(text, summarizer, tokenizer, max_chunk_length=1024, max_length=128, min_length=32, final_max_length=512):
    chunks = get_overlapped_chunks(text, max_chunk_length, overlap=64)
    summarized_chunks = summarizer(chunks, batch_size=4, max_length=max_length, min_length=min_length, truncation=True)

    summarized_text = ' '.join([summary['summary_text'] for summary in summarized_chunks])
    tokenized_summary = tokenizer.tokenize(summarized_text)

    while len(tokenized_summary) > final_max_length:
        summarized_text = summarizer(summarized_text, max_length=final_max_length, min_length=min_length, truncation=True)[0]['summary_text']
        tokenized_summary = tokenizer.tokenize(summarized_text)

    return summarized_text

def load_model(model_path, device):
    model = ALBERTClass().to(device)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.eval()
    return model

def predict(model, tokenizer, text, max_len, device):
    encoded_text = tokenizer.encode_plus(
        text,
        max_length=max_len,
        add_special_tokens=True,
        return_token_type_ids=True,
        pad_to_max_length=True,
        return_attention_mask=True,
        return_tensors='pt',
        truncation=True
    )
    input_ids = encoded_text['input_ids'].to(device)
    attention_mask = encoded_text['attention_mask'].to(device)
    token_type_ids = encoded_text['token_type_ids'].to(device)

    with torch.no_grad():
        outputs = model(input_ids, attention_mask, token_type_ids)
        _, predictions = torch.max(outputs, dim=1)

    return predictions