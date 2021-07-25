import pytest
import db


@pytest.fixture
def example_score_data():
    return [
        {"user": 1, "score": 1220, "level": 3},
        {"user": 2, "score": 1500, "level": 3},
        {"user": 3, "score": 1500, "level": 3},
        {"user": 4, "score": 1500, "level": 3},
        {"user": 21, "score": 1220, "level": 3},
        {"user": 5, "score": 1220, "level": 3},
        {"user": 6, "score": 1500, "level": 45},
        {"user": 7, "score": 1500, "level": 3},
        {"user": 8, "score": 1500, "level": 3},
        {"user": 9, "score": 1220, "level": 3},
        {"user": 10, "score": 1500, "level": 3},
        {"user": 32, "score": 1500, "level": 3},
        {"user": 12, "score": 1500, "level": 3},
        {"user": 13, "score": 1220, "level": 3},
        {"user": 14, "score": 1500, "level": 3},
    ]


def test_check_rank_success():
    assert db.check_rank(1200, 15)


def test_check_rank_failure():
    pass


def test_add_scores_success():
    pass
