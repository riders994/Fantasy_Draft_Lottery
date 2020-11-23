from setuptools import setup, find_packages

setup(
    name="fantasydraftlottery",
    version='1.0',
    packages=find_packages(),
    author='Rohan Vahalia',
    author_email='r.vahalia@gmail.com',
    license='COPYING.txt',
    description='A package that can be used to run a fantasy draft lottery',
    long_description=open('README.md').read(),
    install_requires=[
        'pytest',
        'pandas==1.1.4',
        'numpy==1.19.4',
    ]
)
