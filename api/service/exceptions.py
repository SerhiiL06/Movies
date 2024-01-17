from infrastructure.db.models.base import Base


class ObjectDoesntExists(Exception):
    def __init__(self, model: Base) -> None:
        self.model = model


class UserAlreadyExists(Exception):
    def __init__(self, email) -> None:
        self.email = email


class SomethingWentWrong(Exception):
    pass


class PermissionDenied(Exception):
    pass
