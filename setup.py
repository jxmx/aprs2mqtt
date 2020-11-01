import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aprs2mqtt",
    version="0.9.1",
    author="Jason McCormick",
    author_email="jason@mfamily.org",
    description="Collection of utilities to interface APRS and MQTT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jxmx/aprs2mqtt",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    scripts=[
        "aprs2mqttmsg.py",
        "mqtt2aprsmsg.py"
    ]
)