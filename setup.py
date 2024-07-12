from setuptools import setup, find_packages
import os

with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r') as f:
    long_description = f.read()

setup(
    name='aws_monitor',
    version='0.5',
    packages=find_packages(),
    install_requires=[
        'boto3',
    ],
    entry_points={
        'console_scripts': [
            'aws_monitor=aws_monitor:main',
        ],
    },
    author='Ahmed Belhaj',
    author_email='ahmedbelhaj.it@gmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    description='A package for monitoring AWS resources',
    url='https://github.com/Theemiss/aws_monitor',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
