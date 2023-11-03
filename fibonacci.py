#Ashwin Shrestha         3-11-2023
#Fibonacci Series calculator, can even approximate the golden ratio to a very close approximstion given input is sufficiently large enough
#Can make the fibonacci rectangles.



import turtle
def getFibonacci(first_num,second_num):
    fibonacci = []
    fibonacci.append(first_num)
    fibonacci.append(second_num)
    b = True
    while b:
        a = int(input("enter how many digits of fibonacci: "))
        try:
          a = int(a)
        except Exception as e:
           print("Error: ",e)
           continue
        break
           
    for i in range(a-2):
       new_num = first_num+second_num 
       fibonacci.append(new_num)
       first_num = second_num
       second_num = new_num
    return fibonacci

def GoldenRatio(list):
    if len(list)>2:
        GR = list[-1]/list[-2]
    else:
        print("Please enter bigger range of number")
        return
    return GR
   


def FibonacciRectangle(list):
    a = turtle.Turtle()
    s = turtle.Screen()
    a.setpos(0,0)
    number = 0
    count = 1
    for i in list[1:]:
        if i == 1:
           x = 0
           while x<4:
             a.forward(i*20)
             a.right(90)
             x+= 1
           a.forward(i*20)

        
        if count%2 != 0:
          if i > 1:
             a.left(90)
             for j in range(4):
               a.forward(i*20)
               a.left(90)
             a.forward(i*20)
             count+= 1
        elif count%2 == 0:
           if i>1:
             a.right(90)
             for l in range(4):
               a.forward(i*20)
               a.right(90)
             a.forward(i*20)
             count+= 1
          
    s.exitonclick()



def main():
    first_num = 0
    second_num = 1  
    a = getFibonacci(first_num,second_num)
    b = GoldenRatio(a)
    print("The fibonacci series is: ",a)
    print("The Golden Ratio is:",b)
    user = input("Would you like to see the golden spiral?(y/n)")
    while user!= "y" and user!= "n":
       print("Error!Please enter either (y/n)")
       user = input("Would you like to see the golden spiral?(y/n) ")
    if user == "y":
      c = FibonacciRectangle(a)
    elif user == "n":
       pass

if __name__ == "__main__":
    main()



