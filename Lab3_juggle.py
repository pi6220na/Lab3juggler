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

        #db.commit()


    except sqlite3.Error as e:
        print('rolling back changes because of error' , e)
        traceback.print_exc()
        db.rollback()

    finally:

        #db.close()
        return cur, db


def add_to_db(cur, db, name, country, catches):

    with db:
        cur.execute('insert into juggler values (?,?, ?)', (name, country, catches))
        #cur.execute('insert into phones values ("%s", %d)'% (brand, version))

    #for row in cur.execute('select * from juggler'):
    #    print(row)

    # cur.execute('drop table phones')

    db.commit()

    return cur, db

def close_db(db):

    db.close()


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
    name = input('Enter the name of the juggler to update: ')
    catches = int(input('Enter the correct number of catches: '))

    with db:
        cur.execute('update juggler set catches is (?)', catches, ' where name = ', name)


def delete_juggler(cur, db):
    print("")
    inp_name = input('Enter the name of the juggler: ')
    with db:
        cur.execute('delete from juggler where name is (?)', (inp_name,))


def print_db(cur, db):

    print('')
    for row in cur.execute('select * from juggler'):
        print(row)


def main():

    cur, db = create_db()  # create database and table juggler

    while True:
        choice = print_menu()
        if choice == '1':
            name, country, catches = get_data()
            db, cur = add_to_db(cur, db, name, country, catches)
        if choice == '2':
            update_juggler(cur, db)
        if choice == '3':
            delete_juggler(cur, db)
        if choice == '4':
            print_db(cur, db)
        if choice == 'q':
            break

    close_db(db)


main()