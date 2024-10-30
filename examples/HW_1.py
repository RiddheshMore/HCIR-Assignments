from collections import Counter
import time
from qibullet import SimulationManager, PepperVirtual
import gtts
from playsound import playsound
import threading
import os

class BehaviorRealizer:

    def __init__(self):
        # Loading Robot and Ground
        simulation_manager = SimulationManager()
        client = simulation_manager.launchSimulation(gui=True)
        self.pepper = simulation_manager.spawnPepper(client, spawn_ground_plane=True)
        self.pepper.goToPosture("Crouch", 0.6) 
        time.sleep(1)
        self.pepper.goToPosture("StandInit", 0.6) 
        time.sleep(1)

    def speak(self, text):
        """
        This method makes Pepper speak a given text.
        It uses gtts (Google Text-to-Speech) to generate audio and plays it.
        """
        tts = gtts.gTTS(text)
        tts.save("speech.mp3")
        playsound("speech.mp3")

    def wave(self):
        """
        This method makes Pepper wave its hand.
        It controls the arm joints to simulate a waving gesture.
        """
        # Simulate the wave by moving the elbow
        for _ in range(5):  # Loop to wave 5 times
            self.pepper.setAngles("RShoulderPitch",-0.5,0.5) 
            self.pepper.setAngles("RShoulderRoll",-1.5620, 0.5) 
            self.pepper.setAngles("RElbowRoll",1.5620,0.5)
            time.sleep(1.0) 
            self.pepper.setAngles("RElbowRoll",-1.5620,0.5)
            time.sleep(1.0)
    
    def realize_behavior(self, behavior, text=None):
        """
        A helper method to trigger behaviors like speech or wave.
        """
        if behavior == 'speak' and text:
            self.speak(text)
        elif behavior == 'wave':
            self.wave()

if __name__ == "__main__":

    behavior_realizer_class = BehaviorRealizer()  
    
    # Input options for user
    INPUT_OPTIONS = ["done", "speak", "wave"]
        
    repeat_ = True
    while repeat_:
        user_input = input("INPUT (speak/wave/done): ")
        
        if user_input == INPUT_OPTIONS[0]:  # If 'done' is entered
            repeat_ = False
        
        elif user_input == "speak":
            text = input("Enter the text for Pepper to speak: ")
            threading.Thread(target=behavior_realizer_class.realize_behavior, args=("speak", text)).start()

        elif user_input == "wave":
            threading.Thread(target=behavior_realizer_class.realize_behavior, args=("wave",)).start()
        
        else:
            print("Please enter 'speak', 'wave', or 'done' to exit.")