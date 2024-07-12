from setuptools import setup, find_packages

setup(
    name='aws_monitor_package',
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
    description='A package for monitoring AWS resources',
    url='https://github.com/Theemiss/aws_monitor',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
