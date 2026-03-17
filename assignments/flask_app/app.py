from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to the Flask API application. The server is running successfully."

@app.route("/about")
def about():
    return "This application is developed using Python and Flask as part of a learning assignment."

if __name__ == "__main__":
    app.run(debug=True)
