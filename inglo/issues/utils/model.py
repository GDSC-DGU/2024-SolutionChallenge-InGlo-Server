import torch.nn as nn
from transformers import AlbertModel

class ALBERTClass(nn.Module):
    def __init__(self):
        super(ALBERTClass, self).__init__()
        self.albert = AlbertModel.from_pretrained("albert-base-v2")
        self.dropout = nn.Dropout(0.3)
        self.linear = nn.Linear(768, 17)

    def forward(self, input_ids, attention_mask, token_type_ids):
        
        output = self.albert(input_ids=input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids)
        pooled_output = output.pooler_output
        output_dropout = self.dropout(pooled_output)
        output = self.linear(output_dropout)
        return output