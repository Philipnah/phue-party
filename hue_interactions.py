from phue import Bridge
import time
from secrets import hueIP

bridge = Bridge(hueIP)


try:
    # If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
    bridge.connect()
except Exception:
    print("Press the Hue Bridge button to connect")


# # Get the bridge state (This returns the full dictionary that you can explore)
# print(bridge.get_api())

# controlledLightString = input("Exact name of the light that should be controlled: ")
controlledLightString = "Air"


# You can also use light names instead of the id
controlledLight = bridge.get_light(controlledLightString)
# print(controlledLight)

# The type of light
controlledLightType = str(controlledLight['config']['archetype'])

print("The light you have selected is a '" + controlledLightType + "'")

def BPMtoSeconds(bpm):
	return 60/bpm


# While button is pressed
def StrobeLight():
    # Make sure the light is on
	bridge.set_light(controlledLightString, 'on', True)

	# Turn the light on command
	onCommand = {'transitiontime' : 0, 'bri' : 254}
	offCommand = {'transitiontime' : 0, 'bri' : 0}

    # Flash light 10 times
	for i in range(0, 20):
		bridge.set_light(controlledLightString, onCommand)
		time.sleep(0.0001)
		bridge.set_light(controlledLightString, offCommand)




def BeatLightMatch():
	# Make sure the light is on
	bridge.set_light(controlledLightString, 'on', True)

	# Turn the light on command
	onCommand = {'transitiontime' : 1, 'bri' : 254}
	offCommand = {'transitiontime' : 1, 'bri' : 0}

    # Flash light 10 times
	for i in range(0, 10):
		bridge.set_light(controlledLightString, onCommand)
		time.sleep(0.125)
		bridge.set_light(controlledLightString, offCommand)
		time.sleep(0.125)

def TurnLightOff():
	bridge.set_light(controlledLightString, 'on', False)



StrobeLight()

TurnLightOff()

# BeatLightMatch()


# # Prints if light 1 is on or not
# b.get_light(1, 'on')

# # Set brightness of lamp 1 to max
# b.set_light(1, 'bri', 254)

# # Set brightness of lamp 2 to 50%
# b.set_light(2, 'bri', 127)

# # Turn lamp 2 on
# b.set_light(2,'on', True)

# # You can also control multiple lamps by sending a list as lamp_id
# b.set_light( [1,2], 'on', True)

# # Get the name of a lamp
# b.get_light(1, 'name')

# # You can also use light names instead of the id
# b.get_light('Kitchen')
# b.set_light('Kitchen', 'bri', 254)

# # Also works with lists
# b.set_light(['Bathroom', 'Garage'], 'on', False)

# # The set_light method can also take a dictionary as the second argument to do more fancy stuff
# # This will turn light 1 on with a transition time of 30 seconds
# command =  {'transitiontime' : 300, 'on' : True, 'bri' : 254}
# b.set_light(1, command)
