coverage run -m unittest discover
testStatus="$?"

coverage report --omit=test_*.py,/home/circleci/.local/lib/python3.8/site-packages/parameterized/parameterized.py,/home/circleci/.local/lib/python3.8/site-packages/parameterized/__init__.py
coverage html

exit $testStatus
