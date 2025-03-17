# Deployment Steps for Sentiment Analysis Application

This guide provides detailed instructions for deploying your sentiment analysis application on Render (backend) and Vercel (frontend).

## Backend Deployment on Render

1. **Create a Render account**
   - Go to [render.com](https://render.com) and sign up
   - Verify your email

2. **Create a new Web Service**
   - Click "New" and select "Web Service"
   - Connect your GitHub repository (MACJACKER/ReviewSense)
   - Select the repository

3. **Configure the web service**
   - Name: `sentiment-analysis-api`
   - Environment: Python
   - Build Command: 
     ```
     pip install -r backend/requirements.txt && mkdir -p /opt/render/project/src/model && cp -r model/fine_tuned_model /opt/render/project/src/model/
     ```
   - Start Command: 
     ```
     cd backend && uvicorn app:app --host 0.0.0.0 --port 8001
     ```
   - Select the "Free" plan (or paid if needed)

4. **Add environment variables**
   - Click "Advanced" and add the following:
   - `MODEL_PATH`: `/opt/render/project/src/model/fine_tuned_model`
   - `SECRET_KEY`: (generate a random string or use a secure generator)
   - `PORT`: `8001`

5. **Create a PostgreSQL database**
   - Click "New" and select "PostgreSQL"
   - Name: `sentiment-db`
   - User: `postgres`
   - Select the "Free" plan
   - Click "Create Database"

6. **Link the database to your web service**
   - Go to your PostgreSQL database dashboard
   - Copy the "Internal Connection String"
   - Go back to your web service settings
   - Add environment variable: `DATABASE_URL` with the copied connection string

7. **Deploy the service**
   - Click "Create Web Service"
   - Wait for the build and deployment to complete (this may take several minutes)
   - Note your backend URL (e.g., `https://sentiment-analysis-api.onrender.com`)

## Frontend Deployment on Vercel

1. **Create a Vercel account**
   - Go to [vercel.com](https://vercel.com) and sign up
   - Verify your email

2. **Import your GitHub repository**
   - Click "Add New" and select "Project"
   - Connect your GitHub account if not already connected
   - Select your ReviewSense repository

3. **Configure the project**
   - Framework Preset: Vite
   - Root Directory: `./` (leave as default)
   - Build Command: `cd frontend && npm install && npm run build`
   - Output Directory: `frontend/dist`

4. **Add environment variables**
   - Click "Environment Variables"
   - Add: `VITE_API_URL` with your Render backend URL (e.g., `https://sentiment-analysis-api.onrender.com`)

5. **Deploy the project**
   - Click "Deploy"
   - Wait for the build and deployment to complete
   - Vercel will provide a URL for your frontend (e.g., `https://reviewsense.vercel.app`)

## Important Configuration Files

### vercel.json
```json
{
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ],
  "buildCommand": "cd frontend && npm install && npm run build",
  "outputDirectory": "frontend/dist",
  "framework": "vite",
  "github": {
    "silent": true,
    "autoAlias": true,
    "enabled": true
  },
  "trailingSlash": false,
  "cleanUrls": true
}
```

### render.yaml
```yaml
services:
  - type: web
    name: sentiment-analysis-api
    env: python
    buildCommand: pip install -r backend/requirements.txt && mkdir -p /opt/render/project/src/model && cp -r model/fine_tuned_model /opt/render/project/src/model/
    startCommand: cd backend && uvicorn app:app --host 0.0.0.0 --port 8001
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: sentiment-db
          property: connectionString
      - key: MODEL_PATH
        value: /opt/render/project/src/model/fine_tuned_model
      - key: SECRET_KEY
        generateValue: true
      - key: PORT
        value: 8001

databases:
  - name: sentiment-db
    databaseName: sentiment_db
    user: postgres
    plan: free
```

### Procfile
```
web: cd backend && uvicorn app:app --host 0.0.0.0 --port 8001
```

### frontend/.env.production
```
VITE_API_URL=https://sentiment-analysis-api.onrender.com
```

## Handling Model Files

Since your model files are large, you have a few options:

### Option 1: Upload to Render via SSH
1. After deploying on Render, go to your web service
2. Click on "Shell" to access the terminal
3. Create the model directory: `mkdir -p /opt/render/project/src/model/fine_tuned_model`
4. Use `curl` or `wget` to download your model files from a temporary storage (like Google Drive)

### Option 2: Use Hugging Face Hub
1. Create a Hugging Face account
2. Upload your model to Hugging Face Hub
3. Update your `sentiment_model.py` to load from Hugging Face

## Verification

After deployment:
1. Check the Render logs to ensure the backend is running correctly
2. Visit your Vercel URL to test the frontend
3. Try the sentiment analysis feature to verify everything works

## Troubleshooting

### Backend Issues
- Check Render logs for any errors
- Verify environment variables are set correctly
- Ensure the model files are accessible

### Frontend Issues
- Check Vercel build logs for any errors
- Verify the API URL is set correctly
- Check browser console for any CORS errors

### Database Issues
- Verify the database connection string
- Check if the database is running
- Ensure the tables are created properly 