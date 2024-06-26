SOLIB = $(shell scripts/pyext-solib-filename vec64)

all: $(SOLIB)

$(SOLIB): vec64.c
	pip install -e .[dev]

check: $(SOLIB)
	pytest

test: check

clean:
	rm -f $(SOLIB) *.egg-info .pytest_cache

.PHONY: all check test clean
