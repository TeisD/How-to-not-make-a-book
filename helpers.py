from termcolor import colored, cprint;

def print_ok(s = ''):
    cprint('[OK] ' + s, 'green', attrs=['bold']);

def print_fail(s = ''):
    cprint('[FAIL] ' + s, 'red', attrs=['bold']);
