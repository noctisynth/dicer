@echo off
del dist /F /Q
C://Users/fu050/Desktop/Projects/DicerGirl/.venv/Scripts/python setup.py sdist bdist_wheel
twine upload dist/*
del dist /F /Q
pause