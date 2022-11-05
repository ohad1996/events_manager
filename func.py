import mysql.connector
import datetime


def create_data_base(db, myconsur):
    db = mysql.connector.connect(
        host="100.25.245.120",
        user="hitech_boot",
        passwd="Ht=123456789",
        database="python_tries"
    )

    mycursor = db.cursor()
    mycursor.execute("CREATE TABLE ohad_manager_new("
                     "Event_id varchar(128) PRIMARY KEY,"
                     "Client_name varchar(128),"
                     "Event_name varchar(128),"
                     "Date varchar(12),"
                     "Guests_num varchar(128));")
    return mycursor


class Calender(object):
    #creates the Calander so the users will understand what is in front of him!
    def __init__(self, db, mycursor):
        self.event_list = []
        mycursor.execute("select * from ohad_manager_new")
        result = mycursor.fetchall()
        for event_obj in range(len(result)):
            new_event = list(result[event_obj])
            new_event = Event("",new_event)
            self.event_list.append(new_event)

    # 1st action!
    def show_events(self, db, mycursor):
        for i in self.event_list:
            print(i.to_string())

    # 2nd action!
    def add_event(self, db,mycursor):
        path = input("please enter the path of the event file: ")

        my_event = Event(path,None)
        is_new_event = True
        if my_event.Event_id is None or \
                my_event.Guests_num is None or \
                my_event.Client_name is None or \
                my_event.Event_name is None:
            is_new_event = False

        for event in self.event_list:
            if event.Event_id == my_event.Event_id:
                is_new_event = False

        if is_new_event:
            try:
                mycursor.execute(f"insert into ohad_manager_new(Event_id,Client_name,Event_name,Date,Guests_num) "
                                 f"values("
                                 f"'{my_event.Event_id}',"
                                 f"'{my_event.Client_name}',"
                                 f"'{my_event.Event_name}',"
                                 f"'{my_event.Date}',"
                                 f"'{my_event.Guests_num}')")
                db.commit()
                self.event_list += [my_event]
                print("event added successfully")
            except:
                db.rollback()
                print("didnt work!")
        else:
            print("event is already exist or the event is invalid!")

    # 3rd action!
    def remove_event(self, db,mycursor):
        event_id = input("Please enter the ID of the event to delete: ")
        found = False
        for event in self.event_list:
            if event.Event_id == event_id:
                try:
                    mycursor.execute(f"DELETE FROM ohad_manager_new WHERE Event_id = '{event_id}'")
                    db.commit()
                    print("Event deleted successfully")
                    found = True
                    self.event_list.remove(event)
                except:
                    db.rollback()
                    print("something went wrong...")
        if found == False:
            print("No such event with the given ID. ")

    # 4th action!
    def save_and_exit(self):  # event_list,db, path):
        f = open("events_for_date", 'w')
        my_date = datetime.datetime.now()
        f.write("The date: " + str(my_date.date()) + ".\n" + "number of the events: " + str(len(self.event_list)) + ".")
        print("Good Bye! all saved.")


class Event(object):

    def __init__(self, path,event_detail):
        if event_detail is not None:
            self.Event_id = event_detail[0]
            self.Client_name = event_detail[1]
            self.Event_name = event_detail[2]
            self.Date = event_detail[3]
            self.Guests_num = event_detail[4]
        else:
            try:
                f = open(path, 'r')
                for line in f:
                    cur_line = line
                    cur_line = cur_line.replace("\n", "")
                    line = line.replace("\n", "")
                    line = line.lower()
                    line = line.replace(" ", "")
                    line = line.replace("  ", "")

                    if line[0: len("eventid:")] == "eventid:":
                        id = line[line.find(":") + 1: len(line)]
                        if id.isdigit():
                            self.Event_id = id

                    if line[0:len("clientname:")] == "clientname:":
                        self.Client_name = cur_line[cur_line.find(":") + 1:len(cur_line)]

                    if line[0:len("eventname:")] == "eventname:":
                        self.Event_name = cur_line[cur_line.find(":") + 1: len(cur_line)]

                    if line[0:len("date:")] == "date:":
                        date_string = str(line[len("date:"):len(line)])
                        day, month, year = date_string.split('/')

                        foundDate = False
                        isValidDate = True
                        try:
                            datetime.datetime(int(year), int(month), int(day))
                            foundDate = True
                        except ValueError:
                            isValidDate = False

                        if foundDate:
                            self.Date = date_string

                    if line[0:len("numberofguests:")] == "numberofguests:":
                        guests_num = line[line.find(":") + 1: len(line)]
                        if guests_num.isdigit():
                            self.Guests_num = guests_num
            except:
                print("something went wrong.. check your file!")

    def to_string(self):
        return "\n" \
               "Event ID: " + str(self.Event_id) + "\n" + \
               "Client name: " + str(self.Client_name) + "\n" + \
               "Event name: " + str(self.Event_name) + "\n" + \
               "Date: " + str(self.Date) + "\n" + \
               "Number of guests: " + str(self.Guests_num)
