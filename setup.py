from setuptools import setup,find_packages

setup(
    name='python_tracker',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts':
            ['py_tracker = console_interface.main:main']
    },
    url='',
    license='',
    author='mikita',
    author_email='',
    description='task tracker library and console interface for it'
)
