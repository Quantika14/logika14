from scapy.all import *
import http.client, urllib.request, urllib.parse, urllib.error, requests
from time import sleep
from datetime import datetime

interface = "wlp5s0mon" #Insert your interface
listbox=""
root=""
Find=""
timeoflastprintout = datetime.now()
timestamp = datetime.now()
refresh_interval_seconds = 10
ENDPOINT = ""

clients = []
def send(mac_dispo, AP):
	#PARAMETROS
	par = urllib.parse.urlencode({'chicle':'prueba','mac_dispo':mac_dispo,'vendor':'hello-kity','wifi_dispo':AP,'user_asoc':'MR'})
	cabeceras = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
	abrir_conexion = http.client.HTTPConnection(ENDPOINT)
	abrir_conexion.request("POST", "/api/api.php", par, cabeceras)
	respuesta = abrir_conexion.getresponse()
	print("[info]" + respuesta.reason)
	abrir_conexion.close()

def get_dot11_mgmt(pkt):
	
	f_types = (0, 2, 4)
	macs_val = True
	if pkt.haslayer(Dot11) and pkt.haslayer(Dot11ProbeReq):

		if pkt.type == 0 and pkt.subtype in f_types:
			if pkt.addr2 not in clients:
				if pkt.info:
					timestamp = datetime.now()
					for macs in open("manuf.txt","r").readlines():
						try:
							mac = macs.lower().split("|||")[0]
							finder = pkt.addr2.find(mac)
							if finder != -1:
								pretext = " --------------------------------------------------------------------------- "
								text = "VENDOR: "+macs.split("|||")[1]
								text_2=	'MAC: '+ pkt.addr2 
								text_3=	'AP: '+ pkt.info 
								if Find in text or Find in text_2 or Find in text_3:
									listbox.insert("0", text_3)
									listbox.itemconfig("0", bg = "red")
									listbox.insert("0", text_2)
									listbox.itemconfig("0", bg = "red")
									listbox.insert("0", text)
									listbox.itemconfig("0", bg = "red")
									listbox.insert("0", pretext)
									listbox.update_idletasks()
									macs_val = False
									break
								else:
									listbox.insert("0", text_3)
									listbox.insert("0", text_2)
									listbox.insert("0", text)
									listbox.insert("0", pretext)
									listbox.update_idletasks()
									macs_val = False
									break
							else:
								continue
						except:
							continue

					if macs_val != False:
						pretext = " --------------------------------------------------------------------------- "
						text = "VENDOR: Not Found"
						text_2=	'MAC: '+ pkt.addr2 
						text_3=	'AP: '+ pkt.info 
						if Find in text or Find in text_2 or Find in text_3:
							listbox.insert("0", text_3)
							listbox.itemconfig("0", bg = "red")
							listbox.insert("0", text_2)
							listbox.itemconfig("0", bg = "red")
							listbox.insert("0", text)
							listbox.itemconfig("0", bg = "red")
							listbox.itemconfig("0", bg = "red")
							listbox.update_idletasks()
						else:
							listbox.insert("0", text_3)
							listbox.insert("0", text_2)
							listbox.insert("0", text)
							listbox.insert("0", pretext)
							listbox.update_idletasks()
							
							#SENDING INFO
							#send(pkt.addr2, pkt.info)                   
					else:
						pass
					arch = open(filename_report, "a")
					arch.write("-----------------------------------------------------\n\n"+text+"\n"+text_2+"\n"+text_3+"\n\n")
					arch.close()
					clients.append(pkt.addr2)
					macs_val=True
	elif pkt.haslayer(Dot11) and (pkt.FCfield & 0x03 == 0x01):
		if pkt.addr2 not in clients:
				if pkt.addr1:
					for macs in open("manuf.txt","r").readlines():
						try:
							mac = macs.lower().split("|||")[0]
							finder = pkt.addr2.find(mac)
							if finder != -1:
								pretext = " --------------------------------------------------------------------------- "
								text = "VENDOR: "+macs.split("|||")[1]
								text_2=	'MAC: '+ pkt.addr2 
								text_3=	'AP: '+ pkt.addr1 
								if Find in text or Find in text_2 or Find in text_3:
									listbox.insert("0", text_3)
									listbox.itemconfig("0", bg = "red")
									listbox.insert("0", text_2)
									listbox.itemconfig("0", bg = "red")
									listbox.insert("0", text)
									listbox.itemconfig("0", bg = "red")
									listbox.insert("0", pretext)
									listbox.update_idletasks()
									macs_val = False
									break
								else:
									listbox.insert("0", text_3)
									listbox.insert("0", text_2)
									listbox.insert("0", text)
									listbox.insert("0", pretext)
									listbox.update_idletasks()
									macs_val = False
									break
							else:
								continue
						except:
							continue

					if macs_val != False:
						pretext = " --------------------------------------------------------------------------- "
						text = "VENDOR: Not Found"
						text_2=	'MAC: '+ pkt.addr2 
						text_3=	'AP: '+ pkt.addr1 
						if Find in text or Find in text_2 or Find in text_3:
							listbox.insert("0", text_3)
							listbox.itemconfig("0", bg = "red")
							listbox.insert("0", text_2)
							listbox.itemconfig("0", bg = "red")
							listbox.insert("0", text)
							listbox.itemconfig("0", bg = "red")
							listbox.itemconfig("0", bg = "red")
							listbox.update_idletasks()
						else:
							listbox.insert("0", text_3)
							listbox.insert("0", text_2)
							listbox.insert("0", text)
							listbox.insert("0", pretext)
							listbox.update_idletasks()
							#PETICION PARA MANDAR POR HTTP AL SERVIDOR
							#send(pkt.addr2, pkt.info)                   
					else:
						pass
					arch = open(filename_report, "a")
					arch.write("-----------------------------------------------------\n\n"+text+"\n"+text_2+"\n"+text_3+"\n\n")
					arch.close()
					clients.append(pkt.addr2)
					macs_val=True


def main(listb, ro, data, filename):
	''' OJO!!! Poner la interface wireless en modo monitor primero!!'''
	global listbox
	global root
	global Find
	global filename_report
	global interface

	listbox=listb
	root=ro
	Find=data
	filename_report=filename
	
	if data != "":
		#try:
			sniff(iface=interface, prn=get_dot11_mgmt, store=0)
			listbox.insert("0", "Finalizó el escaneo de dispositivos")
			listbox.itemconfig("0", bg = "green")
			listbox.update_idletasks()
	#	except RuntimeError as e:
	#		sys.exit(1)
	#	except:
	#		listbox.insert("0", "La tarjeta de red no esta en modo monitor")
	#		listbox.itemconfig("0", fg = "red")
	#		listbox.update_idletasks()
	else:
		listbox.insert("0", "Introduce una busqueda")
		listbox.itemconfig("end", bg = "red", store=0)
		listbox.update_idletasks()
