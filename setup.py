from setuptools import setup, find_packages

setup(
    name="ai-review",
    version="0.1",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "ai-review=ai_review.cli:app"
        ]
    },
    install_requires=[
        "typer[all]",
        "rich"
    ]
)
