\
from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='codemate',
    version='0.1.0',
    author='Teresa de Candia',
    author_email='trdeca23@gmail.com',
    description='Utility functions for interacting with Gemini',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/trdeca23/codemate',
    packages=find_packages(),
    install_requires=[
        'google-generativeai',
        'python-dotenv',
        'rich'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
