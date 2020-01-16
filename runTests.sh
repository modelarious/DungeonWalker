coverage-3.8 run -m unittest discover
coverage-3.8 report --omit=test_*.py
coverage-3.8 html
exit 1
