```python
from setuptools import setup, find_packages
import os

def read_readme():
    """Reads the README.md file and returns its content."""
    with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r') as f:
        return f.read()

setup(
    name='aws_monitor',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    packages=find_packages(),
    install_requires=[
        'boto3',
        'matplotlib'
    ],
    entry_points={
        'console_scripts': [
            'aws_monitor=aws_monitor:main',
        ],
    },
    author='Ahmed Belhaj',
    author_email='ahmedbelhaj.it@gmail.com',
    long_description=read_readme(),
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
```