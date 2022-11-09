"""made by ohad borenstein"""
import datetime


# 6th action!
def change_table(my_calender, db):
    try:
        table_name = str(input("Please insert the name of the table \n"
                               "that you would like to work with: "))
        mycursor = create_data_base(db, table_name)
        print("Table " + table_name + " is new.\nCreating new table.")
    except:
        mycursor = db.cursor()
    finally:
        return Calender(db, table_name)


def create_data_base(db, table_name):
    mycursor = db.cursor()
    mycursor.execute(f"CREATE TABLE {table_name}("
                     "Event_id varchar(128) PRIMARY KEY,"
                     "Client_name varchar(128),"
                     "Event_name varchar(128),"
                     "Date varchar(12),"
                     "Guests_num varchar(128));")
    return mycursor


def orginize_name(string):
    string = string.replace(" ", "")
    string = string.replace("\n", "")
    string = string.lower()
    string = string.replace(" ", "")
    string = string.replace("  ", "")
    return string


def insert_event_into_mysql(my_event, db, calender_name):
    mycursor = db.cursor()
    mycursor.execute(f"insert into {calender_name}(Event_id,Client_name,Event_name,Date,Guests_num) "
                     f"values("
                     f"'{my_event.Event_id}',"
                     f"'{my_event.Client_name}',"
                     f"'{my_event.Event_name}',"
                     f"'{my_event.Date}',"
                     f"'{my_event.Guests_num}')")
    db.commit()


def delete_event_from_mysql(event_id, db, calender_name):
    mycursor = db.cursor()
    mycursor.execute(f"DELETE FROM {calender_name} WHERE Event_id = '{event_id}'")
    db.commit()


def create_calander(my_calander, db, table_name):
    mycursor = db.cursor()
    mycursor.execute(f"select * from {table_name}")
    result = mycursor.fetchall()
    for event_obj in range(len(result)):
        new_event = list(result[event_obj])
        new_event = Event("", new_event)
        my_calander.event_list.append(new_event)


class Calender(object):
    # creates the Calander so the users will understand what is in front of him!
    def __init__(self, db, table_name):
        self.Calender_name = table_name
        self.event_list = []
        create_calander(self, db, table_name)

    # 1st action!
    def show_events(self):
        print("In table: " + self.Calender_name)
        for i in self.event_list:
            print(i.to_string())
        if len(self.event_list) == 0:
            print("No up coming events!")

    # 2nd action!
    def add_event(self, db):
        mycursor = db.cursor()
        path = input("please enter the path of the event file: ")
        my_event = Event(path, None)
        is_new_event = True
        if not my_event.valid_event():
            is_new_event = False
            print("the event is unavailable to be created!")

        for event in self.event_list:
            if event.Event_id == my_event.Event_id:
                is_new_event = False
                print("event is already exist!")

        if is_new_event:
            try:
                insert_event_into_mysql(my_event, db, self.Calender_name)
                self.event_list += [my_event]
                print("event added successfully to table: " + self.Calender_name)
            except:
                db.rollback()
                print("didnt work!")

    # 3rd action!
    def remove_event(self, db):
        mycursor = db.cursor()
        event_id = input("Please enter the ID of the event to delete: ")
        found = False
        for event in self.event_list:
            if event.Event_id == event_id:
                try:
                    delete_event_from_mysql(event_id, db, self.Calender_name)
                    found = True
                    self.event_list.remove(event)
                    print("Event deleted successfully from table: " + self.Calender_name)
                except:
                    db.rollback()
                    print("something went wrong...")
        if found == False:
            print("No such event with the given ID. ")

    # 4th action!
    def get_first_event(self):
        if len(self.event_list) == 0:
            self.show_events()
        else:
            up_coming_event = self.event_list[0]
            for event in self.event_list:
                if event.Date <= up_coming_event.Date:
                    up_coming_event = event
            print("In table: " + self.Calender_name + " the up coming event is: \n", up_coming_event.to_string())

    # 5th action!
    def get_events_by_name(self):
        client = str(input("please insert the name of the client: \n"))
        print(client + "'s events are:")
        client = orginize_name(client)
        for event in self.event_list:
            if orginize_name(event.Client_name) == client:
                print(event.to_string())

    # 7th action!
    def save_and_exit(self):  # event_list,db, path):
        f = open("events_for_date", 'a')
        my_date = datetime.datetime.now()
        f.write(
            "\nThe date: " + str(my_date.date()) + ".\n" +
            "Last table been in mysql: " + str(self.Calender_name) + "\n"
            "number of the events: " + str(
            len(self.event_list)) + "\n"
            + "_____________________")
        print("Good Bye! all saved.")


class Event(object):

    def __init__(self, path, event_detail):
        if event_detail is not None:
            self.Event_id, self.Client_name, self.Event_name, self.Date, self.Guests_num = event_detail
        else:
            try:
                f = open(path, 'r')
                for line in f:
                    cur_line = line
                    cur_line = cur_line.replace("\n", "")
                    line = orginize_name(line)

                    if line[0: len("eventid:")] == "eventid:":
                        id = line[line.find(":") + 1: len(line)]
                        if id.isdigit():
                            self.Event_id = id
                        else:
                            self.Event_id = None

                    if line[0:len("clientname:")] == "clientname:":
                        if cur_line[cur_line.find(":") + 1:len(cur_line)] != "":
                            self.Client_name = cur_line[cur_line.find(":") + 1:len(cur_line)]
                        else:
                            self.Client_name = None

                    if line[0:len("eventname:")] == "eventname:":
                        if cur_line[cur_line.find(":") + 1: len(cur_line)] != "":
                            self.Event_name = cur_line[cur_line.find(":") + 1: len(cur_line)]
                        else:
                            self.Event_name = None

                    if line[0:len("date:")] == "date:":
                        date_string = str(line[len("date:"):len(line)])
                        day, month, year = date_string.split('/')

                        foundDate = False
                        try:
                            datetime.datetime(int(year), int(month), int(day))
                            foundDate = True
                        except:
                            foundDate = False

                        if foundDate:
                            self.Date = date_string
                        else:
                            self.Date = None

                    if line[0:len("numberofguests:")] == "numberofguests:":
                        guests_num = line[line.find(":") + 1: len(line)]
                        if guests_num.isdigit():
                            self.Guests_num = guests_num
                        else:
                            self.Guests_num = None
            except:
                self.Event_id = None
                print("something went wrong.. check your file!")

    def valid_event(my_event):
        if my_event.Event_id is None or \
                my_event.Guests_num is None or \
                my_event.Client_name is None or \
                my_event.Event_name is None:
            return False
        else:
            return True

    def to_string(self):
        return "\n" \
               "Event ID: " + str(self.Event_id) + "\n" + \
               "Client name: " + str(self.Client_name) + "\n" + \
               "Event name: " + str(self.Event_name) + "\n" + \
               "Date: " + str(self.Date) + "\n" + \
               "Number of guests: " + str(self.Guests_num)
