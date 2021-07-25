import itertools

store = [
    {"user": 1, "score": 1220, "level": 3},
    {"user": 2, "score": 1500, "level": 3},
    {"user": 3, "score": 1500, "level": 3},
    {"user": 4, "score": 1500, "level": 3},
    {"user": 5, "score": 1220, "level": 3},
    {"user": 6, "score": 1500, "level": 3},
    {"user": 7, "score": 1500, "level": 3},
    {"user": 8, "score": 1500, "level": 3},
    {"user": 9, "score": 1220, "level": 3},
    {"user": 10, "score": 1500, "level": 3},
    {"user": 11, "score": 1500, "level": 3},
    {"user": 12, "score": 1500, "level": 3},
    {"user": 13, "score": 1220, "level": 3},
    {"user": 14, "score": 1500, "level": 3},
    {"user": 15, "score": 1500, "level": 3},
]
# I NEED TO ADD SCORE MATCH BY USER TO ASCENDING


def check_rank(score: int, rank: int = 15):
    if len(store) == rank:
        try:
            score_queryset = (q for q in store if score > q["score"])
            score_rank = sorted(score_queryset, key=lambda q: q["score"], reverse=True)
            store.remove(score_rank[-1])
            return True
        except:
            return False


def peek(iterable):
    try:
        first = next(iterable)
    except StopIteration:
        return None
    return first, itertools.chain([first], iterable)


def get_high_score_list(level_id: int, db: list):
    queryset = (
        {"user": q["user"], "score": q["score"]} for q in db if level_id == q["level"]
    )
    queryset = sorted(queryset, key=lambda q: q["score"], reverse=True)
    return str(queryset)


def add_scores(level_id: int, score: int, user_id: int, db: list):
    lvl_queryset = [q for q in db if level_id == q["level"]]
    user_queryset = [q for q in lvl_queryset if user_id == q["user"]]

    if lvl_queryset == []:
        db.append({"user": user_id, "score": score, "level": level_id})
        return str(
            {"Success": f"User {user_id} has the first high score on level {level_id}"}
        )

    elif user_queryset != []:
        for q in user_queryset:
            if q["score"] < score:
                q["score"] = score
                return str(
                    {
                        "Success": f"User {user_id} has a new high score on level {level_id}"
                    }
                )
            else:
                return str(
                    {
                        "Success": f"User {user_id} keeps their old high score on level {level_id}"
                    }
                )

    else:
        top_score = check_rank(score)
        if top_score:
            db.append({"user": user_id, "score": score, "level": level_id})
            return str(
                {"Success": f"User {user_id} has a new high score on level {level_id}"}
            )
        else:
            return str(
                {
                    "Success": f"User {user_id} did not make the top 15 on level {level_id}"
                }
            )
