import re


def update_version(version, filename):
    with open(filename, 'rt') as f:
        text = f.read()
    text = re.sub(r'   version \d+\.[\d\.]+[a-z]?', '   version ' + version, text)
    with open(filename, 'wt') as f:
        f.write(text)


def get_version(filename):
    with open(filename, 'rt') as f:
        for line in f:
            if line.startswith('version'):
                return line.split()[-1].replace("'", '')


version = get_version('../setup.py')
print('VERSION:', version)
update_version(version, 'index.rst')
