from dataclasses import dataclass, field


@dataclass
class StatusChangedData:
    user_name: str
    application_type: str
    status_verbose_name: str
    status: str
    status_class: str = field(init=False)

    def __post_init__(self):
        self.status_class = self.status.replace(" ", "-")
