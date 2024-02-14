# Function to show History of all the changes in the database
def show_history(cursor, connection, name):
    print( "History ")
    cursor.execute("select * from history")
    res = cursor.fetchall()
    for i in res:
        print(i[0])
    x = 0
    while x != "y" and x != "n":
        x = (input("Do you want to go back to main screen ? (y/n) : "))
    if x == "y":
        mainScreen(cursor, connection, name, {})
    else:
        return 
    

#function to allocate emplyees for the booking
def do_meeting(s, cursor, connection, og, name):
    print("Enter 0 to go back")
    n = int(input("How many seats do you want to allocate? "))
    if n == 0:
        mainScreen(cursor, connection, name, {})
    for i in range(n):
        
        # allocating seat for every i'th employeee
        username = input("Enter the username: ")
        query = """update {} set status = 'Y', occupied_by = %s""".format(s)
        cursor.execute(query, (username,))
        connection.commit()

        # adding history 
        query2 = f""" insert into history (event) values ("{og}, has been occupied by {username}") """
        cursor.execute(query2)
        connection.commit()

    # decreasing the seats left in the room_details table
    query1 = """update room_details set size = size - %s where room_name = %s"""
    cursor.execute(query1, (n, og))
    connection.commit()
    print("\n")
    print("Added successfully!!")
    print("\n")

    # Fetch and print remaining seats
    cursor.execute("""select size from room_details where room_name = %s""", (og,))
    result = cursor.fetchone()
    print("Seats remaining:", result[0])

    k = (input("Do you want to go to main screen? (y/n)"))
    if k == 'y':
        mainScreen(cursor, connection, name, {})
    else : 
        print("Bye!")


def book_discussion_room(cursor, connection, name):
    n = int(input("Enter the number of participants for the meeting: "))
    print("\n")
    print("Fetching the available rooms for your meeting")
    print("\n")

    # Objective 3
    # here this query will show only the rooms that are greater than or equals to the size we entered
    query = """
    select room_name, size from room_details where booking_status = "N" and %s <= size and room_name like "Discussion%";
    """
    cursor.execute(query, (n,))
    result = cursor.fetchall()
    print("These are the options available : ")
    for i in range(len(result)):
        print(i + 1, ". ", result[i][0], "capacity : ", result[i][1])

    print("<- GO BACK")
    print("\n")
    x = int(input("Enter the room you want to book : "))
    if x == 0:
        mainScreen(cursor, connection, name, {})
    else:

        if x > 0 and x <= len(result):
            # updating the status
            query1 = """update room_details set booking_status = 'Y' where room_name = %s;"""

            cursor.execute(query1, (result[x - 1][0], ))
            connection.commit()
            print("\n")
            print("Your room has been Booked Successfully")

            #adding history
            query2 = f""" insert into history (event) values ("{result[x-1][0]}, has been booked by {name[0]}") """
            cursor.execute(query2)
            connection.commit()

            print("\n")
            print("log out ? (y/n) : ")
            m = input()
            if m == 'y':
                return
            else:
                mainScreen(cursor, connection, name, {})
        else:
            print("Invalid Input")

def book_discussion_room_offline(cursor, connection, sync_files):
    
    for i in sync_files["room booking"]["discussion room"]:
        query1 = """update room_details set booking_status = 'Y' where room_name = %s;"""

        cursor.execute(query1, (i, ))
        connection.commit()
        print(i)
        query2 = "insert into history (event) values (%s)" 
        values = (f"{i}, has been booked offline",)
        cursor.execute(query2, values)
        connection.commit()


def book_meeting_room(cursor, connection, name):
    n = int(input("Enter the number of participants for the meeting: "))
    print("\n")
    print("Fetching the available rooms for your meeting")
    print("\n")

    # here this query will show only the rooms that are greater than or equals to the size we entered
    query = """
    select room_name, size from room_details where booking_status = "N" and %s <= size;
    """
    cursor.execute(query, (n,))
    result = cursor.fetchall()
    print("These are the options available : ")
    for i in range(len(result)):
        print(i + 1, ". ", result[i][0], "capacity : ", result[i][1])
    print("\n")
    print("<- GO BACK : 0")
    x = int(input("Enter the room you want to book : "))
    if x == 0:
        mainScreen(cursor, connection, name, {})
    else:
        if x > 0 and x <= len(result):
            query1 = """update room_details set booking_status = 'Y' where room_name = %s;"""

            cursor.execute(query1, (result[x - 1][0], ))
            connection.commit()
            print("\n")
            print("Your room has been Booked Successfully")

            query2 = f""" insert into history (event) values ("{result[x-1][0]}, has been booked by {name[0]}") """
            cursor.execute(query2)
            connection.commit()
            print("\n")
            print("log out ? (y/n) : ")
            m = input()
            if m == 'y':
                return
            else:
                mainScreen(cursor, connection, name, {})
        else:
            print("Invalid Input")


