from flask import Flask, jsonify, request
from flask_cors import CORS
from services.flashcardGenerator import extract_text_from_pdf, generate_flashcards


app = Flask(__name__)
CORS(app)

@app.route('/api/generate', methods=['POST'])
def generate():
    if 'pdf' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    pdf_file = request.files['pdf']
    text = extract_text_from_pdf(pdf_file)
    flashcards = generate_flashcards(text)

    return jsonify({'flashcards': flashcards})

if __name__ == '__main__':
    app.run(debug=True)
