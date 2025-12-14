from fastapi import HTTPException, status


class HabitNotFoundException(HTTPException):
    def __init__(self, detail: str = "Habit not found."):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=detail
        )


class HabitAlreadyMarkedTodayException(HTTPException):
    def __init__(self, detail: str = "Habit already marked for today."):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT, 
            detail=detail
        )


class HabitNameConflictException(HTTPException):
    def __init__(self, detail: str = "Habit with this name already exists."):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=detail
        )


class InvalidInputException(HTTPException):
    def __init__(self, detail: str = "Invalid input data."):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=detail
        )