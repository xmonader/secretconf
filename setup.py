import setuptools

setuptools.setup(
    name="secretconf",
    version="0.1.0",
    url="https://github.com/xmonader/secretconf",

    author="Ahmed Youssef",
    author_email="xmonader@gmail.com",

    description="secret configurations easily",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=[],
    entry_points={
        'console_scripts': ['hush=secretconf:hush']
    },
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
