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
You need to specify things in main bc im the worst.
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
