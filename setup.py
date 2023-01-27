import setuptools

with open('readme.md') as fh:
    long_description = fh.read()

setuptools.setup(
    name='md.python.dict',
    version='1.0.0',
    description='Set of contracts & operations over dict type',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='License :: OSI Approved :: MIT License',
    package_dir={'': 'lib'},
    py_modules=['md.python.dict'],
    install_requires=['md.python==1.*'],
    dependency_links=[
        'https://source.md.land/python/md-python/'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
