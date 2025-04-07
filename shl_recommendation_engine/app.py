from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)
catalogue_df = pd.read_csv("shl_product_catalogue_sample.csv")

# Basic keyword-based recommendation
def recommend_assessments(prompt):
    prompt = prompt.lower()
    keywords = {
        "developer": ["cognitive", "ability", "numerical"],
        "sales": ["sales", "customer", "personality"],
        "manager": ["leadership", "management"],
        "student": ["graduate", "aptitude", "entry-level"],
        "hr": ["talent", "personality", "occupational"]
    }

    matched_types = set()
    for key, types in keywords.items():
        if key in prompt:
            matched_types.update(types)

    if not matched_types:
        matched_types.add("ability")

    recommendations = catalogue_df[catalogue_df["Type"].str.lower().str.contains('|'.join(matched_types), na=False)]
    return recommendations[["Name", "Type", "URL"]].head(5)

@app.route('/', methods=["GET", "POST"])
def index():
    results = None
    if request.method == "POST":
        user_prompt = request.form["prompt"]
        results = recommend_assessments(user_prompt)
    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)
