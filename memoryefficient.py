_Q='Winner! Ai#'
_P='Winner! Player#'
_O='starting'
_N='accepted'
_M='foo.txt'
_L='tie'
_K='ai'
_J='turn'
_I='eliminated'
_H='spock'
_G='lizard'
_F=False
_E='p'
_D=True
_C='paper'
_B='rock'
_A='scissors'
from microbit import*
import radio,os,random
def read():
	with open(_M)as my_file:content=my_file.read()
def write(text):file=open(_M,'w');file.write(text);file.close()
def getButton():
	while _D:
		if button_a.was_pressed():return'a'
		elif button_b.was_pressed():return'b'
		sleep(100)
def getButtonWithAB():
	if button_a.is_pressed()and button_b.is_pressed():return'ab'
	elif button_a.was_pressed():return'a'
	elif button_b.was_pressed():return'b'
	sleep(100)
def getrpschoice(poll):
	choices=['90009:09090:00900:99099:99099','00000:09990:09990:09990:00000','99990:09999:99990:09999:99990'];count=0;display.show(Image(choices[count]))
	while _D:
		if button_a.is_pressed()and button_b.is_pressed():display.show(Image(choices[count]));tostring=[_A,_B,_C,_G,_H];return tostring[count]
		elif button_a.was_pressed():
			if count==0 and not poll:count=2
			elif count==0:count=4
			else:count-=1
			display.show(Image(choices[count]))
		elif button_b.was_pressed():
			if count==2 and not poll:count=0
			elif count==4:count=0
			else:count+=1
			display.show(Image(choices[count]))
key='dWyNlXY7RuYIAqg8N2K3A'
def sendEncrypt(message,key):radio.send(message)
def recieveEncrypt(key):
	while _D:
		a=radio.receive()
		if a:return a
def count():
	count=0;display.show(count)
	while _D:
		if button_a.is_pressed()and button_b.is_pressed():display.show(count);print(count);return count
		elif button_a.was_pressed()and count>0:count-=1;print(count);display.show(count)
		elif button_b.was_pressed()and count<9:count+=1;print(count);display.show(count)
