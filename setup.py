from setuptools import find_packages, setup

setup(
    name="paddle",  ## This will be the name your package will be published with
    version="1.0",
    packages=find_packages(),  # This one is important to explain. See the notebook for a detailed explanation
    install_requires=[
        "selenium",
        "webdriver_manager",
        "pandas",
    ],  # For this project we are using two external libraries
    # Make sure to include all external libraries in this argument
)
