# A text-based adventure: Finding Earl


![Earl](ressources/bear_50x50.png) 

'Finding Earl' is a text-based adventure game created by CribberSix.

The idea for the text-based approach originated from the TV-series 'Chuck' where 
the 1980 text-based video game 'Zork' was mentioned. 


### Useful commands
- 'help' - shows this text
- 'info' - shows some information about the game
- 'look' - shows what the character can see
- 'read' or 'inspect' - shows more details on a specific object
- 'i' or 'inventory' - shows the contents of your inventory
- 'take' - takes an object to inventory
- 'drop' - drops an object from the inventory to the floor
- 'open' or 'open ... with ...' - opens an object (optionally *with* another object such as a key)
- 'go' or 'walk' - let's you move around. Acceptable directions are: *north\\forward, west\\right, south\\backward, east\\left*

### Parser
The algorithm tries to match the input's first word - needs to be a **verb** - to a game functionality.
Some verbs work as a standalone. 
Other verbs require further input, for example what the **object** of the verb is. If there are more than one of the
desired objects around, you will need to specificy which one you mean with a **descriptive ajdective**, for instance *purple book* . 

The parser will tell you if he does not know a verb or if he needs further information, so
the best thing to do is to try it out!

## Running the Game 

To run the game install the necessary requirements with `pip install -r requirements.txt` and run the file `Adventure.py`.
