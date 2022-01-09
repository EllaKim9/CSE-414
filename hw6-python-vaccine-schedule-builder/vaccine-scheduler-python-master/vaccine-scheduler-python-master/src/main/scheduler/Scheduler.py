import sys
from model.Vaccine import Vaccine
from model.Caregiver import Caregiver
from model.Patient import Patient
from util.Util import Util
from db.ConnectionManager import ConnectionManager
import pymssql
import datetime
import random

'''
objects to keep track of the currently logged-in user
Note: it is always true that at most one of currentCaregiver and currentPatient is not null
        since only one user can be logged-in at a time
'''
current_patient = None

current_caregiver = None


def create_patient(tokens):
    # create_patient <username> <password>
    # check 1: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Please try again!")
        return

    username = str(tokens[1]).lower()
    password = tokens[2]
    # check 2: check if the username has been taken already
    if username_exists_patient(username):
        print("Username taken, try again!")
        return

    # check 3: check if password fits criteria
    if not check_password(password):
        print("Try a different password!")
        return

    salt = Util.generate_salt()
    hash = Util.generate_hash(password, salt)

    # create the patient
    try:
        patient = Patient(username, salt=salt, hash=hash)
        # save to caregiver information to our database
        try:
            patient.save_to_db()
        except:
            print("Create failed, Cannot save")
            return
        print(" *** Account created successfully *** ")
    except pymssql.Error:
        print("Create failed")
        return
    pass


def check_password(password):
    works = False
    has_upper = False
    has_lower = False
    has_number = False
    has_letter = False
    has_spec_ch = False
    has_long = False
    if len(password) < 8:
        print("Password is not at least 8 characters!")
    else:
        has_long = True
    for letter in password:
        if has_upper and has_lower and has_number:
            break
        if letter.isupper():
            has_upper = True
            has_letter = True
        if letter.islower():
            has_lower = True
            has_letter = True
        if letter.isnumeric():
            has_number = True
    special_chars = ["!", "@", "#", "?"]
    if not any(special_char in password for special_char in special_chars):
        print("Password does not have at least one special character (\"!\", \"@\", \"#\", or \"?\")!")
    else:
        has_spec_ch = True
    if not has_upper or not has_lower:
        print("Password does not have a mixture of uppercase and lowercase letters!")
    if not has_number or not has_letter:
        print("Password does not have a mixture of letters and numbers!")
    if has_upper and has_lower and has_number and has_letter and has_spec_ch and has_long:
        works = True
    return works


def username_exists_patient(username):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_username = "SELECT * FROM Patients WHERE UsernameP = %s"
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(select_username, username)
        #  returns false if the cursor is not before the first record or if there are no rows in the ResultSet.
        for row in cursor:
            return row['UsernameP'] is not None
    except pymssql.Error:
        print("Error occurred when checking username")
        cm.close_connection()
    cm.close_connection()
    return False


def create_caregiver(tokens):
    # create_caregiver <username> <password>
    # check 1: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Please try again!")
        return

    username = str(tokens[1]).lower()
    password = tokens[2]
    # check 2: check if the username has been taken already
    if username_exists_caregiver(username):
        print("Username taken, try again!")
        return

    # check 3: check if password fits criteria
    if not check_password(password):
        print("Try a different password!")
        return

    salt = Util.generate_salt()
    hash = Util.generate_hash(password, salt)

    # create the caregiver
    try:
        caregiver = Caregiver(username, salt=salt, hash=hash)
        # save to caregiver information to our database
        try:
            caregiver.save_to_db()
        except:
            print("Create failed, Cannot save")
            return
        print(" *** Account created successfully *** ")
    except pymssql.Error:
        print("Create failed")
        return


def username_exists_caregiver(username):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_username = "SELECT * FROM Caregivers WHERE UsernameC = %s"
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(select_username, username)
        #  returns false if the cursor is not before the first record or if there are no rows in the ResultSet.
        for row in cursor:
            return row['UsernameC'] is not None
    except pymssql.Error:
        print("Error occurred when checking username")
        cm.close_connection()
    cm.close_connection()
    return False


