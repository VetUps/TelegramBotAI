from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class Classifier:
    def __init__(self, model: AutoModelForSequenceClassification, tokenizer: AutoTokenizer):
        self.model = model
        self.tokenizer = tokenizer

    def predict(self, text: str):
        pass

    def preprocess(self, text: str):
        pass