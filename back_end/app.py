import sqlite3
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# OpenAI client with environment variable
# Get API key from environment variable or use test mode
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)
USE_TEST_MODE = OPENAI_API_KEY is None

if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)
else:
    client = None
    print("⚠️  WARNING: OPENAI_API_KEY not set. Running in TEST MODE with mock responses.")

# Database setup
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT,
            bot_response TEXT,
            mood TEXT,
            timestamp DATETIME
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Safety filter
def safety_check(message):
    urgent_keywords = ["suicide", "self harm", "kill myself", "end my life"]
    for word in urgent_keywords:
        if word in message.lower():
            return "I'm concerned about what you're sharing. Please reach out to a professional or a crisis helpline immediately."
    return None

@app.route('/')
def home():
    return jsonify({"status": "WellBot Backend is Running"})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    user_mood = data.get('mood', 'Neutral')

    warning = safety_check(user_message)
    if warning:
        return jsonify({"reply": warning})

    try:
        # If API key is not set, use mock response for testing
        if USE_TEST_MODE or client is None:
            # Generate a mock response for testing
            mock_responses = {
                "happy": "That's wonderful! Keep spreading that positive energy!",
                "sad": "I understand you're going through a tough time. Remember, it's okay to feel sad. Consider talking to someone you trust.",
                "anxious": "Anxiety is a common feeling. Try some deep breathing exercises and remember you're not alone.",
                "stressed": "Stress can be overwhelming. Take a break, go for a walk, or practice mindfulness. You've got this!",
                "neutral": "How can I help you today? I'm here to support your wellness journey."
            }
            mood_lower = user_mood.lower()
            bot_reply = mock_responses.get(mood_lower, mock_responses["neutral"])
        else:
            # Use real OpenAI API
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are WellBot, a supportive wellness assistant."},
                    {"role": "user", "content": f"My mood is {user_mood}. {user_message}"}
                ]
            )
            bot_reply = response.choices[0].message.content

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO chats (user_message, bot_response, mood, timestamp) VALUES (?, ?, ?, ?)",
            (user_message, bot_reply, user_mood, datetime.now())
        )
        conn.commit()
        conn.close()

        return jsonify({"reply": bot_reply})

    except Exception as e:
        print("Error:", e)
        return jsonify({"reply": "Server error. Try again later."}), 500

if __name__ == '__main__':
    app.run(debug=False, port=5000)
