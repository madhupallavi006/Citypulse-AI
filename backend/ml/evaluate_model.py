import os
import joblib
import pandas as pd
from backend.ml.feature_engineering import prepare_train_test_data

def evaluate_saved_model(model_path="models/congestion_model.joblib", csv_path="data/synthetic_traffic_dataset.csv"):
    if not os.path.exists(model_path):
        print(f"Model file not found at {model_path}. Please run train_model.py first.")
        return None
        
    artifact = joblib.load(model_path)
    model = artifact["model"]
    model_name = artifact["model_name"]
    metrics = artifact["metrics"]
    
    print(f"=== Model Evaluation Report for {model_name} ===")
    print(f"Saved Accuracy:  {metrics['accuracy']:.4f}")
    print(f"Saved Precision: {metrics['precision']:.4f}")
    print(f"Saved Recall:    {metrics['recall']:.4f}")
    print(f"Saved F1-Score:  {metrics['f1']:.4f}")
    print(f"Saved ROC-AUC:   {metrics['auc']:.4f}")
    print("=================================================")
    
    return metrics

if __name__ == "__main__":
    evaluate_saved_model()
