from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()
VERSION = "0.0.5"

setup(
    name="ReportCheck",
    version=VERSION,
    description="CUP Daily Report Check",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="CUP Daily Report Check",
    author="RhythmLian",
    url="https://github.com/Rhythmicc/ReportCheck",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=["Qpro", "selenium"],
    entry_points={
        "console_scripts": [
            "cup-rc = ReportCheck.main:main",
        ]
    },
)
