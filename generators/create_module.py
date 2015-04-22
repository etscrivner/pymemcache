# -*- coding: utf-8 -*-
"""
    generators.create_module
    ~~~~~~~~~~~~~~~~~~~~~~~~
    Generator that will create a new module file with boilerplate.


"""
import sys
sys.path.append('')

import argparse
import doctest
import os


MODULE_BOILERPLATE = """
# -*- coding: utf-8 -*-
\"\"\"
    {module_name}
    {module_tildes}
    FIXME: Your description here

\"\"\"
import logging


logger = logging.getLogger(__name__)
""".strip()


TEST_BOILERPLATE = """
# -*- coding: utf-8 -*-
from tests import base


class Test{test_name}(base.BaseTestCase):

    def test_should_fail(self):
        self.fail('Should write some tests for this stuff!')
""".strip()


def convert_module_name_to_path(module_name):
    """Convert the given module name into a file path.

    >>> convert_module_name_to_path(None)
    ''
    >>> convert_module_name_to_path('')
    ''
    >>> convert_module_name_to_path('a')
    'a.py'
    >>> convert_module_name_to_path('a.b')
    'a/b.py'
    >>> convert_module_name_to_path('alpha.beta.gamma.delta')
    'alpha/beta/gamma/delta.py'

    :param module_name: A module name
    :type module_name: str or unicode
    :rtype: str or unicode
    """
    if not module_name:
        return ''

    parts = module_name.split('.')
    return os.path.join(*parts) + '.py'


def convert_module_name_to_test_path(module_name):
    """Convert the module name into a test path.

    >>> convert_module_name_to_test_path(None)
    ''
    >>> convert_module_name_to_test_path('')
    ''
    >>> convert_module_name_to_test_path('a')
    'test_a.py'
    >>> convert_module_name_to_test_path('a.b')
    'test_b.py'
    >>> convert_module_name_to_test_path('a.b.c')
    'b/test_c.py'

    :param module_name: A module name
    :type module_name: str or unicode
    :rtype: str or unicode
    """
    if not module_name:
        return ''

    parts = module_name.split('.')
    if len(parts) > 1:
        parts = parts[1:]
    parts[-1] = "test_{}".format(parts[-1])
    return convert_module_name_to_path('.'.join(parts))


def snake_to_uppercase(name):
    """Convert snake-case names to uppercased names.

    >>> snake_to_uppercase(None)
    ''
    >>> snake_to_uppercase('')
    ''
    >>> snake_to_uppercase('herp')
    'Herp'
    >>> snake_to_uppercase('herpderp')
    'Herpderp'
    >>> snake_to_uppercase('herp_derp')
    'HerpDerp'
    >>> snake_to_uppercase('herp_derp_perp')
    'HerpDerpPerp'

    :param name: A snakecase name
    :type name: str or unicode
    :rytpe: str or unicode
    """
    if not name:
        return ''

    return ''.join([each.capitalize() for each in name.split('_')])


def format_module_boilerplate(module_name):
    """Returns the formatted boilerplate for the given module.

    :param module_name: A module name
    :type module_name: str or unicode    
    :rtype: str or unicode
    """
    if not module_name:
        return ''

    return MODULE_BOILERPLATE.format(
        module_name=module_name, module_tildes='~'*len(module_name))


def format_test_boilerplate(module_name):
    """Returns the formatted test boilerplate for the given module.

    :param module_name: A module name
    :type module_name: str or unicode
    :rtype: str or unicode
    """
    if not module_name:
        return ''

    final_part = module_name.split('.')[-1]
    return TEST_BOILERPLATE.format(test_name=snake_to_uppercase(final_part))


def create_module_file(module_name, include_tests=False):
    """Create a module file for the given module name.

    :param module_name: The module name
    :type module_name: str or unicode
    :param include_tests: Should we generate tests too?
    :type include_tests: bool
    """
    module_path = convert_module_name_to_path(module_name)
    test_path = convert_module_name_to_test_path(module_name)

    full_module_path = os.path.join(os.getcwd(), module_path)
    full_test_path = os.path.join(os.getcwd(), 'tests', test_path)

    if os.path.exists(full_module_path):
        print 'ERROR: File {} already exists!'.format(full_module_path)
        exit(1)

    if os.path.exists(full_test_path):
        print 'ERROR: Test {} already exists!'.format(full_test_path)
        exit(1)
    
    sys.stdout.write('--> Creating file "{}"...'.format(full_module_path))
    print 'DONE!'
    with open(full_module_path, 'w') as modulefile:
        modulefile.write(format_module_boilerplate(module_name))
    print
    sys.stdout.write('--> Creating tests "{}"...'.format(full_test_path))
    with open(full_test_path, 'w') as testfile:
        testfile.write(format_test_boilerplate(module_name))
    print 'DONE!'
    print


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate boilerplate file and test given a module path.')
    parser.add_argument('-t', '--test', help='Run doctests for this module',
                        action='store_true')
    parser.add_argument(
        '--module', help='The python dot notation for module (Ex.app.utils)')
    parser.add_argument(
        '--dry-run', help='Print boilerplate without writing file.')
    args = parser.parse_args()

    if args.test:
        doctest.testmod()
    elif args.dry_run:
        print format_module_boilerplate(args.dry_run)
    elif args.module:
        create_module_file(args.module)
