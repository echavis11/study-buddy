from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from models import Flashcard
from utils.openai_helper import extract_text_from_pdf, generate_flashcards

flashcard_bp = Blueprint("flashcard_bp", __name__)

@flashcard_bp.route("/generate", methods=["POST"])
@jwt_required()
def generate():
    if "file" not in request.files:
        return jsonify({"error": "PDF file required"}), 400

    user_id = get_jwt_identity()
    file = request.files["file"]

    text = extract_text_from_pdf(file)
    flashcards = generate_flashcards(text)

    for card in flashcards:
        new_card = Flashcard(user_id=user_id, question=card["question"], answer=card["answer"])
        db.session.add(new_card)
    db.session.commit()

    return jsonify(flashcards), 200

@flashcard_bp.route("/my-flashcards", methods=["GET"])
@jwt_required()
def get_my_flashcards():
    user_id = get_jwt_identity()
    cards = Flashcard.query.filter_by(user_id=user_id).all()
    return jsonify([{"question": c.question, "answer": c.answer} for c in cards])
