#!/usr/bin/env python

import logging
import subprocess


class OpenSSL():
	''' OpenSSL Wrapper Class. '''

	_filepath_cmd = f'which openssl'
	_version_cmd = f'openssl version'

	
	def __init__(self, country, state, city, cn, ou, email, cert_path, key_path):
		''' '''
		# DEV remove hardcoded vars.
		self.nodes = '-x509'
		self.newkey = 'rsa:2048'

		self.cert_path = cert_path
		self.key_path = key_path

		self.country = country
		self.state = state
		self.city = city
		self.cn = cn
		self.ou = ou
		self.email = email
		self.subject = f"/C={country}/ST={state}/L={city}/O={ou}/CN={ou}"
		self._cmd = f"""openssl req \
		 -nodes {self.nodes}\
		 -newkey {self.newkey}\
		 -keyout {self.key_path}\
		 -out {self.cert_path}\
		 -days 365\
		 -subj"""


	@classmethod
	def _filepath(cls):
		''' Return filepath:str '''

		cmdlst = cls.macchanger_filepath_cmd.split(' ')

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
	def _version(cls):
		''' Return version:str '''

		cmdlst = cls.macchanger_version_cmd.split(' ')

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

			output = proc.stdout.split('\n')
		
		return output[0]

	
	def run(self):
		''' Launch Openssl via subprocess wrapper '''

		cmdlst = self._cmd.split()
		cmdlst.append(self.subject)

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

			return cmdlst, proc.stdout, proc.stderr