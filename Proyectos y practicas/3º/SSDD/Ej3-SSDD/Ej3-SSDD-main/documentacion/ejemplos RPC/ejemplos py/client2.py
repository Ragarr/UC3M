import rpyc
conn = rpyc.classic.connect("localhost")

def square(x):
    return x**2

fn = conn.teleport(square)
print(fn(2))


