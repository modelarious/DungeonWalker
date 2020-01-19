class A():
	def __init__(self):
		self.b = None

	def register_b(self, b):
		self.b = b

	def call_b_func(self):
		self.b.sayHi()

	def sayHi(self):
		print("A says hello")

class B():
	def __init__(self):
		self.a = None

	def register_a(self, a):
		self.a = a

	def call_a_func(self):
		self.a.sayHi()

	def sayHi(self):
		print("B says hello")

a = A()
b = B()

a.register_b(b)
b.register_a(a)

a.call_b_func()
b.call_a_func()
