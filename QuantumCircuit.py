from splinter import Browser
import requests
import sys
import time
import getpass
from collections import defaultdict

# stevecarrell63
# sugoidesu
username = str(input("Username: "))
password = getpass.getpass()

url = 'http://quantumcomputer.ac.cn/login'

browser = Browser('firefox')
# browser = Browser('chrome', headless=False)
# browser = Browser('phantomjs')

browser.visit(url)

# cookies = browser.cookies.all()
# print(cookies)

browser.find_by_xpath('//*[@id="username"]').first.type(username)
browser.find_by_xpath('//*[@id="password"]').first.type(password)
browser.find_by_xpath('//*[@id="qasm-wrapper"]/div[3]/div[2]/div[2]/form/button').first.click()

# url1 = 'http://quantumcomputer.ac.cn/list.html'

# browser.visit(url1)

# If we run two javascript files we can generate all the cookies we need. However, that is a bitch so we should deal with that later.
# It would be cool if there was a tool where you post some javscript to it, and it returns the state of the browser to you. Like cookies and all that shit.
# Would allow you to run python with only requests and never have to worry about running javascript or simulating a full browser.
cookies = browser.cookies.all()
print(cookies)

time.sleep(3)

browser.quit()

# sys.exit(0)

class QuantumCircuit:
	"""
	This is a class that interfaces with the Alibaba quantum computer.

	Attributes:
		circuit_name (string) : The name you would like to call your circuit. Defaults to a random string. (TODO)
		cookies (dict) : A dictionary of cookies that you get from logging in to alibaba quantumcomputer.ac.cn.
	"""
	def __init__(self, circuit_name, cookies):
		self.cookies = cookies
		self.circuit_name = circuit_name

		self.data = []

		self.circuit_id = None

		self.is_run = False

		self.results = {}

		# Tracks the furthest occupied x value in the rail
		self.rails = defaultdict(int)

	def update_cookies(self, new_cookies):
		"""
		The function to update cookies. Cookies must be updates every once in a while as they expire.

		Parameters:
			new_cookies (dict) : A dictionary of cookies that you get from logging in to alibaba quantumcomputer.ac.cn.
		"""
		self.cookies = new_cookies

	def get_results(self):
		"""
		The function that fills and returns in the results for the most recent run of this quantum circuit.

		Returns:
			If successful, returns the results as a dict.
			If unsuccessful, returns None.
		"""
		url = 'http://quantumcomputer.ac.cn/experiment/resultlist'
		data = {
			"experimentId": self.circuit_id,
			"version":'',
			"_input_charset": "utf-8"
		}

		get_exp = requests.get(url, params=data, cookies=self.cookies)

		res = get_exp.json()

		if "success" in res and res["success"] == True:
			self.results = res
			# print(get_exp.text)
			return self.results
		return None

	def get_csrf(self, url):
		"""
		Helps us sidestep security precautions to avoid cross-site request forgery (csrf).
		"""
		url = url

		r = requests.get(url, cookies=self.cookies)
		temp = r.text
		csrf = temp.split("var csrf = \'")[1].split("\'")[0]

		return csrf

	def new_circuit(self, realOrSim="SIMULATE", bitWidth=10):
		"""
		The function to deploy this circuit as a new circuit on the quantum computer.

		Parameters:
			realOrSim (boolean?) : If you want to run it on a simulation, then keep it as "SIMULATE".
			self.bitWidth (int) : An integer in the range [10, 25] for "SIMULATE" and [11, 11] for a real
				quantum computer that determines the number of qubits you are allocated.

		Returns:
			True if the new circuit was added and False if not.
			Modifies self.circuit_id if successful so that we can edit and run this circuit by referring to it through circuit_id.
		"""
		url = 'http://quantumcomputer.ac.cn/experiment/infosave?_input_charset=utf-8'

		data = {
			'name': self.circuit_name,
			'type': realOrSim,
			'bitWidth': bitWidth
		}

		csrf = self.get_csrf('http://quantumcomputer.ac.cn/list.html')
		headers = {
			'X-CSRF-TOKEN': csrf,
			"Referer": "http://quantumcomputer.ac.cn/list.html",
			"Host": "quantumcomputer.ac.cn",
			"Origin": "http://quantumcomputer.ac.cn",
			"Content-Type": "application/json"
		}

		make_new_circuit = requests.post(url, headers=headers, json=data, cookies=self.cookies)

		new_circuit_json = make_new_circuit.json()
		if "success" in new_circuit_json and new_circuit_json["success"] == True:
			self.circuit_id = str(new_circuit_json["data"])
			return True
		return False

	def add_gate_single(self, text, x, y, gateDetail={}):
		# We can make it autoincrement the x value, based on the previous largest x in y.
		edit = {
			"text":text,
			"gateDetail":gateDetail,
			"x":x,
			"y":y
		}

		self.data.append(edit)

	def add_gate_double(self, text, x, y, y1, gateDetail={}):
		# We can make it autoincrement the x value, based on the previous largest x in y.
		edit = {
			"text":text,
			"gateDetail":gateDetail,
			"x":x,
			"y":y,
			"x1":x,
			"y1":y1
		}

		self.data.append(edit)

	def add_gate_triple(self, text, x, y, y1, y2, gateDetail={}):
		# We can make it autoincrement the x value, based on the previous largest x in y.
		edit = {
			"text":text,
			"gateDetail":gateDetail,
			"x":x,
			"y":y,
			"x1":x,
			"y1":y1,
			"x2":x,
			"y2":y2
		}

		self.data.append(edit)

	def add_H(self, target):
		last_filled_spot = self.rails[target]
		self.add_gate_single("H", last_filled_spot + 1, target)
		self.rails[target] = last_filled_spot + 1

	def add_X(self, target):
		last_filled_spot = self.rails[target]
		self.add_gate_single("X", last_filled_spot + 1, target)
		self.rails[target] = last_filled_spot + 1

	def add_M(self, target):
		last_filled_spot = self.rails[target]
		self.add_gate_single("M", last_filled_spot + 1, target)
		self.rails[target] = last_filled_spot + 1

	def add_CNOT(self, control, target):
		# When we add the gate, we need to determine an x value. Thus, we got to find the furthest unoccupied level on the rails.
		self.add_H(target)
		self.add_X(control)

		last_filled_spot = max(self.rails[control], self.rails[target]) 

		self.add_gate_double("CP", last_filled_spot + 1, control, target)

		self.rails[control] = last_filled_spot + 1
		self.rails[target] = last_filled_spot + 1

		self.add_H(target)
		self.add_X(control)

	def add_CCNOT(self, control1, control2, target):
		self.add_H(target)
		self.add_X(control1)
		self.add_X(control2)

		last_filled_spot = max(self.rails[control1], self.rails[control2], self.rails[target])

		self.add_gate_triple("CCP", last_filled_spot + 1, control1, control2, target)

		self.rails[control1] = last_filled_spot + 1
		self.rails[control2] = last_filled_spot + 1
		self.rails[target] = last_filled_spot + 1

		self.add_H(target)
		self.add_X(control1)
		self.add_X(control2)

	def add_RZ(self, target, angle):
		"""
		angle is a float or int. degrees
		"""
		text = "RZ_" + str(angle)

		last_filled_spot = self.rails[target]
		self.add_gate_single(text, last_filled_spot + 1, target)
		self.rails[target] = last_filled_spot + 1

	def add_RX(self, target, angle):
		"""
		angle is a float or int. degrees
		"""
		text = "RX_" + str(angle)

		last_filled_spot = self.rails[target]
		self.add_gate_single(text, last_filled_spot + 1, target)
		self.rails[target] = last_filled_spot + 1

	def push_edits(self):
		url = 'http://quantumcomputer.ac.cn/experiment/codesave?_input_charset=utf-8'

		data_json = {}

		data_json['experimentId'] = self.circuit_id
		data_json['data'] = self.data
		data_json['code'] = ""

		csrf_url = 'http://quantumcomputer.ac.cn/home.html?id=' + str(self.circuit_id)
		csrf = self.get_csrf(url=csrf_url)
		headers = {
			'X-CSRF-TOKEN': csrf
		}

		edit_circuit = requests.post(url, headers=headers, json=data_json, cookies=self.cookies)

		return edit_circuit.json()["success"]

	def run_circuit(self, shots=100, seed=420, Type="SIMULATE"):
		url = 'http://quantumcomputer.ac.cn/experiment/submit'
		data = {
			"experimentId": self.circuit_id,
			"type": Type,
			"bitWidth": "",
			"shots": shots,
			"seed": seed,
			"_input_charset": "utf-8"
		}

		csrf_url = 'http://quantumcomputer.ac.cn/home.html?id=' + str(self.circuit_id)
		csrf = self.get_csrf(url=csrf_url)
		headers = {
			'X-CSRF-TOKEN': csrf
		}

		run_circuit = requests.post(url, headers=headers, data=data, cookies=self.cookies)

		if "success" in run_circuit.json():
			self.is_run = True
			return run_circuit.json()["success"]

