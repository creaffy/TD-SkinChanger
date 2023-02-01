import winreg
import json
import os
from colored import fg, bg, attr
from time import *

KEY = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\\ShibaFlow\\Tactical Duty", 0, winreg.KEY_ALL_ACCESS)

class formatter:
    RED = fg('#ff4545')
    ORANGE = fg('#ff8636')
    YELLOW = fg('#ffc936')
    GREEN = fg('#4dff6a')
    AQUA = fg('#46e8ba')
    BLUE = fg('#4692e8')
    PURPLE = fg('#9356f5')
    PINK = fg('#e856f5')
    END = attr('reset')

with open("cosmetics.json") as file:
    cosmetics = json.load(file)

SUPPORTED_SLOTS = []
for key in cosmetics.keys():
    SUPPORTED_SLOTS.append(key)

ABBREVIATIONS = [
    {
        "slot": "OUTFIT",
        "alias": ["OTF", "OUT", "OUTFIT"]
    },{
        "slot": "KNIFE",
        "alias": ["KNI", "KNF", "KNIFE"]
    },{
        "slot": "AK",
        "alias": ["AK47", "AK"]
    }
]
                
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
    print(f"{formatter.ORANGE}[WARNING] Process aborted.{formatter.END}")
    newCommand()

def validateSlot(abbreviation:str):
    if abbreviation in ABBREVIATIONS[0]['alias']: return "OUTFIT"
    elif abbreviation in ABBREVIATIONS[1]['alias']: return "KNIFE"
    elif abbreviation in ABBREVIATIONS[2]['alias']: return "AK"
    else: return None

