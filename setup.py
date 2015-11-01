__author__ = 'Алексей Галкин'

from cx_Freeze import setup, Executable

setup(
    name = "calcal",
    version = "0.1",
    description = "вычисление календаря оптических наблюдений",
    executables = [Executable("calcal.py")]
)