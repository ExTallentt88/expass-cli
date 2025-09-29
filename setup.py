
from setuptools import setup, find_packages

setup(
    name="expass",
    version="0.1.0",
    description="Password Strength Tester CLI (expass)",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "rich>=12.0.0",
        "requests>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "expass = pwcheck.core:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
