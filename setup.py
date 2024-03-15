import setuptools

setuptools.setup(
    name='mimscripts',
    version='0.0.1',
    author='anonymous',
    packages=['mimscripts'],
    install_requires=[
        'typer', 'requests'
    ],
    entry_points={
        'console_scripts':[
            'mimrun = mimscripts.run:app',
            'mimserver = mimscripts.server:app'
        ]
    }
)