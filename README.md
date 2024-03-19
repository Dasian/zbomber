# zbomber
Create and order an army of bots to do your bidding in zoom meetings.  
Bots can join, leave, send a message, and spam messages.

## Install Requirements
```console
$ python3 -m venv .zbomber  
$ source .zbomber/activate/bin  
$ pip3 -r requirements.txt  
```
## Specify Orders
This creates 2 bots which join the
target meeting. The bots alternate sending messages to chat until 100 total are sent.
Then they leave when the job is done.
> You still need to write this all in main bc i'm the worst. I'll make it more interactive eventually maybe probably...
```python
zbomber = ZBomber(num_bots=2, link='zoom-link-here')
zbomber.start_bots()
zbombser.spam('FREE PALESTINE', 100)
zbomber.retreat()
```

## Run
```console
$ source .zbomber/activate/bin
$ python3 zbomber.py
```
