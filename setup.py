from setuptools import setup, find_packages

setup(
    name='arena',
    packages=find_packages(include=['arena', 'arena.*']),
    version='2020.1.10.0',
    description='Multi-user and database example.',
    url='https://github.com/rhythm-collective/arena',
    author='Zageron',
    author_email='hello@zageron.com',
    python_requires='>=3.8',
    install_requires=['pylint', 'pytest', 'pynng>=0.5.0', 'pymongo>=3.10.1'],
    entry_points={"console_scripts": ['arena = arena.__main__:main']}
)
