test: 
	pytest tests/

gendocs: 
	pdoc secretconf --html --html-dir docs/api --overwrite