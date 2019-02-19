SSH_PRIVATE_KEY ?= ''
.PHONY: docker-build docker-push

docker-build:
	docker build  --build-arg SSH_PRIVATE_KEY="$(SSH_PRIVATE_KEY)" -t investabit/images:project-$(BRANCH_NAME) .

docker-push: docker-build
	docker push investabit/images:project-$(BRANCH_NAME)
