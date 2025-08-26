from backend import create_app
from backend.models import db

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure DB tables exist
    app.run(host="0.0.0.0", port=5000, debug=True)