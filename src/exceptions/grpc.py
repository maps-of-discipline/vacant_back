from src.exceptions.general import EntityNotFoundException


class ServiceNotFoundException(EntityNotFoundException):
    entity = "Serice"

    def __init__(self) -> None:
        super().__init__(self.entity)
