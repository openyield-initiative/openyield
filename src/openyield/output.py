"""Trace serialization and offline rendering; no simulation logic."""
import json
from importlib.resources import files
from pathlib import Path


def export(scenario, result, destination):
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    trace = json.dumps(result, indent=2, allow_nan=False)
    (destination / "trace.json").write_text(trace + "\n", encoding="utf-8")
    (destination / "summary.json").write_text(
        json.dumps(result["summary"], indent=2, allow_nan=False) + "\n", encoding="utf-8")
    # Escape markup even when user-supplied IDs contain closing script tags.
    payload = json.dumps(result, allow_nan=False).replace("<", "\\u003c")
    assets = files("openyield").joinpath("replay")
    html = assets.joinpath("template.html").read_text(encoding="utf-8")
    html = html.replace("__STYLE__", assets.joinpath("style.css").read_text(encoding="utf-8"))
    html = html.replace("__SCRIPT__", assets.joinpath("player.js").read_text(encoding="utf-8"))
    html = html.replace("__TRACE__", payload)
    (destination / "replay.html").write_text(html, encoding="utf-8")
