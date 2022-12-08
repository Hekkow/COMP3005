import psycopg2
from psycopg2 import OperationalError


class Book:
    def __init__(self, isbn, title, author, genre, pages, price, quantity, publisher, cut):
        self.isbn = int(isbn)
        self.title = title
        self.author = author
        self.genre = genre
        self.pages = int(pages)
        self.price = float(price)
        self.quantity = int(quantity)
        self.publisher = publisher
        self.cut = float(cut)
    def __str__(self):
        return f"[" + str(self.isbn) + "] " + self.title + " by " + ", ".join(self.author) + " for $" + str(self.price) + "\n"

class User:
    def __init__(self, username, password, cardnumber, address, isAdmin):
        self.username = username
        self.password = password
        self.cardnumber = cardnumber
        self.address = address
        self.isAdmin = isAdmin
    def __str__(self):
        if (self.isAdmin):
            print("Admin")
        else:
            print("User")
        return f"Username: " + self.username + "\nPassword: " + self.password + "\nCard Number: " + str(self.cardnumber) + "\nAddress: " + self.address + "\n"

def main():
    global connection
    global cursor
    global user
    global cart
    cart = []
    startServer()
    # runQueries("Postgres/createtables.sql")
    registration()

    # repeatedly get input and run queries depending on the input 
    print("Type help for a list of commands")
    command = ""
    while command != "quit":
        command = input("\nCommand: ")
        print("")
        commandToQuery(command)

    # close server when done
    cursor.close()
    connection.close()



def commandToQuery(command):
    command = command.lower()
    terms = command.split()
    if command == "help":
        print("Keys include isbn, title, author, genre, pages, quantity, publisher, price\n\nCommands:\n- my info\n- view books\n- details [isbn]\n- search [key] [value]\n- sort [key] [asc/desc]\n- add to cart [isbn]\n- remove from cart [isbn]\n- view cart\n- clear cart\n- checkout\n- logout\n- make me admin (only do this if ur a real admin pls)")
    elif command == "help admin":
        print("- delete all users\n- print all users\n- stats\n- add book\n- remove [isbn]")
    elif command == "view books":
        printBooks()
    elif terms[0] == "details":
        print(len(terms))
        if len(terms) == 2:
            book = getBook(terms[1])
            if book:
                prettyPrint(book)
            else:
                print("Invalid input")
        else:
            print("Invalid input")
    elif command == "my info":
        print(user)
    elif terms[0] == "search":
        if len(terms) != 3:
            print("Invalid input")
        else:
            searchBooks(terms[1], command.split(terms[1])[1][1:]) # gets rest of string instead of just next word, useful for multi word names
    elif terms[0] == "sort":
        if len(terms) == 2:
            sortBooks(terms[1], "asc")
        elif len(terms) == 3:
            sortBooks(terms[1], terms[2])
        else:
            print("Invalid input")
    elif command == "logout":
        logout()
    elif terms[0] == "add" and terms[1] == "to" and terms[2] == "cart":
        if len(terms) == 4:
            book = getBook(terms[3])
            if book:
                addToCart(book)
                print("Added " + book.title + " to cart\n")
            else:
                print("Invalid input")
        else:
            print("Invalid input")
    elif command == "view cart":
        viewCart()
    elif terms[0] == "remove" and terms[1] == "from" and terms[2] == "cart":
        if len(terms) == 4:
            book = getBook(terms[3])
            removeFromCart(book)
            print("Removed " + book.title + " from cart\n")
        else:
            print("Invalid input")
    elif command == "clear cart":
        clearCart()
    elif command == "checkout":
        checkout()
    elif command == "make me admin":
        makeAdmin()
    elif command == "add book":
        if user.isAdmin:
            addBook()
        else:
            print("You're not admin")
    elif terms[0] == "remove":
        if len(terms) == 2:
            cursor.execute("DELETE FROM books WHERE isbn=" + terms[1] + ";")
        else:
            print("Invalid input")
    elif command == "print all users":
        if user.isAdmin:
            printAllUsers()
        else:
            print("You're not admin")
    elif command == "delete all users":
        if user.isAdmin:
            deleteAllUsers()
            logout()
        else:
            print("You're not admin")
    elif command == "stats":
        if user.isAdmin:
            checkStats()
        else:
            print("You're not admin")
    else:
        print("Invalid input")

