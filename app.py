from flask import Flask, request, render_template, redirect, url_for, flash
import joblib
import re

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Load Random Forest model and vectorizer
rf_model = joblib.load('models/xgb_model.pkl')
vectorizer = joblib.load('models/vectorizer.pkl')

valid_users = {
    "gauravp": "0102",
    "preranan": "1112",
    "prernam": "3132",
    "sakshik": "4142"
}

# Use Random Forest to detect SQL Injection
def is_sql_injection(text):
    vector = vectorizer.transform([text])
    prediction = rf_model.predict(vector)
    return prediction[0] == 1  # 1 = malicious

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Predict with ML model
        if is_sql_injection(password):
            flash("⚠️ Malicious input detected! Access blocked.", "error")
            return redirect(url_for('login'))

        if username in valid_users and valid_users[username] == password:
            flash("✅ Login successful!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("❌ Invalid username or password.", "error")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return "<h1>Welcome to the Dashboard! 🚀</h1>"

if __name__ == "__main__":
    app.run(debug=True)
