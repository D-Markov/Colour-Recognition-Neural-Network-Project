from distutils.core import setup
from Cython.Build import cythonize

ext_modules = cythonize([
        r"src\Mathematics\Matrix.pyx"
    ],
    emit_linenums=True,
    annotate = True,
    # gdb_debug=True
    )

# ext_modules[0].extra_compile_args=['/Zi', '/Od']
# ext_modules[0].extra_link_args=['/DEBUG']

setup(
    name="Matrix",
    ext_modules = ext_modules,
    # gdb_debug=True
)
