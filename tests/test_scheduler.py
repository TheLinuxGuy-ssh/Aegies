from scheduler import next_box, next_review_date
from datetime import date, timedelta

def test_next_box_correct_increments():
    assert next_box(1, "correct") == 2

def test_next_box_wrong_increments():
    assert next_box(5, "wrong") == 1

def test_next_box_increment_cap():
    assert next_box(5, "correct") == 5

def test_next_review_date_increments():
    assert next_review_date(2) == (date.today() + timedelta(days=3))