from flask import Blueprint, request, jsonify
from services.cosmos_service import search_documents, save_chat, get_chat_history
from services.gemini_service import ask_gemini

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/ask", methods=["POST"])
def ask_question():
    try:
        data = request.get_json()

        question = data.get("question", "")

        if not question:
            return jsonify({
                "success": False,
                "error": "Question is required"
            }), 400

        documents = search_documents()

        answer = ask_gemini(question, documents)

        save_chat(question, answer)

        return jsonify({
            "success": True,
            "question": question,
            "answer": answer
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@chat_bp.route("/history", methods=["GET"])
def chat_history():
    try:
        history = get_chat_history()

        return jsonify({
            "success": True,
            "history": history
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500