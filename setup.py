from setuptools import setup

setup(
    name='xpath_validator',
    packages=['xpath_validator'],
    version='1.5.1',
    description='validate boolean expressions with XPath syntax',
    long_description=open('README.rst').read(),
    author='Marcelo Fonseca Tambalo',
    author_email='marcelo.tambalo@nectosystems.com.br',
    url='https://github.com/znc-sistemas/xpath_validator/',
    keywords=['XPath', ],
    license='MIT',
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation',
        'Topic :: Software Development :: Libraries',
    ),
)
