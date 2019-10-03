import dataclasses

from django.db import models

# Create your models here.


@dataclasses.dataclass
class Application:
    id: str = dataclasses.field(default=None)
    name: str = dataclasses.field(default="")

    def to_dict(self):
        return {"id": self.id, "name": self.name}
