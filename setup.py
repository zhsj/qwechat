from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='qwechat',
      version='0.3.0',
      description='QWeChat',
      long_description=long_description,
      packages=find_packages(),
      author='Shengjing Zhu',
      author_email='zsj950618@gmail.com',
      url='https://github.com/zhsj/qwechat',
      license='GPLv3',
      entry_points={
          'gui_scripts': ['qwechat=qwechat.app:runApp']
      },
      install_requires=['PyQt5==5.7'],
      package_data={
          'qwechat': ['data/*']
      }
      )
