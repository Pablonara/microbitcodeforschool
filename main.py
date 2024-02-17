# lite version to avoid mem issues
from microbit import *
import radio, os, random
def read():
    with open('foo.txt') as my_file:
        content = my_file.read()
def write(text):
    file = open("foo.txt", "w")
    file.write(text)
    file.close()
    
def getButton():
    while True:
        if button_a.was_pressed():
            return 'a'
        elif button_b.was_pressed():
            return 'b'
        sleep(100)

def getButtonWithAB():
    if button_a.is_pressed() and button_b.is_pressed():
        return 'ab'
    elif button_a.was_pressed():
        return 'a'
    elif button_b.was_pressed():
        return 'b'
    sleep(100)


def getrpschoice(poll):
    choices = [('90009:' #scissors
'09090:'
'00900:'
'99099:'
'99099'), 
('00000:' #rock
 '09990:'
 '09990:'
 '09990:'
 '00000'), ('99990:' #paper
 '09999:'
 '99990:'
 '09999:'
 '99990')]    
    if poll == True: #rpslizspock
        choices.append( #this is lizard
('99999:'
 '90000:'
 '90000:'
 '90000:'
 '99999'))
        choices.append( #i have bad art skills, this is spock
            ('00000:'
 '99099:'
 '99099:'
 '09990:'
 '00000')
        )
    count = 0
    display.show(Image(choices[count]))
    while True:
        if button_a.is_pressed() and button_b.is_pressed():
            display.show(Image(choices[count]))
            tostring = ['scissors', 'rock', 'paper', 'lizard', 'spock']
            return tostring[count]
        elif button_a.was_pressed():
            if count == 0 and not poll:
                count = 2
            elif count == 0: #rpsls
                count = 4
            else:
                count -= 1
            display.show(Image(choices[count]))
        elif button_b.was_pressed():
            if count == 2 and not poll:
                count = 0
            elif count == 4:
                count = 0
            else:
                count += 1
            display.show(Image(choices[count]))
key = 'dWyNlXY7RuYIAqg8N2K3A'
def sendEncrypt(message, key): #just implemented simple XOR encryption for fun
    radio.send(message) #ran out of memory, will add tomorrow

def recieveEncrypt(key):
    while True:
        if button_b.was_pressed():
            breakfromloop = True
            return
        a = radio.receive()
        if a:
            return a

def count():
    count = 0
    display.show(count)
    while True:
        if button_a.is_pressed() and button_b.is_pressed():
            display.show(count)
            print(count)
            return count
        elif button_a.was_pressed() and count >0:
            count -= 1
            print(count)
            display.show(count)
        elif button_b.was_pressed() and count<9:
            count += 1
            print(count)
            display.show(count)
            
hostmode = ''
input1 = ''
radio.on()
radio.config(group=128, power=7)
connected = []
allchoices = []
connected.append("1")
breakfromloop = False
rpslizspock = False
print("Press A to host game, B to not host game")
input1 = getButton()
playerid = 0
if input1 == 'a':
    hostmode = 'host'
    radio.send("join")
elif input1 == 'b':
    hostmode = 'search'
    print('waiting for host to broadcast...')

