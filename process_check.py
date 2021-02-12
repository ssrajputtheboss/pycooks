import wmi
import subprocess

def isProcessRunning():
	f = wmi.WMI()
	for process in f.Win32_Process():
		if 'pythonw' in process.Name.lower():
			return True
	return False

def start_process():
	if not isProcessRunning():
		os.system('pythonw \"runme.pyw\"')
def kill_process():
	os.system('taskkill /F /IM pythonw.exe /T')
