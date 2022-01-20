import ctypes

add_lib = ctypes.CDLL("./libexample.so")

add_one = add_lib.add_one
#  should specify the function signature. 
#  This helps Python ensure that you pass the right type to the function.
add_one.argtypes = [ctypes.POINTER(ctypes.c_int)]

x = ctypes.c_int(2)
print("Python: before add_one x is:{}".format(x.value))
# byref() to allow passing a variable by reference
add_one(ctypes.byref(x))
print("Python: after add_one x is:{}".format(x.value))