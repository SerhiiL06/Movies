from abc import ABC


class AbstractRepository(ABC):
    def reade_model(self):
        raise NotImplementedError()

    def create_model(self):
        raise NotImplementedError()

    def update_model(self):
        raise NotImplementedError()

    def delete_model(self):
        raise NotImplementedError()
