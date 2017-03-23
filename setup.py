from setuptools import setup

setup(name='pyhypothesis',
      version='1.0.0',
      description='The funniest joke in the world',
      url='https://github.com/strongholder/pyhypothesis',
      author='Daniel Popov',
      license='MIT',
      packages=['pyhypothesis'],
      install_requires=[
          'requests>=2.5.0'
      ],
      zip_safe=False
)