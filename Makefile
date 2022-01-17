
TEMP_REPO_STUB := khoury7stt/gslib-testimg
BUILD_ID := $(shell date +%s)

DOCKERFILES_DIR = tests/.docker

PACKER_ARGS += --var lib_version=$(LIB_VERSION)
PACKER_ARGS += --var build_id="$(BUILD_ID)"

$(TEMP_REPO_STUB)-%: $(DOCKERFILES_DIR)/%.Dockerfile
	@docker build --file $^ --build-arg $(subst $(TEMP_REPO_STUB)-,,$@) -t $@:$(BUILD_ID) .
	@docker tag $@:$(BUILD_ID) $@:latest

test/%: $(TEMP_REPO_STUB)-%
	@docker run -it $^

test/local: export PYTHONPATH:=$(PWD)/src:$(PYTHONPATH)
test/local: export LOCAL=True
test/local:
	@cd tests && python3 run_tests

test_all: test/local test/centos test/

images: packer/gradescope-auto.pkr.hcl
	@packer init $^
	@packer build $(PACKER_ARGS) $^

clean:
	@docker rmi -f $(shell docker images '$(TEMP_REPO_STUB)-*' -q | uniq)

.PHONY: clean images test test/%
