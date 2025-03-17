# Deployment Guide

This guide explains how to deploy the Sentiment Analysis application to Vercel (frontend) and Render (backend).

## Prerequisites

- GitHub account
- Vercel account
- Render account
- PostgreSQL database (can be hosted on Render)

## Step 1: Prepare Your Repository

1. Create a GitHub repository for your project
2. Push your code to the repository:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/sentiment-analysis.git
git push -u origin main
```

## Step 2: Deploy the Backend on Render

1. Log in to [Render](https://render.com)
2. Click "New" and select "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - Name: `sentiment-analysis-api`
   - Root Directory: `backend`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Select the appropriate plan (Free tier works for testing)

5. Add environment variables:
   - `DATABASE_URL`: Your PostgreSQL connection string
   - `SECRET_KEY`: A secure random string for JWT token generation
   - `MODEL_PATH`: `/opt/render/project/src/model/fine_tuned_model`

6. Click "Create Web Service"

## Step 3: Create a PostgreSQL Database on Render

1. In Render dashboard, click "New" and select "PostgreSQL"
2. Configure the database:
   - Name: `sentiment-analysis-db`
   - Database: `sentiment_db`
   - User: `sentiment_user`
   - Select the appropriate plan
3. Click "Create Database"
4. Once created, copy the "Internal Database URL"
5. Update the `DATABASE_URL` environment variable in your backend service

## Step 4: Deploy the Frontend on Vercel

1. Log in to [Vercel](https://vercel.com)
2. Click "Add New" and select "Project"
3. Import your GitHub repository
4. Configure the project:
   - Framework Preset: `Vite`
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `dist`
5. Add environment variables:
   - `VITE_API_URL`: Your Render backend URL (e.g., `https://sentiment-analysis-api.onrender.com`)
6. Click "Deploy"

## Step 5: Update CORS Settings

After deployment, update the CORS settings in your backend to allow requests from your Vercel domain:

1. Edit `backend/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

2. Commit and push the changes:
```bash
git add backend/main.py
git commit -m "Update CORS settings for production"
git push
```

## Step 6: Verify Deployment

1. Visit your Vercel frontend URL
2. Register a new account
3. Log in and test the sentiment analysis functionality

## Troubleshooting

### Backend Issues
- Check Render logs for any errors
- Verify environment variables are set correctly
- Ensure the database connection is working

### Frontend Issues
- Check Vercel build logs
- Verify the `VITE_API_URL` is set correctly
- Test API endpoints using tools like Postman

## Maintenance

- Monitor application performance
- Set up automatic database backups
- Implement CI/CD pipelines for continuous deployment 