# Deployment Guide for Sentiment Analysis Application

This guide provides step-by-step instructions for deploying the Sentiment Analysis application using GitHub, Vercel (frontend), and Render (backend).

## Prerequisites

- GitHub account
- Vercel account
- Render account
- Git and Git LFS installed locally

## Step 1: Prepare Your Repository

1. Install Git LFS if not already installed:
   - Windows: Download from https://git-lfs.github.com/
   - Mac: `brew install git-lfs`
   - Linux: `sudo apt-get install git-lfs`

2. Initialize Git LFS:
   ```
   git lfs install
   ```

3. Run the deployment script:
   ```
   .\deploy.ps1
   ```
   
   This script will:
   - Initialize Git and Git LFS
   - Track large model files
   - Commit your changes
   - Push to your GitHub repository

## Step 2: Deploy Backend on Render

1. Log in to your Render account
2. Click "New" and select "Web Service"
3. Connect your GitHub repository
4. Configure the service:
   - Name: `sentiment-analysis-api`
   - Environment: Python
   - Build Command: `pip install -r backend/requirements.txt && mkdir -p /opt/render/project/src/model && cp -r model/fine_tuned_model /opt/render/project/src/model/`
   - Start Command: `cd backend && uvicorn app:app --host 0.0.0.0 --port $PORT`
   - Select appropriate instance type (at least 1GB RAM recommended)

5. Add environment variables:
   - `MODEL_PATH`: `/opt/render/project/src/model/fine_tuned_model`
   - `SECRET_KEY`: (generate a random string)

6. Create a PostgreSQL database:
   - Click "New" and select "PostgreSQL"
   - Name: `sentiment-db`
   - User: `postgres`
   - Connect it to your web service

7. After the database is created, copy its internal connection string to your web service:
   - Go to your PostgreSQL database dashboard
   - Copy the internal connection string
   - Add it as `DATABASE_URL` environment variable in your web service

8. Deploy the service and wait for it to build and start

9. Note your backend URL (e.g., `https://sentiment-analysis-api.onrender.com`)

## Step 3: Deploy Frontend on Vercel

1. Log in to your Vercel account
2. Click "Add New" and select "Project"
3. Import your GitHub repository
4. Configure the project:
   - Framework Preset: Vite
   - Root Directory: `./`
   - Build Command: `cd frontend && npm install && npm run build`
   - Output Directory: `frontend/dist`

5. Add environment variables:
   - `VITE_API_URL`: Your Render backend URL (e.g., `https://sentiment-analysis-api.onrender.com`)

6. Click "Deploy"
7. After deployment, Vercel will provide a URL for your frontend (e.g., `https://sentiment-analysis-frontend.vercel.app`)

## Step 4: Configure Custom Domain (Optional)

### Vercel Custom Domain

1. Go to your Vercel project dashboard
2. Click on "Domains"
3. Add your custom domain
4. Follow Vercel's instructions to configure DNS settings

### Render Custom Domain

1. Go to your Render web service dashboard
2. Click on "Settings" and then "Custom Domain"
3. Add your custom domain
4. Follow Render's instructions to configure DNS settings

## Step 5: Update CORS Settings

If you're using a custom domain, update the CORS settings in your backend:

1. Go to your GitHub repository
2. Edit `backend/app.py`
3. Add your custom domain to the `origins` list
4. Commit and push the changes
5. Render will automatically redeploy your backend

## Step 6: Verify Deployment

1. Visit your frontend URL
2. Test the sentiment analysis functionality
3. Check that the backend API is responding correctly

## Troubleshooting

### Model Loading Issues

If the model fails to load on Render:

1. Check Render logs for errors
2. Verify that the model files were correctly copied during the build process
3. Consider upgrading to a larger instance type if memory is insufficient

### Database Connection Issues

If the backend can't connect to the database:

1. Verify the `DATABASE_URL` environment variable
2. Check that the database is running
3. Ensure the database user has the correct permissions

### CORS Issues

If you encounter CORS errors:

1. Check the browser console for specific error messages
2. Verify that your frontend URL is included in the `origins` list in `backend/app.py`
3. Redeploy the backend after making changes

## Maintaining Your Deployment

### Updating Your Application

1. Make changes to your local repository
2. Commit and push to GitHub
3. Vercel and Render will automatically redeploy your application

### Monitoring

1. Use Render's built-in logs and metrics to monitor your backend
2. Use Vercel's analytics to monitor your frontend
3. Consider setting up additional monitoring tools for production use 