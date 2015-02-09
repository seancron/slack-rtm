from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='slack-rtm',

    version='0.1.0',

    description="Python client for Slack's RTM API",
    url='https://github.com/seancron/slack-rtm',

    author='Sean Cronin',
    author_email='seancron@gmail.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='slack chat api',

    packages=['slack'],
    install_requires=['requests', 'websocket-client']
)
