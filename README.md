# 42-dslr

Poetry usage:
1) create toml file: poetry init
    --> set [tool.poetry] package-mode = false for your project not to be considered as a package 
2) run poetry config virtualenvs.in-project true , to create your venv in your current project
3) run poetry install 
4) run with poetry: poetry run main.py

adding dependencies: poetry add <dependency>
removing dependences: poetry remove <dependency>
making poetry use a supported version of python: poetry env use pyhton3.11