# def view_all_circuits(cookies=cookies):
# 	url = 'http://quantumcomputer.ac.cn/experiment/list?_input_charset=utf-8'

# 	view_all = requests.get(url, cookies=cookies)

# 	# print(view_all.text)

# 	parsed = view_all.json()

# 	if "success" in parsed and parsed["success"] == True:
# 		return parsed['data']

# 	return 'fail'

# def get_experiment_by_id(self, experiment_id):
# 	url = 'http://quantumcomputer.ac.cn/experiment/resultlist'
# 	data = {
# 		"experimentId": experiment_id,
# 		"version":'',
# 		"_input_charset": "utf-8"
# 	}

# 	get_exp = requests.get(url, params=data, cookies=cookies)



# # =================== Testing ================== #
# circuitid = new_circuit('HelloQuantumWorld')

# if circuitid:
# 	print('circuit creation successful')
# 	print('circuitid is ' + str(circuitid))

# # Here is a simple quantum circuit that applies a hadamard and then measures it.
# # Simulator should output 50% |0> and 50% |1>
# quantumCircuit = [
# 	{
# 		"text":"H",
# 		"gateDetail":{},
# 		"x":1,
# 		"y":1
# 	},
# 	{
# 		"text":"M",
# 		"gateDetail":{},
# 		"x":2,
# 		"y":1
# 	}
# ]

