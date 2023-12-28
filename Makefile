#!/usr/bin/env make

build:
	docker build -t akatsuki-lazer:latest .

run:
	docker run --network=host --env-file=.env -it akatsuki-lazer:latest

run-bg:
	docker run --network=host --env-file=.env -d akatsuki-lazer:latest
