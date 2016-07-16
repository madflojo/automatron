'''
Execute Unit, Integration and Functional tests
'''

import unittest
import sys

def run_unittests():
    ''' Execute Unit Tests '''
    tests = unittest.TestLoader().discover('tests/unit')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    return result.wasSuccessful()

def run_integration_tests():
    ''' Execute Integration Tests '''
    tests = unittest.TestLoader().discover('tests/integration')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    return result.wasSuccessful()

def run_functional_tests():
    ''' Execute Functional Tests '''
    tests = unittest.TestLoader().discover('tests/functional')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    return result.wasSuccessful()

if __name__ == '__main__':
    unit_results = run_unittests()
    integration_results = run_integration_tests()
    functional_results = run_functional_tests()
    if unit_results and integration_results and functional_results:
        sys.exit(0)
    else:
        sys.exit(1)
