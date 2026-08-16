def score_post(post, config):
    text = post["post_text"].lower()

    role_hits = [x for x in config["target_roles"] if x.lower() in text]
    keyword_hits = [x for x in config["target_keywords"] if x.lower() in text]

    score = min(len(role_hits) * 15, 45)
    score += min(len(keyword_hits) * 6, 36)

    if any(x in text for x in [
        "0-2 years", "0 - 2 years", "0–2 years", "fresher", "entry level"
    ]):
        score += 15

    if any(x in text for x in [
        "senior", "lead", "staff engineer", "principal", "manager"
    ]):
        score -= 30

    return {
        "score": max(0, min(100, score)),
        "matched_keywords": role_hits + keyword_hits,
    }
