from dataclasses import dataclass

@dataclass
class Problem:
    id: int
    title: str
    difficulty: str

@dataclass
class ReviewLog:
    id: int | None
    problem_id: int
    reviewed_at: date
    result: str