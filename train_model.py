import os
import pandas as pd
import joblib
from xgboost import XGBClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score



# ✅ Check if file exists
if not os.path.exists('data/Cleaned_SQLInjection_Dataset.csv'):
    print("❌ File not found. Please double-check the path!")
    exit()

# ✅ Load dataset
df = pd.read_csv('data/Cleaned_SQLInjection_Dataset.csv')
print("✅ Dataset loaded successfully!")

# ✅ Feature extraction
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['Query'])  # Ensure column is named 'Query'
y = df['Label']

# ✅ Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ✅ Train XGBoost classifier
xgb = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
xgb.fit(X_train, y_train)

# ✅ Predict and evaluate
y_pred = xgb.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

from sklearn.metrics import precision_score, recall_score, f1_score

# ✅ Precision, Recall, F1 Score
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

# ✅ Print metrics
print(f"✅ XGBoost Accuracy: {accuracy * 100:.2f}%")
print(f"✅ Precision: {precision * 100:.2f}%")
print(f"✅ Recall: {recall * 100:.2f}%")
print(f"✅ F1 Score: {f1 * 100:.2f}%")



# ✅ Save model and vectorizer
os.makedirs("models", exist_ok=True)
joblib.dump(xgb, 'models/xgb_model.pkl')
joblib.dump(vectorizer, 'models/vectorizer.pkl')




