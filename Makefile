.PHONY: setup
setup-install:
	source .venv/bin/activate
	pip install requirements.txt

.PHONY: newman
newman:
	newman run automatedtesting/postman/CustomAPIs.postman_collection.json\
		-e automatedtesting/postman/CustomAPIs.postman_environment.json\
		--reporters cli,junit --reporter-junit-export results/newman-output.xml
