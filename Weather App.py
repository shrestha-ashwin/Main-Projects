#Ashwin Shrestha                      24-11-2023
#Description : This is a weather-app which utilizes API to get data, logic to get relevant data, allows the possibility to save this data
#              to a file, and load them later in a new program run-time. You can either get data for the weather right now or weather 
#              forecast for the next five days, and the user have options to choose the metric unit(C or F).



import requests                        # library which has necessary methods for working with APIs.
import pickle                          # Pickle serializes and deserializes data
import sys                             # sys interacts directly with interpreter
import os                              # interacts with os, and ultimately with environmental variables
from dotenv import load_dotenv         # dotenv for storing the API keys as it is safer this way.


def getAPI_KEY():
   load_dotenv()   # loads the environmental variables from .env(dotenv)
   weather_key = os.getenv("Weather_key")    # gets the OpenWeatherApiKey of the environmental variable named "Weather_key"
   if not weather_key:
      print("The OpenWeatherAPI Key was not found. Please set it up in .env file")
   return weather_key

def integer_enforcer(integer):     # Enforces the input to be integer by repeatedly asking the user to enter an integer until the user enters an integer.
   while True:
      try:
         integer = int(integer)
      except Exception as e:
         print("Error: ",e)
         return False
      
      return integer

def input_check(user_input,a,b):                              # checks if user_input is equal to either a or b (anyone of them), and returns False if not equal. Returns True if equal.
      if user_input != a and user_input != b:
          print(f"Error! Please enter either {a} or {b}")
          return False
      return True


def Data_API(weather_key):
   while True:
      city = input("enter the city: ")
      try:
        data = requests.get("http://api.openweathermap.org/geo/1.0/direct?q={0}&limit={1}&appid={2}".format(city,1,weather_key))   #requests data from the api, side note- this api call is just to get the coordinates of the location
        if (data.text) == '[]':                  # returns "[]" in cases where the city is not found but the request was successful
           print("Error, city not found")
           continue
        data.raise_for_status()                  # returns exception if not a 200 level response
      except requests.exceptions.HTTPError as e:           # if it is the case that this is the problem of the API not returning the data, this exception is excecuted.
        print("Unbale to access data from API. Details: ",e)
      break
   return data
      


def getTemp():
    while True:
       temp = input("Choose: Celsius[1] or Farenheit[2]:" )     # choice between celsius and fahrenheit for the user
       temp = integer_enforcer(temp)                            # check if the input is an integer
       if temp == False:                                        # if false, the loop continues until the user enters an integers.
          continue
       if temp not in [1,2]:                                    # checks if the input is either 1 or 2, and if it is not then the loop goes to the first line after while loop.
          print("Error! Please enter [1] or [2]")
          continue
       break
       
    if temp == 1:
       print("Temperature will be displayed in Celsius\n")
       return "metric","C"                                       # necessary parameters for the API key is returned
    else:
       print("Temperature will be displayed in Fahrenheit\n")
       return "imperial","F"                                     # necessary parameters for the API key is returned
       

def coordinates(data):
   coordinate = {}
   coordinate["lat"] = data.json()[0]['lat']                     # gets the latitiude from the data, and makes a key-value pair.
   coordinate["long"] = data.json()[0]['lon']                    # gets the longitude from the data, and makes a key-value pair.
   return coordinate


def weather_getdata(coordinate,temp,weather_key):
   data = {}
   get_data = requests.get("https://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&units={3}&appid={2}".format(coordinate["lat"],coordinate["long"],weather_key,temp))   #gets weather-related data from api
   data_json = get_data.json()                                                # converts data into json format
   data["country"] = data_json["sys"]["country"]                              # following lines go into data to get useful data
   data["location"] = data_json["name"]
   data["description"] = (data_json["weather"][0]["description"])
   for i in data_json["main"]:
      if i != "temp_max" and i != "temp_min":                                 #everything except temp_max and temp_min is added as key-value pair to the dictionary "data".
         data[i] = data_json["main"][i]
   return data

def weatherforecast_getdata(coordinate,temp,user_temp,weather_key):
   get_data = requests.get("https://api.openweathermap.org/data/2.5/forecast?lat={0}&lon={1}&appid={2}&units={3}".format(coordinate["lat"],coordinate["long"],weather_key,temp))    # api call for weather forecast for the next five days
   data_json = get_data.json()                                         #converts data into json (highly desirable as it is a easier form to work with)
   all_data = []
  

   for i in data_json["list"]:                                     # all_data is a list which contains all data, and the individual data is grouped together by date.
      if user_temp in i['dt_txt']:
           data = {}
           data["Date"] = i["dt_txt"]
           data["Country"] = data_json["city"]["country"]
           data["Location"] = data_json["city"]["name"]
           data["Description"] = i["weather"][0]["description"]
           data["Temperature"] = i["main"]["temp"]
           data["Feels_like"] = i["main"]["feels_like"]
           data["Humidity"] = i["main"]["humidity"]
           data["Wind Speed"] = i["wind"]["speed"]
           all_data.append(data)
           

   return all_data
         
