
test: export PYTHONPATH:=$(PWD)/src:$(PYTHONPATH)
test:
	cd tests && python3 run_test

.PHONY: test