def newCommand():
    try:
        print("\n" + "-" * 120 + "\n")
        command = input(f"{formatter.YELLOW}> / {formatter.END}").upper().replace("/", "").split()

        match command[0]:
            case "SET" | "SKIN" | "S":
                match len(command):
                    case 1:
                        slot_choice = input(f"{formatter.AQUA}SLOT: {formatter.END}").upper()
                        if slot_choice in ["ABORT", "A"]:
                            abort()
                        elif validateSlot(slot_choice) is None:
                            error("Invalid slot. Use /SLOTS for a list.")
                        else:
                            id_choice = input(f"{formatter.AQUA}ID: {formatter.END}").upper()
                            if id_choice in ["ABORT", "A"]:
                                abort()
                            else:
                                editKey(validateSlot(slot_choice), int(id_choice))
                                print(f"{formatter.GREEN}[SUCCESS] Your skin has been changed to {getName(validateSlot(slot_choice), int(id_choice))}{formatter.END}")
                    case 2: error("Too little arguments.")
                    case 3:
                        if validateSlot(command[1]) is None:
                            error("Invalid abbreviation.")
                        else:
                            editKey(validateSlot(command[1]), int(command[2]))
                            print(f"{formatter.GREEN}[SUCCESS] Your skin has been changed to {getName(validateSlot(command[1]), int(command[2]))}{formatter.END}")
                    case _: error("Too many arguments.")
            
            case "SLOTS" | "SLOT":
                for key in SUPPORTED_SLOTS:
                    print(f"{formatter.AQUA}{key}{formatter.END}")

            case "IDS" | "ID":
                match len(command):
                    case 1:
                        slot_choice = input(f"{formatter.AQUA}SLOT: {formatter.END}").upper()
                        if slot_choice in ["ABORT", "A"]:
                            abort()
                        elif validateSlot(slot_choice) is None:
                            error("Invalid slot. Use /SLOTS for a list.")
                        else:
                            for skin in cosmetics[validateSlot(slot_choice)]:
                                print(f"{formatter.AQUA}{str(skin[0]).rjust(2, '0')} : {skin[1]}{formatter.END}")
                    case 2:
                        if validateSlot(command[1]) is None:
                            error("Invalid abbreviation.")
                        else:
                            for skin in cosmetics[validateSlot(command[1])]:
                                print(f"{formatter.AQUA}{str(skin[0]).rjust(2, '0')} : {skin[1]}{formatter.END}")
                    case _: error("Too many arguments.")
                    
            case "CURRENT" | "LOCKER":
                print(f'{formatter.AQUA}SKIN: {formatter.END}{str(readKey("Skin_h2089423610")).rjust(2, "0")} : {getName("OUTFIT", readKey("Skin_h2089423610"))}')
                print(f'{formatter.AQUA}KNIFE: {formatter.END}{str(readKey("Knife_h221345514")).rjust(2, "0")} : {getName("KNIFE", readKey("Knife_h221345514"))}')
                print(f'{formatter.AQUA}AK: {formatter.END}{str(readKey("AK_h5861935")).rjust(2, "0")} : {getName("AK", readKey("AK_h5861935"))}')

            case "ABBREVIATIONS" | "ABBREVIATION" | "ABBR" | "ABB":
                for element in ABBREVIATIONS:
                    print(formatter.AQUA + element['slot'] + formatter.END + " : " + formatter.YELLOW + ' '.join(element['alias'][:-1]) + formatter.END)

            case "ALIAS" | "AL":
                ALIAS = [
                    {
                        "command": "/SET",
                        "alias": ["/SKIN", "/S"]
                    },{
                        "command": "/SLOTS",
                        "alias": ["/SLOT"]
                    },{
                        "command": "/IDS",
                        "alias": ["ID"]
                    },{
                        "command": "/CURRENT",
                        "alias": ["/LOCKER"]
                    },{
                        "command": "/ABBREVIATIONS",
                        "alias": ["/ABBREVIATION", "/ABBR", "ABB"]
                    },{
                        "command": "/ALIAS",
                        "alias": ["/AL"]
                    },{
                        "command": "/HELP",
                        "alias": ["/GUIDE", "/H"]
                    },{
                        "command": "/EXIT",
                        "alias": ["/QUIT", "/CLOSE", "/KILL"]
                    },{
                        "command": "/CLEAR",
                        "alias": ["/C"]
                    },
                ]

                for element in ALIAS:
                    print(formatter.AQUA + element['command'] + formatter.END + " : " + formatter.YELLOW + ' '.join(element['alias']) + formatter.END)



            case "HELP" | "GUIDE" | "H":
                print(f"{formatter.AQUA}Setting skins:{formatter.END}\nFirst, we use {formatter.BLUE}/SET{formatter.END} to trigger the command that will change the skin for us.\nWe'll be asked to choose the slot, just type it in. For a list of slots, use {formatter.BLUE}/SLOTS.{formatter.END}\nThe last step is to type in the id of the skin we want.")
                print(f"\n{formatter.AQUA}Getting skin IDs:{formatter.END}\nRun {formatter.BLUE}/IDS{formatter.END}.\nType in the slot you want an IDs list for. (knife, AK, etc.)")
                print(f"\n{formatter.AQUA}What are slots?{formatter.END}\nSlots are basically just elements of your TD locker. So for example outfit or a knife.\nFor a full list of slots supported by this Skin Changer, simple run {formatter.BLUE}/SLOTS{formatter.END}.")
                print(f"\n{formatter.AQUA}Other commands:{formatter.END}\n{formatter.BLUE}/CURRENT{formatter.END} - Sends your current TD locker.\n{formatter.BLUE}/HELP{formatter.END} - Sends this guide.\n{formatter.BLUE}/EXIT{formatter.END} - Kills the process. Click Ctrl+C to cancel.\n{formatter.BLUE}/CLEAR{formatter.END} - Cleans the terminal up.")
                print(f"\n{formatter.AQUA}Protips:{formatter.END}\nYou don't have to use the upper case.\nYou don't have to put a slash before each command.\nMore tips in the github repo README.md!")

            case "ANIMEBIGBONKERS":
                eval(bytearray.fromhex("7072696E74286279746561727261792E66726F6D686578282236373635373432303638363536433730323036323732364622292E6465636F6465282929"))

            case "EXIT" | "QUIT" | "CLOSE" | "KILL":
                try:
                    for i in range(4, -1, -1):
                        print(f"{formatter.RED}TIME LEFT: {i/2}s {formatter.END}")
                        sleep(0.5)
                    raise SystemExit
                except KeyboardInterrupt:
                    print("Process termination cancelled.")
                    newCommand()

            case "CLEAR" | "C":
                startup()

            case _:
                error("Unknown command. Use /HELP for a list.")

        newCommand()
    except Exception as e:
        error(e)
        newCommand()

def startup():
    
    os.system("cls")
    os.system("title TD Skin Changer")

    print(f"{formatter.BLUE}TacticalDuty.io Skin Changer by Creaffy\nhttps://github.com/creaffy/TD-SkinChanger/{formatter.END}")
    print(f"{formatter.AQUA}Run /HELP for a guide.{formatter.END}")

    newCommand()

startup()
