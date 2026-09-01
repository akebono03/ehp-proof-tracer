
from dataclasses import dataclass

from expression import (
  MapSymbol,
)


@dataclass(frozen=True)
class InjectiveMapStatement:
  map: MapSymbol



