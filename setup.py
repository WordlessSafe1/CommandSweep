from setuptools import find_packages, setup

setup(
    name="mswp",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "mswp=mswp.__main__:main",
        ]
    },
)
