from setuptools import setup, find_packages
setup(name='qwechat',
      version='0.3.0',
      packages=find_packages(),
      author='Shengjing Zhu',
      author_email='zsj950618@gmail.com',
      url='https://github.com/zhsj/qwechat',
      license='GPLv3',
      entry_points={
          'gui_scripts': ['qwechat=qwechat.app:runApp']
      },
      install_requires=['PyQt5==5.7'],
      include_package_data=True,
      package_data={
          '': ['data/*']
      }
      )
