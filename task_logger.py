import datetime
import cowsay
import os
import sys

from collections import OrderedDict
from colorama import init, Fore, Back, Style
from peewee import *

###############################################################################

# For colorama
init()

# Database info
DATABASE_NAME = "oakes_task_log.db"
db = SqliteDatabase(DATABASE_NAME)

###############################################################################
##                               DATABASE MODEL
###############################################################################

class BaseModel(Model):
    class Meta:
        database = db


class Task(BaseModel):
    username = CharField()
    title = CharField()
    total_time = IntegerField()
    notes = CharField()
    timestamp = DateTimeField(default=datetime.datetime.now)

###############################################################################
##                                 MAIN
###############################################################################

def clear():
    '''Clears command line screen'''
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def gimme_space():
    print('\n' + '*' * 82 + '\n')


def title_bar(title_name='MAIN MENU'):
    '''Title bar for cleaner presentation'''
    print(Fore.BLUE, '*' * 80)
    print(f'\t\t\t\t{title_name}')
    print('*' * 80, Style.RESET_ALL)


def intialize():
    '''Connect to database, create tables'''
    db.connect()
    db.create_tables([Task])


def main_menu_loop():
    '''Main Menu'''

    clear()

    user_selection = None
    while user_selection != 'q':
        title_bar()
        print(Fore.GREEN, '\n\tWelcome to the task logging portal. Please make a selection.\n', Style.RESET_ALL)

        # Print menu option and docstring of function to be called
        for key, value in main_menu_options.items():
            print(Fore.LIGHTBLUE_EX, f'({key})', Fore.LIGHTWHITE_EX, f'{value.__doc__}')
        user_selection = input(Fore.LIGHTBLUE_EX + '\nAction: ').lower().strip()

        # If valid selection, call selected function; if not, try again.
        if user_selection in main_menu_options:
            main_menu_options[user_selection]()
        else:
            clear()
            print('\nSorry, {} is not a valid selection. Please try again.'.format(user_selection))


def quit():
    '''Quit program'''
    cowsay.dragon("Until next time...")
    sys.exit()

###############################################################################
##                              ADDING TASKS
###############################################################################

def add_task():
    '''Add task'''
    clear()
    title_bar(title_name="ADDING TASK")

    # Get task info from user and enter into database
    employee_username = input('Your username: ').lower().strip()
    task_name = input('Your task name: ').lower().strip()
    task_total_time = input('Total time (in minutes): ')
    task_notes = input('Notes: ')
    try:
        with db.transaction():
            task = Task.create(
                username=employee_username,
                title=task_name,
                total_time=task_total_time,
                notes=task_notes,
            )
    except IntegrityError:
        print('You messed up the task creation.')
    except ValueError:
        print('You messed up the task creation, check those value types!')
        return add_task()

    # TODO: Provide recap showing them they successfully logged a new task

###############################################################################
##                              SEARCHING TASKS
###############################################################################

def search_tasks():
    '''Search tasks'''

    clear()
    show_latest_five_tasks()
    print('\n')

    title_bar(title_name="SEARCH OPTIONS")
    print(Fore.GREEN, '\n\t\tPlease select a strategy for searching through tasks.\n', Style.RESET_ALL)

    # Ask user how they'd like to search for tasks
    for key, value in search_menu_options.items():
        print(Fore.LIGHTBLUE_EX, f'({key})', Fore.LIGHTWHITE_EX, f'{value.__doc__}')
    user_selection = input(Fore.LIGHTBLUE_EX + '\nAction: ').lower().strip()
    if user_selection in search_menu_options:
        search_menu_options[user_selection]()
    else:
        clear()
        print('\nSorry, {} is not a valid selection. Please try again.'.format(user_selection))


def show_latest_five_tasks():
    '''Prints the latest five tasks created'''
    title_bar(title_name="LATEST TASKS")
    latest = Task.select().order_by(Task.timestamp.desc())

    for entry in latest[:5]:
        timestamp = entry.timestamp.strftime('%A %B %d, %Y %I:%M%p')
        print(Fore.GREEN + '\nUser: ' + Style.RESET_ALL + entry.username.title())
        print(Fore.GREEN + 'Task: ' + Style.RESET_ALL + entry.title.title())
        print(Fore.GREEN + 'Total Time: ' + Style.RESET_ALL + f'{entry.total_time} minutes')
        print(Fore.RED + f'({timestamp})' + Style.RESET_ALL)


def search_by_username():
    '''Search by username'''
    print('Search by...username')


def search_by_task_date():
    '''Search by task date'''
    print('Search by...entry date')


def search_by_task_length():
    '''Search by task length (in minutes)'''
    print('Search by...time spent')


def search_by_notes_regex():
    '''Search by notes regex'''
    print('Search by...note regex')

###############################################################################
# Control program flow by calling function based off user selection

main_menu_options = OrderedDict([
    ('1', add_task),
    ('2', search_tasks),
    ('3', quit),
])

search_menu_options = OrderedDict([
    ('1', search_by_username),
    ('2', search_by_task_date),
    ('3', search_by_task_length),
    ('4', search_by_notes_regex),
    ('5', main_menu_loop),
])

###############################################################################

if __name__=='__main__':
    clear()
    intialize()
    main_menu_loop()
