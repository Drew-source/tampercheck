#!/usr/bin/env python3
"""
Setup script for TamperCheck
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tampercheck",
    version="0.1.0",
    author="TamperCheck Contributors",
    description="LLM output tamper detection using token probability analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/tampercheck",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "openai>=1.0.0",
        "python-dotenv>=1.0.0",
        "colorama>=0.4.6",
    ],
    entry_points={
        "console_scripts": [
            "tampercheck=tampercheck:main",
        ],
    },
)

