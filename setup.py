from setuptools import setup, find_packages

PACKAGE_VERSION = '0.1'

deps = [
    'flask',
    'Jinja2',
]

setup(name='fantasy-report',
      version=PACKAGE_VERSION,
      description='A tool for creating an html report from csv formatted hockey rankings.',
      long_description='See https://github.com/ahal/fantasy-report',
      author='Andrew Halberstadt',
      author_email='halbersa@gmail.com',
      url='https://github.com/ahal/fantasy-report',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=deps,
      entry_points="""
        [console_scripts]
        generate-fantasy-report = fantasy_report.generate:cli
      """)
