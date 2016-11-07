#__author__ = 'Administrator'
#-*-coding:utf-8-*-
import socket,os,sys,time
ip,port = '0.0.0.0',0
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
while True:
	ftp = raw_input('ftp> ').strip()
	ftp = ftp.split()
	try:
		if ftp[0] == 'lftp':
			if len(ftp) == 2:
				ip = ftp[1]
				ftp.append(21)
				port = ftp[2]
			else:
				ip = ftp[1]
				port = ftp[2]
	except:continue
	break
try:
	s.connect((ip,int(port)))
except:
	print 'The server is not found,please check the network connection.'
	sys.exit()

def put_file():
	try:
		filename = open(cmd[-1],'rb')
		size = os.stat(cmd[1])[-4]
		cmd.append(size)
	except:
		print 'put: %s: No such file or directory' %cmd[1]
	s.send('%s,%s,%s' %(cmd[0],cmd[1],int(cmd[2])))
	print 'File transfer,wait...'
	time.sleep(1)
	s.sendall(filename.read())


#connection
#=====================================================================================

while True:
	data = raw_input('ftp %s:~> ' %ip).strip()
	if len(data) == 0:
		continue
	cmd = data.split()
	if cmd[0] == 'bye':
		sys.exit()

#Put function area
#=====================================================================================

	if cmd[0] == 'put':
		if len(cmd) != 2:
			print "File name missed. Try 'help put' for more information."
			continue
		if cmd[-1][-1] == '/':
			print 'put: %s: Is a directory' %data
			continue
        try:
            put_file()
            if s.recv(10) == '[OK.]':
                print 'Done!'
        except:
            pass
        if s.recv(10) == 'shutdown':
            print '数据传输失败！'
            continue
	else:
		print "Unknown command '%s'" %data
		continue
