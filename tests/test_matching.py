import pytest
from backend.app.services.matching_engine import MatchingEngine

@pytest.fixture
def engine():
    return MatchingEngine()

def test_matching_engine_rejection(engine):
    # Test rejection when no relevant experience
    jd_data = {
        "job_title": "Python Developer",
        "description": "Looking for a Python Developer with 3 years of experience",
        "key_responsibilities": ["Develop Python applications"]
    }
    resume_data = {
        "full_name": "John Doe",
        "total_experience": 5,
        "experience": [
            {
                "role": "Accountant",
                "company": "Finance Corp",
                "duration": "5 years",
                "description": "Managed books"
            }
        ],
        "skills": ["Accounting", "Excel"]
    }
    skills_weightage = {"python": 50, "django": 50}
    
    result = engine.calculate_ats_score(jd_data, resume_data, skills_weightage)
    
    assert result["overall_score"] == 0.0
    assert result["detailed_analysis"]["rejection_reason"] == "No relevant job role experience"

def test_matching_engine_success(engine):
    # Test success when relevant experience exists
    jd_data = {
        "job_title": "Python Developer",
        "description": "Looking for a Python Developer",
        "key_responsibilities": ["Develop Python applications"]
    }
    resume_data = {
        "full_name": "Jane Smith",
        "total_experience": 3,
        "experience": [
            {
                "role": "Python Developer",
                "company": "Tech Solutions",
                "duration": "3 years",
                "description": "Built web apps with Python"
            }
        ],
        "skills": ["Python", "Flask"]
    }
    skills_weightage = {"python": 100}
    
    result = engine.calculate_ats_score(jd_data, resume_data, skills_weightage)
    
    assert result["overall_score"] > 0.0
