import torch
from issues.utils.model import BERTClass

def get_overlapped_chunks(text, chunk, overlap):
    return [text[i:i+chunk] for i in range(0, len(text), chunk-overlap)]

def load_model(model_path, device):
    model = BERTClass().to(device)
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