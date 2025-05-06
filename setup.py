from setuptools import setup, find_packages

setup(
    name="howard_financial",
    version="0.1",
    packages=find_packages(),
    install_requires=[
    "pandas>=1.5.0,<2.0.0",
    "sentence-transformers>=2.2.2",
    "faiss-cpu>=1.7.3",
    "scikit-learn>=1.0",
    "tqdm>=4.64",
    "ipywidgets>=8.0",
    ],
)
