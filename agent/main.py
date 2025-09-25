# agent/main.py
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import json
from typing import Dict, List
import logging
from agent.training.dataset import DockerGoDataset
from torch.utils.data import DataLoader

class AI_Agent:
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.load_model()
        
    def load_model(self):
        """Load model with GPU support"""
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.tokenizer = AutoTokenizer.from_pretrained("model_path")
        self.model = AutoModelForCausalLM.from_pretrained("model_path")
        self.model.to(device)
        
    async def process_prompt(self, prompt: str) -> Dict:
        """Process incoming prompts"""
        inputs = self.tokenizer(prompt, return_tensors='pt', max_length=512, truncation=True)
        inputs = {k: v.cuda() for k, v in inputs.items()}
        
        outputs = await self.model.generate(**inputs)
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return {"response": response}
    
    async def train_model(self, training_data: List[str]):
        """Train model on provided data"""
        dataset = DockerGoDataset(training_data)
        dataloader = DataLoader(dataset, batch_size=16, shuffle=True)
        
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        optimizer = torch.optim.Adam(self.model.parameters(), lr=1e-5)
        
        for epoch in range(5):
            self.model.train()
            total_loss = 0
            
            for batch in dataloader:
                input_ids = batch['input_ids'].to(device)
                attention_mask = batch['attention_mask'].to(device)
                labels = batch['labels'].to(device)
                
                optimizer.zero_grad()
                
                outputs = self.model(input_ids, attention_mask=attention_mask, labels=labels)
                loss = outputs.loss
                
                loss.backward()
                optimizer.step()
                
                total_loss += loss.item()
            
            logging.info(f'Epoch {epoch+1}, Loss: {total_loss / len(dataloader)}')