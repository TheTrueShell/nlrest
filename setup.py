from setuptools import setup, find_packages

setup(
    name='nlrest',
    version='0.1.3',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'nlrest=nlrest.cli:main',
        ],
    },
    install_requires=[
        'openai',
        'requests'
    ],
    python_requires='>=3.6',
    author='TheTrueShell',
    author_email='thetrueshell@tinymail.uk',
    description='A CLI tool to convert natural language to REST API queries.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/nlrest'
)
