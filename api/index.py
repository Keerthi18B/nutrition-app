from flask import Flask, render_template, request
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")

# This is required for Vercel
if __name__ == "__main__":
    app.run()
