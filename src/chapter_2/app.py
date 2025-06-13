from flask import Flask, Response, jsonify, render_template, request

from .chain import chain

app = Flask(__name__)


@app.route("/")
def index() -> str:
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process() -> Response:
    name = request.form["name"]
    company = request.form["company"]
    job_title = request.form["job_title"]
    summary, photo_url = chain(name, company, job_title)
    return jsonify(
        {
            "summary": summary.summary,
            "interesting_facts": summary.interesting_facts,
            "recent_work_experience": summary.recent_work_experience,
            "estimated_earnings": summary.estimated_earnings,
            "upskilling": summary.upskilling,
            "picture_url": photo_url,
        }
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8647, debug=True)
