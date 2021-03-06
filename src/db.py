import logging

store = []


def check_rank(score: int, rank: int = 15):
    if len(store) == rank:
        try:
            score_queryset = (q for q in store if score > q["score"])
            score_rank = sorted(score_queryset, key=lambda q: (-q["score"], q["user"]))
            logging.info(f"Entry being removed: {score_rank[-1]}")
            store.remove(score_rank[-1])
            return True
        except:
            return False


def add_scores(level_id: int, score: int, user_id: int, db: list):
    lvl_queryset = [q for q in db if level_id == q["level"]]
    user_queryset = [q for q in lvl_queryset if user_id == q["user"]]
    if lvl_queryset == []:
        db.append({"user": user_id, "score": score, "level": level_id})
        logging.info(f"User {user_id} has the first high score on level {level_id}")
    elif user_queryset != []:
        for q in user_queryset:
            if q["score"] < score:
                q["score"] = score
                logging.info(f"User {user_id} has a new high score on level {level_id}")
            else:
                logging.info(
                    f"User {user_id} keeps their old high score on level {level_id}"
                )
    else:
        top_score = check_rank(score)
        if top_score:
            db.append({"user": user_id, "score": score, "level": level_id})
            logging.info(f"User {user_id} has a new high score on level {level_id}")
        else:
            logging.info(f"User {user_id} did not make the top 15 on level {level_id}")


def get_high_score_list(level_id: int, db: list):
    queryset = (
        {"user": q["user"], "score": q["score"]} for q in db if level_id == q["level"]
    )
    queryset = sorted(queryset, key=lambda q: (-q["score"], q["user"]))
    return str(queryset)
