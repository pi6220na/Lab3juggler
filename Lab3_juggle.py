import sqlite3
import traceback


def get_data():


    name = input('Enter the name of the juggler: ')
    country = input('Enter the country of the juggler: ')
    catches = int(input('Enter the number of catches the juggle made: '))

    return name, country, catches


def create_db():

    try:

        db = sqlite3.connect('jugglers_db.db')
        cur = db.cursor()

        cur.execute('create table if NOT EXISTS juggler (name text, country text, catches int)')


    except sqlite3.Error as e:
        print('rolling back changes because of error' , e)
        traceback.print_exc()
        db.rollback()

    finally:

        return cur, db


def add_to_db(cur, db, name, country, catches):

    try:
        with db:
            cur.execute('insert into juggler values (?,?,?)', (name, country, catches))

    except sqlite3.Error as e:
        print('Database error: ', e)
        traceback.print_exc()

    finally:

        return cur, db


def print_menu():

    valid = False

    print('')
    print('1) add a jugglers data')
    print('2) search for a juggler and update')
    print('3) delete a juggler')
    print('4) show all jugglers')
    print('"q" to quit the program')
    print('')

    while not valid:

        choice = input('Enter 1, 2, 3, or 4 or q: ')
        if choice != '1' and choice != '2' and choice != '3' and choice != '4' \
                         and choice != 'q':
            print('Error, please enter 1, 2, 3, or 4, or q to quit: ')
        else:
            valid = True

    return choice


def update_juggler(cur, db):

    name_in = input('Enter the name of the juggler to update: ')
    catches_in = int(input('Enter the correct number of catches: '))

    try:
        with db:
            cur.execute('update juggler set catches = ? where name = ?', (catches_in, name_in))

    except sqlite3.Error as e:
        print('Database error: ', e)
        traceback.print_exc()


def delete_juggler(cur, db):

    print("")
    inp_name = input('Enter the name of the juggler: ')

    try:
        with db:
            cur.execute('delete from juggler where name = ?', (inp_name,))

    except sqlite3.Error as e:
        print('Database error: ', e)
        traceback.print_exc()


def print_db(cur, db):

    print('')
    try:
        for row in cur.execute('select * from juggler'):
            print(row)

    except sqlite3.Error as e:
        print('Database error: ', e)
        traceback.print_exc()


def main():

    cur, db = create_db()  # create database and table juggler

    while True:
        choice = print_menu()
        if choice == '1':
            name, country, catches = get_data()
            cur, db = add_to_db(cur, db, name, country, catches)
        if choice == '2':
            update_juggler(cur, db)
        if choice == '3':
            delete_juggler(cur, db)
        if choice == '4':
            print_db(cur, db)
        if choice == 'q':
            break

    db.commit()
    db.close()


main()
