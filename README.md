# Rugby League Match Simulation

This project simulates a rugby league match using a Python backend and a React frontend. The Python backend handles the game logic and state management, while the React frontend provides a user interface for interacting with the simulation.


## Prerequisites

- **Python 3.8+** (Ensure you have Python installed)
- **Node.js** (Ensure you have Node.js and npm installed)
- **Pipenv** (Optional, for managing Python dependencies)

## Installation Instructions

### 1. Set Up the Python Backend

1. Navigate to the backend directory:

    ```bash
    cd tff-rugbyleague-backend
    ```

2. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

3. Activate the virtual environment:

    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```

    - On Windows:
      ```bash
      venv\Scripts\activate
      ```

4. Install Python dependencies:
    ```bash
    pip install Flask
    pip install flask-cors
    ```

5. Run the Python backend:

    ```bash
    python app.py
    ```

   The backend should start running on `http://127.0.0.1:5000`.

### 2. Set Up the React Frontend

1. Navigate to the frontend directory:

    ```bash
    cd tff-rugbyleague-frontend
    ```

2. Install Node.js dependencies:

    ```bash
    npm install
    ```

3. Start the React development server:

    ```bash
    npm start
    ```

   The frontend should start running on `http://localhost:3000`.

### 3. Running Both Projects in Parallel

You will need to keep both the backend and frontend servers running simultaneously. Here’s a recommended approach:

1. Open two terminal windows or tabs.
2. In the first terminal, run the Python backend as described above.
3. In the second terminal, navigate to the `frontend/` directory and run the React frontend as described above.

### 4. Accessing the Application

Once both servers are running, you can access the application at:

- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend API: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Additional Information

- The backend API is responsible for handling the game logic and state, whilst the frontend provides the user interface.
- The frontend interacts with the backend via RESTful API calls.
- If you encounter CORS issues, make sure the Flask backend is properly configured to allow cross-origin requests.

## Troubleshooting

- If the backend fails to start, make sure you have all dependencies installed and that your Python environment is correctly set up.
- If the frontend fails to load, ensure all Node.js dependencies are installed by running `npm install` again.

## License

This project is licensed under the MIT License.
