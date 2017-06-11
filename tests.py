'''
Execute Unit, Integration and Functional tests
'''

import unittest
import sys
import argparse

def run_unit_tests():
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
    parser = argparse.ArgumentParser(description="Automatron Test Runner")
    parser.add_argument('-i', '--integration', help="Run integration tests", action="store_true", required=False)
    parser.add_argument('-f', '--functional', help="Run functional tests", action="store_true", required=False)
    args = parser.parse_args()

    unit = run_unit_tests()
    functional = True
    integration = True

    if args.integration:
        integration = run_integration_tests()

    if args.functional:
        functional = run_functional_tests()

    if unit and integration and functional:
        sys.exit(0)
    else:
        sys.exit(1)
