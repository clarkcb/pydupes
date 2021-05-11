from setuptools import setup
from pydupes import VERSION

#long_description = open('README.md').read()

setup(name='pydupes',
      version=VERSION,
      description='An alternative to fdupes with more options/features',
      # long_description=long_description,
      url='https://github.com/clarkcb/pydupes.git',
      author='Cary Clark',
      author_email='clarkcb@gmail.com',
      include_package_data=True,
      install_requires=[],
      license='MIT',
      packages=['pydupes'],
      python_requires='>=3',
      scripts=[
          'bin/pydupes',
          # 'bin/pydupes.bat'
      ],
      tests_require=[
          'nose',
      ])
