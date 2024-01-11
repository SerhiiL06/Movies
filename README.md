# Movie API

This project is a FastAPI-based application designed to provide users with the ability to create and manage their lists of favorite movies. Users can easily compile and update their movie lists through the provided API.

## Getting Started

Follow these steps to set up the project on your local machine:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/SerhiiL06/Movies
   cd api
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the FastAPI Application:**
   ```bash
   uvicorn main.web:app --reload
   ```

   The API will be accessible at `http://127.0.0.1:8000`.

## API Endpoints

### User Registration
- `POST /register`: Register a new user.

