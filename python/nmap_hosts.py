from nmap_vscan import vscan 

nmap = vscan.ServiceScan('./nmap-service-probes')
ip_list = []

for i in range(256):
    ip = '192.168.0.%d' % (i+1)
    try:
        nmap.scan(ip, 22, 'tcp')
    except:
        continue
    nmap = ip_list.append