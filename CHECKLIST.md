# Deployment Checklist

Use this checklist to ensure all steps are completed for a successful deployment.

## Pre-Deployment

- [ ] All code changes are committed and pushed to GitHub
- [ ] Frontend environment variables are configured correctly
- [ ] Backend environment variables are configured correctly
- [ ] Database connection string is set up properly
- [ ] Model files are tracked with Git LFS
- [ ] CORS settings include all necessary domains
- [ ] All dependencies are listed in requirements.txt and package.json

## GitHub Setup

- [ ] Repository created on GitHub
- [ ] Git LFS installed and initialized
- [ ] Large model files tracked with Git LFS
- [ ] Code pushed to GitHub repository

## Backend Deployment (Render)

- [ ] Render account created
- [ ] GitHub repository connected to Render
- [ ] Web service created with correct settings
- [ ] PostgreSQL database created
- [ ] Environment variables configured:
  - [ ] DATABASE_URL
  - [ ] MODEL_PATH
  - [ ] SECRET_KEY
- [ ] Build and deployment successful
- [ ] Health endpoint responding correctly

## Frontend Deployment (Vercel)

- [ ] Vercel account created
- [ ] GitHub repository connected to Vercel
- [ ] Project configured with correct settings
- [ ] Environment variables configured:
  - [ ] VITE_API_URL (pointing to Render backend)
- [ ] Build and deployment successful
- [ ] Frontend loading correctly

## Post-Deployment Verification

- [ ] Frontend can connect to backend API
- [ ] Sentiment analysis functionality works
- [ ] User registration works
- [ ] User login works
- [ ] Database operations working correctly
- [ ] Model loading correctly

## Custom Domain Setup (Optional)

- [ ] Custom domain purchased
- [ ] DNS settings configured for Vercel
- [ ] DNS settings configured for Render
- [ ] SSL certificates issued and working
- [ ] CORS settings updated for custom domains

## Final Checks

- [ ] Application is responsive on different devices
- [ ] Error handling works correctly
- [ ] Performance is acceptable
- [ ] Security measures are in place
- [ ] Documentation is up to date 