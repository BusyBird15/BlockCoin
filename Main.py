# This excludes the keeps-alive and admin features.


# Import necessary modules
from replit import db
import os.path
import scratchattach as sa
from time import gmtime, strftime

# Login and connect to Blockcoin.
session = sa.Session(os.environ['Session_Id'], username="S4IL")
conn = session.connect_cloud("824613252")
client = sa.CloudRequests(conn)

# To make things easy and simple, a bottom-up approach was used.
# This means that many functions were used, making updates very easy.
########## Functions ##########

def log(msg):
    # Function for logging a message to the log file.
    # Get the time
    tme = str(strftime("%m/%d at %H:%M:%S > ", gmtime()))
    # Get the database entry
    temp = db['Log']
    # Add a message to the log
    temp.append(str(tme) + msg)
    # Set log to the new value
    db['Log'] = temp

def getbal(user: str):
    # Get a user's balance from the database.
    try:
        balance = db[user]["balance"]
    # If the user dos not exist in the database, create one.
    except KeyError:
        # Set the new entry to default values
        db[user] = {"banned": False,
                   "balance": 150,
                   "friends": [],
                   "tasks": []}
        # Log the action
        log(str("ENTRY CREATE: Slot created for user " + user))
        # Return the balance for a new user, 150
        return 150
    # Before proceeding, if the user is banned, return a -2
    if db[user]["banned"]:
        return -2
    # If the user's balance is -1, return inf
    if balance == -1:
        return "inf"
    # Finally, return the user's balance
    return balance


def start():
    # Method for starting the server.
    # Log the action.
    log("Server started!")
    # Start the server
    client.run()

def give(users, amount=0):
    # Giving Blockcoin from a user to another user.
    # Separate the user string into two strings and assign them to two variables.
    fromuser, touser = users.split(",")
    # Lowercase the usernames
    fromuser = fromuser.lower()
    touser = touser.lower()
    # If, for some reason, a value less than 0 is passed as a transaction, report an error message.
    if float(amount) < 0:
        log(str("TRANSACTION ABORT: " + fromuser + " attempted to steal " + str(abs(float(amount))) + " BlockCoins from " + touser))
        return ["Error Code 1. Please contact @BusyBird15."]
    # If the transaction is extremey high, note the action and proceed.
    if float(amount) > 499:
        log(str("HIGH TRANSACTION NOTICE: " + fromuser + " is giving " + str(abs(float(amount))) + " BlockCoins to " + touser))
    # Log the transaction
    log(str("TRANSACTION: " + fromuser + " is giving " + str(abs(float(amount))) + " Blockcoins to " + touser))
    # Attempt calculting the transaction
    try:
        # If the giver has inf Blockcoins, just give the other user.
        if float(db[fromuser]["balance"]) == -1.0:
            addamount = float(db[touser]["balance"])
            addamount += float(amount)
            db[touser]["balance"] = addamount
        # Otherwise, complete the transaction normally.
        else:
            subamount = float(db[fromuser]["balance"])
            subamount -= float(amount)
            db[fromuser]["balance"] = subamount
            addamount = float(db[touser]["balance"])
            addamount += float(amount)
            db[touser]["balance"] = addamount
        # If the transaction succeeded, print a message
        print("A transaction between " + fromuser + " and " + touser + " was successfully executed.")
    # If it fails, report an error and move on.
    except KeyError:
        log(str("NON-FATAL ERROR: Transaction of " + amount + " between users " + fromuser + " and " + touser + " cancelled due to db error."))
        print("Transaction of " + amount + " between users " + fromuser + " and " + touser + " cancelled due to db error.")
        return ["Error code 2. Please contact @BusyBird15"]
    # Finally, return the new user balance.
    temp = getbal(fromuser)
    return temp

########## Client Requests ##########
@client.request
def getbitbalance(user):
    # Retrieving the balance for a user.
    # Make the username lowercase.
    user = user.lower()
    # Get the balance
    bal = float(getbal(user))
    # Return the balance
    return [bal]

@client.request
def givecurrency(users, amount=0):
    temp = give(users, amount)
    return [temp]

@client.request   
def checkifadmin(user):
    # Function to check if a user is an admin. Used for in-project features
    # Lowercase the username
    user = user.lower()
    # This list defines the admins. Be sure they are all lowercase.
    admins = ["busybird15", "s4il"]
    # If the user is an admin (username is found in the admins list), return true.
    if user in admins:
        return["true"]
    # If the user is not an admin, return false.
    else:
        return["false"]

@client.event
def on_ready():
    # This metho is called when server initialization is complete.
    print("\nServer is ready.\n")

@client.request
def add_friend(touser, username):
    # Adds a user to another user's friend list.
    # Get the user's frien list.
    usrfriends = db[touser]["friends"]
    # Add the username to the friend list.
    usrfriends.append(username)
    # Log the action
    log(str("Added friend " + username, " to " + touser))

@client.request
def remove_friend(toUser, username):
    # Removes a friend from a user's friend list.
    # Get the friend list
    userfriends = db[toUser]["friends"]
    # Make sure the user to remove is a friend to prevent an error.
    if username in userfriends:
        # Remove the user from the list
        userfriends.remove(username)
        # Log the action
        log(str("Removed friend " + username + " from " + toUser))

@client.request
def get_friends(toUser):
    # Function to get the user's friends and return it as a list
    # Simply return the list.
    temp = db[toUser]["friends"]
    return [temp]

@client.request
def leaderboard():
    # Function to find and return the top five richest users
    # Load all the users
    keys = db.keys()
    print(keys)
    # Loop over every key and find the top 1.
    for i in keys:
        maxbalance1 = 0
        # If the user balance is the biggest yet, add it to the leaderboard.
        if float(db[i]['balance']) > maxbalance1:
            maxbalance1 = i + " with a balance of " + str(db[i]['balance'])
    for i in keys:
        maxbalance2 = 0
        # If the user balance is the biggest yet, add it to the leaderboard.
        if float(db[i]['balance']) > maxbalance2:
            maxbalance2 = i + " with a balance of " + str(db[i]['balance'])
    for i in keys:
        maxbalance3 = 0
        # If the user balance is the biggest yet, add it to the leaderboard.
        if float(db[i]['balance']) > maxbalance3:
            maxbalance3 = i + " with a balance of " + str(db[i]['balance'])
    for i in keys:
        maxbalance4 = 0
        # If the user balance is the biggest yet, add it to the leaderboard.
        if float(db[i]['balance']) > maxbalance4:
            maxbalance4 = i + " with a balance of " + str(db[i]['balance'])
    for i in keys:
        maxbalance5 = 0
        # If the user balance is the biggest yet, add it to the leaderboard.
        if float(db[i]['balance']) > maxbalance5:
            maxbalance5 = i + " with a balance of " + str(db[i]['balance'])
    # Finally, return the top 5.
    return [maxbalance1, maxbalance2, maxbalance3, maxbalance4, maxbalance5]

@client.request
def getpassword(user):
    # Function to return a user's password
    # Simply get the password and return it.
    try:
        passw = db[user]["password"]
        return [passw]
    # If the user never created a password, return an empty string.
    except KeyError:
        return [""]

@client.request
def setpassword(user, newpass):
    # Function to set a user's password
    # Simply set the password.
    db[user]["password"] = newpass
    
