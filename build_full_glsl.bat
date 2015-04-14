@echo off

python.exe find_glsl.py
python.exe read_glsl_spec.py
python.exe compile_glsl.py --full

pause
