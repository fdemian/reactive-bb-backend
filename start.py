import argparse
import subprocess


def start_app():
    subprocess.run("poetry run python3 main.py", shell=True)


def start_app_background():
    subprocess.Popen(["poetry", "run", "python3.11", "main.py"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Application panel")
    parser.add_argument(
        "--background",
        metavar="b",
        type=bool,
        nargs=1,
        default=False,
        help="Run in background",
    )
    args = parser.parse_args()
    run_in_background = args.background

    if run_in_background:
        start_app_background()
    else:
        start_app()