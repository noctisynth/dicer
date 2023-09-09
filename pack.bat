@echo off
python setup.py sdist bdist_wheel
twine upload dist/*
rm dist/*
pause