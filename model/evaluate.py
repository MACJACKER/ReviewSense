import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from datasets import load_dataset
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    confusion_matrix,
    classification_report,
    roc_curve,
    auc
)
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

def load_model_and_tokenizer(model_path):
    print("Loading model and tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    return model, tokenizer

def prepare_test_dataset():
    print("Preparing test dataset...")
    dataset = load_dataset("yelp_review_full", split="test")
    
    # Convert 5-class to binary
    def convert_to_binary(example):
        if example['label'] <= 2:
            return {'label': 0}  # negative
        elif example['label'] >= 4:
            return {'label': 1}  # positive
        else:
            return {'label': -1}  # to be filtered
    
    dataset = dataset.map(convert_to_binary)
    dataset = dataset.filter(lambda x: x['label'] != -1)
    return dataset

def get_predictions(model, tokenizer, texts):
    model.eval()
    predictions = []
    probabilities = []
    
    with torch.no_grad():
        for text in texts:
            inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
            outputs = model(**inputs)
            logits = outputs.logits
            probs = torch.softmax(logits, dim=1)
            pred = torch.argmax(logits, dim=1)
            predictions.append(pred.item())
            probabilities.append(probs[0][1].item())  # Probability of positive class
    
    return np.array(predictions), np.array(probabilities)

def plot_confusion_matrix(y_true, y_pred, save_path):
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.savefig(save_path)
    plt.close()

def plot_roc_curve(y_true, y_prob, save_path):
    fpr, tpr, _ = roc_curve(y_true, y_prob)
    roc_auc = auc(fpr, tpr)
    
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend(loc="lower right")
    plt.savefig(save_path)
    plt.close()

def main():
    # Create results directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir = f"evaluation_results_{timestamp}"
    os.makedirs(results_dir, exist_ok=True)
    
    # Load model and test data
    model_path = "fine_tuned_model"
    model, tokenizer = load_model_and_tokenizer(model_path)
    test_dataset = prepare_test_dataset()
    
    # Get predictions
    print("Generating predictions...")
    predictions, probabilities = get_predictions(model, tokenizer, test_dataset['text'])
    true_labels = test_dataset['label']
    
    # Calculate metrics
    accuracy = accuracy_score(true_labels, predictions)
    precision, recall, f1, _ = precision_recall_fscore_support(true_labels, predictions, average='binary')
    
    # Generate classification report
    report = classification_report(true_labels, predictions)
    
    # Plot confusion matrix
    cm_path = os.path.join(results_dir, 'confusion_matrix.png')
    plot_confusion_matrix(true_labels, predictions, cm_path)
    
    # Plot ROC curve
    roc_path = os.path.join(results_dir, 'roc_curve.png')
    plot_roc_curve(true_labels, probabilities, roc_path)
    
    # Save results
    results_file = os.path.join(results_dir, 'evaluation_results.txt')
    with open(results_file, 'w') as f:
        f.write("Model Evaluation Results\n")
        f.write("=======================\n\n")
        f.write(f"Accuracy: {accuracy:.4f}\n")
        f.write(f"Precision: {precision:.4f}\n")
        f.write(f"Recall: {recall:.4f}\n")
        f.write(f"F1 Score: {f1:.4f}\n\n")
        f.write("Classification Report:\n")
        f.write("--------------------\n")
        f.write(report)
    
    print(f"\nEvaluation completed! Results saved to {results_dir}")
    print("\nKey Metrics:")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1 Score: {f1:.4f}")

if __name__ == "__main__":
    main() 