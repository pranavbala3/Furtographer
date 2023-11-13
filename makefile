PY := python
PYM := $(PY) -m
MODEL := model
EVAL := $(MODEL).eval
TESTER := pytest
SCRIPTS := $(MODEL).scripts
PY_FORMATER := autopep8
VENV_PATHS := -not -path "./env/*" -not -path "./venv/*"
PY_FILES := $(shell find . -name '*.py' $(VENV_PATHS))

setup_training:
	$(PYM) $(SCRIPTS).get_datasets
	$(PYM) $(SCRIPTS).get_bottleneck_features

eval_%:
	$(PYM) $(EVAL).$@

predict:
	$(PYM) $(MODEL).predict $(IMG)

format:
	$(PY_FORMATER) --in-place $(PY_FILES)

test:
	$(TESTER)

test_cov:
	$(TESTER) --cov

count_lines:
	find . -type f \( -name '*.py' -o -name '*.html' \) $(VENV_PATHS) | xargs wc -l
