from setuptools import setup, find_packages

setup(
    name="unam_resultados",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "shiny>=1.4.0",
        "pandas>=2.3.0",
        "numpy>=2.0.0",
        "matplotlib>=3.9.0",
        "plotly>=6.3.0",
        "seaborn>=0.13.0"
    ],
)