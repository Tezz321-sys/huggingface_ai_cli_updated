from setuptools import setup, find_packages

setup(
    name="ai-cli",
    version="2.0.0",
    packages=find_packages(),
    install_requires=[
        "google-generativeai",
        "pillow"
    ],
    entry_points={
        "console_scripts": [
            "ai=ai_cli.main:main",
        ]
    },
)
