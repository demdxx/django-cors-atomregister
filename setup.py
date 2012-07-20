from setuptools import setup

setup(
    name='django-cors-atomregister',
    version='0.0.0',
    author='Dmitriy Ponomarev',
    author_email='demdxx@gmail.com',

    description='module add simple events',
    long_description=open('README.md').read(),
    url='http://github.com/demdxx/corsatomregister',
    license='MIT',

    packages=['corsatomregister'],
    install_requires=[
        'django>=1.2',
    ],

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',

        'Framework :: Django',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)