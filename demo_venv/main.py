#from module1 import addition, double, greet,x,y #means specifically import the functions addition, double, greet,x,y from module1.py
#from module2 import minus #means specifically import the function minus from module2.py

#from module1 import * #means import all the functions from module1.py function are used by name directely
#from module2 import * #means import all the functions from module2.py function are used by name directely

import module1 as m1 #means import the module1.py module and use it as m1
import module2 as m2 #means import the module2.py module and use it as m2
import math

print(math.pi)
print(math.sqrt(16))
print(math.sqrt(36))
print(m1.greet("John"))#this will give error because module1 is not defined(we defined it as m1)
print(math.sqrt(25))

print(math.sqrt(36))

print(math.sqrt(49))

print(math.sqrt(64))

print(m1.addition(1, 2, 3, 4, 5))

print(m1.double(10))

print(  .greet("John"))    

print(m1.x)
print(m1.y)

print(m2.minus(m1.x,m1.y))

if __name__ == "__main__":
    print("This is the main file")
