#!/usr/bin/env python3
"""Setup script for the RAG AI shared module."""

from setuptools import setup, find_packages

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="rag-ai-shared",
    version="0.1.0",
    author="RAG AI Team",
    author_email="team@rag-ai.com",
    description="Shared foundational module for RAG AI system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/rag-ai",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.991",
        ],
        "full": [
            "langdetect>=1.0.9",
            "redis>=4.0.0",
            "psycopg2-binary>=2.9.0",
            "motor>=3.0.0",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)