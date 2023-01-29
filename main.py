import winreg
import json
from time import *

KEY = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\\ShibaFlow\\Tactical Duty", 0, winreg.KEY_ALL_ACCESS)

with open("cosmetics.json") as file:
    cosmetics = json.load(file)

def editKey(raw_slot:str, value:int):
    match raw_slot:
        case "OUTFIT": slot = "Skin_h2089423610"
        case "KNIFE": slot = "Knife_h221345514"
        case "AK": slot = "AK_h5861935"
    winreg.SetValueEx(KEY, slot, 0, winreg.REG_DWORD, value)

def readKey(slot:str):
    return winreg.QueryValueEx(KEY, slot)[0]

def getName(type:str, id:int):
    for skin in cosmetics[type]:
        if skin[0] == int(id):
            return skin[1]

def showCommands():
    print("** ALL COMMANDS")
    print("- /SET -> slot -> id")
    print("- /SLOTS")
    print("- /IDS -> slot")
    print("- /CURRENT")
    print("- /HELP")

def newCommand():
    command = input("\n>>> ").upper()

    match command:
        case "/SET":
            try:
                slot_choice = input("SLOT: ").upper()
                if slot_choice == "ABORT":
                    newCommand()
                else:
                    id_choice = input("ID: ")
                    if id_choice == "ABORT":
                        newCommand()
                    else:
                        editKey(slot_choice, int(id_choice))
                        print(f"Your skin has been changed to {getName(slot_choice, int(id_choice))}")

            except Exception as e:
                print(f"FATAL ERROR: \n{e}")
        
        case "/SLOTS":
            try:
                print("*** SUPPORTED SLOTS")
                print("- OUTFIT")
                print("- KNIFE")
                print("- AK")
            except Exception as e:
                print(f"FATAL ERROR: \n{e}")
            
        case "/IDS":
            try:
                slot_choice = input("SLOT: ").upper()
                if slot_choice == "ABORT":
                    newCommand()
                else:
                    for skin in cosmetics[slot_choice]:
                        print(f"{str(skin[0]).rjust(2, '0')} : {skin[1]}")
            except Exception as e:
                print(f"FATAL ERROR: \n{e}")

        case "/CURRENT":
            try:
                print(f'SKIN: {str(readKey("Skin_h2089423610")).rjust(2, "0")} | {getName("OUTFIT", readKey("Skin_h2089423610"))}')
                print(f'KNIFE: {str(readKey("Knife_h221345514")).rjust(2, "0")} | {getName("KNIFE", readKey("Knife_h221345514"))}')
                print(f'AK: {str(readKey("AK_h5861935")).rjust(2, "0")} | {getName("AK", readKey("AK_h5861935"))}')
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
