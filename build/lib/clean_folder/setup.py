from setuptools import setup

setup(name='clean_folder',
      version='0.0.1',
      description='Clean Folder Tool',
      url='https://github.com/GennadiyPob/goit-home-work-07-extra/clean_folder',
      author='Gennadiy Pobereznichenko',
      author_email='gennadiy.pob@gmail.com',
      license='MIT',
      packages=['clean_folder'],
      entry_points={'console_scripts': ['clean-folder=clean_folder.clean:main']}
)