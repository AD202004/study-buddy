import json
from matcher import *

with open("config.json") as f:
        config = json.load(f)
        input_student={
                    "student_id": "test_2",
                    "goal": "Master Python",
                    "preferred_study_time": "early_morning",
                    "study_type": "visual",
                    "personality": ["introvert", "organized"]
                }

        students = load_students("data/students.json")
        matched_id, score, reason = match_student(input_student, students, config)
        print(reason)
        response = {
            "matched_student_id": matched_id,
            "match_score": score,
            "reasoning": reason
        }
        print(response)
        