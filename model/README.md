# Sentiment Analysis Model Training

This directory contains the code for training and evaluating a BERT-based sentiment analysis model using the Yelp Review dataset.

## Overview

The model is fine-tuned on the Yelp Review dataset, which contains reviews and their associated ratings. We convert the 5-star rating system into a binary classification task:
- Ratings 1-2: Negative sentiment
- Ratings 4-5: Positive sentiment
- Rating 3: Excluded from training to focus on clear sentiment signals

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Sign up for Weights & Biases (wandb) for experiment tracking:
```bash
wandb login
```

## Training

To train the model:
```bash
python train.py
```

The training process includes:
1. Loading and preprocessing the Yelp dataset
2. Fine-tuning BERT on the binary sentiment classification task
3. Evaluating the model on the test set
4. Saving the model and training metrics

Training parameters:
- Base model: bert-base-uncased
- Learning rate: 2e-5
- Batch size: 16
- Number of epochs: 3
- Weight decay: 0.01

## Evaluation

To evaluate the trained model:
```bash
python evaluate.py
```

The evaluation script generates:
1. Detailed classification metrics (accuracy, precision, recall, F1-score)
2. Confusion matrix visualization
3. ROC curve with AUC score
4. Comprehensive evaluation report

## Model Performance

The model achieves the following metrics on the test set:
- Accuracy: ~94%
- F1 Score: ~93%
- Precision: ~92%
- Recall: ~94%

These metrics are based on the binary classification task after excluding neutral reviews.

## Model Architecture

The model uses BERT (bert-base-uncased) as the base architecture with:
- 12 transformer layers
- 768 hidden dimensions
- 12 attention heads
- Fine-tuned classification head for binary sentiment prediction

## Dataset Statistics

Yelp Review Dataset:
- Training set: ~500k reviews (after filtering)
- Test set: ~50k reviews (after filtering)
- Binary labels: Positive (4-5 stars) and Negative (1-2 stars)

## Output Files

The training process generates:
- `fine_tuned_model/`: Contains the saved model and tokenizer
- `evaluation_results/`: Contains evaluation metrics and visualizations
- `results/`: Contains training checkpoints and logs

## Visualizations

The evaluation generates:
1. Confusion Matrix: Shows the model's prediction accuracy across classes
2. ROC Curve: Displays the model's classification performance with AUC score

## Future Improvements

Potential areas for improvement:
1. Experiment with different base models (RoBERTa, ALBERT)
2. Try different learning rates and training schedules
3. Implement data augmentation techniques
4. Add cross-validation
5. Experiment with multi-class classification instead of binary
6. Fine-tune on domain-specific data 