import torch
from transformers import BertTokenizer, pipeline
from model import BERTClass

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


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
summarizer = pipeline('summarization', model='facebook/bart-large-cnn', device=0)
model_path = "./output_multi_class/best_model_state.pt"
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = load_model(model_path, device)

text= ""

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

print(f'Summary: {summary}')
print(f'SDG: {predictions.item()+1}')