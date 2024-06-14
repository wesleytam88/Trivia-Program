--------------------------------------------------------------------------------------------------------------------------------------
   Description 
--------------------------------------------------------------------------------------------------------------------------------------

Trivia Program
 - Baisc trivia program developed with python
 - Designed for a display screen, and control screen, and controler intput
 - See 'help.txt' for more information

--------------------------------------------------------------------------------------------------------------------------------------
   Edit Log
--------------------------------------------------------------------------------------------------------------------------------------

Contibuters:
 - Kian (creator) spykian@gmail.com

Edit Log:
 19/10/10 - Kian
  - Added confirmation to closing
 19/05/15 - Kian
  - Added video images
  - Adjusted display of player scores
 19/05/14 - Kian
  - Added history logging
  - Pause and end now function during answer display
 19/04/12 - Kian
  - Added volume seetings
  - Settings now saved between launches
  - Multiple display changes
  - Re-orginzed file structure
 18/07/26 - Kian
  - Program Launch

--------------------------------------------------------------------------------------------------------------------------------------
   Development Details
--------------------------------------------------------------------------------------------------------------------------------------

Code Location:
 - Source code located in the 'misc/development' folder
 - Program can be run from any of the code files instead of executable
 - Sample questions in the development folder can be used for debugging

Dependencies:
 - pygame
 - pandas
 - opencv-python
 - pyinstaller

Most of the code involves tkinter, so you should get familiar with that first.
 - The entire app and main screen is run by the Tk object (you can only have one)
 - Each additional window is run by the Toplevel object
 - Each page is a frame that is attached to the window
    - Frames are switched with the tkraise method
 - Items in each page must by positioned in the page to show up (via pack or grid)
 - In order for the app to run, update and update_idletasks methods must be called on the Tk object
    - If you have a loop running, you need both to be called to update screens and get user input
	
Turning this into an executable is a pain. Thankfully, I found the needed workaround already.
 - Open command prompt in the 'misc/development' folder
 - Type 'pyinstaller TriviaProgram.spec'
 - Wait for it to finish (~5 minutes)
 - Copy the executable from the 'dist' folder to the same level as the toplevel 'files' folder
 - You can then delete the 'dist', 'build', and '__pychache__' folders
