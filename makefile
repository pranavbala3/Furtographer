PY := python
PY_FORMATER := autopep8
PY_FILES := $(shell find . -name '*.py' -not -path "./env/*")

setup:
	$(PY) get_datasets.py
	$(PY) get_bottleneck_features.py

predict: $(PY_FILES)
	$(PY) model.py $(IMG)

train: $(PY_FILES)
	$(PY) nets/train.py

format: $(PY_FILES)
	$(PY_FORMATER) --in-place $(PY_FILES)
