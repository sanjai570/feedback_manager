#!/bin/bash

# Navigate to the backend directory if running from outside
if [ -f "backend/manage.py" ]; then
    cd backend
fi

echo "Starting Backend Server..."
python3 manage.py runserver 0.0.0.0:8000 &
BACKEND_PID=$!

echo "Starting Frontend Server..."
cd frontend
npm run dev -- --host 0.0.0.0 &
FRONTEND_PID=$!

# Function to handle script termination
cleanup() {
    echo "Stopping servers..."
    kill $BACKEND_PID
    kill $FRONTEND_PID
    exit
}

# Trap SIGINT (Ctrl+C) to run cleanup
trap cleanup SIGINT

# Keep script running to maintain processes
wait
