from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from typing import Tuple
import os
from dotenv import load_dotenv
import numpy as np
import json

load_dotenv()

class SentimentAnalyzer:
    def __init__(self):
        # Get the current working directory
        current_dir = os.getcwd()
        print(f"Current working directory: {current_dir}")
        
        # Check if fine-tuned model exists, otherwise use pre-trained model
        model_path = os.getenv("MODEL_PATH", "../model/fine_tuned_model")
        print(f"MODEL_PATH from environment: {model_path}")
        
        # Convert to absolute path if it's a relative path
        if not os.path.isabs(model_path):
            model_path = os.path.abspath(os.path.join(current_dir, model_path))
            print(f"Converted to absolute path: {model_path}")
        
        # Check if the model path exists
        if os.path.exists(model_path):
            print(f"Model path exists: {model_path}")
        else:
            print(f"Model path does not exist: {model_path}")
            
        # Check if config.json exists in the model path
        config_path = os.path.join(model_path, "config.json")
        if os.path.exists(config_path):
            print(f"Config file exists: {config_path}")
        else:
            print(f"Config file does not exist: {config_path}")
        
        # Check if the model path exists and contains necessary files
        if os.path.exists(model_path) and os.path.exists(os.path.join(model_path, "config.json")):
            try:
                print(f"Loading fine-tuned model from {model_path}")
                # Use the same model name for both tokenizer and model to ensure compatibility
                self.tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
                self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
                print("Successfully loaded fine-tuned model")
            except Exception as e:
                print(f"Error loading fine-tuned model: {e}")
                print("Falling back to pre-trained model")
                model_name = "distilbert-base-uncased-finetuned-sst-2-english"
                self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        else:
            print("Fine-tuned model not found, using pre-trained model")
            model_name = "distilbert-base-uncased-finetuned-sst-2-english"
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        
        # Move model to GPU if available
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        
        print(f"Model loaded successfully on {self.device}")

    def analyze(self, text: str) -> Tuple[str, float]:
        try:
            # Tokenize the input text
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
            
            # Remove token_type_ids if present (DistilBERT doesn't use them)
            if 'token_type_ids' in inputs:
                del inputs['token_type_ids']
                
            inputs = {name: tensor.to(self.device) for name, tensor in inputs.items()}

            # Get model prediction
            with torch.no_grad():
                outputs = self.model(**inputs)
                probabilities = torch.nn.functional.softmax(outputs.logits, dim=1)

            # Get prediction and confidence
            prediction = torch.argmax(probabilities, dim=1)
            confidence = torch.max(probabilities).item()

            # Map prediction to sentiment
            sentiment_map = {0: "negative", 1: "positive"}
            sentiment = sentiment_map[prediction.item()]

            return sentiment, confidence
        except Exception as e:
            print(f"Error in sentiment analysis: {e}")
            # Return a default response in case of error
            return "neutral", 0.5
    
    def get_model_info(self) -> dict:
        """Return information about the model"""
        model_info = {
            "model_type": self.model.config.model_type,
            "hidden_size": self.model.config.hidden_size,
            "num_labels": self.model.config.num_labels,
            "vocab_size": self.model.config.vocab_size,
            "device": str(self.device)
        }
        
        # Try to load additional metrics from model_info.json if it exists
        model_path = os.getenv("MODEL_PATH", "../model/fine_tuned_model")
        model_info_path = os.path.join(model_path, "model_info.json")
        
        if os.path.exists(model_info_path):
            try:
                with open(model_info_path, 'r') as f:
                    additional_info = json.load(f)
                model_info.update(additional_info)
            except Exception as e:
                print(f"Error loading model_info.json: {e}")
        
        return model_info

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, '_instance'):
            cls._instance = cls()
        return cls._instance 