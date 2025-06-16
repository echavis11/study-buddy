#!/bin/bash

# Exit on any error
set -e

# --- BACKEND ---
echo "🔧 Starting Flask backend..."
cd backend

# Optional: activate virtualenv
if [ -d "venv" ]; then
  source venv/bin/activate
fi

# Load env vars
if [ -f ".env" ]; then
  export $(grep -v '^#' .env | xargs)
fi

export FLASK_APP=app.py
export FLASK_ENV=development
flask run &
BACKEND_PID=$!
cd ..

# --- FRONTEND ---
echo "🧩 Starting React frontend..."
cd study-buddy
npm run dev &
FRONTEND_PID=$!
cd ..

# Optional: Open browser
sleep 2
if command -v xdg-open >/dev/null; then
  xdg-open http://localhost:5173
elif command -v open >/dev/null; then
  open http://localhost:5173
fi

# Wait for background processes
trap "kill $BACKEND_PID $FRONTEND_PID" EXIT
wait
