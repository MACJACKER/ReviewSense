from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import models
import schemas
from database import engine, get_db
from sentiment_model import SentimentAnalyzer
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sentiment Analysis API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Initialize sentiment analyzer
sentiment_analyzer = SentimentAnalyzer.get_instance()

# Authentication functions
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def authenticate_user(db, email: str, password: str):
    user = get_user(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = get_user(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

# API Endpoints
@app.post("/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        logger.info(f"Registration attempt for email: {user.email}")
        db_user = get_user(db, email=user.email)
        if db_user:
            logger.warning(f"Email already registered: {user.email}")
            raise HTTPException(status_code=400, detail="Email already registered")
        
        logger.debug(f"Hashing password for user: {user.email}")
        try:
            hashed_password = get_password_hash(user.password)
            logger.debug(f"Password hashed successfully")
        except Exception as hash_error:
            logger.error(f"Password hashing error: {str(hash_error)}", exc_info=True)
            raise HTTPException(status_code=500, detail=f"Password hashing failed: {str(hash_error)}")
        
        logger.debug(f"Creating user object for: {user.email}")
        try:
            db_user = models.User(email=user.email, hashed_password=hashed_password)
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            logger.info(f"User registered successfully: {user.email}")
            return db_user
        except Exception as db_error:
            logger.error(f"Database error: {str(db_error)}", exc_info=True)
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(db_error)}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Registration error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    logger.info(f"Login attempt for username: {form_data.username}")
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        logger.warning(f"Failed login attempt for username: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    logger.info(f"User logged in successfully: {form_data.username}")
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/me", response_model=schemas.User)
async def read_users_me(current_user = Depends(get_current_user)):
    return current_user

@app.get("/")
async def root():
    return {"message": "Welcome to the Sentiment Analysis API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/analyze", response_model=schemas.SentimentResponse)
async def analyze_sentiment(
    request: schemas.SentimentRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(f"Sentiment analysis request from user: {current_user.email}")
    # Perform sentiment analysis
    sentiment, confidence = sentiment_analyzer.analyze(request.text)
    
    # Create database record
    db_analysis = models.SentimentAnalysis(
        text=request.text,
        sentiment=sentiment,
        confidence=confidence
    )
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    
    # Return response
    return schemas.SentimentResponse(
        sentiment=sentiment,
        confidence=confidence,
        timestamp=datetime.now()
    )

@app.post("/analyze-public", response_model=schemas.SentimentResponse)
async def analyze_sentiment_public(
    request: schemas.SentimentRequest,
    db: Session = Depends(get_db)
):
    logger.info(f"Public sentiment analysis request")
    # Perform sentiment analysis
    sentiment, confidence = sentiment_analyzer.analyze(request.text)
    
    # Create database record
    db_analysis = models.SentimentAnalysis(
        text=request.text,
        sentiment=sentiment,
        confidence=confidence
    )
    db.add(db_analysis)
    db.commit()
    db.refresh(db_analysis)
    
    # Return response
    return schemas.SentimentResponse(
        sentiment=sentiment,
        confidence=confidence,
        timestamp=datetime.now()
    ) 