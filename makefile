PY := python
PYM := $(PY) -m
MODEL := model
TESTS := $(MODEL).tests
SCRIPTS := $(MODEL).scripts
PY_FORMATER := autopep8
PY_FILES := $(shell find . -name '*.py' -not -path "./env/*")

setup_training:
	$(PYM) $(SCRIPTS).get_datasets
	$(PYM) $(SCRIPTS).get_bottleneck_features

test_%:
	$(PYM) $(TESTS).$@

predict:
	$(PYM) $(MODEL).predict $(IMG)

format:
	$(PY_FORMATER) --in-place $(PY_FILES)

count_lines:
	find . -name '*.py' -not -path './env/**'| xargs wc -l
