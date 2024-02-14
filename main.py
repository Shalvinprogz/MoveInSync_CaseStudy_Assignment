import mysql.connector
import main_screen


def check_internet():
    try:
        connection = mysql.connector.connect(
        host="sql6.freesqldatabase.com",
        user="sql6683891",
        password="YG7kNqGqH2",
        database="sql6683891"
        )
        return True
    except:
        return False

# Objective 2
room_details = [
    {"name": "Meeting Room 1", "capacity": 110, "status": "N"},
    {"name": "Meeting Room 2", "capacity": 80, "status": "N"},
    {"name": "Meeting Room 3", "capacity": 250, "status": "N"},
    {"name": "Meeting Room 4", "capacity": 50, "status": "N"},
    {"name": "Discussion Room 1", "capacity": 20, "status": "N"},
    {"name": "Discussion Room 2", "capacity": 20, "status": "N"}
    # Add more dictionaries for additional rooms
]
changes_made = {"room booking" : {"meeting room" : [], "discussion room" : []}, "allot" : []}


def allot_seats(cursor, connection, name):
    
    for i in changes_made:
        t = i["room booking"]
        if t["meeting room"]:
            for j in t["meeting room"]:
                print(j)
        if t["discussion room"]:
            for j in t["discussion room"]:
                print(j)

    x = int(input())

    # tmp = result[x - 1][0]
    # if '1' in tmp and "Meeting" in tmp:
    #     do_meeting("meeting_room_1", cursor, connection, "Meeting Room 1", name)
    # elif '2' in tmp and "Meeting" in tmp:
    #     do_meeting("meeting_room_2", cursor, connection, "Meeting Room 2", name)
    # elif '3' in tmp and "Meeting" in tmp:
    #     do_meeting("meeting_room_3", cursor, connection, "Meeting Room 3", name)
    # elif '4' in tmp and "Meeting" in tmp:
    #     do_meeting("meeting_room_4", cursor, connection, "Meeting Room 4", name)
    # elif '1' in tmp and "Discussion" in tmp:
    #     do_meeting("discussion_room_1", cursor, connection, "Discussion Room 1", name)
    # elif '2' in tmp and "Discussion" in tmp:
    #     do_meeting("discussion_room_2", cursor, connection, "Discussion Room 2", name)

def book_discussion_room():
    n = int(input("Enter the number of participants for the meeting: "))
    print("Fetching the available rooms for your meeting")

    availableRooms = []
    for i in room_details:
        if "Discussion" in i["name"]:
            if i["capacity"] >= n:
                availableRooms.append(i)
                print(i["name"], "Capacity", i["capacity"])

    print("Enter 0 to go back")
    x = int(input("Enter the room you want to book : "))
    if x == 0:
        mainScreen()
    else:
        if x > 0 and x <= len(availableRooms):
            changes_made["room booking"]["discussion room"].append(availableRooms[x - 1]["name"])

            print("Your room has been Booked Successfully")
            # print(changes_made)
        else:
            print("Invalid Input")
    print("\n")
    p = input("Try connecting to the internet? y/n")
    if p == 'y':
        print("\n")
        print("Fetching details...")
        if check_internet():
            online(sync_files=changes_made)
        else:
            print("\n")
            print(" Uh ooh...there is no internet connection")
            mainScreen()

def book_meeting_room():
    n = int(input("Enter the number of participants for the meeting: "))
    print("Fetching the available rooms for your meeting")

    availableRooms = []
    for i in room_details:
        if "Meeting" in i["name"]:
            if i["capacity"] >= n:
                availableRooms.append(i)
                print(i["name"], "Capacity", i["capacity"])

    print("Enter 0 to go back")
    x = int(input("Enter the room you want to book : "))
    if x == 0:
        mainScreen()
    else:
        if x > 0 and x <= len(availableRooms):
            changes_made["room booking"]["meeting room"].append(availableRooms[x - 1]["name"])

            print("Your room has been Booked Successfully")
            # print(changes_made)
        else:
            print("Invalid Input")
    p = input("Try connecting to the internet? y/n")
    if p == 'y':
        print("\n")
        print("Fetching details...")
        if check_internet():
            online(sync_files=changes_made)
        else:
            print("\n")
            print(" Uh ooh...there is no internet connection")
            mainScreen()

