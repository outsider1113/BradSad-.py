import pyautogui, time

f = open("forrestgumpscript.txt")
time.sleep(5)

for word in f:
    pyautogui.typewrite(word)
    pyautogui.press("enter")

print("Sad Brad")
sadbrad = True 
if (sadbrad):
    print("brad is sad")
else:
    print("brad is glad")
