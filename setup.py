from setuptools import setup, find_packages

# Read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="Project-USB-Security",
    version="0.1.0",
    authors=["Satvik Shrivastava","Moulik Sharma", "Nipun Dehariya", "Nipun Yadav"],
    author_email="satvik.shrivastava.exe@gmail.com",
    description="A USB physical security system for computers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/satvikx/Project-USB",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "pyusb",  # Example dependency
        "pillow",  # Example dependency for image handling
        # Add other dependencies here
    ],
    entry_points={
        "console_scripts": [
            "Project-USB-Security=main:main",
        ],
    },
)
