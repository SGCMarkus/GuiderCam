import socket

class Anel(object):

    uidpwd="adminanel"

    def __init__(self,ip):
        self.UDP_host = "192.168.1.116"
        self.UDP_IP = ip
        self.UDP_SEND = 75
        self.UDP_RECV = 77
        self.adr_send = (self.UDP_IP,self.UDP_SEND)
        self.adr_recv = (self.UDP_host,self.UDP_RECV)
        self.comobj = None
        self.errmsg = ""
        self.sock1 = None
        self.sock2 = None
        self.stat = {}

    def connect(self):
        connected = False
        if self.comobj is None:
        # connect to anel
            try:
                self.sock1=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                self.sock2=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                self.sock2.settimeout(2)
                self.sock2.bind(self.adr_recv)
                self.comobj=True
                connected = True
            except:
                connected = False
                self.errmsg = "No Anel connection possible to " + str(self.UDP_IP)
        self.comobj = None
        return connected

    def disconnect(self):
        self.comobj=None
        self.sock1=None
        self.sock2=None

    def send(self,msg):
        self.sock1.sendto(msg,self.adr_send)

    def recv(self,len):
        return self.sock2.recvfrom(len)

    def status(self):
        # ('NET-PwrCtrl:NET-CONTROL2   :192.168.1.102:255.255.255.0:10.0.0.1:0.4.163.14.5.68:Lhires Power,0:Lhires Flat,0:Lhires Arc,0:Watec Power,0:Nr. 5,0:Nr. 6,0:Nr. 7,0:Nr. 8,0:0:80:IO-1,0,0:IO-2,0,0:IO-3,0,0:IO-4,0,0:IO-5,0,0:IO-6,0,0:IO-7,0,0:IO-8,0,0:22.3\xb0C:NET-PWRCTRL_05.0\r\n', ('192.168.1.102', 75))
        self.send("wer da?")
        stat=self.recv(4096)
        print(stat)
        data=stat[0].split(":")
        self.stat["name"]=data[1]
        self.stat["ip"]=data[2]
        self.stat["mask"]=data[3]
        self.stat["gateway"]=data[4]
        self.stat["MAC"]=data[5]
        for i in range(1,9):
            n,o=data[5+i].split(",")
            self.stat["SD"+str(i)+" name"]=n
            self.stat["SD"+str(i)+" onoff"]=int(o)
            self.stat["locked"]=data[14]
        self.stat["http"]=data[15]
        for i in range(1,9):
            n,ea,o=data[15+i].split(",")
            self.stat["IO"+str(i)+" name"]=n
            self.stat["IO"+str(i)+" einaus"]=int(ea)
            self.stat["IO"+str(i)+" onoff"]=int(o)
        self.stat["temp"]=float(data[24][:-2])
        self.stat["firmware"]=data[25].strip()

    def on(self,nr):
        if(self.connect()):
            self.send(str("Sw_on"+str(nr)+Anel.uidpwd).encode())
            print(self.recv(4096))
            self.disconnect()

    def off(self,nr):
        if(self.connect()):
            self.send(str("Sw_off"+str(nr)+Anel.uidpwd).encode())
            print(self.recv(4096))
            self.disconnect()

    def io_on(self,nr):
        if(self.connect()):
            self.send(str("IO_on"+str(nr)+Anel.uidpwd).encode())
            print(self.recv(4096))
            self.disconnect()

    def io_off(self,nr):
        if(self.connect()):
            self.send(str("IO_off"+str(nr)+Anel.uidpwd).encode())
            print(self.recv(4096))
            self.disconnect()
