from setuptools import find_packages, setup

setup(
    name="LitigAItor-mini",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # List your project dependencies here
    ],
    entry_points={
        "console_scripts": [
            # Define any command-line scripts here
        ],
    },
    author="TommyBark",
    #    author_email='your.email@example.com',
    #    description='A brief description of your project',
    long_description=open("README.md").read(),
    #    long_description_content_type='text/markdown',
    #    url='https://github.com/yourusername/myproject',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
