from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()  # creates your backend app

# Structure of data
class Feedback(BaseModel):
    name: str
    message: str

# Temporary database (list)
feedback_list = []

# API 1: Home (check working)
@app.get("/")
def home():
    return {
  "name": "Hemanth",
  "message": "Backend working perfectly!"

}

# API 2: Create feedback
@app.post("/feedback")
def create_feedback(item: Feedback):
    feedback_list.append(item)
    return {"message": "Feedback saved", "data": item}

# API 3: Get all feedbacks
@app.get("/feedback")
def get_feedback():
    return feedback_list