def book_room():
    print("Choose the room type you want to book: ")
    print("1. Meeting room")
    print("2. Discussion room")
    print("3. Go back")
    k = int(input())
    if k == 1:
        book_meeting_room()
    elif k == 2:
        book_discussion_room()
    elif k == 3:
        mainScreen()

def mainScreen():
    print("--------------Main Screen--------------")
    print(" 1. Make a room booking")
    print(" 2. Allot seats for Booked rooms -- feature coming soon")
    print(" 3. Exit")
    print(" 4. Try connecting to the internet ? (y/n) : ")
    print( "You are in offline mode, connect to the internet")

    x = input()
    try :
        c = int(x)
        if c == 1:
            book_room()
        elif c == 3:
            return
        else:
            print("Invalid Input")
            mainScreen()
    except:
        if x == 'y':
            if check_internet():
                online(changes_made)
            else:
                print("\n")
                print(" Uh ooh...there is no internet connection")
                print("\n")
                mainScreen()
    

def lock_mutex(cursor, connection):
    lock_query = """update mutex_lock set is_locked = 1"""
    cursor.execute(lock_query)
    connection.commit()

def unlock_mutex(cursor, connection):
    unlock_query = """update mutex_lock set is_locked = 0"""
    cursor.execute(unlock_query)
    connection.commit()

def validate_credentials(username, password):
    # Establishing database connection
    connection = mysql.connector.connect(
        host="sql6.freesqldatabase.com",
        user="sql6683891",
        password="YG7kNqGqH2",
        database="sql6683891"
    )
    
    # Creating a cursor
    cursor = connection.cursor()

    select_query = """
    select password from admin where username = %s
    """
    # fetching password from the server
    cursor.execute(select_query, (username,))
    result = cursor.fetchone()

    cursor.close()
    connection.close()

    # Check if the username exists in the database
    if result:
        if result[0] == password:
            return True
        else:
            return False
    else:
        return False


# Objective 1
def online(sync_files = {}):
    username = input("Enter username: ")
    password = input("Enter password: ")

    if validate_credentials(username, password):
        print("Login successfull.")
        print("\n")
        print("Loading...")
        
        # Establishing database connection again
        try:
            connection = mysql.connector.connect(
                host="sql6.freesqldatabase.com",
                user="sql6683891",
                password="YG7kNqGqH2",
                database="sql6683891"
            )
        # creating a cursor
            cursor = connection.cursor()
            cursor.execute("select name from admin where username = %s", (username, ))
            name = cursor.fetchone()

            # Here I'm implementing a mutex locking mechanism, so that no one can log on to the database interface 
            # at the same time
            # Mutex lock is a table in the database which contains only one element which is is_locked
            # Mutex is initially 0 and whenever somone enters the interface it is changed to 1, so no one can enter 
            # the interface while
            # someone is already inside.
            query = """select is_locked from mutex_lock"""
            
            # checking the mutex
            cursor.execute(query)
            mutex = cursor.fetchone()
            # print(mutex[0])

            while mutex is not None and mutex[0] == 1:
                print("Application is locked. Some other admin is editing the plan...")
                cursor.execute(query)
                mutex = cursor.fetchone()
                connection.commit()

            # If mutex is None, handle error
            if mutex is None:
                print("Unable to get mutex status")
            else:
                main_screen.mainScreen(cursor, connection, name, sync_files)
                
            # unlocking mutex
            unlock_mutex(cursor, connection)
        except mysql.connector.Error as e:
            print("Error : ", e)
        
        # Close cursor and connection
        finally:
            cursor.close()
            connection.close()
    else:
        print("Invalid username or password.")
  
print("Loading...")
if check_internet():
    # cursor = connection.cursor()
    online()
else:
    print("Note : ")
    print("You don't have internet connection, so loading offline database.")
    print("You will need to have an internet connection to synchronise the changes made.")
    print("\n")
    mainScreen()