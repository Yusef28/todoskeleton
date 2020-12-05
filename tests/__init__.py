

#either:
#path> py -m unittest 
#or
#path> green tests
#"tests" is the directory with all tests and an empty __init__.py


#from the directory with tests directory inside it.
#and we need this __init__.py file which can be empty!
#https://github.com/CleanCut/green
#__init__.py siglaliziert zu python das es ok ist, von diese
#verzeichnis zu importieren
#gutfur spaater: https://www.patricksoftwareblog.com/unit-testing-a-flask-application/


#coverage reports https://coverage.readthedocs.io/en/coverage-5.3/
#pip -m install coverage
#coverage run -m unitttest discover
#coverage html
#and then find the htmlcov folder and open index.htmls

#or

#green -vvv --run-coverage
#but this gives that error where it tries to execute one testcase after another

#good tutorial by a senior AI Engineer
#https://medium.com/better-programming/introduction-to-unittest-a-unit-testing-framework-in-python-fa0d96fc8262

#best practices:
#https://docs.python-guide.org/writing/tests/
#https://github.com/CleanCut/green

#Later for automatic constant Testing:
#https://pycrunch.com/