def login_patient(tokens):
    # login_patient <username> <password>
    # check 1: if someone's already logged-in, they need to log out first
    global current_patient
    if current_patient is not None or current_caregiver is not None:
        print("Already logged-in!")
        return

    # check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Please try again!")
        return

    username = str(tokens[1]).lower()
    password = tokens[2]

    patient = None
    try:
        try:
            patient = Patient(username, password=password).get()
        except:
            print("Get Failed")
            return
    except pymssql.Error:
        print("Error occurred when logging in")

    # check if the login was successful
    if patient is None:
        print("Please try again!")
    else:
        print("Patient logged in as: " + username)
        current_patient = patient


def login_caregiver(tokens):
    # login_caregiver <username> <password>
    # check 1: if someone's already logged-in, they need to log out first
    global current_caregiver
    if current_caregiver is not None or current_patient is not None:
        print("Already logged-in!")
        return

    # check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Please try again!")
        return

    username = str(tokens[1]).lower()
    password = tokens[2]

    caregiver = None
    try:
        try:
            caregiver = Caregiver(username, password=password).get()
        except:
            print("Get Failed")
            return
    except pymssql.Error:
        print("Error occurred when logging in")

    # check if the login was successful
    if caregiver is None:
        print("Please try again!")
    else:
        print("Caregiver logged in as: " + username)
        current_caregiver = caregiver


def search_caregiver_schedule(tokens):
    # search_caregiver_schedule <date>
    # check 1: do not check logged in, as I think it's reasonable to not be logged and to just check for openings

    # check 2: the length for tokens need to be exactly 2 to include all information (with the operation name)
    if len(tokens) != 2:
        print("Please try again!")
        return

    # check 3: valid date
    date = tokens[1]
    d = check_date(date)
    if d is None:
        return

    cm = ConnectionManager()
    conn = cm.create_connection()
    select_schedule = "SELECT UsernameC as username FROM Availabilities as a WHERE a.Time = %s"
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(select_schedule, d)

        result = cursor.fetchall()
        cm.close_connection()
        if result:
            print("Available caregivers:")
            for x in result:
                key = list(x.keys())[0]
                print(x.get(key))
            # now get vaccine availability
            conn1 = cm.create_connection()
            check_vaccines = "SELECT * FROM Vaccines"
            try:
                cursor1 = conn1.cursor(as_dict=True)
                cursor1.execute(check_vaccines)

                result1 = cursor1.fetchall()
                cm.close_connection()
                if result1:
                    print("Vaccines and their current stock count:")
                    for x in result1:
                        vaccine_name = list(x.keys())[0]
                        count = list(x.keys())[1]
                        print(x.get(vaccine_name), ': ', x.get(count))
                else:
                    print("Although caregivers are available, no vaccines are available at this time")
            except pymssql.Error:
                print("Error occurred when checking vaccines")
                cm.close_connection()
        else:
            print("There is no available caregivers on this date, please try a different date")
    except pymssql.Error:
        print("Error occurred when searching schedule")
        cm.close_connection()


