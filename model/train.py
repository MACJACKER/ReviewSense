import torch
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorWithPadding
)
from datasets import load_dataset
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
import wandb
import os
from datetime import datetime

# Initialize wandb for experiment tracking
wandb.init(project="yelp-sentiment-analysis")

def compute_metrics(pred):
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)
    
    precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='binary')
    acc = accuracy_score(labels, preds)
    
    return {
        'accuracy': acc,
        'f1': f1,
        'precision': precision,
        'recall': recall
    }

def preprocess_function(examples):
    return tokenizer(examples['text'], truncation=True, padding=True)

def main():
    # Load Yelp dataset
    print("Loading Yelp dataset...")
    dataset = load_dataset("yelp_review_full")
    
    # Convert 5-class to binary (1-2: negative, 4-5: positive, dropping 3)
    def convert_to_binary(example):
        if example['label'] <= 2:
            return {'label': 0}  # negative
        elif example['label'] >= 4:
            return {'label': 1}  # positive
        else:
            return {'label': -1}  # to be filtered
    
    dataset = dataset.map(convert_to_binary)
    dataset = dataset.filter(lambda x: x['label'] != -1)
    
    # Initialize tokenizer and model
    print("Initializing model and tokenizer...")
    model_name = "bert-base-uncased"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(
        model_name,
        num_labels=2
    )
    
    # Preprocess dataset
    print("Preprocessing dataset...")
    tokenized_dataset = dataset.map(
        preprocess_function,
        batched=True,
        remove_columns=dataset["train"].column_names
    )
    
    data_collator = DataCollatorWithPadding(tokenizer=tokenizer)
    
    # Define training arguments
    training_args = TrainingArguments(
        output_dir="./results",
        learning_rate=2e-5,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        num_train_epochs=3,
        weight_decay=0.01,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        push_to_hub=False,
        report_to="wandb"
    )
    
    # Initialize Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset["train"],
        eval_dataset=tokenized_dataset["test"],
        tokenizer=tokenizer,
        data_collator=data_collator,
        compute_metrics=compute_metrics,
    )
    
    # Train model
    print("Starting training...")
    trainer.train()
    
    # Evaluate model
    print("Evaluating model...")
    eval_results = trainer.evaluate()
    
    # Save results
    results_dir = "evaluation_results"
    os.makedirs(results_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = os.path.join(results_dir, f"eval_results_{timestamp}.txt")
    
    with open(results_file, "w") as f:
        f.write("Model Evaluation Results\n")
        f.write("=======================\n\n")
        for metric, value in eval_results.items():
            f.write(f"{metric}: {value:.4f}\n")
    
    # Save model
    print("Saving model...")
    save_dir = "fine_tuned_model"
    os.makedirs(save_dir, exist_ok=True)
    trainer.save_model(save_dir)
    tokenizer.save_pretrained(save_dir)
    
    print(f"Training completed! Results saved to {results_file}")
    print("\nEvaluation Results:")
    for metric, value in eval_results.items():
        print(f"{metric}: {value:.4f}")

if __name__ == "__main__":
    main() 