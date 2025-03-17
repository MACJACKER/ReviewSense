import os
import glob
import re
from datetime import datetime

def find_latest_evaluation_file():
    """Find the latest evaluation results file in the model/evaluation directory."""
    eval_dir = "evaluation"  # Changed from "model/evaluation" to "evaluation"
    
    if not os.path.exists(eval_dir):
        print(f"Evaluation directory not found: {eval_dir}")
        return None
    
    # Find all results files
    result_files = glob.glob(os.path.join(eval_dir, "results_*.txt"))
    
    if not result_files:
        print(f"No evaluation result files found in {eval_dir}")
        return None
    
    # Sort by timestamp in filename
    result_files.sort(reverse=True)
    return result_files[0]

def parse_metrics(file_path):
    """Parse the metrics from the evaluation results file."""
    metrics = {}
    
    try:
        with open(file_path, 'r') as f:
            content = f.read()
            
            # Extract metrics using regex
            accuracy = re.search(r'accuracy: ([\d\.]+)', content)
            f1 = re.search(r'f1: ([\d\.]+)', content)
            precision = re.search(r'precision: ([\d\.]+)', content)
            recall = re.search(r'recall: ([\d\.]+)', content)
            
            if accuracy:
                metrics['accuracy'] = float(accuracy.group(1))
            if f1:
                metrics['f1'] = float(f1.group(1))
            if precision:
                metrics['precision'] = float(precision.group(1))
            if recall:
                metrics['recall'] = float(recall.group(1))
                
            # Extract timestamp from filename
            timestamp_match = re.search(r'results_(\d{8}_\d{6})\.txt', os.path.basename(file_path))
            if timestamp_match:
                timestamp_str = timestamp_match.group(1)
                timestamp = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
                metrics['timestamp'] = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    
    except Exception as e:
        print(f"Error parsing metrics file: {str(e)}")
        return None
    
    return metrics

def find_confusion_matrix_image(timestamp_str):
    """Find the confusion matrix image corresponding to the results file."""
    if not timestamp_str:
        return None
    
    eval_dir = "evaluation"  # Changed from "model/evaluation" to "evaluation"
    cm_pattern = os.path.join(eval_dir, f"confusion_matrix_{timestamp_str}.png")
    
    # Also check for .txt files if .png is not found
    if not os.path.exists(cm_pattern):
        cm_pattern = os.path.join(eval_dir, f"confusion_matrix_{timestamp_str}.txt")
    
    cm_files = glob.glob(cm_pattern)
    if cm_files:
        return cm_files[0]
    
    return None

def main():
    print("Checking model evaluation metrics...")
    
    # Find the latest evaluation file
    latest_file = find_latest_evaluation_file()
    
    if not latest_file:
        print("No evaluation files found. Please run the fine-tuning script first.")
        return
    
    print(f"Found evaluation file: {latest_file}")
    
    # Parse metrics
    metrics = parse_metrics(latest_file)
    
    if not metrics:
        print("Failed to parse metrics from the evaluation file.")
        return
    
    # Print metrics
    print("\nModel Evaluation Metrics:")
    print("=========================")
    print(f"Accuracy:  {metrics.get('accuracy', 'N/A'):.4f}")
    print(f"F1 Score:  {metrics.get('f1', 'N/A'):.4f}")
    print(f"Precision: {metrics.get('precision', 'N/A'):.4f}")
    print(f"Recall:    {metrics.get('recall', 'N/A'):.4f}")
    print(f"Timestamp: {metrics.get('timestamp', 'N/A')}")
    
    # Find confusion matrix image
    timestamp_str = os.path.basename(latest_file).replace("results_", "").replace(".txt", "")
    cm_file = find_confusion_matrix_image(timestamp_str)
    
    if cm_file:
        print(f"\nConfusion Matrix: {cm_file}")
        print("To view the confusion matrix, open the image file.")
    else:
        print("\nConfusion matrix image not found.")
    
    print("\nTo improve these metrics, you can:")
    print("1. Adjust hyperparameters in fine_tune.py")
    print("2. Use a different pre-trained model")
    print("3. Increase the training data size")
    print("4. Implement data augmentation techniques")

if __name__ == "__main__":
    main() 