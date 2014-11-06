from setuptools import setup, find_packages

setup(
    name='samuraizer',
    version='0.1',
    description='Keyword and summary extraction.',
    packages=find_packages(exclude=['test']),
    package_data={'samuraizer': ['resources/stopwords.txt']},
    include_package_data=True,
    install_requires=[],
    license='BSD',
)
