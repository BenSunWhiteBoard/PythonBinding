import ctypes

lib = ctypes.CDLL("./libexample.so")

print_my_struct = lib.print_my_struct

# struct object in python
class MyStruct(ctypes.Structure):
    """ creates a struct to match mystruct in C"""

    _fields_ = [('data', ctypes.POINTER(ctypes.c_double)),
                ('size', ctypes.c_int)]

print_my_struct.argtypes = [ctypes.POINTER(MyStruct)]

data = (1.3, 3.5, 2.7, 4.1)
L = len(data)

my_st = MyStruct()
my_st.data = (ctypes.c_double * L)(*data)
my_st.size = ctypes.c_int(L)

# could be?
# print_my_struct(ctypes.pointer(my_st))
# pointer does a lot more work since it constructs a real pointer object, 
# so it is faster to use byref if you don't need the pointer object in Python itself.

print_my_struct(ctypes.byref(my_st))