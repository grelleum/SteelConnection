from __future__ import print_function

import sys

from .__version__ import __url__, __version__

if __name__ == '__main__':
    print('Python version:', '.'.join(str(x) for x in sys.version_info[:3]))
    print('SteelConnection version:', __version__)
    print('Project home:', __url__)
