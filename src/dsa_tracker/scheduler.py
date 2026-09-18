from datetime import date, timedelta

def next_box(current_box: int, result: int) -> int:
    if result == "correct":
        if current_box < 5:
            return current_box + 1
        else:
            return 5
    else:
        return 1

def next_review_date(box: int) -> date:
    duration = 0

    match box:
        case 1:
            duration = 1
        case 2:
            duration = 3
        case 3:
            duration = 7
        case 4:
            duration = 14
        case 5:
            duration = 30

    return date.today() + timedelta(days=duration)