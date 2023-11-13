PY := python
PYM := $(PY) -m
MODEL := model
TESTS := $(MODEL).tests
SCRIPTS := $(MODEL).scripts
PY_FORMATER := autopep8
VENV_PATHS := -not -path "./env/*" -not -path "./venv/*"
PY_FILES := $(shell find . -name '*.py' $(VENV_PATHS))

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
	find . -type f \( -name '*.py' -o -name '*.html' \) $(VENV_PATHS) | xargs wc -l
