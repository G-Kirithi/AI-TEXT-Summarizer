from flask import Flask, render_template, request
from transformers import pipeline

app = Flask(__name__)

# Load model once (important for speed)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

@app.route("/", methods=["GET", "POST"])
def index():
    summary_short = summary_medium = summary_long = ""

    if request.method == "POST":
        text = request.form["text"]

        summary_short = summarizer(text, max_length=50, min_length=10, do_sample=False)[0]['summary_text']
        summary_medium = summarizer(text, max_length=120, min_length=30, do_sample=False)[0]['summary_text']
        summary_long = summarizer(text, max_length=200, min_length=60, do_sample=False)[0]['summary_text']

    return render_template("index.html",
                           summary_short=summary_short,
                           summary_medium=summary_medium,
                           summary_long=summary_long)

if __name__ == "__main__":
    app.run(debug=True)