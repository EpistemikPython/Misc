
class testClass:
	def __init__(self, p_i:int):
		self.i = p_i

	def get_int(self):
		return self.i


def print_int(obj:object):
	my_i = obj.get_int()
	print(F"int = {my_i}")


test_int = 37
test_obj = testClass(test_int)
print_int(test_obj)
