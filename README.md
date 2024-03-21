# DISCLAIMER
FOR EDUCATIONAL PURPOSES ONLY!!! IF U ABUSE THIS I'M NOT RESPONSIBLE!
> plz don't go after me

# zbomber
Create and order an army of bots to do your bidding in zoom meetings. Takes advantage of
the "join from your browser" feature. New selenium browser instances allow for
multiple, independent zoom sessions.

## Current Functionality
- Join/Leave Meetings
- Send/Spam Messages

## Install Requirements
### Linux
```console
$ python3 -m venv .zbomber  
$ source .zbomber/activate/bin  
$ pip3 -r requirements.txt  
```
### Windows
```console
$ python -m venv .zbomber
$ call .zbomber/scripts/activate.bat
$ pip3 install -r requirements.txt
```
## Specify Commands
### Programatically
This creates 2 bots which join the
target meeting. The bots alternate sending messages to chat until 100 total are sent.
Then they leave when the job is done.
> You need to write this in the zbomber.py main function
```python
# controller for all bots
zbomber = ZBomber(num_bots=2, link='zoom-link-here')

# opens a window for each bot
zbomber.start_bots()

# prepares all bots to join the meeting (opens link and inputs name)
zbomber.prepare_bots()

# all bots join the meeting and opens chat window
zbomber.join_all()

# spam messages then they all leave
zbomber.spam('FREE PALESTINE', 100)
zbomber.retreat()
```
Then you run the script.
```console
$ source .zbomber/activate/bin
$ python3 zbomber.py
```
### Interactive
Terminal user interface to control bots.
```console
$ source .zbomber/bin/activate
$ python3 zbomber-tui.py
```
