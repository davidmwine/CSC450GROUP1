from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = [], excludes = [])

base = 'Console'

executables = [
    Executable('msu_game.py', base=base, icon="img\logo.ico")
]

setup(name='Mastering MSU',
      version = '1.0',
      description = 'The Missouri State University Game',
      options = dict(build_exe = buildOptions),
      executables = executables,
      data_files = [('C:\\Windows\\Fonts', ['freesansbold.ttf'])])
