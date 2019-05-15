from setuptools import setup

setup(
    name='xpath_validator',
    packages=['xpath_validator'],
    version='1.0.0',
    description='validate boolean expressions with XPath syntax',
    long_description=open('README.rst').read(),
    author='Marcelo Fonseca Tambalo',
    author_email='marcelo.tambalo@nectosystems.com.br',
    keywords=['XPath', ],
    license='MIT',
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation',
        'Topic :: Software Development :: Libraries',
    ),
)
