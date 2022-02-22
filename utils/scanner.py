#!/usr/bin/env python

import logging
import subprocess


class Scanner:
	''' Wpa_cli class wrapper '''

	# Wpa_cli cls cmds.
	interfaces_cmd = f'wpa_cli interface'
	filepath_cmd = f'which wpa_cli'
	version_cmd = f'wpa_cli -v'


	def __init__(self, ifname):
		''' '''
		self.ifname = ifname
		self.cmd = f'wpa_cli'
		self.interface_arg = f'-i'
		self.scanresults_arg = f'scan_results'

	
	@classmethod
	def get_filepath(cls):
		''' Return Wpa_cli filepath:str'''
		
		cmdlst = cls.filepath_cmd.split(' ')

		try:
			proc = subprocess.run(cmdlst,
				shell=False,
				check=True,
				capture_output=True,
				text=True
				)
		except Exception as e:
			# Set check=True for the exception to catch.
			logging.exception(e)
			raise e
		else:
			# Debug print only.
			logging.info(f'STDOUT:\n{proc.stdout}')
			logging.debug(f'STDERR:\n{proc.stderr}')

			return proc.stdout.strip()
	
	
	@classmethod
	def get_version(cls):
		''' Return Wpa_cli version:str'''
		
		cmdlst = cls.version_cmd.split(' ')

		try:
			proc = subprocess.run(cmdlst,
				shell=False,
				check=True,
				capture_output=True,
				text=True
				)
		except Exception as e:
			# Set check=True for the exception to catch.
			logging.exception(e)
			raise e
		else:
			# Debug print only.
			logging.info(f'STDOUT:\n{proc.stdout}')
			logging.debug(f'STDERR:\n{proc.stderr}')

			output = proc.stdout.split('\n')[0]

			return output.strip()

	
	@classmethod
	def get_interfaces(cls):
		''' Return Wpa_cli Interfaces:str'''
		
		cmdlst = cls.interfaces_cmd.split(' ')

		try:
			proc = subprocess.run(cmdlst,
				shell=False,
				check=True,
				capture_output=True,
				text=True
				)
		except Exception as e:
			# Set check=True for the exception to catch.
			logging.exception(e)
			raise e
		else:
			# Debug print only.
			logging.info(f'STDOUT:\n{proc.stdout}')
			logging.debug(f'STDERR:\n{proc.stderr}')

			output = proc.stdout.split('\n')[2:-1]

			return output


	def run_scan(self):
		''' Launch Wpa_cli via subprocess wrapper '''

		# Wpa_cli scan_results.
		cmdlst = self.cmd.split(' ')
		cmdlst.append(self.interface_arg)
		cmdlst.append(self.ifname)
		cmdlst.append(self.scanresults_arg)

		try:
			proc = subprocess.run(cmdlst,
				shell=False,
				check=True,
				capture_output=True,
				text=True)
		except Exception as e:
			# Set check=True for the exception to catch.
			logging.exception(e)
			raise e
		else:
			# Debug print only.
			logging.info(f'STDOUT:\n{proc.stdout}')
			logging.debug(f'STDERR:\n{proc.stderr}')

			return proc.stdout