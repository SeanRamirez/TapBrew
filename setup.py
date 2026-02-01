from setuptools import setup, find_packages

setup(
    name="tapflow",
    version="0.1.0",
    description="Real-time brewery analytics platform",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/tapflow",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.11",
    install_requires=[
        "fastapi>=0.109.0",
        "uvicorn[standard]>=0.27.0",
        "pandas>=2.1.4",
        "duckdb>=0.10.0",
        # ... other dependencies from requirements.txt
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.4",
            "black>=23.12.1",
            "flake8>=7.0.0",
        ]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
    ],
)
