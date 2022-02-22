#!/usr/bin/env python

from utils import arguments
from utils import certificate
from utils import channels
from utils import clearscreen
from utils import hostapd
from utils import interface
from utils import richard as r
from utils import scanner
from simple_term_menu import TerminalMenu
from configparser import ConfigParser, ExtendedInterpolation
import os
import sys
# # DEV
from rich.prompt import Prompt
# # DEV
from rich import box


# Argparse - Init and parse.
args = arguments.parser.parse_args()

# ConfigParser - init and defined instance options.
config = ConfigParser(
	allow_no_value=True,
 	delimiters='=',
	interpolation=ExtendedInterpolation())
# DEv - fix
config.optionxform = str

# ConfigParser - main confg.ini file.
config_ini = './my_configs/config.ini'

# Interface - defaults.
interface_cc = 'GY'
interface_txpower = '30'

# Hostapd - defaults.
hostapd_cc = 'GY'
hostapd_template = f'./templates/hostapd-wpe.conf'
eapuser_template = f'./templates/eapuser_default'
hostapd_custom = f'./my_hostapds/'
hostapd_logfile = f'./my_logs/'
hostapd_servercert = f'./my_certs/'
hostapd_privatekey = f'./my_certs/'

# Openssl - defaults.
openssl_country = f"US"
openssl_state =  f"CA"
openssl_city = f"San Diego"
openssl_company = f"Contoso"
openssl_ou = f"Contoso Ltd."
openssl_email = f"info@contoso.com"

# Application versions.
hostapd.Hostapd.get_version()
interface.Interface.macchanger_version()
scanner.Scanner.get_version()

# Application filepaths.
hostapd.Hostapd.get_filepath()
interface.Interface.macchanger_filepath()
scanner.Scanner.get_filepath()

# Banner
r.console.print(r.Panel('', title="Scanner", title_align='left', box=box.SQUARE, height=10))
# Heading1
# print('\n')
# r.console.print(f'{scanner.Scanner.get_version()}, {scanner.Scanner.get_filepath()}', style='appheading')
# r.console.rule(style='rulecolor')


def set_config(menu_item):
	'''
	'''
	
	#  Permit whitespaces in essid value. I.e (split 4)
	v = menu_item.split(' ', 4)
	# Convert 'menu_item:str' to 'ap_dic:dict'.
	k = ['bssid', 'frequency', 'power', 'flags', 'essid']
	ap_dic = dict(zip(k, v))

	# Return channel/band from a given fequency. I.e (freq 2462 to chan 11/band G)
	band = ''
	frequency = ap_dic['frequency']
	for k, v in channels.bg_channels.items():
		if v == frequency:
			channel = k
			band = 'g'
	for k, v in channels.a_channels.items():
		if v == frequency:
			channel = k
			band = 'a'

	# ConfigParser - default dict.
	config['Main'] = {
		'hostapd_filepath':hostapd_custom + '${Hostapd:essid}.conf'
		}
	
	# ConfigParser - interface dict.
	config['Interface'] = {	
		'interface':f'{args.ifname}',
		'bssid':ap_dic['bssid'],
		'tx_power':f'{interface_txpower}',
		'regulatory_domain':f'{interface_cc}'
		}
	
	# ConfigParser - hostapd dict.
	config['Hostapd'] = {
		'interface':f'{args.ifname}',
		'channel':f'{channel}',
		'band':f'{band.lower()}',
		'essid':ap_dic['essid'],
		'country_code':f'{hostapd_cc}',
		'logfile':f'{hostapd_logfile}' + '${Hostapd:essid}.log',
		'cert_pem_filepath':f'{hostapd_servercert}' + '${essid}.pem',
		'cert_key_filepath':f'{hostapd_privatekey}' + '${essid}.key',
		'eap_user_file':f'{eapuser_template}'
		}
	
	# ConfigParser - openssl dict.
	config['OpenSSL'] = {
		'country':f'{openssl_country}',
		'state':f'{openssl_state}',
		'city':f'{openssl_city}',
		'company':f'{openssl_company}',
		'ou':f'{openssl_ou}',
		'email':f'{openssl_email}',
		'cert_pem_filepath':f'{hostapd_servercert}' + '${Hostapd:essid}.pem',
		'cert_key_filepath':f'{hostapd_privatekey}' + '${Hostapd:essid}.key'
		}

	return config


