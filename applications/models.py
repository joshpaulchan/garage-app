import dataclasses

from django.db import models

# Create your models here.


@dataclasses.dataclass
class Application:
    id: str = dataclasses.field(default=None)
    name: str = dataclasses.field(default="")

    def to_dict(self):
        return {"id": self.id, "name": self.name}


@dataclasses.dataclass
class DeployTarget:
    cluster_id: str = dataclasses.field(default=None)
    application_id: str = dataclasses.field(default=None)
    version: str = dataclasses.field(default=None)

    def to_dict(self):
        return {
            "id": self.id,
            "application_id": self.application_id,
            "version": self.version,
        }


class ApplicationState(enum.Enum):
    STOPPED = "STOPPED"
    STARTED = "STARTED"
    RESTARTING = "RESTARTING"


@dataclasses.dataclass
class StateTarget:
    cluster_id: str = dataclasses.field(default=None)
    application_id: str = dataclasses.field(default=None)
    state: ApplicationState = dataclasses.field(default=None)

    def to_dict(self):
        return {
            "id": self.id,
            "application_id": self.application_id,
            "state": self.state,
        }
