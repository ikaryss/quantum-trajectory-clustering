# python setup.py build_ext --inplace
from setuptools import setup
from Cython.Build import cythonize
import numpy

setup(
    name="rdp app",
    ext_modules=cythonize("rdp_recursive.pyx", compiler_directives={'language_level' : "3"}),
    zip_safe=False,
    include_dirs=[numpy.get_include()],
)
