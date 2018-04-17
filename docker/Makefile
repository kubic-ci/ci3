VERSION=`cat VERSION`


build:
		@echo "build kubic CI image ${VERSION}"
		@docker build -t kubic3/ci3:local .
		@docker tag kubic3/ci3:local kubic3/ci3:latest
		@docker tag kubic3/ci3:local kubic3/ci3:${VERSION}

run:
		@docker run -it kubic3/ci3:local /bin/bash

push: build
		@docker push kubic3/ci3:${VERSION}
		@docker push kubic3/ci3:latest