# ec_success = edit_circuit(circuitid, quantumCircuit)

# if ec_success == True:
# 	print('circuit successfully edited')

# rc_success = run_circuit(circuitid)

# if rc_success == True:
# 	print('circuit successfully ran')

# results = get_experiment_by_id(circuitid)

# print('Here are the results:')
# print(results)

# ==============================
# Native Gate Set:
"""
CPhase
{
	"text":"CP",
	"gateDetail":{},
	"x":14,
	"y":3,
	"x1":14,
	"y1":2
}

RZ_Theta
{  
	"text":"RZ_45",
	"gateDetail":{},
	"x":2,
	"y":1
}

RX_Theta
{
	"text":"RX_25",
	"gateDetail":{},
	"x":4,
	"y":1
}

S†
{
	"text":"S†",
	"gateDetail":{
	#	"needGateParams":null
	},
	"x":40,
	"y":3
}
"""

print('making new circuit...')
qc = QuantumCircuit('testing CZ direction', cookies)

print(qc.new_circuit())

qc.add_H(1)
qc.add_CNOT(1, 2)
qc.add_M(1)
qc.add_M(2)

# # qc.add_gate("H", 1, 1)
# # qc.add_gate_single("X", 1, 1)
# qc.add_gate_double("CP", 3, 1, 3, 2)
# qc.add_gate_single("H", 2, 2)
# qc.add_gate_single("H", 4, 2)
# qc.add_gate_single("M", 5, 1)
# qc.add_gate_single("M", 5, 2)

# # qc.add_gate("H", 3, 1)
# # qc.add_gate("M", 4, 1)

print('pushing edits...')
print(qc.push_edits())

print('running the circuit...')
print(qc.run_circuit())

print(qc.get_results())
time.sleep(5)
print(qc.get_results())

# print(qc.)
