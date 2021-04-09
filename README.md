# Text-based adventure: Finding Earl

'Finding Earl' is a text-based adventure game created by CribberSix.

The idea for the text-based approach originated from the TV-series 'Chuck' where 
the 1980 video game 'Zork' was mentioned. 


##### Useful commands
- 'help' - shows this text
- 'info' - shows some information about the game
- 'look' - shows what the character can see
- 'read' or 'inspect' - shows more details on a specific object
- 'i' or 'inventory' - shows the inventory
- 'take' - takes an object to inventory
- 'drop' - drops an object to the floor
- 'open' or 'open ... with ...' - opens an object (optionally with another object)
- 'go' or 'walk' - let's you move around. Acceptable directions are: north\\forward, west\\right, south\\backward, east\\left

##### Parser
The algorithm tries to match the input's first word - needs to be a <verb> - to a game functionality.

Certain verbs require further input, for example what the <object> of the verb is. Some verbs
work without further input and may even ignore further input.

The parser will tell you if he does not know a verb or if he needs further information, so
the best thing to do is to try it out!

