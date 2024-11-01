import strawberry


@strawberry.type
class MonthPayroll:
    id: int
    teacher_id: int
    teacher_name: str
    year: int
    month: int
    month_hours: int
    month_salary: float
