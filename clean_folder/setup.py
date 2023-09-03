from setuptools import setup

setup(name='clean_folder',
      version='1.0',
      description='Clean Folder Tool',
      url='https://github.com/GennadiyPob/goit-home-work-07-extra/clean_folder',
      author='Gennadiy Pobereznichenko',
      author_email='gennadiy.pob@gmail.com',
      license='ABC',
      packages=['clean_folder'],
      entry_points={'console_scripts': ['sortfilesfolders=clean_folder.clean:clean_folder_']}
)