hostmode=''
input1=''
radio.on()
radio.config(group=128,power=7)
connected=[]
allchoices=[]
connected.append('1')
breakfromloop=_F
rpslizspock=_F
print('Press A to host game, B to not host game')
input1=getButton()
playerid=0
if input1=='a':hostmode='host';radio.send('join')
elif input1=='b':hostmode='search';print('waiting for host to broadcast...')
print('searching on channel 128')
print('Press reset to cancel operation, b to continue')
if hostmode=='host':
	while breakfromloop==_F:
		if button_b.is_pressed():print('Button B pressed. Press again to stop new connections and enter game mode');breakfromloop=_D
		if recieveEncrypt(key)==_N:connected.append(int(connected[-1])+1);sendEncrypt(str(connected[-1]),key);print('1 user connected')
	breakfromloop=_F;print('Choose how much AI in game (limit 9)');ainum=count();print('A for RPS, B for RPSLIZSPOCK');input1=getButton()
	if input1=='a':rpslizspock=_F
	elif input1=='b':rpslizspock=_D;sendEncrypt('True',key)
	sendEncrypt(_O,key);sleep(300)
	for i in range(1,len(connected)+1):
		if i==1:
			a=getrpschoice(_F);allchoices.append((a,playerid))
			for i in range(ainum):allchoices.append((random.choice([_B,_H,_C,_G,_A])if rpslizspock==_D else random.choice([_B,_C,_A]),i*-1))
		else:sendEncrypt(_E+str(connected[i-1])+_J,key);choice=recieveEncrypt(key)
	while len(allchoices)!=1:
		for i in range(len(allchoices)):
			if rpslizspock and len(allchoices)>1:
				choice,id=allchoices.pop(random.randint(0,len(allchoices)-1));choice1,id1=allchoices.pop(random.randint(0,len(allchoices)-1));indexer=[_B,_H,_C,_G,_A];print(choice+str(id));print(choice1+str(id1));choice=indexer.index(choice.lower());choices1=indexer.index(choice1.lower());difference=(choice-choices1)%5
				if difference in[1,2]:
					sendEncrypt(_E+str(id1)+_I if id1>=0 else _K+str(id1*-1)+_I,key)
					if id1==0:choice1=getrpschoice(_F);allchoices.append((choice1,id1))
					elif id1>0:sendEncrypt(_E+str(id1)+_J,key);allchoices.append((recieveEncrypt(key),id1))
					elif id1<0:allchoices.append((random.choice([_B,_H,_C,_G,_A])if rpslizspock==_D else random.choice([_B,_C,_A]),id1))
				elif difference in[3,4]:
					sendEncrypt(_E+str(id)if id>=0 else _K+str(id*-1),key)
					if id==0:choice=getrpschoice(_F);allchoices.append((choice,id))
					elif id>0:sendEncrypt(_E+str(id)+_J,key);allchoices.append((recieveEncrypt(key),id))
					elif id<0:allchoices.append((random.choice([_B,_H,_C,_G,_A])if rpslizspock==_D else random.choice([_B,_C,_A]),id))
				else:
					sendEncrypt(_L,key)
					if id==0:choice=getrpschoice(_F);allchoices.append((choice,id))
					elif id>0:sendEncrypt(_E+str(id)+_J,key);allchoices.append((recieveEncrypt(key),id))
					elif id<0:allchoices.append((random.choice([_B,_H,_C,_G,_A])if rpslizspock==_D else random.choice([_B,_C,_A]),id));sendEncrypt(_E+str(id1)+_I if id1>=0 else _K+str(id1*-1)+_I,key)
					if id1==0:choice1=getrpschoice(_F);allchoices.append((choice1,id1))
					elif id1>0:sendEncrypt(_E+str(id1)+_J,key);allchoices.append((recieveEncrypt(key),id1))
					elif id1<0:allchoices.append((random.choice([_B,_H,_C,_G,_A])if rpslizspock==_D else random.choice([_B,_C,_A]),id1))
					allchoices.append((choice1,id1))
			elif not rpslizspock and len(allchoices)>1:
				choice,id=allchoices.pop(random.randint(0,len(allchoices)-1));choice1,id1=allchoices.pop(random.randint(0,len(allchoices)-1));print(choice+str(id));print(choice1+str(id1));indexer=[_B,_H,_C,_G,_A];choice=indexer.index(choice.lower());choices1=indexer.index(choice1.lower());difference=(choice-choices1)%3
				if difference in[1]:
					sendEncrypt(_E+str(id1)+_I if id1>=0 else _K+str(id1*-1)+_I,key)
					if id1==0:choice1=getrpschoice(_F);allchoices.append((choice1,id1))
					elif id1>0:sendEncrypt(_E+str(id1)+_J,key);allchoices.append((recieveEncrypt(key),id1))
					elif id1<0:allchoices.append((random.choice([_B,_H,_C,_G,_A])if rpslizspock==_D else random.choice([_B,_C,_A]),id1))
				elif difference in[2]:
					sendEncrypt(_E+str(id)if id>=0 else _K+str(id*-1),key)
					if id==0:choice=getrpschoice(_F);allchoices.append((choice,id))
					elif id>0:sendEncrypt(_E+str(id)+_J,key);allchoices.append((recieveEncrypt(key),id))
					elif id<0:allchoices.append((random.choice([_B,_H,_C,_G,_A])if rpslizspock==_D else random.choice([_B,_C,_A]),id))
				else:
					sendEncrypt(_L,key)
					if id==0:choice=getrpschoice(_F);allchoices.append((choice,id))
					elif id>0:sendEncrypt(_E+str(id)+_J,key);allchoices.append((recieveEncrypt(key),id))
					elif id<0:allchoices.append((random.choice([_B,_H,_C,_G,_A])if rpslizspock==_D else random.choice([_B,_C,_A]),id));sendEncrypt(_E+str(id1)+_I if id1>=0 else _K+str(id1*-1)+_I,key)
					if id1==0:choice1=getrpschoice(_F);allchoices.append((choice1,id1))
					elif id1>0:sendEncrypt(_E+str(id1)+_J,key);allchoices.append((recieveEncrypt(key),id1))
					elif id1<0:allchoices.append((random.choice([_B,_H,_C,_G,_A])if rpslizspock==_D else random.choice([_B,_C,_A]),id1))
					allchoices.append((choice1,id1))
	winner=allchoices[0][1];sendEncrypt('win'+str(winner),key);print(_P+str(winner+1)if winner>=0 else _Q+str(winner))
else:
	eliminated=_F;poll=_F;playerid=-1
	while _D:
		a=recieveEncrypt(key)
		if a=='join':sendEncrypt(_N,key);sleep(20);playerid=recieveEncrypt(key)
		if a=='True':poll=_D
		if a==_O:
			print('game starting....')
			while not eliminated:
				a=recieveEncrypt(key)
				if a==_E+str(playerid)+_J:print('Choose your option');b=str(getrpschoice(poll));sendEncrypt(b,key)
				if a==_E+str(playerid)+_I:print('Player eliminated!');eliminated=_D;a=''
				elif str(a).endswith(_I):a=str(a).replace(_I,'');print('Player '+a[1:]+' eliminated!');a=''
				elif str(a)==_L:print('Tie! No one was eliminated.')
				elif str(a).startswith('win'):winner=int(str(a)[3:]);print('Winner! '+str(_P+str(winner+1))if winner>=0 else _Q+str(winner))
		if eliminated:break
