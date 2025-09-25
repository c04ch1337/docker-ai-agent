# training/dataset.py
from transformers import AutoTokenizer
import torch
from torch.utils.data import Dataset
from typing import List, Dict

class DockerGoDataset(Dataset):
    def __init__(self, examples: List[str], tokenizer=None):
        self.tokenizer = tokenizer or AutoTokenizer.from_pretrained("model_path")
        self.examples = self._prepare_examples(examples)
    
    def _prepare_examples(self, examples: List[str]) -> List[Dict]:
        prepared = []
        for example in examples:
            encoding = self.tokenizer.encode_plus(
                example,
                max_length=512,
                padding='max_length',
                truncation=True,
                return_attention_mask=True,
                return_tensors='pt'
            )
            prepared.append({
                'input_ids': encoding['input_ids'].flatten(),
                'attention_mask': encoding['attention_mask'].flatten()
            })
        return prepared
    
    def __len__(self):
        return len(self.examples)
    
    def __getitem__(self, idx):
        return self.examples[idx]