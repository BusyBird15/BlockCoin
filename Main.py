# Install ScratchAttach on the system (if you have it already, omit these lines)
import os
os.system("pip install -U scratchattach")

# Import ScratchAttach and os.path
import scratchattach as scratch3
import os.path

# Define session and connection vars
# Login as you; see the ScratchAttach repo for details on getting a session ID
session = scratch3.Session("SESSIONID", username="USERNAME")
# Connect to the project.
conn = session.connect_cloud("PROJECTID")

# Connect to Scratch
client = scratch3.CloudRequests(conn)

# Below this line will need to be adjusted to your needs.
# I used a separate txt file to store each user's balance.

@client.request
def getbitbalance(user):                     # function for getbitbalance
    print("Getting user balance...")
    if os.path.exists(user + ".txt"):
        userfile = open(user + ".txt", "r")
        rawbalance = userfile.readline()
        userfile.close()
        print(str(rawbalance))
        return [rawbalance]
    else:
        userfile = open(user + ".txt", "w")
        rawbalance = 150                            # This is how much new users get. Change as you wish.
        userfile.write(str(rawbalance))
        userfile.close()
        return [rawbalance]

@client.request
def givecurrency(users, amount):
    print("Transaction request received")
    newUsers = users.split(",")                      # Get both users
    userfile = open(newUsers[0] + ".txt", "r")       # Open the file
    valueFrom = float(userfile.read())               # Read the file
    print("User 1 beginning bal", str(valueFrom))
    userfile.close()                                 # Close the file
    open(newUsers[0] + ".txt", 'w').close()          # Clear the file
    userfile = open(newUsers[0] + ".txt", "w")       # Reopen the file
    valueFrom -= float(amount)                       # Subtract currency
    print("User 1 new bal", str(valueFrom))
    userfile.write(str(valueFrom))                   # Write the new balance
    userfile.close()                                 # Close the file
    userfile = open(newUsers[1] + ".txt", "r")       # Open the file
    valueTo = float(userfile.read())                 # Read the user's balance
    print("User 2 beginning bal", str(valueTo))
    userfile.close()                                 # Close the file
    open(newUsers[1] + ".txt", 'w').close()          # Clear the file
    userfile = open(newUsers[1] + ".txt", "w")       # Reopen the file
    valueTo += float(amount)                         # Add currency
    print("User 2 new bal", str(valueTo))
    userfile.write(str(valueTo))                     # Write the new balance
    userfile.close()                                 # Close the file
    userfile = open(newUsers[0] + ".txt", "r")       # Open the player's balance
    rawbalance = userfile.readline()                 # Read the balance
    userfile.close()                                 # Close the file
    print("New balance, returned to project is", str(rawbalance))
    return [rawbalance]                              # Return the user's new balance

@client.event
def on_ready():
    print("Request handler is running...")


client.run()                                         # Starts the request handler
