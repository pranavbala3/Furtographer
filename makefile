PY := python
PY_FORMATER := autopep8
PY_FILES := $(shell find . -name '*.py' -not -path "./env/*")
NETS := nets

setup:
	$(PY) get_datasets.py
	$(PY) get_bottleneck_features.py

predict: $(PY_FILES)
	$(PY) model.py $(IMG)

train: $(PY_FILES)
	$(PY) $(NETS)/train.py

test_breeds: $(PY_FILES)
	$(PY) $(NETS)/test_breeds.py

test_detector: $(PY_FILES)
	$(PY) $(NETS)/test_detector.py

format: $(PY_FILES)
	$(PY_FORMATER) --in-place $(PY_FILES)

count_lines:
	find . -name '*.py' -not -path './env/**'| xargs wc -l
