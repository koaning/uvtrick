from setuptools import setup, find_packages

setup(
    name='uvtrick',
    version='0.2.0',
    packages=find_packages(),
    install_requires=[
        'uv'
    ],
    python_requires='>=3.8',
)
