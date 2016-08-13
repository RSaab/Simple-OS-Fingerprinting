from scapy.all import *
from wifi import *

def sniffReq(p):
        
#In case there was Deauth Attack 

    if p.haslayer(Dot11Deauth):
        print p.sprintf("Deauthentication Attack Found from AP [%Dot11.addr2%]  Client [%Dot11.addr1%], Reason [%Dot11Deauth.reason%]")
       

sniff(iface="wlan0",prn=sniffReq)
