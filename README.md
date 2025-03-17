# Sentiment Analysis Application

A full-stack application for sentiment analysis using a fine-tuned BERT model.

## Project Structure

- `frontend/`: React frontend application
- `backend/`: FastAPI backend server
- `model/`: Fine-tuned sentiment analysis model

## Features

- User authentication (register/login)
- Sentiment analysis of text input
- Display of model information and performance metrics
- Responsive UI built with React and Tailwind CSS

## Tech Stack

- **Frontend**: React, TypeScript, Tailwind CSS, Vite
- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **ML**: PyTorch, Transformers, DistilBERT

## Local Development

### Backend

1. Navigate to the project root
2. Set up a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r backend/requirements.txt
   ```
4. Set up environment variables in `.env` file
5. Start the backend server:
   ```
   cd backend
   uvicorn app:app --reload --port 8001
   ```

### Frontend

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```
2. Install dependencies:
   ```
   npm install
   ```
3. Start the development server:
   ```
   npm run dev
   ```

## Deployment

### GitHub Setup

1. Create a new GitHub repository
2. Push your code to GitHub:
   ```
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/sentiment-analysis.git
   git push -u origin main
   ```

### Backend Deployment (Render)

1. Create a Render account at https://render.com
2. Connect your GitHub repository
3. Create a new Web Service:
   - Select your GitHub repository
   - Name: `sentiment-analysis-api`
   - Environment: Python
   - Build Command: `pip install -r backend/requirements.txt && mkdir -p /opt/render/project/src/model && cp -r model/fine_tuned_model /opt/render/project/src/model/`
   - Start Command: `cd backend && uvicorn app:app --host 0.0.0.0 --port $PORT`
4. Add environment variables:
   - `MODEL_PATH`: `/opt/render/project/src/model/fine_tuned_model`
   - `SECRET_KEY`: (generate a random string)
5. Create a PostgreSQL database:
   - Name: `sentiment-db`
   - Connect it to your web service

### Frontend Deployment (Vercel)

1. Create a Vercel account at https://vercel.com
2. Install Vercel CLI:
   ```
   npm install -g vercel
   ```
3. Connect your GitHub repository to Vercel
4. Configure project settings:
   - Framework Preset: Vite
   - Build Command: `cd frontend && npm install && npm run build`
   - Output Directory: `frontend/dist`
   - Environment Variables:
     - `VITE_API_URL`: Your Render backend URL (e.g., https://sentiment-analysis-api.onrender.com)
5. Deploy the project

## Continuous Deployment

Both Vercel and Render support automatic deployments when you push changes to your GitHub repository.

## Important Notes

- The model files are large. Consider using Git LFS for version control.
- Ensure your Render instance has enough resources to load the model.
- The free tier of Render may have cold starts, which can affect model loading time.

## License

MIT 