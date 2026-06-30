from flask import Flask, render_template, request, jsonify, redirect, url_for
import ollama
import subprocess  # NEW: Ye Mac ki aawaz ke liye zaroori hai

app = Flask(__name__)

# --- NEW: Mac Voice Function ---
def speak(text):
    """Uses the native macOS 'say' command for high-quality speech."""
    clean_text = text.replace('"', '').replace("'", "")
    subprocess.run(["say", clean_text])
# -------------------------------

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login_system', methods=['POST'])
def login_system():
    user = request.form.get('username')
    pwd = request.form.get('password')
    with open("saved_logins.txt", "a") as file:
        file.write(f"Username: {user} | Password: {pwd}\n")
    return redirect(url_for('assistant_page'))

@app.route('/assistant')
def assistant_page():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message')

    if not user_message:
        return jsonify({'error': 'Message is empty'}), 400

    try:
        response = ollama.chat(
            model='llama3.2:1b', 
            messages=[{'role': 'user', 'content': user_message}]
        )
        reply = response['message']['content']
        
        # NEW: Python will instantly speak the reply using Mac's premium voice!
        speak(reply)
        
        return jsonify({'reply': reply})
        
    except Exception as e:
        print(f"Backend Error: {e}")
        return jsonify({'error': 'Ollama is not responding.'}), 500

if __name__ == '__main__':
    # host='0.0.0.0' allows other devices on the Wi-Fi to connect
    app.run(host='0.0.0.0', debug=True, port=5001)