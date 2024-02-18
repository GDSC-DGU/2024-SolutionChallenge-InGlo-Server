import torch
from transformers import BertTokenizer
from model import BERTClass

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


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model_path = "./output_multi_class/best_model_state.pt"
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = load_model(model_path, device)

raw_text = "The Convention on the Conservation of Migratory Species of Wild Animals (CMS) has launched the first-ever comprehensive assessment of the state of the world’s migratory species. The report warns that almost half of the world’s migratory species are in decline and more than a fifth are threatened with extinction, including nearly all of CMS-listed fish. It provides a set of recommendations for priority action to save migratory animals."
max_len = 256
predictions = predict(model, tokenizer, raw_text, max_len, device)
print(f'text: {raw_text}')
print(f'sdg: {predictions.item()+1}')