def preview_config(menu_item):
	'''
	'''

	# Lst container.
	preview_lst = []
	# Return config from nested func 'set_config'.
	config = set_config(menu_item)
	# Declare config dict.
	cp_main = {k: v for k, v in config.items()}

	# Append config's entries/subentries to preview_lst.
	for k in cp_main.keys():
		# Exclude ConfigParsers 'DEFAULT' dict.
		if not k == 'DEFAULT':
			preview_lst.append(f'\n[{k}]\n')
			cp_subsection = {k: v for k, v in cp_main[k].items()}
			[preview_lst.append(f'{k} = {v}\n') for k, v in cp_subsection.items()]
		
	preview_str = ' '.join(preview_lst)

	return preview_str


def write_config(config, filename):
	''' 
	Write config.ini file.
	arg(s) config:ConfigParser-Object,
	filename:str
	Return config.ini filename.
	'''

	with open(filename, 'w') as f1:
		config.write(f1)

	return f1.name


def edit_config():
	pass


def write_hostapd(config, input_file, output_file):
	'''
	'''
	
	# ConfigParser - read Hostpad dict
	hostapd_dic = {k: v for k, v in config['Hostapd'].items()}

	with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
		lines = infile.readlines()
		lines[3] = f"interface={hostapd_dic['interface']}\n"
		lines[6] = f"eap_user_file={hostapd_dic['eap_user_file']}\n"
		lines[8] = f"server_cert={hostapd_dic['cert_pem_filepath']}\n"
		lines[9] = f"private_key={hostapd_dic['cert_key_filepath']}\n"
		lines[14] = f"ssid={hostapd_dic['essid']}\n"
		lines[15] = f"channel={hostapd_dic['channel']}\n"
		lines[19] = f"wpe_logfile={hostapd_dic['logfile']}\n"
		lines[146] = f"country_code={hostapd_dic['country_code']}\n"
		lines[183] = f"hw_mode={hostapd_dic['band']}\n"
		outfile.writelines(lines)

	return outfile.name


def list_files(directory):
	''' 
	'''
	files = []
	
	for i in os.listdir(directory):
		if os.path.isfile(os.path.join(directory, i)):
			files.append(i)
	
	return files


def status(mystr):
	''' SimpleTermMenu Callable for Status.'''
	pass
	
	return mystr


def status2(str2):
	''' '''
	pass
	
	return f'Loaded: {str2}'


# DEV - might be able to consolidate both menus into single function.
def action_menu(menu_options):
	''' '''
	terminal_submenu = TerminalMenu(
		menu_options,
		clear_menu_on_exit=False,
		# show_search_hint=True,
		# preview_title='Preview',
		preview_border=True,
		# preview_command=preview2,
		# preview_command="bat --color=always configs/hostapd-wpe.conf", 
		# preview_size=0.75,
		# show_shortcut_hints_in_status_bar=True,
		status_bar=status2,
		status_bar_style=("fg_gray", "bg_blue"),
		status_bar_below_preview=True
		)
	# Menu print.
	menu_entry_index = terminal_submenu.show()
	# Selected entry.
	selected = menu_options[menu_entry_index]

	return menu_entry_index
def ap_menu(menu_options):
	''' '''
	terminal_menu = TerminalMenu(
		menu_options,
		clear_menu_on_exit=False,
		show_search_hint=True,
		preview_title='Preview Config.ini',
		preview_border=True,
		preview_command=preview_config,
		preview_size=0.75,
		# show_shortcut_hints_in_status_bar=True,
		status_bar=status,
		status_bar_style=("fg_gray", "bg_blue"),
		status_bar_below_preview=True
		)
	# Menu print.
	menu_entry_index = terminal_menu.show()
	# AP selected entry.
	selected = menu_options[menu_entry_index]

	return selected
