from setuptools import setup

setup(
	name='stonk_scraper',
	version='1.0.0',
	packages=['stonk_scraper'],
	include_package_Data=True,
	install_requires=[
		'Flask==1.1.1',
	],
)