def book_meeting_room_offline(cursor, connection, sync_files):
    
    for i in sync_files["room booking"]["meeting room"]:
        query1 = """update room_details set booking_status = 'Y' where room_name = %s;"""

        cursor.execute(query1, (i, ))
        connection.commit()

        query2 = "insert into history (event) values (%s)" 
        values = (f"{i}, has been booked offline",)
        cursor.execute(query2, values)
        connection.commit()
        # print("Your room has been Booked Successfully")

    # query2 = f""" insert into history (event) values ("{result[x-1][0]}, has been booked by {name[0]}") """
    # cursor.execute(query2)
    # connection.commit()

    

def book_room(cursor, connection, name):
    print("\n")
    print("Choose the room type you want to book: ")
    print("1. Meeting room")
    print("2. Discussion room")
    print("3. Go back")
    print("\n")
    k = int(input())
    if k == 1:
        book_meeting_room(cursor, connection, name)
    elif k == 2:
        book_discussion_room(cursor, connection, name)
    elif k == 3:
        mainScreen(cursor, connection, name, {})

def allot_seats(cursor, connection, name):
    # function to allot seats to employees or students
    query = """
    select room_name, size from room_details where booking_status = "Y";
    """
    cursor.execute(query)
    result = cursor.fetchall()
    print("\n")
    print("These are the options available : ")
    for i in range(len(result)):
        print(i + 1, ".","Allot seats for", result[i][0], "capacity left: ", result[i][1])
    print("\n")
    x = int(input())

    # checking whether which room did the user choose
    tmp = result[x - 1][0]
    if '1' in tmp and "Meeting" in tmp:
        do_meeting("meeting_room_1", cursor, connection, "Meeting Room 1", name)
    elif '2' in tmp and "Meeting" in tmp:
        do_meeting("meeting_room_2", cursor, connection, "Meeting Room 2", name)
    elif '3' in tmp and "Meeting" in tmp:
        do_meeting("meeting_room_3", cursor, connection, "Meeting Room 3", name)
    elif '4' in tmp and "Meeting" in tmp:
        do_meeting("meeting_room_4", cursor, connection, "Meeting Room 4", name)
    elif '1' in tmp and "Discussion" in tmp:
        do_meeting("discussion_room_1", cursor, connection, "Discussion Room 1", name)
    elif '2' in tmp and "Discussion" in tmp:
        do_meeting("discussion_room_2", cursor, connection, "Discussion Room 2", name)

def show_all_details(cursor, connection, name):
    query = """select * from room_details"""
    cursor.execute(query)
    result = cursor.fetchall()
    for i in result:
        print(i[0],"|", i[1], "|", "status : ", i[2],"|", "capacity left : ", i[3])
    print("\n")
    x = input("Go back? (y/n) : ")
    if x == 'y':
        mainScreen(cursor, connection, name, {})
    else:
        return


def mainScreen(cursor, connection, name, sync_files):
    if len(sync_files) !=0:
        if len(sync_files["room booking"]["meeting room"]) != 0:
            book_meeting_room_offline(cursor, connection, sync_files)
        if len(sync_files["room booking"]["discussion room"]) != 0:
            book_discussion_room_offline(cursor, connection, sync_files)
        
    # locking the mutex
    lock_query = """UPDATE mutex_lock SET is_locked = 1"""
    cursor.execute(lock_query)
    connection.commit()
    print("\n")
    print("--------------Main Screen--------------")
    print(" 1. Make a room booking")
    print(" 2. Allot seats for Booked rooms")
    print(" 3. Show History")
    print(" 4. Show Room details")
    print(" 5. Exit")

    x = int(input())
    if x == 1:
        book_room(cursor, connection, name)
    elif x == 2:
        allot_seats(cursor, connection, name)
    elif x == 3:
        show_history(cursor, connection, name)
    elif x == 4:
        show_all_details(cursor, connection, name)
    else:
        return 