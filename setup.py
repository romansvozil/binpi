from setuptools import setup, find_packages

setup(
      name='binpi',
      version='0.1.17',
      description='Simple library for de/serializing binary data',
      readme = "README.md",
      long_description=open("README.md", "r").read(),
      long_description_content_type="text/markdown",
      url='https://github.com/romansvozil/binpi',
      author='Roman Svozil',
      license='MIT',
      packages=find_packages(),
)