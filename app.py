from flask import Flask, request, jsonify, render_template
from agent import agent_executor

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("message", "").strip()
    try:
        resp = agent_executor.invoke({"input": user_input})
        return jsonify({"reply": resp["output"]})
    except Exception as e:
        print("Error in /ask:", e)
        return jsonify({"reply": "Sorry, something went wrong. please try again. (Using a free tier model, so the the model might overload)"}), 500

if __name__ == "__main__":
    app.run(debug=True)
