NAME = 'abuse-utils'

test:
	PYTHONPATH=lib nosetests -d -v -v --with-coverage \
		   --cover-erase --cover-package=abuseutils

clean:
	@echo 'Cleaning distutils leftovers'
	rm -rf build
	rm -rf dist
	@echo 'Cleaning up byte compiled python files'
	find . -type f -regex ".*\.py[co]$$" -delete
	@echo 'Cleaning up RPM build files'
	rm -rf MANIFEST rpm-build
