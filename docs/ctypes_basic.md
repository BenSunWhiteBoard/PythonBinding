# C structure in Python
For a C structure in C: 
```C
struct MyStruct 
{
    double *data;
    int size;
};
```
We will have to create a corresponding object in Python:
```python
# struct object in Python 
class MyStruct(ctypes.Structure):
    """ creates a struct to match mystruct in C"""

    _fields_ = [('data', ctypes.POINTER(ctypes.c_double)),
                ('size', ctypes.c_int)]

```

# C pointers in Python

Let's say we have a int object x in Python, and following is how you get create a pointer pointing to it:
```python
x = ctypes.c_int(2)
x_ptr = ctypes.byref(x)
# it can also be
x_ptr = ctypes.pointer(x)
```
pointer() does a lot more work since it constructs a real pointer object, so it is faster to use byref() if you don't need the pointer object in Python itself(e.g. only use x_ptr as a argument to pass to a function).

