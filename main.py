import func
import mysql.connector

db = mysql.connector.connect(
    host="100.25.245.120",
    user="hitech_boot",
    passwd="Ht=123456789",
    database="python_tries"
)

mycursor = db.cursor()
menu = \
    "1. Show all upcoming events\n" \
    "2. Add new event by path\n" \
    "3. Delete event by event ID\n" \
    "4. Exit"

my_calender = func.Calender(db, mycursor)

operation = [
    func.Calender.show_events,
    func.Calender.add_event,
    func.Calender.remove_event,
    func.Calender.save_and_exit
]

while True:
    print("\nchoose operation:")
    print(menu)
    option = input("option: ")
    option = int(option)
    if 1 <= option <= 4:
        if 1 <= option <= 3:
            operation[option - 1](my_calender, db,mycursor)
        else:
            operation[option - 1](my_calender)
            break
    else:
        print("wrong number! try again!")
