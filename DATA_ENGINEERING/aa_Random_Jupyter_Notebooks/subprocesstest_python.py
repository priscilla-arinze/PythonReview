import subprocess

subprocess.run("echo hi; echo  ; echo bleh ", check=True, shell=True)