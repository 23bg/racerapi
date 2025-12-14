import subprocess


def dev_cmd():
    subprocess.run(["uvicorn", "main:app", "--reload"])
