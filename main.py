import winreg
import json
import os
from time import *

KEY = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\\ShibaFlow\\Tactical Duty", 0, winreg.KEY_ALL_ACCESS)

class formatter:
    GREY = '\033[90m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    AQUA = '\033[96m'
    END = '\033[0m'

with open("cosmetics.json") as file:
    cosmetics = json.load(file)

SUPPORTED_SLOTS = []
for key in cosmetics.keys():
    SUPPORTED_SLOTS.append(key)

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
        if skin[0] == id:
            return skin[1]
        
def error(errorMessage:str):
    print(f"{formatter.RED}[ERROR] {errorMessage}{formatter.END}")

def abort():
    print(f"{formatter.RED}[WARNING] Process aborted.{formatter.END}")
    newCommand()

def newCommand():
    print("\n" + "-" * 120 + "\n")
    raw_command = input(f"{formatter.YELLOW}> / {formatter.END}").upper()
    if raw_command.startswith("/"): command = raw_command
    else: command = "/" + raw_command

    match command:
        case "/SET":
            try:
                slot_choice = input(f"{formatter.AQUA}SLOT: {formatter.END}").upper()
                if slot_choice == "ABORT":
                    abort()
                elif not slot_choice in SUPPORTED_SLOTS:
                    error("Invalid slot. Use /SLOTS for a list.")
                else:
                    id_choice = input(f"{formatter.AQUA}ID: {formatter.END}").upper()
                    if id_choice == "ABORT":
                        abort()
                    else:
                        editKey(slot_choice, int(id_choice))
                        print(f"{formatter.GREEN}[SUCCESS] Your skin has been changed to {getName(slot_choice, int(id_choice))}{formatter.END}")

            except Exception as e:
                error(e)
        
        case "/SLOTS":
            try:
                for key in SUPPORTED_SLOTS:
                    print(f"{formatter.AQUA}{key}{formatter.END}")

            except Exception as e:
                error(e)
            
        case "/IDS":
            try:
                slot_choice = input(f"{formatter.AQUA}SLOT: {formatter.END}").upper()
                if slot_choice == "ABORT":
                    abort()
                elif not slot_choice in SUPPORTED_SLOTS:
                    error("Invalid slot. Use /SLOTS for a list.")
                else:
                    for skin in cosmetics[slot_choice]:
                        print(f"{str(skin[0]).rjust(2, '0')} : {skin[1]}")
            except Exception as e:
               error(e)

        case "/CURRENT":
            try:
                print(f'{formatter.AQUA}SKIN: {formatter.END}{str(readKey("Skin_h2089423610")).rjust(2, "0")} : {getName("OUTFIT", readKey("Skin_h2089423610"))}')
                print(f'{formatter.AQUA}KNIFE: {formatter.END}{str(readKey("Knife_h221345514")).rjust(2, "0")} : {getName("KNIFE", readKey("Knife_h221345514"))}')
                print(f'{formatter.AQUA}AK: {formatter.END}{str(readKey("AK_h5861935")).rjust(2, "0")} : {getName("AK", readKey("AK_h5861935"))}')
            except Exception as e:
                error(e)

        case "/HELP":
            try:
                print(f"{formatter.AQUA}Setting skins:{formatter.END}\nFirst, we use {formatter.GREY}/SET{formatter.END} to trigger the command that will change the skin for us.\nWe'll be asked to choose the slot, just type it in. For a list of slots, use {formatter.GREY}/SLOTS.{formatter.END}\nThe last step is to type in the id of the skin we want.")
                print(f"\n{formatter.AQUA}Getting skin IDs:{formatter.END}\nRun {formatter.GREY}/IDS{formatter.END}.\nType in the slot you want an IDs list for. (knife, AK, etc.)")
                print(f"\n{formatter.AQUA}What are slots?{formatter.END}\nSlots are basically just elements of your TD locker. So for example outfit or a knife.\nFor a full list of slots supported by this Skin Changer, simple run {formatter.GREY}/SLOTS{formatter.END}.")
                print(f"\n{formatter.AQUA}Other commands:{formatter.END}\n{formatter.GREY}/CURRENT{formatter.END} - Sends your current TD locker.\n{formatter.GREY}/HELP{formatter.END} - Sends this guide.\n{formatter.GREY}/EXIT{formatter.END} - Kills the process. Click Ctrl+C to cancel.\n{formatter.GREY}/CLEAR{formatter.END} - Cleans the terminal up.")
                print(f"\n{formatter.AQUA}Protips:{formatter.END}\nYou don't have to use the upper case.\nYou don't have to put a slash before each command.\nMore tips in the github repo README.md!")
            except Exception as e:
                error(e)

        case "/ANIMEBIGBONKERS":
            try:
                eval(bytearray.fromhex("7072696E74286279746561727261792E66726F6D686578282236373635373432303638363536433730323036323732364622292E6465636F6465282929"))
            except Exception as e:
                error(e)

        case "/EXIT":
            try:
                for i in range(4, -1, -1):
                    print(f"{formatter.RED}TIME LEFT: {i/2}s {formatter.END}")
                    sleep(0.5)
                raise SystemExit
            except KeyboardInterrupt:
                print("Process termination cancelled.")
                newCommand()

        case "/CLEAR":
            try:
                startup()
            except Exception as e:
                error(e)

        case _:
            try:
                error("Unknown command. Use /HELP for a list.")
            except Exception as e:
                error(e)

    newCommand()

def startup():
    
    os.system("cls")
    os.system("title TD Skin Changer")

    print(f"{formatter.YELLOW}TacticalDutyio Skin Changer by Creaffy\nhttps://github.com/creaffy/TD-SkinChanger/{formatter.END}")
    print(f"{formatter.AQUA}Run /HELP for a guide.{formatter.END}")

    newCommand()

startup()
