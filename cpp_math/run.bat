@echo off
cmake --build build
if errorlevel 1 exit /b 1
build\Debug\vector_demo.exe