# I know this has a lot of repetition of code from getting the schedule, I will go back and make it less lengthy when
# I have the time
def reserve(tokens):
    # reserve <date> <vaccine>
    # check 1: if caregiver is logged-in, they need to log out
    global current_caregiver
    if current_caregiver is not None:
        print("Appointments are for patients only, logout and sign-in as a patient")
        return

    # check 2: if no one is signed-in, ask for patient sign-in
    global current_patient
    if current_patient is None and current_caregiver is None:
        print("Patients must sign-in to reserve a vaccine appointment, please sign-in")
        return

    # check 3: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Please try again!")
        return

    # check 3: valid date
    date = tokens[1]
    d = check_date(date)
    if d is None:
        return

    app_id = 0
    vaccine_name = str(tokens[2]).lower()
    result = get_caregiver_avail_reserve(d)
    if result:
        username_patient = current_patient.get_username()
        index = random.randint(0, len(result) - 1)
        key = list(result[index].keys())[0]
        username_caregiver = result[index].get(key)
        cm = ConnectionManager()
        conn = cm.create_connection()
        check_vaccines = "SELECT * FROM Vaccines as v WHERE v.Name = %s"
        try:
            cursor = conn.cursor(as_dict=True)
            cursor.execute(check_vaccines, vaccine_name)

            result1 = cursor.fetchall()
            if result1:
                count = result1[0].get(list(result1[0].keys())[1])
                cm.close_connection()
                # check if there is no vaccines available
                if count <= 0:
                    print("Caregiver(s) available, but cannot make appointment with desired vaccine: out of stock")
                    return
                else:
                    try:
                        vaccine = Vaccine(vaccine_name, count).get()
                        if vaccine is not None:
                            try:
                                vaccine.decrease_available_doses(int(1))
                                conn1 = cm.create_connection()
                                check_num_app = "SELECT COUNT(*) FROM Appointments"
                                try:
                                    cursor1 = conn1.cursor()
                                    cursor1.execute(check_num_app)
                                    result2 = cursor1.fetchall()
                                    cm.close_connection()
                                    if result2:
                                        # check 4: to see if there are already appointments made on same date
                                        if test_already_app(d):
                                            print("Already have an appointment reserved for this date!")
                                            return
                                        else:
                                            app_id = int(result2[0][0]) + 10000001
                                            conn4 = cm.create_connection()
                                            delete_care_avail = '''DELETE FROM Availabilities WHERE Time = %s AND ''' \
                                                                '''UsernameC = %s'''
                                            try:
                                                cursor4 = conn4.cursor()
                                                cursor4.execute(delete_care_avail, (d, username_caregiver))
                                                conn4.commit()
                                                conn5 = cm.create_connection()
                                                cursor5 = conn5.cursor(as_dict=True)
                                                add_app = "INSERT INTO Appointments VALUES (%d, %s, %s, %s, %s)"
                                                try:
                                                    cursor5.execute(add_app, (int(app_id), username_patient,
                                                                              username_caregiver, vaccine_name,
                                                                              d))
                                                    conn5.commit()
                                                except pymssql.Error as db_err:
                                                    print("Error occurred when inserting Appointments")
                                            except pymssql.Error:
                                                print("Error occurred when deleting caregiver from availability")
                                                cm.close_connection()
                                    else:
                                        print("Although caregivers are available, no vaccines are available at this "
                                              "time")
                                except pymssql.Error:
                                    print("Error occurred when checking number of appointments")
                                    cm.close_connection()
                                print("Appointment Created!")
                                print("Assigned Caregiver: ", username_caregiver)
                                print("Appointment ID: ", app_id)
                            except:
                                print("Failed to decrease available doses!")
                                return
                    except:
                        print("Failed to get Vaccine")
                        return
            else:
                print(
                    "Caregiver(s) available, but cannot make appointment with desired vaccine: does not exist/out of "
                    "stock")
                return
        except pymssql.Error:
            print("Error occurred when checking vaccines")
            cm.close_connection()
    else:
        print("There is no caregivers available on this date, use search_caregiver_schedule to find a valid date")


def get_caregiver_avail_reserve(d):
    cm = ConnectionManager()
    conn = cm.create_connection()

    select_schedule = "SELECT UsernameC as username FROM Availabilities as a WHERE a.Time = %s"
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(select_schedule, d)

        result = cursor.fetchall()
        return result
    except pymssql.Error:
        print("Error occurred when searching schedule availabilities")
        cm.close_connection()
    cm.close_connection()
    return []


def test_already_app(date):
    global current_patient
    cm = ConnectionManager()
    conn = cm.create_connection()
    check_app = "SELECT UsernameP FROM Appointments as a WHERE a.Time = %s"
    try:
        cursor = conn.cursor(as_dict=True)
        cursor.execute(check_app, date)
        result = cursor.fetchall()
        cm.close_connection()
        if result:
            for x in result:
                key = list(x.keys())[0]
                if x.get(key) == current_patient.get_username():
                    return True
            return False
        else:
            return False
    except pymssql.Error:
        print("Error occurred when checking vaccines")
        cm.close_connection()


