from distutils.core import setup
from Cython.Build import cythonize

ext_modules = cythonize(
    [r"src\Mathematics\Matrix.pyx"],
    emit_linenums=True,
    annotate = True,
    compiler_directives={
        # 'linetrace': True,
        'initializedcheck' : True,
        'boundscheck': True
    })
    
# ext_modules[0].define_macros=[('CYTHON_TRACE', '1')]

setup(
    name="Matrix",
    ext_modules = ext_modules,
)
