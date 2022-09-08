from evdev import InputDevice, categorize, ecodes
from motor import Controller

controller = Controller()
gamepad = InputDevice('/dev/input/event2')

print(gamepad)

x_dir = 0
y_dir = 0

for event in gamepad.read_loop():
    #print(categorize(event))
    #print(str(event.code) + " / " + str(event.value))
    
    if event.code == 16:
        # links
        if event.value == -1:
            if y_dir == 0:
                controller.spin_l()
            elif y_dir == -1:
                controller.turn_l()
            
            x_dir = -1
        # rechts
        elif event.value == 1:
            if y_dir == 0:
                controller.spin_r()
            elif y_dir == -1:
                controller.turn_r()
            
            x_dir = 1
        # losgelassen 
        elif event.value == 0:
            controller.idle()
            x_dir = 0
    
    elif event.code == 17:
        # oben
        if event.value == -1:
            if x_dir == 0:
                controller.forward()
            elif x_dir == -1:
                controller.turn_l()
            elif x_dir == 1:
                controller.turn_r()
            
            y_dir = -1
        # unten
        elif event.value == 1:
            controller.backward()
            y_dir = 1
        # losgelassen
        elif event.value == 0:
            controller.idle()
            y_dir = 0
    
    elif event.code == 9 or event.code == 10:
        # gedrueckt
        if event.value > 0:
            if event.code == 9:
                mode = -1
            else:
                mode = 1
            controller.shoot(True, mode)
            
            
        # losgelassen
        elif event.value == 0:
            controller.shoot(False)
            