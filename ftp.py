#-*-coding:utf-8-*-
import SocketServer,socket,sys,time,os
host = socket.gethostname()
ip = socket.gethostbyname(host)
port = 21

# 定义接收数据上线阈值
def recv_all(obj,msg,filename):
    while msg != 0:
        if msg <= 4096:
            data = obj.recv(msg)
            msg = 0
        else:
            data = obj.recv(4096)
            msg -= 4096
        filename.write(data)

# 定义进度条
def progress(size):
    size = int(size) + 1
    for i in range(1,size):
        sys.stdout.write(str((float(i)/size)*100)+'%')
        sys.stdout.flush()

print u'服务器正在侦听：%s %s' %(ip,port)
print '============================================'
class mysock(SocketServer.BaseRequestHandler):
    def handle(self):
        print u'客户端连接来自：',self.client_address
        while True:
            data = self.request.recv(1024)
            if not data:
                print u'没有数据，终止当前这个连接！'
                break
            option,filename,size = data.split(',')
            print data
#            size1 = float(size) / 1024 # 转换单位
            if option == 'put':
                if int(size) != 0:
                    print  u'传输文件大小为 %s' %size
                    print u'文件传输中 ...'
                    f = open('public/%s' %filename,'rw')
                    recv_all(self.request,int(size),f)
                    progress(size)
                    self.request.send('[OK.]')
                    f.flush()
                    f.close()
                    print '[OK.]'
                else:
                    self.request.send('shutdown')
                    print u'没有数据！',self.client_address
                    break
if __name__ == '__main__':
    s = SocketServer.ThreadingTCPServer((ip, port), mysock)
    s.serve_forever()
