from setuptools import Extension, setup

setup(
    ext_modules=[
        Extension(
            name="vec64",
            sources=[
                "vec64.c",
            ]
        ),
    ]
)
