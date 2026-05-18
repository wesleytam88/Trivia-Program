# Description 

## Trivia Program
 - Basic trivia program developed with python
 - Designed for a display screen, control screen, and controller input
 - See `src/files/help.txt` for more information on how to play

# Development Details

## Code Location
 - Source code located in the `src` folder
 - Program can be run from any of the code files instead of executable
 - `sample_questions` can be used for debugging

## Dependencies
See `requirements.txt`

## Tkinter 
Most of the code involves tkinter, so you should get familiar with that first.
 - The entire app and main screen is run by the Tk object (you can only have one)
 - Each additional window is run by the Toplevel object
 - Each page is a frame that is attached to the window
    - Frames are switched with the tkraise method
 - Items in each page must by positioned in the page to show up (via pack or grid)
 - In order for the app to run, update and update_idletasks methods must be called on the Tk object
    - If you have a loop running, you need both to be called to update screens and get user input
	
## Executable Creation
Turning this into an executable is a pain. Thankfully, I found the needed workaround already.
 - Open command prompt in the the `src` folder
 - Run `pyinstaller TriviaProgram.spec`
   - If that does not work try `python -m PyInstaller TriviaProgram.spec`
 - Wait for it to finish (~5 minutes)
 - Copy the executable from the `dist` folder to the top level root folder
   - The .exe looks for the sounds, logs, and other files it needs to run in the `files` folder in its current directory, which is why we have to move it to the root folder
 - You can then delete the `dist`, `build`, and `__pycache__` folders

## Customization

### Sounds
If you do not like the default sounds that play during the game, you can use your own custom sounds by adding them to the `files/sounds` folder. Sounds are chosen by the game randomly, so if you want only your own custom sounds to play you can remove all but your own sounds.
 - `alarm`: plays when time has run out on a question
 - `correct`: plays when a player answers a question correctly
 - `ding`: plays when a player buzzes in
 - `incorrect`: plays when a player answers a question incorrectly

### Icon
To change the icon, replace the `icon.ico` file in the `misc` folder.