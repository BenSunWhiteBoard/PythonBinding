# from wasmtime import Engine, Store, Module, Instance, Trap

# print("Initializing...")
# engine = Engine()
# store = Store(engine)

# print("Loading binary...")
# with open("start.wasm", "rb") as f:
#     binary = f.read()
#     print("Compiling module...")
#     module = Module(engine, binary)

# print("Instantiating module...")
# try:
#     instance = Instance(store, module, [])
# except Trap as trap:
#     print("Printing message...")
#     print(f">{trap.message}")
#     frame = trap.frames
#     print("Printing origin...")

from wasmtime import Store, Module, Instance, Func, FuncType

store = Store()
module = Module(store.engine, """
  (module
    (func $hello (import "" "hello"))
    (func (export "run") (call $hello))
  )
""")

def say_hello():
    print("Hello from Python!")
hello = Func(store, FuncType([], []), say_hello)

instance = Instance(store, module, [hello])
run = instance.exports(store)["run"]
run(store)