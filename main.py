from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import SessionLocal, engine
from models import Base, Feedback as FeedbackModel


from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request


# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")


# Schema for input validation (from user)
class Feedback(BaseModel):
    name: str
    message: str

# Dependency - creates a new database session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.get("/home", response_class=HTMLResponse)
def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/")
def read_root():
    return {
  "message": "Feedback API connected Woth SQLite"
}



@app.post("/feedback")
def create_feedback(item: Feedback, db: Session = Depends(get_db)):
    feedback_data = FeedbackModel(name=item.name, message=item.message)
    db.add(feedback_data)
    db.commit()
    db.refresh(feedback_data)
    return {"message": "Feedback saved to database!", "data": item}

@app.get("/feedback")
def get_feedback(db: Session = Depends(get_db)):
    feedbacks = db.query(FeedbackModel).all()
    return feedbacks
