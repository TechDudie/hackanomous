import argparse
import os
import pathlib
import uvicorn

def app_factory():
    from app.server import app
    return app

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hackanomous Server")
    parser.add_argument(
        "--dev",
        action="store_true",
        help="run in development mode with hot reloading",
    )
    parser.add_argument(
        "--config",
        "-c",
        type=pathlib.Path,
        default=pathlib.Path("./config.toml"),
        help="path to config file",
    )
    args = parser.parse_args()

    os.environ["HACKANOMOUS_DEVELOPMENT"] = "1" if args.dev else "0"
    os.environ["HACKANOMOUS_CONFIG_FILE"] = str(args.config.resolve())

    uvicorn.run("main:app_factory", host="0.0.0.0", port=8080, workers=8, reload=args.dev, factory=True)