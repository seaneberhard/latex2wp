from setuptools import setup

setup(
    name='latex2wp',
    version='1.0.0',
    packages=['latex2wp', 'latex2wp.test'],
    url='https://github.com/seaneberhard/latex2wp',
    license='GNU GPL3+',
    author='seaneberhard',
    author_email='eberhard.math@gmail.com',
    description='convert LaTeX to WordPress-ready HTML',
    entry_points=dict(console_scripts=['latex2wp = latex2wp.main:main']),
)