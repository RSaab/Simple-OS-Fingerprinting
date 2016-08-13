import os
import pyperclip

# Deauthenticate devices
# Skip this MAC 00:16:44:60:53:ec (wlan0)
# or this MAC 00:22:b0:07:58:d4 (D-Link USB)
os.system("python de_auth.py -s 00:22:b0:07:58:d4 -d & sleep 30; kill $!")
# renew DHCP on linux "sudo dhclient -v -r & sudo dhclient -v"


# Capture DHCP Packet
os.system("tcpdump -lenx -s 1500 port bootps or port bootpc -v > dhcp.txt & sleep 20; kill $!")


# read packet txt file
DHCP_Packet = open("dhcp.txt", "r")

# Get info from txt file of saved packet
line1 = DHCP_Packet.readline()
line1 = line1.split()
sourceMAC = line1[1]
destMAC = line1[3]
TTL = line1[12]
length = line1[8]

#Parse packet
line = DHCP_Packet.readline()
while "0x0100" not in line:
	line = DHCP_Packet.readline()

packet = line + DHCP_Packet.read()

packet = packet.replace("0x0100:", "")
packet = packet.replace("0x0110:", "")
packet = packet.replace("0x0120:", "")
packet = packet.replace("0x0130:", "")
packet = packet.replace("0x0140:", "")
packet = packet.replace("0x0150:", "")
packet = packet.replace("\n", "")
packet = packet.replace(" ", "")
packet = packet.replace("	", "")
packet = packet.replace("000000000000000063825363", "")

# Locate option (55) = 0x0037
option = "0"
i=0
length = 0 
while option != "37":
	option = packet[i:i+2]
	hex_length = packet[i+2:i+4]
	length = int(packet[i+2:i+4], 16)
	i = i+ length*2 + 4

i = i - int(hex_length, 16)*2
option55 = packet[i:i+length*2 ]
pyperclip.copy(option55)
print "Option " + str(int(packet[i-4:i-2], 16)) +": " + option55 + \
	 "\nLength: " + str(length) + " Bytes"
print "Source MAC: " + sourceMAC



