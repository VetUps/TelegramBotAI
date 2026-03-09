from transformers import (
    PreTrainedModel,
    TokenizersBackend
)
import torch
import re

class Classifier:
    TARGET_COLS = ['normal', 'insult', 'threat', 'obscenity']

    def __init__(self, model: PreTrainedModel, tokenizer: TokenizersBackend):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = self.initialize_model(model)
        self.tokenizer = tokenizer

    def predict(self, text: str, threshold: float = 0.5):
        """
        Предсказание тональности текста
        :param text: текст для которого будет происходить предсказание
        :param threshold: порог засчитывания класса тональности как истинного
        :return: словарь с информацией о предсказании
        """
        text = self.preprocess(text)

        inputs = self.tokenizer(
            text,
            truncation=True,
            padding=True,
            max_length=128,
            return_tensors="pt"
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = torch.sigmoid(outputs.logits).cpu().numpy()
            predictions = (probs >= threshold).astype(int)

        return {
            "text": text,
            "predictions": {col: bool(predictions[0][i]) for i, col in enumerate(self.TARGET_COLS)},
            "probabilities": {col: round(float(probs[0][i]), 4) for i, col in enumerate(self.TARGET_COLS)}
        }

    def preprocess(self, text: str) -> str:
        """
        Базовая предобработка текста
        :param text: необработанный текст
        :return: обработанный текст
        """
                   
        text = re.sub(r'<[^>]+>', ' ', text)
             
        text = re.sub(r'http\S+|www\.\S+', ' ', text)
                        
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def initialize_model(self, model: PreTrainedModel) -> PreTrainedModel:
        """
        Инициализация модели
        :param model: pre_trained модель
        :return: инициализированная модель
        """
        model = model.to(self.device)
        model.eval()
        return model
