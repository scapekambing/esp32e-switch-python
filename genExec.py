import subprocess

def run_exec():
  try:
    subprocess.run(['pyinstaller', '--onefile', 'spray.py'], check=True)
    print("Executable created successfully.")
  except subprocess.CalledProcessError as e:
    print(f"Error creating executable: {e}")

if __name__ == "__main__":
  run_exec()
