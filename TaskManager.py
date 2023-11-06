#Ashwin Shrestha     4-11-2023
#The following code is for a task manager which can add tasks, view tasks, mark tasks as completed and finally exit.


def Display():
    print("Task Manager")
    print("1. Add Tasks")
    print("2. View Tasks")
    print("3. Mark Task as completed")
    print("4. Exit")

    while True:
        user = input("Enter any choice(1-4): ")
        try:
            user = int(user)
        except:
            print("Error! Please enter an integer..")
            continue
        if user == 1 or user == 2 or user == 3 or user == 4:
            break
        else:
            print("enter numbers between 1 and 4 only")
            continue
    return user

def Choice():
    task = {}
    initial = "pending"
    while True:
      num = Display()
      if num == 1:
          task_title = input("enter task title: ")
          task[task_title] = []
          task[task_title].append(initial)
          print("Task added successfully\n\n")
      elif num == 2:
          count = 1
          for key,value in task.items():
               print("{0}.".format(count),key," - ",value)
               count+= 1
          print("\n")
        
          
      elif num == 3:
          required = 0
          task_complete = int(input("enter task number to be completed: "))
          if task_complete <= 0:
              print("Please enter a task first!")
              continue
          task_dict = list(task)
          task[task_dict[(task_complete)-1]] = ["completed"]
          print("Task is marked as completed\n\n")
            
    
      elif num == 4:
          print("Exiting Task manager")
          break


def main():
    b = Choice()



if __name__ == "__main__":
    main()