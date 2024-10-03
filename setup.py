import os
import sys
import argparse
import subprocess


def create_virtualenv():
    try:
        subprocess.check_call([sys.executable, "-m", "venv", "env"])
    except subprocess.CalledProcessError as e:
        print(f"Failed to create virtualenv: {e}")


def install_requirements():
    try:
        if os.name == "nt":
            subprocess.check_call([r"env\Scripts\pip", "install", "-r", "requirements.txt"])
        else:
            subprocess.check_call([r"env/bin/pip", "install", "-r", "requirements.txt"])

    except subprocess.CalledProcessError as e:
        print(f"Failed to install requirements: {e}")


def create_env_file(dbname):
    env_content = (
        f"\nDATABASE_URL=postgresql+asyncpg://postgres:<password>@localhost:5432/{dbname}\n"
        'SECRET_KEY="my_secret"\n'
        'USER_NAME="test"\n'
        'PASS_WORD="test"\n'
    )

    if os.path.exists(".env"):
        with open(".env", "a") as f:
            f.write(env_content)
    else:
        with open(".env", "w") as f:
            f.write(env_content)


def create_database(dbname):
    try:
        if os.name == "nt":
            subprocess.check_call(["psql", "-U", "postgres", "-c", f'CREATE DATABASE "{dbname}";'])

        else:
            subprocess.check_call(["sudo", "-u", "postgres", "psql", "-c", f'CREATE DATABASE "{dbname}";'])

    except subprocess.CalledProcessError as e:
        print(f"Failed to create database: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Setup the project")
    parser.add_argument(
        "--dbname", type=str, default="credit-app", help="Database name"
    )
    args = parser.parse_args()
    create_virtualenv()
    install_requirements()
    create_env_file(args.dbname)
    create_database(args.dbname)
    print("Setup complete.")
