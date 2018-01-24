import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

requires = (
    'Arche',
    'pyramid',
    'py-trello',
    )

setup(name='betahaus.roadrunner',
      version='0.1.dev1',
      description='Betahaus time and project tracker',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Development Status :: 3 - Alpha",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Betahaus',
      author_email='',
      url='http://www.betahaus.net',
      keywords='web pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="betahaus.roadrunner",
      entry_points="""\
      [fanstatic.libraries]
      roadrunner = betahaus.roadrunner.fanstatic_lib:library
      """,
      )
