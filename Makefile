.PHONY: test python # these are not real files

backend_path=./services/backend
frontend_path=./services/frontend
python=${backend_path}/env/bin/python

env-api: precommit ${backend_path}/environment.yaml
	conda env create -f ${backend_path}/environment.yaml -p ${backend_path}/env
	${python} -m pip install -e ${backend_path}

env-ui:
	cd ${frontend_path} && npm install

run-api:
	source ./scripts/variables.sh && ${python} -m uvicorn services.backend.src.ppl.api.main:app --host localhost --port 8000 --reload

run-ui:
	cd ${frontend_path} && npm run dev

precommit:
	bash ./scripts/install_precommit.sh

test-api:
	${python} -m pytest ${backend_path}/tests

test-docker:
	cd ${backend_path} && docker build -f api.Dockerfile -t test-ppl-api .
	cd ${backend_path} && docker run -p 8000:8000 test-ppl-api
