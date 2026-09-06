from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database import Base # Importing the Base from the file you just made!

class Professor(Base):
    __tablename__ = "professors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    
    students = relationship("Student", back_populates="professor")

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    roll_no = Column(String, unique=True, index=True)
    name = Column(String)
    professor_id = Column(Integer, ForeignKey("professors.id"))
    
    professor = relationship("Professor", back_populates="students")
    submissions = relationship("Submission", back_populates="student")

class Submission(Base):
    __tablename__ = "submissions"
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    essay_text = Column(Text)
    status = Column(String, default="PENDING") 
    anomaly_score = Column(Float, nullable=True)
    
    student = relationship("Student", back_populates="submissions")
    interview = relationship("Interview", back_populates="submission", uselist=False)

class Interview(Base):
    __tablename__ = "interviews"
    id = Column(Integer, primary_key=True, index=True)
    submission_id = Column(Integer, ForeignKey("submissions.id"), unique=True)
    
    generated_questions = Column(JSON) 
    transcript = Column(JSON, nullable=True)
    final_verdict = Column(String, nullable=True) 
    
    submission = relationship("Submission", back_populates="interview")