DOCTEST_CMD = python3 -m doctest
UNITTEST_CMD = python3 -m unittest
COMPILE_CMD = python3 -m py_compile
CHECKSTYLE_CMD = flake8 --max-line-length=99

# ==================================================================================================

checkstyle:
	@find * -name "*.py" | xargs $(CHECKSTYLE_CMD)

compile:
	@find * -name "*.py" | xargs $(COMPILE_CMD)

test: doctest unittest

doctest:
	@find * -name "*.py" | xargs $(DOCTEST_CMD)

unittest:
	@find * -name "test_*.py" | xargs $(UNITTEST_CMD)

clean:
	@find . -name *.pyc | xargs rm -rf
	@find . -name __pycache__ | xargs rm -rf

install:
	@pip3 install .