from math import inf
from pathlib import Path

import pandas as pd

from repository import SphereRepository


BASE_DIR = Path(__file__).resolve().parent


def main():
  csv_path = (
    BASE_DIR
    / "data"
    / "sphere.csv"
  )

  df = pd.read_csv(csv_path)

  repo = SphereRepository(
    csv_path
  )

  keys = (
    df[["n", "k"]]
    .dropna(
      subset=[
        "n",
        "k",
      ]
    )
    .drop_duplicates()
    .sort_values(
      [
        "n",
        "k",
      ]
    )
  )

  print(
    "=== mixed groups in sphere.csv ==="
  )

  count = 0

  for _, row in keys.iterrows():
    n = int(row["n"])
    k = int(row["k"])

    group = repo.get_group(
      n,
      k,
    )

    orders = group.orders

    has_free = any(
      order == inf
      for order in orders
    )

    has_torsion = any(
      order not in {
        0,
        1,
        inf,
      }
      for order in orders
    )

    if not (
      has_free
      and has_torsion
    ):
      continue

    count += 1

    print()
    print(
      f"(n={n}, k={k})"
    )

    print(
      "orders =",
      orders,
    )

    print(
      "generators =",
      group.generators,
    )

  print()
  print(
    f"mixed group count = {count}"
  )


if __name__ == "__main__":
  main()

