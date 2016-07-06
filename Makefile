
clean:
	rm -rf .eggs build dist *.egg-info 

upload:
	python setup.py sdist upload -r pypi

test_upload:
	python setup.py sdist upload -r pypitest
