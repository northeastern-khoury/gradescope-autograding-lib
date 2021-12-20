
NO_CACHE := 0
LIB_REFRESH := 0
LIB_VERSION := 0.7.4
BUILD_ARGS = --build-arg LIB_VERSION="v$(LIB_VERSION)"
ifneq ($(NO_CACHE), 0)
	BUILD_ARGS := --no-cache $(BUILD_ARGS)
endif
ifneq ($(LIB_REFRESH), 0)
	BUILD_ARGS := $(BUILD_ARGS) --build-arg LIB_REFRESH="$(shell date +%s)"
endif

build:
	docker build $(BUILD_ARGS) -t khoury7stt/gradescope-auto:$(LIB_VERSION)-ubuntu --secret id=deploy_token,src=.deploy_token .
	docker push khoury7stt/gradescope-auto:$(LIB_VERSION)-ubuntu

.PHONY: build
