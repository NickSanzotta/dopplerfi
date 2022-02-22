#!/usr/bin/env python

import os
from time import sleep


def clear_screen():
   '''
   System based func to clear screen.
   '''
   
   # Linux
   if os.name == 'posix':
      _ = os.system('clear')
   # Windows
   else:
      _ = os.system('cls')