def checkStats():
    key = input("Type [total/shop cut/key]: ")
    if key == "total":
        cursor.execute("SELECT SUM (price) FROM sales")
        print("Total sold is $" + str(cursor.fetchall()[0][0]) + " before publisher cuts")
    elif key == "shop cut":
        cursor.execute("SELECT SUM (cut) FROM sales")
        print("Total sold is $" + str(cursor.fetchall()[0][0]) + " after publisher cuts")
    else:
        try:
            cursor.execute("SELECT " + key + ", SUM (sales.price) FROM books JOIN sales ON books.isbn = sales.isbn GROUP BY " + key + ";")
            stats = cursor.fetchall()
            for i in range(len(stats)):
                print(key + " " + str(stats[i][0][0]) + " has sold $" + str(stats[i][1]))
        except Exception as err:
            print("Invalid input" + err)

def viewCart():
    cursor.execute("SELECT cart FROM users WHERE username='" + user.username + "';")
    isbns = cursor.fetchall()[0][0]
    if not isbns:
        print("Nothing in cart")
    else:
        for i in range(len(isbns)):
            prettyPrint(getBook(isbns[i]))
def addBook():
    isbn = input("ISBN: ")
    cursor.execute("SELECT isbn FROM books WHERE isbn=" + str(isbn))
    print()
    if len(cursor.fetchall()) > 0:
        quantity = input("Quantity: ")
        cursor.execute("UPDATE books SET quantity=" + str(getBook(isbn).quantity+int(quantity)) + " WHERE isbn=" + str(isbn))
    else:
        title = input("Title: ")
        numAuthors = input("Number of authors: ")
        authors = []
        for i in range(int(numAuthors)):
            authors.append(input("Author " + str(i+1) + ": "))
        numGenres = input("Number of genres: ")
        genres = []
        for i in range(int(numGenres)):
            genres.append(input("Genre " + str(i+1) + ": "))
        pages = input("Number of pages: ")
        price = input("Price: $")
        quantity = input("Quantity: ")
        publisher = input("Publisher: ")
        cut = input("Publisher's cut: %")
        cursor.execute("INSERT INTO books VALUES (" + isbn + ", '" + title + "', '{" + str(authors)[1:][:-1].replace("'", "\"") + "}', '{" + str(genres)[1:][:-1].replace("'", "\"") + "}', " + pages + ", " + price + ", " + quantity + ", '" + publisher + "', " + cut + ");")

def makeAdmin():
    user.isAdmin = True
    cursor.execute("UPDATE users SET isAdmin=true WHERE username='" + user.username + "';")
    commandToQuery("help admin")

def checkout():
    cursor.execute("SELECT cart FROM users WHERE username='" + user.username + "';")
    isbns = cursor.fetchall()[0][0]
    if len(isbns) == 0:
        print("Cart empty")
        return
    cardnumber = user.cardnumber
    address = user.address
    useCard = input("Use your default card and address (y/n): ")
    if useCard == "n":
        cardnumber = int(input("Card number: "))
        address = input("Address: ")

    for i in range(len(isbns)):
        if getBook(isbns[i]).quantity-1 >= 0:
            cursor.execute("UPDATE books SET quantity=" + str(getBook(isbns[i]).quantity-1) + " WHERE isbn=" + str(isbns[i]))
            print("Thank you for purchasing " + getBook(isbns[i]).title)
            cursor.execute("INSERT INTO sales VALUES ('" + str(isbns[i]) + "', '" + str(getBook(isbns[i]).price) + "', " + str(getBook(isbns[i]).price * (1-getBook(isbns[i]).cut/100)) + ");")
                # cursor.execute("DELETE FROM books WHERE isbn=" + str(isbns[i]) + ";")
        else:
            print("Couldn't buy " + getBook(isbns[i]).title + ", out of stock")
    cursor.execute("INSERT INTO orders (cardnumber, address) VALUES ('" + str(cardnumber) + "', '" + address + "');")
    clearCart()
    


def startServer():
    global connection
    global cursor
    connection = psycopg2.connect(dbname="Look Inna Book", user="postgres", password="7975727667", host="localhost")
    cursor = connection.cursor()
    connection.autocommit = True

def runQueries(filename):
    # gets all queries from createtables.sql
    createTablesFile = open(filename, "r")
    createTablesLines = createTablesFile.read()
    createTablesFile.close()
    createTablesQueries = createTablesLines.split(";")

    # runs all queries
    for query in createTablesQueries[:-1]:
        try:
            # print(query)
            cursor.execute(query)
        except (OperationalError, msg):
            print("Error: " + msg)

