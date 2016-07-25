from setuptools import setup

setup(name='YHandler',
      version='1.0.0',
      classifer=[
      	'Development Status :: 3 - Alpha',
      	'Intended Audience :: Developers',
      	'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2.7',
            'Topic :: Games/Entertainment',
            'Topic :: Games/Entertainment :: Fantasy Sports'
      ],
      description='Yahoo Fantasy API Wrapper',
      url='https://github.com/BrutalSimplicity/YHandler',
      author='BrutalSimplicity',
      author_email='kory.taborn@gmail.com',
      license='MIT',
      packages=['YHandler'],
      install_requires=[
            'oauth-lib',
            'requests',
            'lxml'
      ],
      zip_safe=False)