print("searching on channel 128")
print("Press reset to cancel operation, b to continue")
if hostmode == 'host': 
    while breakfromloop == False:
        if button_b.is_pressed(): #some wierd issue with button_b.was_pressed() not working. Super wierd issue, probably the way async works on the microbit
            print("Button B pressed. Press again to stop new connections and enter game mode")
            breakfromloop = True
        if recieveEncrypt(key) == 'accepted': #handshake     
            connected.append(int(connected[-1])+1)
            sendEncrypt(str(connected[-1]), key)
            print("1 user connected")
    breakfromloop = False #run under assumption only way to reach here is if breakfromloop is true
    print("Choose how much AI in game (limit 9)")
    ainum = count()
    print("A for RPS, B for RPSLIZSPOCK")
    input1 = getButton()
    if input1 == 'a':
        rpslizspock = False
    elif input1 == 'b':
        rpslizspock = True
        sendEncrypt('True', key)
    sendEncrypt('starting', key)
    sleep(300)
    
    for i in range(1, (len(connected)+1)):
        if i == 1:
            a = getrpschoice(False)
            allchoices.append((a, playerid))
            for i in range(ainum):
                allchoices.append((random.choice(['rock', 'spock', 'paper', 'lizard', 'scissors']) if rpslizspock==True else random.choice(['rock', 'paper', 'scissors']), i*-1))
        else:
            sendEncrypt('p'+str(connected[i-1])+'turn', key)
            choice = recieveEncrypt(key)
    while len(allchoices) != 1:
        for i in range(len(allchoices)):
            if rpslizspock and len(allchoices)>1:
                choice, id = allchoices.pop(random.randint(0, len(allchoices)-1))
                choice1, id1 = allchoices.pop(random.randint(0, len(allchoices)-1))
                indexer = ['rock', 'spock', 'paper', 'lizard', 'scissors']
                print(choice+str(id))
                print(choice1+str(id1))
                choice = indexer.index(choice.lower())
                choices1 = indexer.index(choice1.lower())
                difference = (choice - choices1) % 5
                if difference in [1, 2]: #player1 win
                    sendEncrypt(('p'+str(id1)+'eliminated') if id1>=0 else ('ai'+str(id1*-1)+'eliminated'), key)
                    if id1 == 0:
                        choice1 = getrpschoice(False)
                        allchoices.append((choice1, id1))
                    elif id1>0:
                        sendEncrypt('p'+str(id1)+'turn', key)
                        allchoices.append((recieveEncrypt(key), id1))
                    elif id1<0:
                        allchoices.append((random.choice(['rock', 'spock', 'paper', 'lizard', 'scissors']) if rpslizspock==True else random.choice(['rock', 'paper', 'scissors']), id1))
                elif difference in [3, 4]: #player0 win
                    sendEncrypt(('p'+str(id)) if id>=0 else ('ai'+str(id*-1)), key)
                    if id == 0:
                        choice = getrpschoice(False)
                        allchoices.append((choice, id))
                    elif id>0:
                        sendEncrypt('p'+str(id)+'turn', key)
                        allchoices.append((recieveEncrypt(key), id))
                    elif id<0:
                        allchoices.append((random.choice(['rock', 'spock', 'paper', 'lizard', 'scissors']) if rpslizspock==True else random.choice(['rock', 'paper', 'scissors']), id))
                else: #tie
                    sendEncrypt('tie', key)
                    if id == 0:
                        choice = getrpschoice(False)
                        allchoices.append((choice, id))
                    elif id>0:
                        sendEncrypt('p'+str(id)+'turn', key)
                        allchoices.append((recieveEncrypt(key), id))
                    elif id<0:
                        allchoices.append((random.choice(['rock', 'spock', 'paper', 'lizard', 'scissors']) if rpslizspock==True else random.choice(['rock', 'paper', 'scissors']), id))
                        sendEncrypt(('p'+str(id1)+'eliminated') if id1>=0 else ('ai'+str(id1*-1)+'eliminated'), key)
                    if id1 == 0:
                        choice1 = getrpschoice(False)
                        allchoices.append((choice1, id1))
                    elif id1>0:
                        sendEncrypt('p'+str(id1)+'turn', key)
                        allchoices.append((recieveEncrypt(key), id1))
                    elif id1<0:
                        allchoices.append((random.choice(['rock', 'spock', 'paper', 'lizard', 'scissors']) if rpslizspock==True else random.choice(['rock', 'paper', 'scissors']), id1))
                    allchoices.append((choice1, id1))
            elif (not rpslizspock) and len(allchoices)>1:
                choice, id = allchoices.pop(random.randint(0, len(allchoices)-1))
                choice1, id1 = allchoices.pop(random.randint(0, len(allchoices)-1))
                print(choice+str(id))
                print(choice1+str(id1))
                indexer = ['rock', 'spock', 'paper', 'lizard', 'scissors']
                choice = indexer.index(choice.lower())
                choices1 = indexer.index(choice1.lower())
                difference = (choice - choices1) % 3
                if difference in [1]: #player1 win
                    sendEncrypt(('p'+str(id1)+'eliminated') if id1>=0 else ('ai'+str(id1*-1)+'eliminated'), key)
                    if id1 == 0:
                        choice1 = getrpschoice(False)
                        allchoices.append((choice1, id1))
                    elif id1>0:
                        sendEncrypt('p'+str(id1)+'turn', key)
                        allchoices.append((recieveEncrypt(key), id1))
                    elif id1<0:
                        allchoices.append((random.choice(['rock', 'spock', 'paper', 'lizard', 'scissors']) if rpslizspock==True else random.choice(['rock', 'paper', 'scissors']), id1))
                elif difference in [2]: #player0 win
                    sendEncrypt(('p'+str(id)) if id>=0 else ('ai'+str(id*-1)), key)
                    if id == 0:
                        choice = getrpschoice(False)
                        allchoices.append((choice, id))
                    elif id>0:
                        sendEncrypt('p'+str(id)+'turn', key)
                        allchoices.append((recieveEncrypt(key), id))
                    elif id<0:
                        allchoices.append((random.choice(['rock', 'spock', 'paper', 'lizard', 'scissors']) if rpslizspock==True else random.choice(['rock', 'paper', 'scissors']), id))
                else: #tie
                    sendEncrypt('tie', key)
                    if id == 0:
                        choice = getrpschoice(False)
                        allchoices.append((choice, id))
                    elif id>0:
                        sendEncrypt('p'+str(id)+'turn', key)
                        allchoices.append((recieveEncrypt(key), id))
                    elif id<0:
                        allchoices.append((random.choice(['rock', 'spock', 'paper', 'lizard', 'scissors']) if rpslizspock==True else random.choice(['rock', 'paper', 'scissors']), id))
                        sendEncrypt(('p'+str(id1)+'eliminated') if id1>=0 else ('ai'+str(id1*-1)+'eliminated'), key)
                    if id1 == 0:
                        choice1 = getrpschoice(False)
                        allchoices.append((choice1, id1))
                    elif id1>0:
                        sendEncrypt('p'+str(id1)+'turn', key)
                        allchoices.append((recieveEncrypt(key), id1))
                    elif id1<0:
                        allchoices.append((random.choice(['rock', 'spock', 'paper', 'lizard', 'scissors']) if rpslizspock==True else random.choice(['rock', 'paper', 'scissors']), id1))
                    allchoices.append((choice1, id1))
    winner = allchoices[0][1]
    sendEncrypt('win'+str(winner), key)
    print(("Winner! Player#"+str(winner+1)) if winner>=0 else ("Winner! Ai#"+str(winner)))
    
else:
    eliminated = False
    poll = False
    playerid = -1
    a = recieveEncrypt(key)
    if a == 'join':
        sendEncrypt('accepted', key)
        sleep(20)
        playerid = recieveEncrypt(key)
    if a == 'True':
        poll = True
    if a == 'starting':
        while not eliminated:
            a = recieveEncrypt(key)
            if a == 'p'+str(playerid)+'turn':
                sendEncrypt(str(getrpschoice(poll)), key)
            if a == 'p'+str(playerid)+'eliminated':
                print('Player eliminated!')
                a = ''
            elif str(a).endswith('eliminated'):
                a = str(a).replace('eliminated', '')
                print('Player '+a[1:]+' eliminated!')
                a = ''
            elif str(a) == 'tie':
                print("Tie! No one was eliminated.")
            elif str(a).startswith('win'):
                winner = int(str(a)[3:])
                print("Winner! "+str("Winner! Player#"+str(winner+1)) if winner>=0 else ("Winner! Ai#"+str(winner)))

