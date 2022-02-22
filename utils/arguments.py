#!/usr/bin/env python3

import sys
import argparse
from argparse import RawTextHelpFormatter

# Custom usage / help menu.
class HelpFormatter(argparse.HelpFormatter):
    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None:
            prefix = ''
        return super(HelpFormatter, self).add_usage(
            usage, actions, groups, prefix)


# Custom help menu.
custom_usage = """
  
DopplerFi
--------------------------------------------------\n
Usage Examples: 
  python3 [].py -i wlan0
  python3 [].py -c ./my_configs/config.ini
  
"""

# Define parser
parser = argparse.ArgumentParser(formatter_class=HelpFormatter, description='', usage=custom_usage, add_help=False)

# Group1 Options.
group1 = parser.add_argument_group('Arguments')
group1.add_argument('-i', dest='ifname', type=str, required=True, help='network interface')
group1.add_argument('-c', dest='configfile', type=str, required=False, help='filePath to config file.')


# Print 'help' if no options are defined.
if len(sys.argv) == 1 \
or sys.argv[1] == '-h' \
or sys.argv[1] == '--help':
  parser.print_help(sys.stderr)
  sys.exit(1)


if __name__ == "__main__":
    main()
