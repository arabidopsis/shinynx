from pathlib import Path

with open(Path(__file__).parent / "script.js", encoding="utf-8") as fp:
    JS = fp.read()
