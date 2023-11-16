.PHONY: dist clean

clean:
	rm -rf dist build
	rm -rf **/*.pyc
	rm -rf **/__pycache__
	rm -rf .coverage
	rm -rf .pytest_cache
	rm -rf coverage.xml


dist:
	pyinstaller src/openapi_splitter/main.py --onefile --name openapi_splitter --distpath dist

test:
	coverage run -m pytest . && coverage xml
