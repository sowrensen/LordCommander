try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from lordcommander import __version__

with open("readme.md", "r") as readme:
    long_description = readme.read()
    

setup(
    name='lordcommander',
    description='Run shell commands recursively throughout the predefined directories',
    packages=['lordcommander'],
    version=__version__,
    author='Sowren Sen',
    author_email='sowrensen@gmail.com',
    url='https://github.com/sowrensen/LordCommander',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords=['shell', 'commands', 'directory', 'projects', 'instances', 'linux', 'sever', 'devops'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: Unix",
        "Operating System :: POSIX :: Linux"
        "Programming Language :: Python :: 3"
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Version Control"
        "Topic :: System :: Shells",
        "Topic :: System :: Installation/Setup",
        "Topic :: Terminals",
    ],
    install_requires=[
        'Colr>=0.9.1',
        'fire>=0.2.1',
        'pytest>=5.4.3'
    ],
    python_requires=">=3.7"
)
