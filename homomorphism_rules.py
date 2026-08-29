from dataclasses import dataclass

from expression import MapSymbol


@dataclass(frozen=True)
class HomomorphismStatement:
  map: MapSymbol




