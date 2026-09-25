from repository.attendance import create_checkin, load_attendance


def check_in(employee_id: str, employee_name: str) -> dict:
    return create_checkin(employee_id, employee_name)


def get_attendance() -> list[dict]:
    return load_attendance()
