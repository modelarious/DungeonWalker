coverage-3.8 run -m unittest discover
testStatus="$?"

coverage-3.8 report --omit={test_*.py, *circleci*}
coverage-3.8 html

exit $testStatus
