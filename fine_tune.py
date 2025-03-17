import os
import torch
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset
from datetime import datetime

# Configuration
MODEL_NAME = "distilbert-base-uncased"
OUTPUT_DIR = "fine_tuned_model"
EVAL_DIR = "evaluation"
BATCH_SIZE = 16
EPOCHS = 3
LEARNING_RATE = 2e-5

# Create directories if they don't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(EVAL_DIR, exist_ok=True)

# Sample data for sentiment analysis
# In a real scenario, you would load this from a file or database
def create_sample_data():
    positive_samples = [
        "This product is amazing! I love it.",
        "Great service, would recommend to everyone.",
        "The quality exceeded my expectations.",
        "Best purchase I've made this year.",
        "Very satisfied with the results.",
        "Excellent customer support.",
        "The team was very helpful and responsive.",
        "I'm impressed with how well this works.",
        "This has made my life so much easier.",
        "Fantastic experience from start to finish."
    ]
    
    negative_samples = [
        "Terrible product, don't waste your money.",
        "The customer service was awful.",
        "I'm very disappointed with the quality.",
        "This didn't work as advertised.",
        "Would not recommend to anyone.",
        "Complete waste of time and money.",
        "The worst experience I've had.",
        "I regret this purchase.",
        "Very frustrating to use.",
        "Poor design and implementation."
    ]
    
    # Create a balanced dataset
    texts = positive_samples + negative_samples
    labels = [1] * len(positive_samples) + [0] * len(negative_samples)
    
    # Create a DataFrame
    df = pd.DataFrame({"text": texts, "label": labels})
    
    # Add more synthetic data for better training
    for _ in range(45):  # Add 45 more examples of each class
        for sample in positive_samples:
            words = sample.split()
            # Create variations by removing or shuffling words
            if len(words) > 3:
                new_sample = " ".join(words[1:])
                new_df = pd.DataFrame({"text": [new_sample], "label": [1]})
                df = pd.concat([df, new_df], ignore_index=True)
        
        for sample in negative_samples:
            words = sample.split()
            # Create variations by removing or shuffling words
            if len(words) > 3:
                new_sample = " ".join(words[1:])
                new_df = pd.DataFrame({"text": [new_sample], "label": [0]})
                df = pd.concat([df, new_df], ignore_index=True)
    
    return df

# Load and prepare data
print("Preparing dataset...")
df = create_sample_data()
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

# Convert to Hugging Face datasets
train_dataset = Dataset.from_pandas(train_df)
test_dataset = Dataset.from_pandas(test_df)

# Load tokenizer and model
print(f"Loading model: {MODEL_NAME}")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2)

# Tokenize datasets
def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=128)

train_dataset = train_dataset.map(tokenize_function, batched=True)
test_dataset = test_dataset.map(tokenize_function, batched=True)

# Define training arguments
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    num_train_epochs=EPOCHS,
    per_device_train_batch_size=BATCH_SIZE,
    per_device_eval_batch_size=BATCH_SIZE,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=10,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
    learning_rate=LEARNING_RATE,
)

# Define trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
)

# Train the model
print("Starting fine-tuning...")
trainer.train()

# Save the model
print(f"Saving model to {OUTPUT_DIR}")
trainer.save_model(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

# Evaluate the model
print("Evaluating model...")
predictions = trainer.predict(test_dataset)
preds = np.argmax(predictions.predictions, axis=1)
labels = predictions.label_ids

# Calculate metrics
accuracy = accuracy_score(labels, preds)
precision, recall, f1, _ = precision_recall_fscore_support(labels, preds, average='weighted')

# Create confusion matrix
cm = confusion_matrix(labels, preds)

# Save results
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
results_file = os.path.join(EVAL_DIR, f"results_{timestamp}.txt")
cm_file = os.path.join(EVAL_DIR, f"confusion_matrix_{timestamp}.png")

# Save metrics to file
with open(results_file, "w") as f:
    f.write("Model Evaluation Results\n")
    f.write("=======================\n")
    f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write(f"Model: fine-tuned {MODEL_NAME} for sentiment analysis\n\n")
    f.write("Metrics:\n")
    f.write(f"- accuracy: {accuracy:.4f}\n")
    f.write(f"- f1: {f1:.4f}\n")
    f.write(f"- precision: {precision:.4f}\n")
    f.write(f"- recall: {recall:.4f}\n\n")
    f.write(f"Test set size: {len(test_df)} samples\n")
    f.write(f"Training time: {EPOCHS} epochs\n\n")
    f.write("Notes:\n")
    f.write("- Model fine-tuned on synthetic sentiment analysis data\n")
    f.write("- Performance metrics are based on the test set\n")
    f.write("- For production use, consider fine-tuning on a larger, domain-specific dataset\n")

# Plot confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
            xticklabels=['Negative', 'Positive'],
            yticklabels=['Negative', 'Positive'])
plt.xlabel('Predicted')
plt.ylabel('True')
plt.title('Confusion Matrix')
plt.savefig(cm_file)
plt.close()

print(f"Evaluation results saved to {results_file}")
print(f"Confusion matrix saved to {cm_file}")
print("\nModel Evaluation Metrics:")
print(f"Accuracy: {accuracy:.4f}")
print(f"F1 Score: {f1:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")

print("\nFine-tuning completed successfully!") 