def upload_availability(tokens):
    #  upload_availability <date>
    #  check 1: check if the current logged-in user is a caregiver
    global current_caregiver
    if current_caregiver is None:
        print("Please login as a caregiver first!")
        return

    # check 2: the length for tokens need to be exactly 2 to include all information (with the operation name)
    if len(tokens) != 2:
        print("Please try again!")
        return

    # check 3: valid date
    date = tokens[1]
    d = check_date(date)
    if d is None:
        return

    # check 4: check if caregiver is in list of dates already available
    cm = ConnectionManager()
    conn = cm.create_connection()
    cursor = conn.cursor(as_dict=True)
    check_already_avail = "SELECT UsernameC as username FROM Availabilities as a WHERE a.Time = %s"
    try:
        cursor.execute(check_already_avail, d)

        result = cursor.fetchall()
        cm.close_connection()

        is_avail = True
        if result:
            for x in result:
                key = list(x.keys())[0]
                if x.get(key) == current_caregiver.get_username():
                    print("You already uploaded availability for this day!")
                    return
        # end of check 4
        if is_avail:
            # check 5: check if caregiver already has an appointment
            conn1 = cm.create_connection()
            cursor1 = conn1.cursor(as_dict=True)

            check_already_avail = "SELECT UsernameC as username FROM Appointments as a WHERE a.Time = %s"
            try:
                cursor1.execute(check_already_avail, d)

                result1 = cursor1.fetchall()
                cm.close_connection()
                no_app = True
                if result1:
                    for x in result1:
                        key = list(x.keys())[0]
                        if x.get(key) == current_caregiver.get_username():
                            print("You already have an appointment for this day!")
                            return
                # end of check 5
                if no_app:
                    try:
                        current_caregiver.upload_availability(d)
                    except:
                        print("Upload Availability Failed")
                    print("Availability uploaded!")
            except pymssql.Error:
                print("Error occurred when uploading availability")
    except pymssql.Error:
        print("Error occurred when checking availability")


def check_date(date):
    # assume input is hyphenated in the format mm-dd-yyyy
    date_tokens = date.split("-")
    if len(date_tokens) != 3:
        print("Please enter a valid date!")
        return
    month = int(date_tokens[0])
    day = int(date_tokens[1])
    year = int(date_tokens[2])
    d = None

    try:
        d = datetime.datetime(year, month, day)
        if d >= datetime.datetime.now():
            return d
        else:
            print("Date entered is in the past!")
            return None
    except ValueError:
        # assume always in format, does not catch invalid dates/throws error
        print("Please enter a valid date!")
        return d


def cancel(tokens):
    """
    TODO: Extra Credit
    """
    pass


def add_doses(tokens):
    #  add_doses <vaccine> <number>
    #  check 1: check if the current logged-in user is a caregiver
    global current_caregiver
    if current_caregiver is None:
        print("Please login as a caregiver first!")
        return

    #  check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
    if len(tokens) != 3:
        print("Please try again!")
        return

    vaccine_name = str(tokens[1]).lower()
    doses = int(tokens[2])
    vaccine = None
    try:
        try:
            vaccine = Vaccine(vaccine_name, doses).get()
        except:
            print("Failed to get Vaccine!")
            return
    except pymssql.Error:
        print("Error occurred when adding doses")

    # check 3: if getter returns null, it means that we need to create the vaccine and insert it into the Vaccines
    #          table

    if vaccine is None:
        try:
            vaccine = Vaccine(vaccine_name, doses)
            try:
                vaccine.save_to_db()
            except:
                print("Failed To Save")
                return
        except pymssql.Error:
            print("Error occurred when adding doses")
    else:
        # if the vaccine is not null, meaning that the vaccine already exists in table
        try:
            try:
                vaccine.increase_available_doses(doses)
            except:
                print("Failed to increase available doses!")
                return
        except pymssql.Error:
            print("Error occurred when adding doses")

    print("Doses updated!")


