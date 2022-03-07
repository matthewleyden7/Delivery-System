# Matthew Leyden
# Student ID: 001008459
# Data Structures and Algorithms 2

from datetime import timedelta, datetime
from truck_handling import load_trucks, deliver, total_miles, truck_packages_information, search_package, remove_package, update_package


print('Preparing packages for transport...')
print('Loading the trucks...')
print('Finding best routes...')
print('trucks are loaded and ready!\n\n')
print('Welcome to the WGUPS delivery system!')



time_stamp = datetime(2020, 10, 20, 8, 0, 0)
time_of_update = datetime(2020, 10, 20, 10, 20, 0)

while True:
    print('To see truck and package information, type "info". \n'
          'To search for an individual package at the current time, type "search". \n'
          'To remove or cancel a package, type "remove". \n'
          'To check the status of all deliveries at a particular time, enter a military time.  (please enter in format 00:00:00) \n'
          'The current time is {}'.format(time_stamp.time()))
    user = input('>>>>>>  ')
    print()

    try:
        # user requested information for all trucks and payload.
        if user == 'info':
            truck_packages_information()

        # user requested information on particular package. Searching by package ID
        elif user == 'search':
            id = input('Please enter the id of the package you want to search for  --->  ')
            search_package(id)
            print()

        elif user == 'remove':
            id = input('Please enter the id of the package you want to remove  --->  ')
            remove_package(id)
            print()

        else:
            # use map to convert user entered time to integer hours, minutes, seconds.
            try:
                hours, minutes, seconds = map(int, user.split(':'))
            except:
                hours, minutes = map(int, user.split(':'))
                seconds = 0

            # convert the time user requested to see into datetime format
            time_stamp = datetime(2020, 10, 20, hours, minutes, seconds)

            # if time is greater than 10:20 am, make sure to update the wrongly addressed package
            if time_stamp.time() > time_of_update.time():
                updated_pkg = ['9', '410 S State St', 'Salt Lake City', 'UT', '84111', '17:00', '2', 'Address updated at {}'.format(str(time_of_update.time()))]
                update_package(updated_pkg)

            # if user enters a time below 8 am, remind that the workday has not begun yet.
            if time_stamp.time() < datetime(2020, 10, 20, 8, 0, 0).time():
                print('The work day has not started yet. Starts at 8:00:00')
                print()

            else:
                print('CURRENT DELIVERY INFORMATION AT {}\n'.format(time_stamp.time()))

                # send requested time to deliver function which will calculate which packages have been delivered and when
                deliver('truck 1', time_stamp)
                deliver('truck 2', time_stamp)
                deliver('truck 3', time_stamp)
                # calculate total miles
                total_miles()
                print()
    except:
        print('It seems you have made an invalid request. Please try again')
        print()




