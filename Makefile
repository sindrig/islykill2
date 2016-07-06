
clean:
	rm -rf .eggs build dist *.egg-info 

build: clean
	python setup.py build

upload:
	python setup.py sdist upload -r pypi

test_upload:
	python setup.py sdist upload -r pypitest
