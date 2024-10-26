<<<<<<< HEAD
# 1 1 2 3 5 8 13 
x = 1
y = 1
def fib_gen(n):
    global x
    global y
    y = x+y
    yield y

def fibonacci(n): # 5
    a = 1
    print(a)
    b = 1
    print(b)
    i = 3
    while int(i)<=int(n):
        c = b
        b = a+b
        a = c
        print(b)
        i += 1


n = input("Enter number of entries: ")
print("Function:")
fibonacci(n)
print("Generator: ")
i = 2
print(1)
print(1)
while int(i)<int(n):
    c = y
    print(next(fib_gen(n)))
    x = c
    i+=1
=======
# 1 1 2 3 5 8 13 
x = 1
y = 1
def fib_gen(n):
    global x
    global y
    y = x+y
    yield y

def fibonacci(n): # 5
    a = 1
    print(a)
    b = 1
    print(b)
    i = 3
    while int(i)<=int(n):
        c = b
        b = a+b
        a = c
        print(b)
        i += 1


n = input("Enter number of entries: ")
print("Function:")
fibonacci(n)
print("Generator: ")
i = 2
print(1)
print(1)
while int(i)<int(n):
    c = y
    print(next(fib_gen(n)))
    x = c
    i+=1
>>>>>>> 21803d967ffdc3cef0cbd857276f4ef9b0ff6064
