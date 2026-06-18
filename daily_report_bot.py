import pyautogui
import time
from datetime import datetime
import pyperclip

pyautogui.FAILSAFE = True
pyautogui.PAUSE=1.0

print("Step 1: Open the Chrome Browser....")
pyautogui.hotkey('win', 'r', interval=0.15)
pyautogui.typewrite('chrome', interval=0.15)
pyautogui.press('enter')
time.sleep(2)
print("Click on User profile icon....")
pyautogui.press('tab', presses=1, interval=0.15)
pyautogui.press('enter')
time.sleep(2)

print("Step 2: Open a new tab and navigate to times now website....")
pyautogui.hotkey('ctrl', 't', interval=0.15)
pyautogui.typewrite('https://www.timesnownews.com/', interval=0.15)
pyautogui.press('enter')
time.sleep(5)

print("Step 3: Select the Breaking News section....")
pyautogui.hotkey('ctrl', 'a', interval=0.15)
time.sleep(1)
pyautogui.hotkey('ctrl', 'c', interval=0.15)
time.sleep(1)



print("Step 4: Open Excel and paste the copied content....")
pyautogui.hotkey('win', 'r', interval=0.15)
pyautogui.typewrite('excel', interval=0.15)
pyautogui.press('enter')
time.sleep(5)
pyautogui.press('enter')
time.sleep(5)
pyautogui.press('f2', interval=0.15)
pyautogui.typewrite('Date and Time', interval=0.15)
pyautogui.press('f2', interval=0.15)
pyautogui.press('right', interval=0.15)
datetime_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
pyautogui.typewrite(datetime_now, interval=0.15)
pyautogui.press('enter', interval=0.15)
pyautogui.press('left', interval=0.15)
pyautogui.press('f2', interval=0.15)
pyautogui.typewrite('Breaking News', interval=0.15)
pyautogui.press('f2', interval=0.15)
pyautogui.press('right', interval=0.15)
pyautogui.press('f2', interval=0.15)
pyautogui.hotkey('ctrl', 'v', interval=0.15)
pyautogui.press('f2', interval=0.15)
pyautogui.press('enter', interval=0.15)
pyautogui.press('left', interval=0.15)
pyautogui.typewrite('Comments', interval=0.15)
pyautogui.press('right', interval=0.15)
pyautogui.typewrite('This is the content copied from Times Now website', interval=0.15)

print("Step 5: Save the Excel file....")
pyautogui.hotkey('ctrl', 's', interval=0.15)
datetime_now = datetime.now().strftime("%Y-%m-%d")
pyautogui.typewrite(datetime_now, interval=0.15)
pyautogui.press('enter', interval=0.15)
