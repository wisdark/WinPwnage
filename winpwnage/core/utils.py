import os
import ctypes
import platform
from subprocess import check_output

try:
	import _winreg	# Python 2
except ImportError:	# Python 3
	import winreg as _winreg

from .winstructures import *

class disable_fsr():
	disable = ctypes.windll.kernel32.Wow64DisableWow64FsRedirection
	revert = ctypes.windll.kernel32.Wow64RevertWow64FsRedirection

	def __enter__(self):
		self.old_value = ctypes.c_long()
		self.success = self.disable(ctypes.byref(self.old_value))

	def __exit__(self, type, value, traceback):
		if self.success:
			self.revert(self.old_value)

class payloads():
	def exe(self, payload):
		if os.path.isfile(os.path.join(payload[0])) and payload[0].endswith(".exe"):
			commandline = ""
			for index, object in enumerate(payload):
				if index >= len(payload)-1:
					commandline += payload[index]
				else:
					commandline += payload[index] + " "
			return True, commandline
		else:
			return False

	#def dll(self, payload):
	#	return bool(os.path.isfile(os.path.join(payload[0])) and payload[0].endswith(".dll"))

class makecab():
	def makecab(self, source, destination):
		if not os.path.exists(source):
			return False

		exit_code = process().create("makecab.exe", params="{source} {destination}".format(source=source,
									destination=destination), window=False, get_exit_code=True)
		if exit_code == 0:
			return True
		else:
			return False

class wusa():
	def extract(self, cabinet, destination):
		if not os.path.exists(cabinet):
			return False

		results = process().create("wusa.exe", params="{cabinet} /extract:{destination} /quiet".format(cabinet=cabinet,
									destination=destination), window=False, get_exit_code=True)
		if results == 0:
			try:
				os.remove(cabinet)
			except Exception as error:
				pass
			finally:
				return True
		else:
			return False

class process():
	def create(self, payload, params="", window=False, get_exit_code=False):
		shinfo = ShellExecuteInfoW()
		shinfo.cbSize = sizeof(shinfo)
		shinfo.fMask = SEE_MASK_NOCLOSEPROCESS
		shinfo.lpFile = payload
		shinfo.nShow = SW_SHOW if window else SW_HIDE
		shinfo.lpParameters = params

		if ShellExecuteEx(byref(shinfo)):
			if get_exit_code:
				ctypes.windll.kernel32.WaitForSingleObject(shinfo.hProcess, -1)
				i = ctypes.c_int(0)
				pi = ctypes.pointer(i)
				if ctypes.windll.kernel32.GetExitCodeProcess(shinfo.hProcess, pi) != 0:
					return i.value

			return True
		else:
			return False

	def runas(self, payload, params=""):
		shinfo = ShellExecuteInfoW()
		shinfo.cbSize = sizeof(shinfo)
		shinfo.fMask = SEE_MASK_NOCLOSEPROCESS
		shinfo.lpVerb = "runas"
		shinfo.lpFile = payload
		shinfo.nShow = SW_SHOW
		shinfo.lpParameters = params
		try:
			return bool(ShellExecuteEx(byref(shinfo)))
		except Exception as error:
			return False

	def enum_processes(self):
		size = 0x1000
		cbBytesReturned = DWORD()
		unit = sizeof(DWORD)
		dwOwnPid = os.getpid()
		while 1:
			process_ids = (DWORD * (size // unit))()
			cbBytesReturned.value = size
			EnumProcesses(byref(process_ids), cbBytesReturned, byref(cbBytesReturned))
			returned = cbBytesReturned.value
			if returned < size:
				break
			size = size + 0x1000
		process_id_list = list()
		for pid in process_ids:
			if pid is None:
				break
			if pid == dwOwnPid and pid == 0:
				continue
			process_id_list.append(pid)
		return process_id_list

	def enum_process_names(self):
		pid_to_name = {}
		for pid in self.enum_processes():
			name = False
			try:
				process_handle = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, pid)
			except Exception as e:
				continue
			name = get_process_name(process_handle)
			if name:
				pid_to_name[pid] = name
			if process_handle:
				CloseHandle(process_handle)
		return pid_to_name

	def get_process_pid(self, processname):
		for pid, name in self.enum_process_names().items():
			if processname in name:
				return pid

	def terminate(self, processname):
		pid = self.get_process_pid(processname)
		if pid:
			try:
				phandle = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, False, pid)
				os.kill(pid, phandle)
				return True
			except Exception:
				pass
		return False

class registry():
	def __init__(self):
		self.hkeys = {
			"hkcu": _winreg.HKEY_CURRENT_USER,
			"hklm": _winreg.HKEY_LOCAL_MACHINE
		}

	def modify_key(self, hkey, path, name, value, create=False):
		try:
			if not create:
				key = _winreg.OpenKey(self.hkeys[hkey], path, 0, _winreg.KEY_ALL_ACCESS)
			else:
				key = _winreg.CreateKey(self.hkeys[hkey], os.path.join(path))
			_winreg.SetValueEx(key, name, 0, _winreg.REG_SZ, value)
			_winreg.CloseKey(key)
			return True
		except Exception as e:
			return False

	def remove_key(self, hkey, path, name="", delete_key=False):
		try:
			if delete_key:
				_winreg.DeleteKey(self.hkeys[hkey], path)
			else:
				key = _winreg.OpenKey(self.hkeys[hkey], path, 0, _winreg.KEY_ALL_ACCESS)
				_winreg.DeleteValue(key, name)
				_winreg.CloseKey(key)
			return True
		except Exception as e:
			return False

