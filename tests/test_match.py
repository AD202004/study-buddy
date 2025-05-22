'''import time
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_match_profile_1():
    payload = {
        "student_id": "stu_test1",
        "goal": "Crack GATE 2025",
        "preferred_study_time": "early_morning",
        "study_type": "visual",
        "personality": ["focused", "introvert"]
    }
    response = client.post("/match", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "matched_student_id" in data
    assert isinstance(data["match_score"], float)
    assert 0 <= data["match_score"] <= 1
    assert isinstance(data["reasoning"], dict)
    assert data["reasoning"]  # Not empty

def test_match_profile_2():
    payload = {
        "student_id": "stu_test2",
        "goal": "Learn Data Science",
        "preferred_study_time": "late_night",
        "study_type": "kinesthetic",
        "personality": ["creative", "patient"]
    }
    response = client.post("/match", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "matched_student_id" in data
    assert isinstance(data["match_score"], float)
    assert 0 <= data["match_score"] <= 1
    assert isinstance(data["reasoning"], dict)
    assert data["reasoning"]  # Not empty

def test_missing_fields():
    # Missing required field 'goal'
    payload = {
        "student_id": "stu_test3",
        "preferred_study_time": "afternoon",
        "study_type": "visual",
        "personality": ["creative"]
    }
    response = client.post("/match", json=payload)
    assert response.status_code == 422  # Unprocessable Entity

def test_no_match_found():
    # Use a profile that is very different from all students
    payload = {
        "student_id": "stu_test4",
        "goal": "Quantum Astrophysics",
        "preferred_study_time": "midnight",
        "study_type": "tactile",
        "personality": ["unique"]
    }
    response = client.post("/match", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["matched_student_id"] is None
    assert data["match_score"] == 0
    assert data["reasoning"] == {}

def test_response_time_1000_candidates(monkeypatch):
    # Simulate 1000 candidates
    import matcher
    students = []
    for i in range(1000):
        students.append({
            "student_id": f"stu_{i}",
            "goal": "Test Goal",
            "preferred_study_time": "evening",
            "study_type": "visual",
            "personality": ["focused"]
        })
    monkeypatch.setattr(matcher, "load_students", lambda path: students)
    payload = {
        "student_id": "stu_XYZ",
        "goal": "Test Goal",
        "preferred_study_time": "evening",
        "study_type": "visual",
        "personality": ["focused"]
    }
    start = time.time()
    response = client.post("/match", json=payload)
    end = time.time()
    assert (end - start) < 1.0  # Less than 1 second
    assert response.status_code == 200
'''
from fastapi.testclient import TestClient
from main import app
import time

client = TestClient(app)

# 1. Test /health endpoint
def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

# 2. Test /match endpoint with two different valid profiles
def test_match_profile_1():
    payload = {
        "student_id": "test_1",
        "goal": "Crack GATE 2025",
        "preferred_study_time": "early_morning",
        "study_type": "visual",
        "personality": ["focused", "introvert"]
    }
    response = client.post("/match", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "matched_student_id" in data
    assert isinstance(data["match_score"], float)
    assert 0 <= data["match_score"] <= 1
    assert isinstance(data["reasoning"], dict)
    assert data["reasoning"]  # Not empty

def test_match_profile_2():
    payload = {
        "student_id": "test_2",
        "goal": "Learn Data Science",
        "preferred_study_time": "late_night",
        "study_type": "kinesthetic",
        "personality": ["creative", "patient"]
    }
    response = client.post("/match", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "matched_student_id" in data
    assert isinstance(data["match_score"], float)
    assert 0 <= data["match_score"] <= 1
    assert isinstance(data["reasoning"], dict)
    assert data["reasoning"]  # Not empty

# 3. Test missing/invalid fields
def test_missing_fields():
    payload = {
        "student_id": "test_3",
        # missing 'goal'
        "preferred_study_time": "afternoon",
        "study_type": "visual",
        "personality": ["creative"]
    }
    response = client.post("/match", json=payload)
    assert response.status_code == 422  # Unprocessable Entity

# 4. Test no match found (very different profile)
def test_no_match_found():
    payload = {
        "student_id": "test_4",
        "goal": "Quantum Astrophysics",
        "preferred_study_time": "midnight",
        "study_type": "tactile",
        "personality": ["unique"]
    }
    response = client.post("/match", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["matched_student_id"] is None
    assert data["match_score"] == 0
    assert data["reasoning"] == {}

# 5. Test response time for 1000 candidates
def test_response_time_1000_candidates(monkeypatch):
    import matcher
    students = []
    for i in range(1000):
        students.append({
            "student_id": f"stu_{i}",
            "goal": "Test Goal",
            "preferred_study_time": "evening",
            "study_type": "visual",
            "personality": ["focused"]
        })
    monkeypatch.setattr(matcher, "load_students", lambda path: students)
    payload = {
        "student_id": "stu_XYZ",
        "goal": "Test Goal",
        "preferred_study_time": "evening",
        "study_type": "visual",
        "personality": ["focused"]
    }
    start = time.time()
    response = client.post("/match", json=payload)
    end = time.time()
    assert (end - start) < 1.0  # Less than 1 second
    assert response.status_code == 200
