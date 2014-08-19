from distutils.core import setup

setup(
    name='coinbase',
    version='0.2.1',
    packages=['coinbase', 'coinbase.models'],
    package_data={'coinbase': ['ca_certs.txt']},
    url='https://github.com/sibblegp/coinbase_python',
    license='MIT',
    author='George Sibble',
    author_email='george.sibble@gmail.com',
    description='Integration Library for the Coinbase API',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'httplib2>=0.8',
        'requests>=1.1.0',
        'oauth2client>=1.1',
    ],
    tests_require=[
        'sure>=1.2.5',
        'httpretty>=0.8.0',
    ],
)
