import uvicorn
from ev_charging_env.server.app import app


def main():
    # This is the entry point OpenEnv expects.
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()