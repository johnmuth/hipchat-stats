from setuptools import setup

setup(name='hipchat-stats',
      version='0.1',
      description='A webapp for stats about HipChat chats',
      url='http://github.com/johnmuth/hipchat-stats',
      author='John Muth',
      author_email='johnmuthyewkay@gmail.com',
      license='MIT',
      install_requires=[
          'flask',
          'hypchat',
          'datetime',
          'nltk',
          'numpy',
          'scipy'
      ],
      zip_safe=False)
