from setuptools import setup


setup(
    name='ccopy',
    version='0.1.1',
    packages=['ccopy'],
    entry_points={
        'console_scripts': [
            'ccopy=ccopy.__main__:main',
        ]
    },
    setup_requires=[
        'setuptools>=18.0',
    ],
    python_requires='>=3.5',
    install_requires=[
        'mysqlclient',
        'sqlalchemy>=1.3,<1.4'
    ]
)
