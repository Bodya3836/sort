from setuptools import find_packages, setup

setup(name='clean_folder',
    version='0.0.1',
    packages=find_packages(),
    author='Fly',
    description='Very usefull code',
    entry_points={
          'console_scripts' : ('clean-folder = clean_folder.clear:main',
                               'fill-files = clean_folder.files_generator:file_generator')
          
    }

    install_requires=[
        'numpy'
        'Pillow'
    ],

)