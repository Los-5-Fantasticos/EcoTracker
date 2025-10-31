
import os, subprocess, sys, venv

ROOT = os.path.dirname(os.path.abspath(__file__))
VENV_DIR = os.path.join(ROOT, ".venv")

def ensure_venv():
    if not os.path.isdir(VENV_DIR):
        venv.create(VENV_DIR, with_pip=True)
    py = os.path.join(VENV_DIR, "Scripts", "python.exe")
    return py if os.path.exists(py) else sys.executable

def run(cmd):
    print(">>", " ".join(cmd))
    subprocess.check_call(cmd, cwd=ROOT)

def main():
    py = ensure_venv()
    run([py, "-m", "pip", "install", "--upgrade", "pip"])
    run([py, "-m", "pip", "install", "-r", "requirements.txt"])
    run([py, "manage.py", "makemigrations"])
    run([py, "manage.py", "migrate"])
    try:
        run([py, "manage.py", "collectstatic", "--noinput"])
    except Exception:
        pass
    run([py, "manage.py", "runserver", "0.0.0.0:8000"])

if __name__ == "__main__":
    main()
