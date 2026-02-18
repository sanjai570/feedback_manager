# Campus Resource Management System - Frontend

This is the React frontend for the Campus Resource Management System. It connects to the Django backend to provide a user interface for managing users, resources, and bookings.

## Tech Stack

*   **React** (Vite)
*   **Axios** for API requests
*   **React Router** for navigation
*   **Lucide React** for icons
*   **Vanilla CSS** for styling

## Prerequisites

*   Node.js (v16 or higher)
*   npm
*   Django Backend running on `http://127.0.0.1:8000`

## Installation

1.  Navigate to the frontend directory:
    ```bash
    cd frontend
    ```

2.  Install dependencies:
    ```bash
    npm install
    ```

## Running the Project

1.  Start the development server:
    ```bash
    npm run dev
    ```

2.  Open your browser at the URL shown (usually `http://localhost:5173`).

## Configuration

The frontend is configured to proxy API requests to `http://127.0.0.1:8000` (the Django backend) to avoid CORS issues during development. This is configured in `vite.config.js`.

## Features

*   **Dashboard**: Overview of system statistics.
*   **Users**: Manage students and staff users.
*   **Resources**: Manage labs, classrooms, and halls.
*   **Bookings**: Create and manage bookings with conflict detection.
