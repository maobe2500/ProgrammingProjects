#!/usr/bin/env python3

class TV:
    def __init__(self, tv_name, max_volume, current_volume, max_channel, current_channel):
        self.tv_name = tv_name
        self.current_volume = current_volume
        self.current_channel = current_channel
        self.max_volume = max_volume
        self.max_channel = max_channel

    #A String representation of a file
    def __str__(self):
        return f"{self.tv_name}, channel {self.current_channel}, volume {self.current_volume}"

    #Checks if able to change channel
    def change_channel(self, new_channel):
        if new_channel < 1 or new_channel > self.max_channel:
            return False
        self.current_channel = new_channel
        return True

    #Checks if able to increase the volume
    def increase_volume(self):
        if (self.current_volume + 1) > self.max_volume:
            return False
        self.current_volume += 1
        return True

    #checks if abel to increase the volume
    def decrease_volume(self):
        if (self.current_volume - 1) < 0:
            return False
        self.current_volume -= 1
        return True

    #Retruns a string to write to a file
    def str_for_file(self):
        return f"{self.tv_name},{self.max_volume},{self.current_volume},{self.max_channel},{self.current_channel}\n" 
'''       
tv = TV("Vardagsrunms TV", 100, 22, 10, 9)
tv2 = TV("Sovrums TV", 50, 7, 20, 4)
print(tv)
print(tv2)
print(tv2.change_channel(55))
tv.increase_volume()
print(tv)
'''