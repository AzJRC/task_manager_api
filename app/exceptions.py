from fastapi import HTTPException, status

class ExceptionObj:
    def __init__(self, status, detail):
        self.exception = HTTPException(status_code=status, detail=detail)

    def return_exception(self):
        return self.exception


def returnUnknownError():
    return ExceptionObj(status.HTTP_500_INTERNAL_SERVER_ERROR, "Something gone wrong.").return_exception()


def returnNotFound(item: str = "Item"):
    return ExceptionObj(status.HTTP_404_NOT_FOUND, f"{item} not found").return_exception()


def returnIntegrityError(item: str = "Item"):
    return ExceptionObj(status.HTTP_403_FORBIDDEN, f"{item} could not been created due to an integrity error. Maybe the item is already created.").return_exception()