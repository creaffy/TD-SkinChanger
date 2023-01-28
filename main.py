import winreg
import json
from time import *

KEY = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\\ShibaFlow\\Tactical Duty", 0, winreg.KEY_ALL_ACCESS)

with open("cosmetics.json") as file:
    cosmetics = json.load(file)

def editKey(slot, value):
    winreg.SetValueEx(KEY, slot, 0, winreg.REG_DWORD, value)

def readKey(slot):
    return winreg.QueryValueEx(KEY, slot)[0]

def getName(type, id):
    for skin in cosmetics[type]:
        if skin[0] == int(id):
            return skin[1]

def showCommands():
    print("ALL COMMANDS:\n/SKIN - change your skin by id\n/KNIFE - change your knife by id\n/SKINS - skins ids list\n/KNIVES - knives ids list\n/CURRENT - your currently equipped skins\n/HELP - this menu")

def newCommand():
    global command 
    command = input("\n>>> ").upper()
    match command:
        case "/SKINS":
            try:
                for skin in cosmetics['skins']:
                    print(f"{str(skin[0]).rjust(2, '0')} : {skin[1]}")
            except Exception as e:
                print(f"FATAL ERROR: \n{e}")
        case "/KNIVES":
            try:
                for skin in cosmetics['knives']:
                    print(f"{str(skin[0]).rjust(2, '0')} : {skin[1]}")
            except Exception as e:
                print(f"FATAL ERROR: \n{e}")
        case "/SKIN":
            try:
                print('Enter Skin ID, type "ABORT" to cancel.')
                choice = input("ID: ")
                if choice.upper() == "ABORT":
                    newCommand()
                else:
                    editKey("Skin_h2089423610", int(choice))
                    print(f"Your skin has been changed to {getName('skins', int(choice))}")
            except Exception as e:
                print(f"FATAL ERROR: \n{e}")
        case "/KNIFE":
            try:
                choice = input("ID: ")
                if choice.upper() == "ABORT":
                    newCommand()
                else:
                    editKey("Knife_h221345514", int(choice))
                    print(f"Your knife has been changed to {getName('knives', int(choice))}")
            except Exception as e:
                print(f"FATAL ERROR: \n{e}")
        case "/CURRENT":
            try:
                print(f'SKIN: {str(readKey("Skin_h2089423610")).rjust(2, "0")} | {getName("skins", readKey("Skin_h2089423610"))}')
                print(f'KNIFE: {str(readKey("Knife_h221345514")).rjust(2, "0")} | {getName("knives", readKey("Knife_h221345514"))}')
            except Exception as e:
                print(f"FATAL ERROR: \n{e}")
        case "/HELP":
            try:
                showCommands()
            except Exception as e:
                print(f"FATAL ERROR: \n{e}")
        case _:
            try:
                print("Unknown Command. Use /HELP for a list.")
            except Exception as e:
                print(f"FATAL ERROR: \n{e}")
    newCommand()

print("TacticalDuty.io Skin Changer by Creaffy")
print("https://github.com/creaffy/TD-SkinChanger/\n")

showCommands()

newCommand()