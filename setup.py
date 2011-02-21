from distutils.core import setup

setup(
 name='stockquotes',
 author = "Evan Davey",
 version='0.1',
 packages=['stockquotes'],
 package_dir={'stockquotes':'src/stockquotes'},
 scripts=['stockquotes'],
 package_data={'stockquotes':['*.xrc']}
)

