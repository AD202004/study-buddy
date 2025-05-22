import json
import numpy as np
import fasttext

# Load FastText model (must be trained and saved as 'fasttext.bin')
model = fasttext.load_model('fasttext.bin')

def get_avg_vector(text):
    words = text.lower().split()
    if not words:
        return np.zeros(model.get_dimension())
    vectors = [model.get_word_vector(w) for w in words]
    return np.mean(vectors, axis=0)

def cosine_similarity(vec1, vec2):
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return float(np.dot(vec1, vec2) / (norm1 * norm2))

def goal_similarity(goal1, goal2):
    vec1 = get_avg_vector(goal1)
    vec2 = get_avg_vector(goal2)
    return cosine_similarity(vec1, vec2)

def personality_similarity(personality1, personality2):
    # Join personality lists into space-separated strings
    vec1 = get_avg_vector(" ".join(personality1))
    vec2 = get_avg_vector(" ".join(personality2))
    return cosine_similarity(vec1, vec2)

def load_students(path):
    with open(path, "r") as f:
        return json.load(f)

def match_student(input_student, candidates, config):
    best_score = 0
    best_match = None
    best_reason = None

    for c in candidates:
        if c["student_id"] == input_student["student_id"]:
            continue

        goal_sim = goal_similarity(input_student["goal"], c["goal"])
        study_time_match = input_student["preferred_study_time"] == c["preferred_study_time"]
        study_type_match = input_student["study_type"] == c["study_type"]
        personality_sim = personality_similarity(input_student["personality"], c["personality"])
        personality_overlap = list(set(input_student["personality"]) & set(c["personality"]))

        score = (
            goal_sim * config["boost_goal_match"] +
            (config["study_time_weight"] if study_time_match else 0) +
            (config["study_type_weight"] if study_type_match else 0) +
            personality_sim * config["personality_weight"]
        ) / (config["boost_goal_match"] + config["study_time_weight"] + config["study_type_weight"] + config["personality_weight"])

        if score > best_score:
            best_score = score
            best_match = c
            best_reason = {
                "goal_similarity": round(goal_sim, 2),
                "study_time_match": study_time_match,
                "study_type_match": study_type_match,
                "personality_overlap": personality_overlap
            }
        print(f"Candidate: {c['student_id']}, Goal Sim: {goal_sim}, Study Time: {study_time_match}, Study Type: {study_type_match}, Personality Sim: {personality_sim}, Score: {score}")
    if best_match and best_score >= config["minimum_match_score"]:
        return best_match["student_id"], round(best_score, 2), best_reason
    else:
        return None, 0, {}

    