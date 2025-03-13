import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="aws_cdk_iot",
    version="0.0.1",

    description="A CDK Python app for IoT Connection",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="Stanislav Karpikov",

    package_dir={"": "aws_cdk_iot"},
    packages=setuptools.find_packages(where="aws_cdk_iot"),

    install_requires=[
        "aws-cdk-lib==2.183.0",
        "constructs",
        "aws-cdk.aws-iot-alpha",
        "aws-cdk.aws-iot-actions-alpha"
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "License :: OSI Approved :: Apache Software License",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.12",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)