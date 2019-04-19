from mysql.connector import errorcode

import time
import mysql.connector
import os
import logging
import csv
import string
import random
import json

random.seed(7331)

data_store = {}
record = []

def gen_random():
	my_str = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
	return my_str

def experiment(name):
	def record_response(func):
		record_response.counter = {}
		def wrapper(*args, **kwargs):
			global data_store

			try:
				record_response.counter[name] += 1
			except KeyError as e:
				record_response.counter[name] = 1

			ts = time.time()
			results = func(*args,**kwargs)
			te = time.time()

			try:
				data_store[name].append([ts,te,te-ts])
			except KeyError as e:
				data_store[name] = [[ts,te,te-ts]]

			print("Finished {0} Count {1}\n\tTS: {2}\n\tTE: {3}\n\tTime: {4}\n".format(name,record_response.counter[name],ts,te,te-ts))

			return results
		return wrapper

	return record_response
	
################################START OF CODE##################################################

ips = [
	"172.31.15.135",
	"172.31.15.164"
]

cnx = None
mysql_root_password = None

try:
	mysql_root_password = os.environ['MYSQL_ROOT_PASSWORD']
except KeyError as e:
	print("Please set Environment Var MYSQL_ROOT_PASSWORD")
	

for ip in ips:
	try:
		cnx = mysql.connector.connect(user='root',password=mysql_root_password,host=ip)
	except Exception as e:
		pass

if not cnx:
	print("Failed to connect to db server")
	quit()
else:
	print("connected to " + ip)


##
#Step 1
##
cur = cnx.cursor()
cur.execute("DROP DATABASE IF EXISTS testdb")
cur.execute("CREATE DATABASE testdb")
cur.execute("use testdb")
##
#Finished creating my DB
##

cur.execute("DROP TABLE IF EXISTS user_test")
cur.execute("CREATE TABLE user_test (id INT AUTO_INCREMENT PRIMARY KEY,user VARCHAR(255), pwd VARCHAR(255))")


for i in range(10000):
	record.append([gen_random(),gen_random()])

@experiment("write")
def write_record(record,cur,cnx):
	sql = "INSERT INTO user_test (user, pwd) VALUES (%s,%s)"
	val = (record[0],record[1])
	cur.execute(sql,val)
	cnx.commit()

@experiment("read")
def read_record(record,cur,cnx):
	sql = "SELECT COUNT(*) FROM user_test WHERE user LIKE %s"
	val = (record[0],)
	cur.execute(sql,val)
	cur.fetchall()

for i in record:
	write_record(i,cur,cnx)

for i in record:
	read_record(i,cur,cnx)

fout = open('/data/query_results.json','w');
fout.write(json.dumps(data_store))
fout.close()

print("finished :)")
