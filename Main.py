# Copy all code and paste in your IDE. No need to install ScratchAttch, this code will do it for you!

# Check for ScratchAttach on the system
import os
os.system("pip install -U scratchattach")

# Import ScratchAttach and os.path
import scratchattach as scratch3
import os.path

# Define session and connection vars
session = scratch3.Session(".eJxVj81OwzAQhN_FZwiu65-6N5B6AQESt3CJNvYmMUnsEjtUKuLdsaVcelt9M7Oa-SVrxMXDjORIQnQpRHBT04Ind6SBNQ1NMTTOZv2gKWcHKbOUMCYTwuhK7hKWEe1toAUzoi-pwtAnZyC54KtNiNUHnqcNPm3m_DfkI4eY5towxdUBFKdaaikpRUEptEqZPRy_zamrP4WJSof6eXlp69OV_bwjfe3zmyn0zt-7cyktKqEqRnfVXpSKE_h-hb70xpiB_cogNMnNeA2-4McZl1zs4Q0vTZ2n3Q4bIA7ZJKjUAlrkDK1FqjrRyU4KYfXOgKDc2K4UtuTvHxh3cxA:1pRzrS:3V0g7XVSUjEicpA3CVzdG-8i_ug", username="ositosail_ban")  # Login as @ositosail_ban
conn = session.connect_cloud("804030120")  # connect to BlockCoins

# Connect to Scratch
client = scratch3.CloudRequests(conn)

@client.request
def getbitbalance(user):  # called when user logs on
    print("Getting user balance...")
    if os.path.exists(user + ".txt"):
        userfile = open(user + ".txt", "r")
        rawbalance = userfile.readline()
        userfile.close()
        return [rawbalance]
    else:
        userfile = open(user + ".txt", "w")
        rawbalance = 150 # This is how much new users get. Change as you wish.
        userfile.write(str(rawbalance))
        userfile.close()
        return [rawbalance]

@client.request
def givecurrency(users, amount):
    print("Transaction request received")
    newUsers = users.split(",")
    if os.path.exists(newUsers[1] + ".txt"):
        userfile = open(newUsers[0] + ".txt", "r")
        valueFrom = float(userfile.readline())
        valueFrom -= amount
        userfile.write(str(valueFrom))
        userfile.close()
        userfile = open(newUsers[1] + ".txt", "r+")
        valueTo = float(userfile.readline())
        valueTo += amount
        userfile.write(str(valueTo))
        userfile.close()
        userfile = open(newUsers[0] + ".txt", "r")
        rawbalance = userfile.readline()
        userfile.close()
        return [rawbalance]
    else:
        return ["ERROR: UNREGISTERED USER"]

@client.event
def on_ready():
    print("Request handler is running...")


client.run()  # Starts the request handler
