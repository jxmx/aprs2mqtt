import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aprs2mqtt", # Replace with your own username
    version="0.1.0",
    author="Jason McCormick",
    author_email="jason@mfamily.org",
    description="A collection of Ham Radio Utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jxmx/aprs-wulf",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)