def stringToBook(book):
    return Book(book[0], book[1], book[2], book[3], book[4], book[5], book[6], book[7], book[8])

def stringToUser(user):
    return User(user[1], user[2], user[3], user[4], user[5])

def searchBooks(key, value):
    books = []
    try:
        cursor.execute("SELECT * FROM books WHERE '" + value + "' = ANY(" + key + ");")
    except Exception:
        try:
            cursor.execute("SELECT * FROM books WHERE " + key + " = '" + value + "';")
        except:
            print("Invalid search term")
            return
    booksRaw = cursor.fetchall()
    for i in range(len(booksRaw)):
        books.append(stringToBook(booksRaw[i]))
    prettyPrintList(books)
    if len(booksRaw) == 0:
        print("Nothing found for that search term")

def sortBooks(key, direction):
    books = []
    try:
        cursor.execute("SELECT * FROM books ORDER BY " + key + " " + direction)
    except Exception:
        print("Invalid sort key")
        return
    booksRaw = cursor.fetchall()
    for i in range(len(booksRaw)):
        books.append(stringToBook(booksRaw[i]))
    printList(books)

def prettyPrint(book):
    print("Title           | " + book.title)
    print("Author          | " + ", ".join(book.author))
    print("Genre           | " + ", ".join(book.genre))
    print("Pages           | " + str(book.pages))
    print("Left in stock   | " + str(book.quantity))
    print("Published by    | " + book.publisher)
    print("Price           | $" + str(book.price))
    print("Publisher's cut | " + str(book.cut) + "%")
    print("ISBN            | " + str(book.isbn))
    print("")

def printList(l):
    for i in range(len(l)):
        print(l[i])
def prettyPrintList(l):
    for i in range(len(l)):
        prettyPrint(l[i])


def printBooks():
    books = []
    cursor.execute("SELECT * FROM books;")
    booksRaw = cursor.fetchall()
    for i in range(len(booksRaw)):
        books.append(stringToBook(booksRaw[i]))
    printList(books)

def getBook(isbn):
    try:
        cursor.execute("SELECT * FROM books WHERE isbn='" + str(isbn) + "';")
        book = cursor.fetchall()
        if len(book) > 0:
            return stringToBook(book[0])
    except (OperationalError, msg):
        print("Error: " + msg)
        return None
    return None
def registration():
    which = input("log in or register: ")
    username = input("Username: ")
    if which == "register":
        if getUser(username) is None:
            password = input("Password: ")
            cardnumber = int(input("Card number: "))
            address = input("Address: ")
            register(username, password, cardnumber, address)
            
        else:
            print("User already exists\n")
            registration()
    else:
        password = input("Password: ")
        login(username, password)
    
def register(username, password, cardnumber, address):
    cursor.execute("INSERT INTO users (username, pass, cardnumber, address, isAdmin) VALUES ('" + username + "', '" + password + "', '" + str(cardnumber) + "', '" + address + "', false);")
    global user
    user = User(username, password, cardnumber, address, False)
    connection.commit()

        

def login(username, password):
    userRaw = getUser(username)
    if userRaw is not None:
        if userRaw.password == password:
            global user
            user = userRaw
        else:
            print("Password incorrect\n")
            registration()
    else:
        print("User not found")
        registration()

def logout():
    global user
    user = None
    registration()

def addToCart(book):
    cursor.execute("UPDATE users SET cart = array_append(cart, " + str(book.isbn) + ") WHERE username = '" + user.username + "';")

def removeFromCart(book):
    cursor.execute("UPDATE users SET cart = array_remove(cart, " + str(book.isbn) + ") WHERE username = '" + user.username + "';")


def clearCart():
    cursor.execute("UPDATE users  SET cart = '{}' WHERE username = '" + user.username + "';")

def getUser(username):
    cursor.execute("SELECT * FROM users WHERE username='" + username + "';")
    user = cursor.fetchall()
    if (len(user) == 0):
        return None
    return stringToUser(user[0])

# ADMIN COMMANDS

def deleteAllUsers():
    cursor.execute("TRUNCATE users;")
def printAllUsers():
    cursor.execute("SELECT * FROM users")
    print(cursor.fetchall())

if __name__ == '__main__':
    main()
