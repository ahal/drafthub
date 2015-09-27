from setuptools import setup, find_packages

PACKAGE_VERSION = '0.1'

deps = [
    'flask',
]

setup(name='drafthub',
      version=PACKAGE_VERSION,
      description='A tool for real time drafting in fantasy sports.',
      long_description='See https://github.com/ahal/drafthub',
      author='Andrew Halberstadt',
      author_email='halbersa@gmail.com',
      url='https://github.com/ahal/drafthub',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=deps,
)
