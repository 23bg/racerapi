from racerapi.core.bootstrap import create_app


app = create_app()


def run() -> None:
    import uvicorn

    uvicorn.run("racerapi.main:app", host="0.0.0.0", port=8000, reload=False)


if __name__ == "__main__":
    run()
