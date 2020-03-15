# Can't pip freeze on Windows + Pycharm

import os


venv_dir = 'C:/Users/TJ Hoeft/Python_Projects/Covid19/venv/Lib/site-packages'

for f_or_dir in os.listdir(venv_dir):

    print(f_or_dir)

    if os.path.isdir(f_or_dir):
        dir_name = os.path.basename(f_or_dir)
        print(dir_name)