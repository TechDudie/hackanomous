import argparse
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
    args = parser.parse_args()

    uvicorn.run("main:app_factory", host="0.0.0.0", port=8080, workers=8, reload=args.dev, factory=True)