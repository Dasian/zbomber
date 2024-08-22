# zbomber
> [!CAUTION]
> FOR EDUCATIONAL PURPOSES ONLY!!! IF YOU ABUSE THIS I'M NOT RESPONSIBLE!

Create and order an army of bots to do your bidding in zoom meetings. Takes advantage of
the "join from your browser" feature. New selenium browser instances allow for
multiple, independent zoom sessions. Tested on Windows and Linux

## Current Functionality
- Join/Leave meetings
- Send/Spam messages
- Control bots in a python script or an interactive terminal user interface

## Install Requirements
### Python Virtual Environment (optional)
Isolates packages from the rest of your system. The environment needs to be activated before you can run the scripts.
> First command creates a venv, second command activates it.
#### Windows
```cmd
python -m venv .zbomber
call .zbomber/scripts/activate.bat
```
#### Linux
```bash
python3 -m venv .zbomber  
source .zbomber/bin/activate
```
### Install Python Libraries
```bash
pip3 install -r requirements.txt
```
## Specify Commands
> Make sure to activate the venv if you created one!
### Terminal User Interface (tui)
Lets you pick individual or mass bot commands from a menu. Navigate the
interface with `tab` and arrow keys.
#### Windows
> Run this in cmd
```cmd
python zbomber-tui.py
```
#### Linux
```bash
python3 zbomber-tui.py
```
### Python
This creates 2 bots which join the
target meeting. The bots alternate sending messages to chat until 100 total are sent.
Then they leave when the job is done.
> You can write this in the zbomber.py main function or import zbomber in your own script
```python
# controller for all bots
zbomber = ZBomber(num_bots=2, link='zoom-link-here')

# update bot changes
zbomber.refresh_bots()

# opens a window for each bot
zbomber.start_bots()

# prepares all bots to join the meeting (opens link and inputs name)
zbomber.prepare_bots()

# all bots join the meeting and opens chat window
zbomber.join_all()

# spam messages
zbomber.spam('FREE PALESTINE', 100)

# leave meeting
zbomber.retreat()

# close window for each bot
zbomber.kill_all()
```
Then you can run the script:
```bash
python3 zbomber.py
```
