from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='web_gpt',
    version='1.0.0',
    author='ZeroN',
    author_email='dotdot20072607@gmail.com',
    description='WebGPT is a library based on the Openal API and Long Chain. It allows you to connect ChatGPT to the Internet without a seam to make requests and receive responses with up-to-date information.',
    long_description=readme(),
    url='https://github.com/OnaZeroN/WebGPT',
    packages=find_packages(),
    install_requires=['requests>=2.25.1'],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='example python',
    project_urls={
        'Documentation': 'link'
    },
    python_requires='>=3.9'
)
