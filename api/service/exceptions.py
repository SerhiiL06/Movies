from infrastructure.db.models.base import Base


class ObjectDoesntExists(Exception):
    def __init__(self, model: Base) -> None:
        self.model = model


class SomethingWentWrong(Exception):
    pass


class PermissionDenied(Exception):
    pass
