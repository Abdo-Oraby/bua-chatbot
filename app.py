# app.py
from flask import Flask, render_template, request, jsonify
from fuzzywuzzy import fuzz
from knowledge_base import get_knowledge_base

app = Flask(__name__)

# جلب قاعدة المعرفة
kb = get_knowledge_base()

def match_question(user_input):
    user_input = user_input.strip().lower()
    best_match = None
    best_score = 0

    for item in kb:
        for keyword in item["keywords"]:
            score = fuzz.partial_ratio(user_input, keyword)
            if score > best_score:
                best_score = score
                best_match = item

    if best_score >= 70:
        return best_match["answer"]
    
    return "آسف، ما فهمتش سؤالك جيدًا. من فضلك وضّح أكثر، أو تواصل مع إدارة الاستعلامات على الرقم: 01201599913-01201599914."

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_message = data.get("message", "")
    bot_response = match_question(user_message)
    # استبدل \n بـ <br> علشان يظهر في السطر الجديد
    bot_response = bot_response.replace("\n", "<br>")
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
