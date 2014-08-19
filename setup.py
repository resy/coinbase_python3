from distutils.core import setup

setup(
    name='coinbase',
    version='0.3.0',
    packages=['coinbase', 'coinbase.models'],
    url='https://github.com/resy/coinbase_python3',
    license='MIT',
    author='Michael Montero',
    author_email='mike@resy.com',
    description='Python3 Coinbase API',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
