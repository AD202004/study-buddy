from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

test_set = [
    {
        "input": {
            "student_id": "test_1",
            "goal": "Crack GATE 2025",
            "preferred_study_time": "early_morning",
            "study_type": "visual",
            "personality": ["focused", "introvert"]
        },
        "expected_match": "stu_1017"
    },
    {
        "input": {
            "student_id": "test_2",
            "goal": "Learn Data Science",
            "preferred_study_time": "late_night",
            "study_type": "kinesthetic",
            "personality": ["creative", "patient"]
        },
        "expected_match": "stu_1007"
    },
    {
        "input": {
            "student_id": "test_3",
            "goal": "Ace GRE",
            "preferred_study_time": "evening",
            "study_type": "auditory",
            "personality": ["introvert", "organized"]
        },
        "expected_match": "stu_1004"
    },
    {
        "input": {
            "student_id": "test_4",
            "goal": "Prepare for CAT",
            "preferred_study_time": "evening",
            "study_type": "reading",
            "personality": ["collaborative", "creative", "focused"]
        },
        "expected_match": "stu_1005"
    },
    {
        "input": {
            "student_id": "test_5",
            "goal": "Get into IIT",
            "preferred_study_time": "early_morning",
            "study_type": "reading",
            "personality": ["organized", "collaborative"]
        },
        "expected_match": "stu_1002"
    },
    {
        "input": {
            "student_id": "test_6",
            "goal": "Improve Math Skills",
            "preferred_study_time": "early_morning",
            "study_type": "visual",
            "personality": ["analytical", "extrovert", "patient"]
        },
        "expected_match": "stu_1003"
    },
    {
        "input": {
            "student_id": "test_7",
            "goal": "Ace GRE",
            "preferred_study_time": "early_morning",
            "study_type": "auditory",
            "personality": ["creative", "analytical", "extrovert"]
        },
        "expected_match": "stu_1008"
    },
    {
        "input": {
            "student_id": "test_8",
            "goal": "Master Python",
            "preferred_study_time": "afternoon",
            "study_type": "visual",
            "personality": ["creative", "introvert"]
        },
        "expected_match": "stu_1001"
    },
    {
        "input": {
            "student_id": "test_9",
            "goal": "Crack GATE 2025",
            "preferred_study_time": "late_night",
            "study_type": "reading",
            "personality": ["organized", "analytical"]
        },
        "expected_match": "stu_1010"
    },
    {
        "input": {
            "student_id": "test_10",
            "goal": "Prepare for CAT",
            "preferred_study_time": "late_night",
            "study_type": "reading",
            "personality": ["focused", "creative"]
        },
        "expected_match": "stu_1014"
    },
    {
        "input": {
            "student_id": "test_11",
            "goal": "Excel in Physics",
            "preferred_study_time": "afternoon",
            "study_type": "auditory",
            "personality": ["introvert", "extrovert", "organized"]
        },
        "expected_match": "stu_1015"
    },
    {
        "input": {
            "student_id": "test_12",
            "goal": "Crack GATE 2025",
            "preferred_study_time": "afternoon",
            "study_type": "visual",
            "personality": ["analytical", "introvert", "creative"]
        },
        "expected_match": "stu_1006"
    },
    {
        "input": {
            "student_id": "test_13",
            "goal": "Get into IIT",
            "preferred_study_time": "evening",
            "study_type": "kinesthetic",
            "personality": ["collaborative", "creative"]
        },
        "expected_match": "stu_1016"
    },
    {
        "input": {
            "student_id": "test_14",
            "goal": "Ace GRE",
            "preferred_study_time": "late_night",
            "study_type": "reading",
            "personality": ["introvert", "organized", "creative"]
        },
        "expected_match": "stu_1018"
    },
    {
        "input": {
            "student_id": "test_15",
            "goal": "Prepare for CAT",
            "preferred_study_time": "afternoon",
            "study_type": "auditory",
            "personality": ["focused", "extrovert"]
        },
        "expected_match": "stu_1019"
    },
    {
        "input": {
            "student_id": "test_16",
            "goal": "Learn Data Science",
            "preferred_study_time": "evening",
            "study_type": "reading",
            "personality": ["collaborative", "analytical", "patient"]
        },
        "expected_match": "stu_1020"
    },
    {
        "input": {
            "student_id": "test_17",
            "goal": "Master Python",
            "preferred_study_time": "early_morning",
            "study_type": "kinesthetic",
            "personality": ["introvert", "creative"]
        },
        "expected_match": "stu_1021"
    },
    {
        "input": {
            "student_id": "test_18",
            "goal": "Excel in Physics",
            "preferred_study_time": "late_night",
            "study_type": "visual",
            "personality": ["organized", "analytical", "focused"]
        },
        "expected_match": "stu_1022"
    },
    {
        "input": {
            "student_id": "test_19",
            "goal": "Improve Math Skills",
            "preferred_study_time": "evening",
            "study_type": "auditory",
            "personality": ["patient", "collaborative"]
        },
        "expected_match": "stu_1023"
    },
    {
        "input": {
            "student_id": "test_20",
            "goal": "Get into IIT",
            "preferred_study_time": "afternoon",
            "study_type": "visual",
            "personality": ["focused", "introvert", "creative"]
        },
        "expected_match": "stu_1024"
    }
]

def test_accuracy():
    correct = 0
    for case in test_set:
        response = client.post("/match", json=case["input"])
        data = response.json()
        if data["matched_student_id"] == case["expected_match"]:
            correct += 1
    accuracy = correct / len(test_set) if test_set else 0
    print(f"Accuracy: {accuracy:.2%} ({correct}/{len(test_set)})")
    assert accuracy >= 0.7  # for example, expect at least 70% accuracy