class whoami():
	def __init__(self):
		self.privs = {"SeIncreaseQuotaPrivilege" : "Adjust memory quotas for a process",
					"SeSecurityPrivilege" : "Manage auditing and security log",
					"SeTakeOwnershipPrivilege" : "Take ownership of files or other objects",
					"SeLoadDriverPrivilege" : "Load and unload device drivers",
					"SeSystemProfilePrivilege" : "Profile system performance",
					"SeSystemtimePrivilege" : "Change the system time",
					"SeProfileSingleProcessPrivilege" : "Profile single process",
					"SeIncreaseBasePriorityPrivilege" : "Increase scheduling priority",
					"SeCreatePagefilePrivilege" : "Create a pagefile",
					"SeBackupPrivilege" : "Back up files and directories",
					"SeRestorePrivilege" : "Restore files and directories",
					"SeShutdownPrivilege" : "Shut down the system",
					"SeDebugPrivilege" : "Debug programs",
					"SeSystemEnvironmentPrivilege" : "Modify firmware environment values",
					"SeChangeNotifyPrivilege" : "Bypass traverse checking",
					"SeRemoteShutdownPrivilege" : "Force shutdown from a remote system",
					"SeUndockPrivilege" : "Remove computer from docking station",
					"SeManageVolumePrivilege" : "Perform volume maintenance tasks",
					"SeImpersonatePrivilege" : "Impersonate a client after authentication",
					"SeCreateGlobalPrivilege" : "Create global objects",
					"SeIncreaseWorkingSetPrivilege" : "Increase a process working set",
					"SeTimeZonePrivilege" : "Change the time zone",
					"SeCreateSymbolicLinkPrivilege" : "Create symbolic links",
					"SeDelegateSessionUserImpersonatePrivilege" : "Obtain an impersonation token for another user in same session"}

		self.sids = {"S-1-2-0" : "Local",
					"S-1-0-0" : "Nobody",
					"S-1-1-0" : "Everyone",
					"S-1-5-32-545" : "Users",
					"S-1-5-32-546" : "Guests",
					"S-1-0" : "Null Authority",
					"S-1-1" : "World Authority",
					"S-1-2" : "Local Authority",
					"S-1-5-4" : "Interactive",
					"S-1-2-1" : "Console Logon",
					"S-1-5-18" : "Local System",
					"S-1-5-19" : "Local Service",
					"S-1-5-20" : "Network Service",
					"S-1-5-32-547" : "Power Users",
					"S-1-5-15" : "This Organization",
					"S-1-5-32-544" : "Administrators",
					"S-1-5-11" : "Authenticated Users",
					"S-1-5-32-549" : "Server Operators",
					"S-1-5-32-550" : "Print Operators",
					"S-1-5-32-551" : "Backup Operators",
					"S-1-5-32-548" : "Account Operators",
					"S-1-5-64-10" : "NTLM Authentication",
					"S-1-5-32-559" : "Builtin\Performance Log Users",
					"S-1-5-32-582" : "Storage Replica Administrators"}

	def elevated(self):
		return bool(ctypes.windll.shell32.IsUserAnAdmin())

	def privileges(self):
		return check_output(["whoami", "/priv", "/fo", "table",
								"|", "findstr", "Enabled"], shell=True).decode("latin1")
	def groups(self):
		return check_output(["whoami", "/groups"], shell=True).decode("latin1")

	def getgroups(self):
		result = []
		groups = self.groups()
		for sid in self.sids:
			if sid in groups:
				result.append(self.sids[sid])
		return result

	def getprivileges(self):
		result = []
		privs = self.privileges()
		for priv in self.privs:
			if priv in privs:
				result.append(priv)
		return result

class information():
	def system_directory(self):
		return os.path.join(os.environ.get("windir"), "system32")

	def system_drive(self):
		return os.environ.get("systemdrive")

	def windows_directory(self):
		return os.environ.get("windir")

	def architecture(self):
		return platform.machine()

	def username(self):
		return os.environ.get("username")

	def admin(self):
		return bool(ctypes.windll.shell32.IsUserAnAdmin())

	def build_number(self):
		try:
			key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,
									os.path.join("Software\\Microsoft\\Windows NT\\CurrentVersion"), 0, _winreg.KEY_READ)
			cbn = _winreg.QueryValueEx(key, "CurrentBuildNumber")
			_winreg.CloseKey(key)
		except Exception as error:
			return False
		else:
			return cbn[0]

	def uac_level(self):
		try:
			key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE,
									os.path.join("Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System"), 0, _winreg.KEY_READ)
			cpba = _winreg.QueryValueEx(key, "ConsentPromptBehaviorAdmin")
			cpbu = _winreg.QueryValueEx(key, "ConsentPromptBehaviorUser")
			posd = _winreg.QueryValueEx(key, "PromptOnSecureDesktop")
			_winreg.CloseKey(key)
		except Exception as error:
			return False
		else:
			cpba_cpbu_posd = (cpba[0], cpbu[0], posd[0])
			return {(0, 3, 0): 1, (5, 3, 0): 2, (5, 3, 1): 3, (2, 3, 1): 4}.get(cpba_cpbu_posd, False)
