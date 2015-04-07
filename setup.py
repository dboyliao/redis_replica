from setuptools import setup, find_packages

setup(
    name='redis_replica',
    version='0.0.4',
    description='Redis Replica Set Client',
    author='Yin-Chen Liao',
    author_email='qmalliao@gmail.com',
    packages=find_packages(),
    install_requires=['redis']
)