from setuptools import setup, find_packages
setup(name='qwechat',
      version='0.2.0',
      packages=find_packages(),
      author='Shengjing Zhu',
      author_email='zsj950618@gmail.com',
      url='https://github.com/zhsj/qwechat',
      license='GPLv3',
      entry_points={
          'gui_scripts': ['qwechat=qwechat.app:runApp']
      })
