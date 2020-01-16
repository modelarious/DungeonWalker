coverage-3.8 run -m unittest discover
testStatus="$?"

coverage-3.8 report --omit=test_*.py,/home/circleci/.local/lib/python3.8/site-packages/parameterized/parameterized.py,/home/circleci/.local/lib/python3.8/site-packages/parameterized/__init__.py
coverage-3.8 html

exit $testStatus
