import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="syncgit",
    version="0.0.2",
    author="RainingComputers",
    author_email="vishnu.vish.shankar@gmail.com",
    description="Sync python dicts, strings ad modules to git repository.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RainingComputers/syncgit",
    packages=setuptools.find_packages(exclude=["docs", "tests"]),
    python_requires=">=3.8",
    install_requires=["PyYAML"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development :: Version Control :: Git",
        "Topic :: Utilities"
    ],
    keywords="syncgit"
)
