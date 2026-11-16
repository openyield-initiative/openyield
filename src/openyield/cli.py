"""Command-line entry point."""
import argparse
from importlib.resources import files

from .model import load_scenario
from .output import export
from .simulation import run


def main():
    parser = argparse.ArgumentParser(description="Run the OpenYield scripted demonstration")
    parser.add_argument("--scenario", type=str)
    parser.add_argument("--output", default="outputs/default")
    parser.add_argument("--seed", type=int, default=0, help="recorded but unused: no randomness")
    args = parser.parse_args()
    try:
        scenario = load_scenario(args.scenario or files("openyield").joinpath("scenarios/default.json"))
        result = run(scenario, seed=args.seed)
        export(scenario, result, args.output)
    except (ValueError, OSError) as error:
        parser.error(str(error))
    print(f"{result['summary']['outcome']}: {result['summary']['reason']} ({args.output})")
    return 0 if result["summary"]["outcome"] == "success" else 1