def print_f(data):                                                   # the function which has the method for printing the data which we kept in all_data
   for i in data:
      print("\n")
      for keys,val in i.items():
           print(keys,":",val)
   return
   


def save(data):
    user_file = input("enter your file name(without any .extensions): ")
    if ".txt" not in user_file:                                 # if .txt not in the input, then .txt is added to the filename
         user_file = user_file+".txt"
    with open(user_file, "wb") as file:                         # file with the name that the user has specified is created (with method is superior in respect that we don;t have to close the file as it is automatically)
         pickle.dump(data, file)                                # pickle method converts the whole data to binary, and saves it to the file.

def load():
    user_file = input("enter the file name(without .extension): ")
    if ".txt" not in user_file:
          user_file = user_file+".txt"
    try:
       with open(user_file, "rb") as file:                      # rb - read binary. opens a file named what the user specified
          file = pickle.load(file)                              # pickle load converts binary to a human readable format
    except FileNotFoundError:                                   # if file is not found
          print(f"The file {user_file} was not found")
    except Exception as e:                                      # for any other error
          print("Error: ",e)
          sys.exit()                                            # total exit, the user needs to restart
      
                                                                # following condition helps us distinguish between a file of a normal weather data, and one of weather forecast data. This is needed as these two files needed to be printed differently.
    if len(file)>5:                                             # just the weather call has a length more than 5
          for i in file:
             print(i,":",file[i])
      
    else:                                                       # because the forecast has 5 dictionaries inside a list because of data of 5 days, the length is 5
        print_f(file)

def weather_displaydata(weather_key):
    data = Data_API(weather_key)                                # calls function for data on co-ordinates
    coordinate = coordinates(data)                              # calls function which goes through data to get co-ordinates
    temp,sign = getTemp()                                       # calls function which gives user the option to choose between fahrenheit and celsius
    data = weather_getdata(coordinate,temp,weather_key)         # calls function which uses coordinate, and temperature to get data on weather
    print("Country: {0} \nLocation: {1}".format(data["country"],data["location"]))   #the print statements print out data that we stored in the variable "data" from our api calls.
    print("Description: {0} \nTemperature: {1} {5} \nFeels Like: {2} {5} \nPressure: {3} hPa \nHumidity: {4}%".format(data["description"],data["temp"],data["feels_like"],data["pressure"],data["humidity"],sign))
    return data
    
def weatherforecast_displaydata(weather_key):
    while True:
        user_temp = input("Choose forecast for the following times in the day: 00,03,06,09,12,15,18,21: ")         # as a way to restrict printing just about everything about the data, and also giving the user the choice to choose times of the day to get the weather for
        if user_temp != "00" and user_temp != "03" and user_temp != "06" and user_temp != "12" and user_temp != "15" and user_temp != "18" and user_temp != "21":    #input invalidation
             print("Error!Please enter only the values listed above")
             continue
                  
        user_temp = user_temp+":00:00"                                        # user temp is to be in the form "00:00:00" as it is what we look for in the data in conditions
        data = Data_API(weather_key)                                          # calls function for data on co-ordinates
        coordinate = coordinates(data)                                        # calls function which goes through data to get co-ordinates
        temp,sign = getTemp()                                                 # calls function which gives user the option to choose between fahrenheit and celsius
        data = weatherforecast_getdata(coordinate,temp,user_temp,weather_key) # calls function which uses coordinate, and temperature to get data on weather forecast
        print_f(data)                                                         # calls function which calls this data
        return data
    



def main():
    print("#################################################")                                          # prints banner
    print("Welcome to this weather forecaster\n")                                                       
    weather_key = getAPI_KEY()                                                                          # calls a function which gets the API key from enviornmental variable
    while True:
      user_choice = input("Please enter either : [w]eather, [l]oad previous data, [e]xit: ")            # gives user option to choose between different options
      
      if user_choice == "w":                                                                            # choice "w" - weather has its own sub-choices
         while True:
           user_input = input("\n""Enter either: [t]emperature, weather[f]orecast, [s]ave, [e]xit: ")
           if user_input != "t" and user_input != "e" and user_input != "s" and user_input != "f":      # if user input does not match either of the options, this pattern ensures that program will continue to ask for the same input till the user inputs correct input.
              print("Error! Enter [t] or [s] or [e]")
              continue
           
           if user_input == "t":                                                                        # calls a function that contains all functions for weather
              data = weather_displaydata(weather_key)
              
           elif user_input == "f":                                                                      # calls a function that contains all functions for weather forecast
              data = weatherforecast_displaydata(weather_key)
                  
           elif user_input == "s":                                                                      # calls a function to save the data
              save(data)

           elif user_input == "e":                                                                      # exits the function, and exits this loop, but program still has one more loop.
              print()
              break
           
      elif user_choice == "l":                # calls a function load which loads file if found
          load()
      
   
      elif user_choice == "e":                # user chose to exit by pressing e, we break the loop, and the program ends
         break
          
    




if __name__ == "__main__":                 # checks if true, and proceeds to calling main function
    main()