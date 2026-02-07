import internal_speech
import not_slop
import camera_undistort_and_rectify
import asyncio

# get user voice input
usr_txt = internal_speech.get_speech()
# get confirmation input is correct
resp = -1
if(usr_txt!=None):
    print("Did you say {usr_txt}?")
    print("1: yes")
    print("2: no")
    resp = input()
# if not, get text input
if(usr_txt==None or resp==2 or resp==-1):
    print("Input your command: ")
    usr_txt = input()
# add user input to AI
# await ai response
ai_resp = asyncio.run(not_slop.ai_cmd(usr_txt))
print(ai_resp)
red = False
green = False
blue = False
if "red" in ai_resp: 
    red = True
if "green" in ai_resp:
    green = True
if "blue" in ai_resp:
    blue = True
# get arm out of the way
# take pic, get good image
camera_undistort_and_rectify.unr()
# analyze for the colors


# depending on the selected color and destination, have commands
# move to src
# grab
# move to dest
# release

# go back to beginning