def load_menu(menu_options):
	''' '''
	terminal_submenu = TerminalMenu(
		menu_options,
		clear_menu_on_exit=False,
		# show_search_hint=True,
		# preview_title='Preview',
		preview_border=True,
		# preview_command=preview2,
		preview_command="cat ./my_configs/{}", 
		preview_size=0.75,
		# show_shortcut_hints_in_status_bar=True,
		status_bar=status,
		status_bar_style=("fg_gray", "bg_blue"),
		status_bar_below_preview=True
		)
	# Menu print.
	menu_entry_index = terminal_submenu.show()
	# Selected entry.
	selected = menu_options[menu_entry_index]

	return selected


def main():
	''' 
	'''

	# Scanner - Print interface list from wpa_cli.
	# scanner.Scanner.get_interfaces()

	# Quit toggle for menus.
	quit = False

	# ACTION_MENU - menu options lst.
	action_menu_options = [
	f"[0] Scan",
	f"[1] Save",
	f"[2] Load",
	f"[3] Launch",
	f"[4] Quit"
	]


	while not quit:
		# MENU_ACTION - launch and return the user's selection.
		r.console.print('\n')
		action_selected = action_menu(action_menu_options)

		# MENU - Scan
		if action_selected == 0:
			clearscreen.clear_screen()
			# Banner
			r.console.print(r.Panel('', title="Scanner", title_align='left', box=box.SQUARE, height=10))

			# AP_MENU - menu options lst.

			# Scanner - Init and return 'scan_results:str' from instance.
			wpa_cli_scanner = scanner.Scanner(args.ifname)
			scan_results = wpa_cli_scanner.run_scan()
			# Scanner - Remove '\t' from 'scan_results:str'.
			scan_results_clean = scan_results.replace(f'\t', ' ')
			# Scanner - Convert datatype 'str' to 'lst'.
			ap_menu_options = scan_results_clean.splitlines()
			# Scanner - Remove 'Selected interface:0' from lst.
			ap_menu_options.pop(0)
			# Scanner - Remove 'bssid / frequency / signal level / flags / ssid:0'.
			ap_menu_options.pop(0)

			# MENU_AP - launch and return the user's selection.
			ap_selected = ap_menu(ap_menu_options)
			
			
			# DEV - old technique of loading config.
			# ConfigParser - construct config.ini dictionaries from 'ap_selection'.
			# cp_config = set_config(ap_selected)
			
			# DEBUG - preview config, uncomment for debug only.
			# preview = preview_config(ap_selected)
			# print(preview)
			# exit()

			# DEV - config test.
			set_config(ap_selected)
			x = config.read()
			print(x)



		# MENU - Save
		if action_selected == 1:
			essid_filename = config['Hostapd']['essid']
			save_as = Prompt.ask('Save as: ', default=f"./my_configs/{essid_filename}.ini")
			# DEV - need overwrite feature.
			# ConfigParser - write config.ini file.
			config_filepath = write_config(config, save_as)
			print(f'Config-file saved: {config_filepath}')
			quit = True
		
		# MENU - Load
		if action_selected == 2:
			clearscreen.clear_screen()
			# Banner
			r.console.print(r.Panel('', title="Scanner", title_align='left', box=box.SQUARE, height=10))
			load_options = list_files('./my_configs/')
			# print(load_options)

			load_config = load_menu(load_options)
			
			# ConfigParser - clear config cache and read newconfig file.
			config.clear()
			x = config.read(f'./my_configs/{load_config}')
			print(x)
			

			# print(config.sections())
			# print({k:v for k, v in config['Hostapd'].items()})
			continue

		# MENU - Launch
		elif action_selected == 3:

			essid_filename = config['Hostapd']['essid']
			save_as = f"./my_configs/{essid_filename}.ini"
			# DEV - No need to write config.ini if loaded.
			# ConfigParser - write config.ini file.
			config_filepath = write_config(config, save_as)
			print(f'\nConfig-file saved: {config_filepath}')
			# open_file = Prompt.ask('Open Config-file: ', default=f"./my_configs/{essid_filename}.ini")

			# Hostpad - write hostapdfile.
			hostapd_filename = config['Main']['hostapd_filepath']
			hostapd_filepath = write_hostapd(config, hostapd_template, hostapd_filename)
			print(f'Hostpad file written: {hostapd_filepath}\n\n')
			# DEBUG - exit.
			# exit()

			# DEV - using config[], not cp_config[] need to look into this.
			# ConfigParser - declare interface_dic values.
			interface_dic = {k: v for k, v in config['Interface'].items()}
				
			# Interface - class init.
			int1 = interface.Interface(interface_dic['interface'])
			# Interface - place interface in down state.
			int1.isup(state=False)
			# Interface - declare mac addresss.
			mac_address = f"{interface_dic['bssid']}"	
			# Interface - set mac address and print result.
			setmac_results = int1.set_mac(f"--mac={mac_address}")
			# DEV - do I need setmaac_results_lst?
			setmac_results_lst = list(setmac_results)
			cmd = f"{' '.join(setmac_results_lst[0])}\n"
			stdout = setmac_results_lst[1]
			stderr = setmac_results_lst[2]
			# Heading1
			r.console.print(f'MAC ADDRESS', style='appheading')
			r.console.rule(style='rulecolor')
			print(cmd)
			print(stdout)
			print(stderr)

			# Interface - set reg.
			setreg_results = int1.set_reg(f'{interface_cc}')
			setreg_cmd = f"{' '.join(setreg_results[0])}\n"
			setreg_stdout = setreg_results[1]
			setreg_stderr = setreg_results[2]
			# Heading1
			r.console.print(f'Regulatory Domain', style='appheading')
			r.console.rule(style='rulecolor')
			print(setreg_cmd)
			print(setreg_stdout)
			print(setreg_stderr)

			# Interface - set Txpower and print result.
			tx_power = f"{interface_dic['tx_power']}"
			setpower_results = int1.set_txpower(f'{tx_power}')
			setpower_results_lst = list(setpower_results)
			setpower_cmd = f"{' '.join(setpower_results_lst[0])}\n"
			setpower_stdout = setpower_results_lst[1]
			setpower_stderr = setpower_results_lst[2]
			# Heading1
			r.console.print(f'TX-Power', style='appheading')
			r.console.rule(style='rulecolor')
			print(setpower_cmd)
			print(setpower_stdout)
			print(setpower_stderr)
			# Interface - place interface in up state.
			int1.isup(state=True)

			# ConfigParser - declare dict values.
			openssl_dic = {k: v for k, v in config['OpenSSL'].items()}
			cert = certificate.OpenSSL(
				openssl_dic['country'], 
				openssl_dic['state'], 
				openssl_dic['city'],
				openssl_dic['company'], 
				openssl_dic['ou'], 
				openssl_dic['email'],
				openssl_dic['cert_pem_filepath'],
				openssl_dic['cert_key_filepath']
				)
			cert_results = cert.run()
			cert_cmd = cert_results[0]
			cert_stdout = cert_results[1]
			cert_stderr = cert_results[2]
			# Heading1
			r.console.print(f'OpenSSL', style='appheading')
			r.console.rule(style='rulecolor')
			print(' '.join(cert_cmd))
			print(cert_stdout)
			print(cert_stderr)

			# ConfigParser - declare dict values.
			try:
				eviltwin = hostapd.Hostapd(hostapd_filepath)
				# Heading1
				r.console.print(f'HOSTAPD-WPE', style='appheading')
				r.console.rule(style='rulecolor')
				eviltwin.run()
			except KeyboardInterrupt:
				print(f'\nQuit: detected [CTRL-C] ')
				sys.exit(0)
		
		# MENU - Quit.
		elif action_selected == 4:
			quit = True


if __name__ == "__main__":
	main()

