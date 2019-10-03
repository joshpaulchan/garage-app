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
        return {"id": self.id, "name": self.name}
