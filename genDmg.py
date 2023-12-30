from setuptools import setup

def run_exec():
  APP = ['spray.py']
  OPTIONS = {
      'argv_emulation': True,
      'packages': ['fcntl'],
  }

  setup(
      app=APP,
      options={'py2app': OPTIONS},
      setup_requires=['py2app'],
  )

if __name__ == "__main__":
  run_exec()
