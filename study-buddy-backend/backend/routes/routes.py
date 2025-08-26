from flask import Blueprint, request, jsonify
import asyncio
from src.slides import slide_generation
from backend.models import db, Flashcard
import json

routes = Blueprint("routes", __name__)

@routes.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    text = data.get("text", "")
    n = data.get("n", 5)

    try:
        flashcards_json = asyncio.run(slide_generation(text, n))
        flashcards = json.loads(flashcards_json)

        # Save to DB
        for fc in flashcards:
            card = Flashcard(
                question=fc.get("q", ""),
                answer=fc.get("a", ""),
                source_text=text
            )
            db.session.add(card)
        db.session.commit()

        return jsonify({"flashcards": flashcards})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@routes.route("/flashcards", methods=["GET"])
def list_flashcards():
    """
    Return all flashcards stored in DB
    """
    cards = Flashcard.query.order_by(Flashcard.created_at.desc()).all()
    return jsonify([
        {"id": c.id, "q": c.question, "a": c.answer, "source_text": c.source_text}
        for c in cards
    ])
