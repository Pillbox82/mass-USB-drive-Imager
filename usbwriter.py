'''
Norman USB Imager:
Dit script is bedoeld om snel grote hoeveelheden USB drives te imagen. (bijv. Norman Rescue Disk.
'''
__Author__ = "Jeroen Hentschke"

#Importeer Regex
import re
#Importeer subprocess om shell commando's te kunnen gebruiken
import subprocess
#importeer listdir om de /dev/ directory te kunnen uitlezen
from os import listdir

# In de list usbdrives slaan we de drives op die we willen beschrijven
usbdrives=[]

# In contents slaan we alle items op die in /dev/ staan en sorteren alfabetisch met .sort()
contents = listdir("/dev/")
contents.sort()

# We halen alleen de devices uit contents die we daadwerkelijk nodig hebben (de sda drives)
for items in contents:
    match = re.search('sd[a-z]*[a-z]$', items)
    if match:
        usbdrives.append(items)
usbdrives.sort()        

# sda is de harddisk, deze mag niet beschreven worden anders ligt het systeem plat! Deze moet er dus uit!
for drive in usbdrives:
    if drive == "sda":
        usbdrives.pop(usbdrives.index(drive))

# Voor iedere drive die overblijft printen wij op het scherm dat de drive is gevonden en gebruikt zal worden voor het imagebestand
print "Er zijn in totaal "+ str(len(usbdrives)) + " aangesloten."

# De gebruiker voert de naam van het bronbestand in. Dit script bevat nog niet de functionaliteit om te checken of het bestand wel bestaat. 
bronbestand = raw_input("\nVoer bronbestand in:")

# command is een string die uiteindelijk het commando gaat bevatten dat wordt uitgevoerd, het begin kunnen we alvast maken.
command = "pv " + bronbestand + " | tee >"

# hieronder bouwen we verder aan de command. Voor iedere drive die gevonden wordt voegen we een stukje toe aan de command.
# Het stukje van de laatste en voorlaatste drive zijn iets anders daarom hebben ze hun eigen voorwaarde (if)
for drive in usbdrives:
    if usbdrives.index(drive) == len(usbdrives)-1:
        command = command + "| dd of=/dev/%s bs=32M conv=notrunc" % drive
    elif usbdrives.index(drive) == len(usbdrives)-2:
        command = command + "(dd of=/dev/%s bs=32M conv=notrunc) " % drive
    else:
        command = command + "(dd of=/dev/%s bs=32M conv=notrunc) >" % drive

# Hiermee checken we of het commando wel klopt
print "\nHet commando dat uitgevoerd zal worden is: " + command

# Een ietwat simpele lompe manier om de gebruiker de kans te geven om te stoppen
raw_input "Druk op Enter om door te gaan of CTRL-C om te stoppen: "

# Hier wordt het opgebouwde commando daadwerkelijk uitgevoerd via subprocess met shell=True en de shell die gebruikt wordt is /bin/bash
subprocess.call(command, shell=True, executable='/bin/bash')