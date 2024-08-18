class ApplicationError(Exception):
    def __init__(self, message: str):
        self.message = message


class EmailError(ApplicationError):
    def __init__(self, message: str):
        super().__init__(message)


class ZoomError(ApplicationError):
    def __init__(self, message: str):
        super().__init__(message)


class AWSS3Error(ApplicationError):
    def __init__(self, message: str):
        super().__init__(message)
