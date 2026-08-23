from math import inf

import pandas as pd

from models import AbelianGroup, GroupComponent, MapImage

from algebra import GroupMap


class SphereRepository:
  def __init__(self, csv_path):
    self.df = pd.read_csv(csv_path)

  def _resolve_n(self, n, k):
    if k <= -1:
      return 0

    if k + 2 >= n:
      return n

    return k + 2

  def _rows(self, n, k):
    rows = self.df[
      (self.df["n"] == n)
      & (self.df["k"] == k)
    ]

    if not rows.empty:
      return rows.sort_values("id")

    data_n = self._resolve_n(n, k)

    rows = self.df[
      (self.df["n"] == data_n)
      & (self.df["k"] == k)
    ]

    return rows.sort_values("id")

  def _parse_int_list(self, value):
    if pd.isna(value):
      return []

    return [int(x) for x in str(value).split()]

  def _parse_order(self, value):
    if pd.isna(value):
      return 0

    if str(value).lower() in {"inf", "infinity"}:
      return inf

    value = float(value)

    if value == inf:
      return inf

    return int(value)

  def _parse_text(self, value):
    if pd.isna(value):
      return ""

    return str(value)

  def get_group(self, n, k):
    rows = self._rows(n, k)

    components = []

    for _, row in rows.iterrows():
      component = GroupComponent(
        id=int(row["id"]),
        order=self._parse_order(row["orders"]),
        generator=self._parse_text(row["generator"]),
        element=self._parse_int_list(row["Element"]),
        gen_coe=self._parse_int_list(row["gen_coe"]),
      )

      components.append(component)

    return AbelianGroup(
      n=n,
      k=k,
      components=components,
    )

  def get_map_images(self, n, k, map_name):
    if map_name not in {"P", "E", "H"}:
      raise ValueError(
        "map_name must be P, E, or H"
      )

    rows = self._rows(n, k)

    coe_column = f"{map_name}_coe"

    images = []

    for _, row in rows.iterrows():
      images.append(
        MapImage(
          map_name=map_name,
          source_id=int(row["id"]),
          coefficients=self._parse_int_list(
            row[coe_column]
          ),
          reference=(
            None
            if pd.isna(row[map_name])
            else str(row[map_name])
          ),
        )
      )

    return images

  def get_group_map(self, map_name, source_n, source_k):
    if map_name not in {"P", "E", "H"}:
      raise ValueError(
        "map_name must be P, E, or H"
      )

    source = self.get_group(
      source_n,
      source_k
    )

    if map_name == "E":
      target_n = source_n + 1
      target_k = source_k

    elif map_name == "H":
      target_n = 2 * source_n - 1
      target_k = (
        source_k
        - source_n
        + 1
      )

    elif map_name == "P":
      if source_n % 2 == 0:
        raise ValueError(
          "EHP の P の source sphere は"
          "奇数次元である必要があります"
        )

      target_n = (
        source_n - 1
      ) // 2

      target_k = (
        source_k
        + source_n
        - target_n
        - 2
      )

    target = self.get_group(
      target_n,
      target_k
    )

    images = self.get_map_images(
      source_n,
      source_k,
      map_name
    )

    matrix = [
      [0] * source.direct_sum
      for _ in range(
        target.direct_sum
      )
    ]

    for image in images:
      source_id = image.source_id

      for target_id in range(
        target.direct_sum
      ):
        if target_id < len(
          image.coefficients
        ):
          matrix[target_id][
            source_id
          ] = (
            image.coefficients[
              target_id
            ]
          )

    return GroupMap(
      name=map_name,
      source=source,
      target=target,
      matrix=matrix,
    )


  