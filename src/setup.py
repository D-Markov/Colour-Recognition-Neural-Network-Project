from distutils.core import setup
from Cython.Build import cythonize
from distutils.extension import Extension

matrix_ext = Extension(
    "src.Mathematics.Matrix",
    language="c++",
    sources=["src/Mathematics/Matrix.pyx"],
    # extra_compile_args=["-Ox", "-Zi"], # disabling all optimizations, generate full debug information
    # extra_link_args=["-debug:full"], # produce the PDB file
    # define_macros=[('CYTHON_TRACE', '1')]
    )


ext_modules = cythonize(
    matrix_ext,
    language_level=3,
    annotate = True,
    compiler_directives={
        'embedsignature': True,
        # 'linetrace': True,
        'annotation_typing': True,
        'emit_code_comments': True,
        'initializedcheck' : False,
        'boundscheck': False
    },
    emit_linenums=True, # adds “#line” directives to the  C/C++ code which instruct MSVC to generate a source map back to the original Cython file.
    # gdb_debug=True
    )

setup(
    name="Matrix",
    ext_modules = ext_modules,
)
