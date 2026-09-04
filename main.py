import os
import json
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm.session import Session
from google import genai
from google.genai import types

from database import engine, get_db
import models
import schemas

# Ensure tables exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="ProvenanceAI Backend", version="1.0.0")

# Initialize Gemini
client = genai.Client()

def generate_interrogation(essay_text: str):
    system_instruction = """
    You are an academic forensic examiner. Read the provided student essay. 
    Extract the 3 most complex analytical claims. 
    Generate exactly 3 deep, Socratic questions testing comprehension. 
    Output strictly as a JSON array of 3 strings.
    """
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=essay_text,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.2,
            response_mime_type="application/json",
        )
    )
    return json.loads(response.text)

@app.get("/")
def health_check():
    return {"status": "online"}

@app.post("/api/v1/submissions/analyze", response_model=schemas.SubmissionResponse, status_code=status.HTTP_201_CREATED)
def create_submission(payload: schemas.SubmissionCreate, db: Session = Depends(get_db)):
    # 1. Setup a mock student
    student = db.query(models.Student).filter(models.Student.id == payload.student_id).first()
    if not student:
        student = models.Student(roll_no=f"STU-{payload.student_id}", name="Test Student")
        db.add(student)
        db.commit()
        db.refresh(student)

    # 2. Mocking the Anomaly Score (Pretending the math flagged it as suspicious!)
    mock_anomaly_score = 0.85 
    status_verdict = "FLAGGED"

    # 3. Record the new submission
    new_submission = models.Submission(
        student_id=student.id,
        essay_text=payload.essay_text,
        status=status_verdict,
        anomaly_score=mock_anomaly_score,
    )
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)

    # 4. TRIGGER GEMINI: If flagged, generate questions and save to Interviews table
    if status_verdict == "FLAGGED":
        # Ask Gemini for the 3 questions
        questions_json = generate_interrogation(payload.essay_text)
        
        # Save the AI's questions to the database
        new_interview = models.Interview(
            submission_id=new_submission.id,
            generated_questions=questions_json,
            transcript=[], # Empty list ready for the chat UI
            final_verdict="PENDING"
        )
        db.add(new_interview)
        db.commit()

    return new_submission