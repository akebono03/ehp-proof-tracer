from pathlib import Path


TARGET = Path("toda_proof_dependency.py")


def main():
  data = TARGET.read_bytes()

  normalized = (
    data
    .replace(b"\r\n", b"\n")
    .replace(b"\r", b"\n")
  )

  TARGET.write_bytes(
    normalized
  )

  print(
    "Normalized LF line endings:",
    TARGET,
  )


if __name__ == "__main__":
  main()
