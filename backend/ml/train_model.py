import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

from backend.ml.feature_engineering import prepare_train_test_data, FEATURE_COLUMNS

def train_and_save_models(csv_path="data/synthetic_traffic_dataset.csv", model_output_dir="models"):
    os.makedirs(model_output_dir, exist_ok=True)
    
    print("Loading synthetic dataset for ML model training...")
    X, y = prepare_train_test_data(csv_path)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Dataset split: {len(X_train)} training samples, {len(X_test)} test samples.")
    
    # 1. Random Forest Model
    print("\n--- Training Random Forest Classifier ---")
    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=12,
        random_state=42,
        n_jobs=-1
    )
    rf_model.fit(X_train, y_train)
    rf_preds = rf_model.predict(X_test)
    rf_probs = rf_model.predict_proba(X_test)[:, 1]
    
    rf_acc = accuracy_score(y_test, rf_preds)
    rf_prec = precision_score(y_test, rf_preds)
    rf_rec = recall_score(y_test, rf_preds)
    rf_f1 = f1_score(y_test, rf_preds)
    rf_auc = roc_auc_score(y_test, rf_probs)
    
    print(f"Random Forest Metrics:")
    print(f"  Accuracy:  {rf_acc:.4f}")
    print(f"  Precision: {rf_prec:.4f}")
    print(f"  Recall:    {rf_rec:.4f}")
    print(f"  F1-Score:  {rf_f1:.4f}")
    print(f"  ROC-AUC:   {rf_auc:.4f}")
    
    # 2. Gradient Boosting Model
    print("\n--- Training Gradient Boosting Classifier ---")
    gb_model = GradientBoostingClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=6,
        random_state=42
    )
    gb_model.fit(X_train, y_train)
    gb_preds = gb_model.predict(X_test)
    gb_probs = gb_model.predict_proba(X_test)[:, 1]
    
    gb_acc = accuracy_score(y_test, gb_preds)
    gb_prec = precision_score(y_test, gb_preds)
    gb_rec = recall_score(y_test, gb_preds)
    gb_f1 = f1_score(y_test, gb_preds)
    gb_auc = roc_auc_score(y_test, gb_probs)
    
    print(f"Gradient Boosting Metrics:")
    print(f"  Accuracy:  {gb_acc:.4f}")
    print(f"  Precision: {gb_prec:.4f}")
    print(f"  Recall:    {gb_rec:.4f}")
    print(f"  F1-Score:  {gb_f1:.4f}")
    print(f"  ROC-AUC:   {gb_auc:.4f}")
    
    # Compare & Save Best Model
    if rf_f1 >= gb_f1:
        best_model_name = "Random Forest"
        best_model = rf_model
        best_metrics = {"accuracy": rf_acc, "precision": rf_prec, "recall": rf_rec, "f1": rf_f1, "auc": rf_auc}
    else:
        best_model_name = "Gradient Boosting"
        best_model = gb_model
        best_metrics = {"accuracy": gb_acc, "precision": gb_prec, "recall": gb_rec, "f1": gb_f1, "auc": gb_auc}
        
    model_path = os.path.join(model_output_dir, "congestion_model.joblib")
    
    artifact = {
        "model_name": best_model_name,
        "model": best_model,
        "feature_columns": FEATURE_COLUMNS,
        "metrics": best_metrics
    }
    
    joblib.dump(artifact, model_path)
    print(f"\nSaved best model ({best_model_name}) artifact to {model_path}")
    return artifact

if __name__ == "__main__":
    train_and_save_models()
