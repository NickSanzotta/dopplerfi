#!/usr/bin/env python

import logging
import subprocess


class Hostapd():
	''' Hostapd-wpe class wrapper '''

	filepath_cmd = f'which hostapd-wpe'
	version_cmd = f'hostapd-wpe -v'

	
	def __init__(self, conf_arg):
		''' '''
		self.cmd = f'hostapd-wpe'
		self.conf_arg = conf_arg
	

	@classmethod
	def get_filepath(cls):
		''' Return filepath:str '''

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
		''' Return version:str '''

		cmdlst = cls.version_cmd.split(' ')

		try:
			proc = subprocess.run(cmdlst,
				shell=False,
				check=False,
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

			output = proc.stderr.split('\n')
		
		return output[0]


	def run(self):
		''' Launch Hostapd-wpe via subprocess wrapper '''
		
		cmdlst = self.cmd.split(' ')
		cmdlst.append(self.conf_arg)

		try:
			# Popen was used in place of subprocess.run() to allow live stream.
			proc = subprocess.Popen(cmdlst,
				shell=False,
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE
				)
		except Exception as e:
			# Set check=True for the exception to catch.
			logging.exception(e)
			raise e
		else:
			# Poll proc.stdout to show stdout live stream.
			while True:
				output = proc.stdout.readline()
				output_decoded = output.decode('UTF-8')
				if proc.poll() is not None:
					break
				if output:
					print(output_decoded.strip())
			rc = proc.poll()
		
		return None