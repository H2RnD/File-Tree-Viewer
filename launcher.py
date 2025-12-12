import sys
import os
import subprocess
import platform

def check_pyqt6():
    try:
        import PyQt6
        return True
    except ImportError:
        return False

def install_pyqt6():
    consent = input("PyQt6 is not installed. Install it now? (y/n): ").strip().lower()
    if consent == 'y':
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyqt6"])
            print("PyQt6 installed successfully!")
            return True
        except subprocess.CalledProcessError:
            print("Installation failed. Please install PyQt6 manually: pip install pyqt6")
            return False
    else:
        print("Skipping installation. App requires PyQt6 to run.")
        return False

def run_app():
    app_path = os.path.join(os.path.dirname(__file__), "file_tree_viewer.py")
    subprocess.call([sys.executable, app_path])

if __name__ == "__main__":
    print(f"Platform: {platform.system()}")
    
    if not check_pyqt6():
        if not install_pyqt6():
            sys.exit(1)
    
    print("Launching the app...")
    run_app()
