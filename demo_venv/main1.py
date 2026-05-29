#from module1 import addition, double, greet,x,y #means specifically import the functions addition, double, greet,x,y from module1.py
#from module2 import minus #means specifically import the function minus from module2.py

#from module1 import * #means import all the functions from module1.py function are used by name directely
#from module2 import * #means import all the functions from module2.py function are used by name directely

#import module1 as m1 #means import the module1.py module and use it as m1
#import module2 as m2 #means import the module2.py module and use it as m2
import math
from mypackage import module1
from mypackage import module2

print(module1.addition(1, 2, 3, 4, 5))

print(module1.double(10))

print(module1.greet("John"))    

print(module1.x)
print(module1.y)

print(module2.x)
print(module2.y)
print(module2.minus(module1.x,module1.y))

if __name__ == "__main__":
    print("This is the main file")