def show_appointments(tokens):
    # show_appointments
    # check 1: if no one is signed-in, ask for patient sign-in
    global current_patient
    global current_caregiver
    if current_patient is None and current_caregiver is None:
        print("You must sign-in to show confirmed appointments, please sign-in first!")
        return

    # check 2: the length for tokens need to be exactly 1 to include all information (with the operation name)
    if len(tokens) != 1:
        print("Please try again!")
        return

    cm = ConnectionManager()
    conn = cm.create_connection()
    check_app = None
    if current_patient is not None:
        check_app = "SELECT * FROM Appointments as a WHERE a.usernameP = %s"
    else:
        check_app = "SELECT * FROM Appointments as a WHERE a.usernameC = %s"
    cursor = conn.cursor(as_dict=True)
    try:
        if current_patient is not None:
            cursor.execute(check_app, current_patient.get_username())
        else:
            cursor.execute(check_app, current_caregiver.get_username())
        result = cursor.fetchall()
        cm.close_connection()
        if result:
            print("Scheduled appointments:")
            counter = 0
            for x in result:
                print("Appointment #" + str(counter+1))
                print("Appointment ID: ", end=""),
                key1 = list(x.keys())[0]
                print(str(x.get(key1)) + ", ", end=""),
                if current_patient is None:
                    print("Patient Name: ", end=""),
                    key3 = list(x.keys())[1]
                    print(x.get(key3) + ", ", end=""),
                else:
                    print("Caregiver Name: ", end=""),
                    key3 = list(x.keys())[2]
                    print(x.get(key3) + ", ", end=""),
                print("Date: ", end=""),
                key3 = list(x.keys())[4]
                print(str(x.get(key3)) + ", ", end=""),
                print("Vaccine Name: ", end=""),
                key2 = list(x.keys())[3]
                print(x.get(key2)),
                counter += 1
        else:
            print("There are no appointments scheduled!")
            return
    except pymssql.Error:
        print("Error occurred when checking appointments")
        cm.close_connection()


def logout(tokens):
    # login_caregiver <username> <password>
    # check 1: if no one is logged-in, they need to log-in first
    global current_caregiver
    global current_patient
    if current_caregiver is None and current_patient is None:
        print("Log-in to log-out!")
        return

    # check 2: the length for tokens need to be exactly 1 to include all information (only the operation name)
    if len(tokens) != 1:
        print("Please try again!")
        return

    current_caregiver = None
    current_patient = None

    print("Successfully logged-out!")


def start():
    stop = False
    while not stop:
        print()
        print(" *** Please enter one of the following commands *** ")
        print("> create_patient <username> <password>")  # //TODO: implement create_patient (Part 1)
        print("> create_caregiver <username> <password>")
        print("> login_patient <username> <password>")  # // TODO: implement login_patient (Part 1)
        print("> login_caregiver <username> <password>")
        print("> search_caregiver_schedule <date>")  # // TODO: implement search_caregiver_schedule (Part 2)
        print("> reserve <date> <vaccine>")  # // TODO: implement reserve (Part 2)
        print("> upload_availability <date>")
        print("> cancel <appointment_id>")  # // TODO: implement cancel (extra credit)
        print("> add_doses <vaccine> <number>")
        print("> show_appointments")  # // TODO: implement show_appointments (Part 2)
        print("> logout")  # // TODO: implement logout (Part 2)
        print("> Quit")
        print()
        response = ""
        print("> Enter: ", end='')

        try:
            response = str(input())
        except ValueError:
            print("Type in a valid argument")
            break

        tokens = response.split(" ")
        if len(tokens) == 0:
            ValueError("Try Again")
            continue
        operation = tokens[0].lower()
        if operation == "create_patient":
            create_patient(tokens)
        elif operation == "create_caregiver":
            create_caregiver(tokens)
        elif operation == "login_patient":
            login_patient(tokens)
        elif operation == "login_caregiver":
            login_caregiver(tokens)
        elif operation == "search_caregiver_schedule":
            search_caregiver_schedule(tokens)
        elif operation == "reserve":
            reserve(tokens)
        elif operation == "upload_availability":
            upload_availability(tokens)
        elif operation == cancel:
            cancel(tokens)
        elif operation == "add_doses":
            add_doses(tokens)
        elif operation == "show_appointments":
            show_appointments(tokens)
        elif operation == "logout":
            logout(tokens)
        elif operation == "quit":
            print("Thank you for using the scheduler, Goodbye!")
            stop = True
        else:
            print("Invalid Argument")


if __name__ == "__main__":
    '''
    // pre-define the three types of authorized vaccines
    // note: it's a poor practice to hard-code these values, but we will do this ]
    // for the simplicity of this assignment
    // and then construct a map of vaccineName -> vaccineObject
    '''

    # start command line
    print()
    print("Welcome to the COVID-19 Vaccine Reservation Scheduling Application!")

    start()
