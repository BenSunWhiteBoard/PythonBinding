# 1. General idea of a Wasm runtime python binding

## 1.1 wasmer-python

[This](https://github.com/wasmerio/wasmer-python) repo is

## 1.2 wasmtime-py

# 2. Python Bindings
A simple tutorial can be find [here](https://realpython.com/python-bindings-overview/) Sample code can be find in this [directory](./python-bindings)

## 2.1 Python Bindings Overview
### 2.1.1 Goal of Python bindings for WAMR

You already have a large, tested, stable `library` written `in C++` that you’d like to take advantage of in Python. This may be a communication library or a library to talk to a specific piece of hardware. What it does is unimportant.

### 2.1.2 Marshalling Data Types

For your purposes, marshalling is what the Python bindings are doing when they prepare data to move it from Python to C or vice versa. Python bindings need to do marshalling because Python and C store data in different ways. 

- `Integers` store counting numbers. Python stores integers with arbitrary precision, meaning that you can store very, very, large numbers. C specifies the exact sizes of integers. You need to be aware of data sizes when you’re moving between languages to prevent Python integer values from overflowing C integer variables.

- `Floating-point numbers` are numbers with a decimal place. Python can store much larger (and much smaller) floating-point numbers than C. This means that you’ll also have to pay attention to those values to ensure they stay in range.

- `Complex numbers` are numbers with an imaginary part. While Python has built-in complex numbers, and C has complex numbers, there’s no built-in method for marshalling between them. To marshal complex numbers, you’ll need to build a struct or class in the C code to manage them.

- `Strings` are sequences of characters. For being such a common data type, strings will prove to be rather tricky when you’re creating Python bindings. As with other data types, Python and C store strings in quite different formats. (Unlike the other data types, this is an area where C and C++ differ as well, which adds to the fun!) Each of the solutions you’ll examine have slightly different methods for dealing with strings.

- `Boolean variables` can have only two values. Since they’re supported in C, marshalling them will prove to be fairly straightforward.

### 2.1.3 Understanding Mutable and Immutable Values
You’ll also have to be aware of how Python objects can be mutable or immutable. C has a similar concept with function parameters when talking about pass-by-value or pass-by-reference. In C, all parameters are pass-by-value. If you want to allow a function to change a variable in the caller, then you need to pass a pointer to that variable.

### 2.1.4 Managing Memory
C and Python manage memory differently. In C, the developer must manage all memory allocations and ensure they’re freed once and only once. Python takes care of this for you using a garbage collector.

While each of these approaches has its advantages, it does add an extra wrinkle into creating Python bindings. You’ll need to be aware of where the memory for each object was allocated and ensure that it’s only freed on the same side of the language barrier

## 2.2 Different tools 

### 2.2.1 Using the invoke Tool
Invoke is the tool you’ll be using to build and test your Python bindings in this tutorial. It has a similar purpose to make but uses Python instead of Makefiles. 

### 2.2.2 Ctypes

Cyptes is a tool in the standard library for creating Python bindings. It provides a low-level toolset for loading shared libraries and marshalling data between Python and C.

Basic Usage:

1. Load your library.
2. Wrap some of your input parameters.
3. Tell ctypes the return type of your function.

Example usage can be find [here](/python-bindings/ctypes_c_test.py)

Pros and cons:

The biggest advantage ctypes has over the other tools you’ll examine here is that it’s `built into the standard library`. It also requires no extra steps, as all of the work is done as part of your Python program.

In addition, the concepts used are low-level, which makes exercises like the one you just did manageable. However, more `complex tasks grow cumbersome` with the `lack of automation`. In the next section, you’ll see a tool that adds some automation to the process.

### 2.2.3 CFFI

CFFI is the `C Foreign Function Interface` for Python. It takes a more `automated approach` to generate Python bindings. CFFI has multiple ways in which you can build and use your Python bindings. There are two different options to select from, which gives you four possible modes:

- ABI vs API: `API` mode uses a `C compiler` to generate a full Python module, whereas `ABI` mode `loads the shared library` and interacts with it directly. `Without` running the `compiler`, getting the structures and parameters correct is error-prone. The documentation heavily recommends using the API mode.

- in-line vs out-of-line: The difference between these two modes is a trade-off between speed and convenience:

  - In-line mode `compiles` the Python bindings `every time` your script runs. This is convenient, as you don’t need an extra build step. It does, however, slow down your program.

  - Out-of-line mode requires an extra step to generate the Python bindings a single time and then uses them each time the program is run. This is much faster, but that may not matter for your application.

Basic usage:
- Write some Python code describing the bindings.
- Run that code to generate a loadable module.
- Modify the calling code to import and use your newly created module.

Pros and cons:

It might seem that ctypes requires less work than the CFFI example you just saw. While this is true for this use case, `CFFI scales to larger projects` much better than ctypes due to automation of much of the function wrapping.

CFFI also produces quite a different user experience. ctypes allows you to load a pre-existing C library directly into your Python program. CFFI, on the other hand, `creates a new Python module` that can be loaded like other Python modules.

What’s more, with the out-of-line-API method you used above, the `time penalty for creating the Python bindings is done once` when you build it and doesn’t happen each time you run your code. For small programs, this might not be a big deal, but CFFI scales better to larger projects in this way, as well.

Like ctypes, using CFFI `only` allows you to interface with `C libraries` directly. C++ libraries require a good deal of work to use. In the next section, you’ll see a Python bindings tool that focuses on C++.

### 2.2.4 PyBind11

PyBind11 takes a quite different approach to create Python bindings. In addition to shifting the focus from C to C++, it also uses `C++ `to specify and build the module, allowing it to take advantage of the metaprogramming tools in C++. Like CFFI, the Python bindings `generated` from PyBind11 are a `full Python module` that can be imported and used directly.

PyBind11 is modeled after the Boost::Python library and has a similar interface. It restricts its use to C++11 and newer, however, which allows it to simplify and speed things up compared to Boost, which supports everything.

Basic usage:



# 3. APIs

# 4. Structure of python project and test

“Structure” means making clean code whose `logic` and `dependencies` are `clear` as well as how the `files` and `folders` are `organized` in the filesystem.

## 4.1 One possible structure

One possible structure can be find [here](https://docs.python-guide.org/writing/structure/), and the related codes in this [directories](./samplemod)

```
Python_Project/
├── README.md/README.rst()
├── LICENSE
├── setup.py(Package and distribution management.)
├── requirements.txt(Development dependencies.)
├── Makefile(Generic management tasks)
├── docs(Package reference documentation)/
│   ├── conf.py
│   └── index.rst
├── sample(The Actual Module)/
│   ├── __init__.py
│   ├── core.py
│   └── helpers.py
└── tests(Package integration and unit tests)/
    ├── context.py(to resolve the package properly.)
    ├── test_basic.py
    └── test_advanced.py
```

# 5. How to Publish Python package

## 5.1 Python packaging

Any directory with an `__init__.py` file is considered a Python package. The different modules in the package are imported in a similar manner as plain modules, but with a special behavior for the `__init__.py` file, which is used to gather all package-wide definitions.

e.g. A file modu.py in the directory pack/ is imported with the statement `import pack.modu`. This statement will `first` look for `__init__.py` file in pack and execute all of its top-level statements. `Then` it will look for a file named `pack/modu.py` and execute all of its top-level statements. After these operations, any variable, function, or class defined in modu.py is available in the pack.modu namespace.

A commonly seen issue is adding too much code to `__init__.py` files. When the project complexity grows, there may be sub-packages and sub-sub-packages in a deep directory structure. In this case, importing a single item from a sub-sub-package will require executing all `__init__.py` files met while traversing the tree.

Leaving an `__init__.py` file empty is considered normal and even good practice, if the package’s modules and sub-packages do not need to share any code.

## 5.2 Package tool

A simple tutorial from PyPA can be find [here](https://packaging.python.org/en/latest/tutorials/packaging-projects/)

```
packaging_tutorial/
├── LICENSE
├── pyproject.toml
├── README.md
├── setup.cfg
├── src/
│   └── example_package/
│       ├── __init__.py
│       └── example.py
└── tests/
```

`pyproject.toml` tells build tools (like pip and build) what is required to build your project.

There are two types of metadata: static and dynamic. Static metadata (setup.cfg) should be preferred. Dynamic metadata (setup.py) should be used only as an escape hatch when absolutely necessary. setup.py used to be required, but can be omitted with newer versions of setuptools and pip.

- Static metadata (setup.cfg): guaranteed to be the same every time. This is simpler, easier to read, and avoids many common errors, like encoding errors.
- Dynamic metadata (setup.py): possibly non-deterministic. Any items that are dynamic or determined at install-time, as well as extension modules or extensions to setuptools, need to go into setup.py.


The files listed above will be included automatically in your source distribution. If you want to control what goes in this explicitly, see [Including files in source distributions with MANIFEST.in](https://packaging.python.org/en/latest/guides/using-manifest-in/#using-manifest-in).

To publish our package:

- Generating distribution archives

    ```shell
    # ensure that latest version of PyPA’s build installed:
    python3 -m pip install --upgrade build
    # start to build
    python3 -m build
    ```

    Generated files:

    ```shell
    dist/
    example_package_YOUR_USERNAME_HERE-0.0.1-py3-none-any.whl
    example_package_YOUR_USERNAME_HERE-0.0.1.tar.gz
    ```

    The tar.gz file is a source archive whereas the .whl file is a built distribution.

- Uploading the distribution archives

    Example using `TestPyPI`:

    1. Register an account on [TestPyPI](https://test.pypi.org/account/register/)
    2. Create a [PyPI API token](https://test.pypi.org/manage/account/#api-tokens)
    3. Use twine to upload the distribution packages.

    ```shell
    python3 -m pip install --upgrade twine
    python3 -m twine upload --repository testpypi dist/*
    # for the username, use __token__. 
    # for the password, use the token value, including the pypi- prefix.
    ```

    4. Now you can use pip to install 
    ```shell
    python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps example-pkg-YOUR-USERNAME-HERE
    ```


    When you are ready to upload a `real` package to the Python Package Index you can do much the same as you did in the tutorial, but with these important differences:

    - Choose a memorable and unique name for your package. 
    
    - Register an account on https://pypi.org - note that these are two separate servers and the login details from the test server are not shared with the main server.
    
    - Use twine upload dist/* to upload your package and enter your credentials for the account you registered on the real PyPI. Now that you’re uploading the package in production, you don’t need to specify --repository; the package will upload to https://pypi.org/ by default.
    
    - Install your package from the real PyPI using `python3 -m pip install [your-package].`
     

