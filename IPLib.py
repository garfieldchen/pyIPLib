import csv
import socket

class IPLib:
	def __init__(self, fn):
		self.ips = self.build(fn)
		
	@staticmethod
	def build(fn):
		ip_reader = csv.reader(open(fn))
		
		ip_list = []
		for row in ip_reader:
			ip2 = map(lambda i: int(row[i]), [2,3])
			ip_section = {
				"id_from": min(ip2),
				"id_to": max(ip2),
				
				"ip_from": row[0],
				"ip_to": row[1],
				
				"country": row[5],
				"country_abbr":row[4]
			}
			
			ip_list.append(ip_section)
			
		return ip_list
		
	@staticmethod
	def ip2key(ip):
		return int(socket.inet_aton(ip).encode('hex'), 16)
		
	def find(self, ip):
		def match_fun(key, item):
			if key < item["id_from"]:
				return -1
			elif key > item["id_to"]:
				return 1
			else:
				return 0				
			
		return self.bin_find(self.ips, self.ip2key(ip), match_fun)
			
	@staticmethod
	def bin_find(lst, key, fun):
		start = 0
		end = len(lst) - 1
		
		#line = 0
		while True:
			index = (end + start) / 2
			
			#print "line :%d "%line, start, end, index
			#line += 1
			
			item = lst[index]
			cmp_ret = fun(key, item)
			
			if start > end:
				break
				
			if (start == end and cmp_ret != 0):
				break
			
			if cmp_ret == 0:
				return item
			elif cmp_ret < 0:
				end = index
			else:
				start = index
		
		return None
		
if __name__ == "__main__":
	ip_lib = IPLib("GeoIPCountryWhois.csv")
	print map(lambda ip: ip_lib.find(ip), ["1.1.128.0", "1.4.128.0"])
	print ip_lib.find("1.8.255.33")
	print ip_lib.find("223.223.208.0")
		