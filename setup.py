from setuptools import setup

with open('README.md', 'rt') as f:
    long_description = f.read()

setup(
    name='steelconnection',
    install_requires=['requests>=2.12.1'],
    version='0.9.9',
    author='Greg Mueller',
    author_email='steelconnection@grelleum.com',
    description='Simplify access to the Riverbed SteelConnect REST API.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/grelleum/SteelConnection',
    keywords=['SteelConnect', 'REST', 'API', 'Riverbed', 'Grelleum'],
    packages=['steelconnection'],
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
)
