"""made by ohad borenstein"""
import func
import mysql.connector

print("when you useing the code, add all the "
      "parameters into the code for connecting to mysql :\n"
      "host,user,passwd,database")
db = mysql.connector.connect(
    host="--type here--",
    user="--type here--",
    passwd="--type here--",
    database="--type here--"
)

mycursor = db.cursor()
calender = ""
my_calender = func.change_table(calender,db)

menu = \
    "1. Show all upcoming events\n" \
    "2. Add new event by path\n" \
    "3. Delete event by event ID\n" \
    "4. Show the up coming event\n" \
    "5. Show all the events by client name\n" \
    "6. Change table\n" \
    "7. Exit"


operation = [
    func.Calender.show_events,
    func.Calender.add_event,
    func.Calender.remove_event,
    func.Calender.get_first_event,
    func.Calender.get_events_by_name,
    func.change_table,
    func.Calender.save_and_exit
]

while True:
    print("\nchoose operation:")
    print(menu)
    option = input("option: ")
    if option.isdigit():
        option = int(option)
        if 1 <= option <= 7:
            if 2 <= option <= 3 or option == 6:
                operation[option - 1](my_calender,db)
            elif 4 <= option <= 5 or option == 1:
                operation[option - 1](my_calender)
            else:
                operation[option - 1](my_calender)
                break
        else:
            print("wrong number! try again!")
    else:
        print("Please enter a number! try again!")
