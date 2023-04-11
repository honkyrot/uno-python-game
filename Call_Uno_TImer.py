from threading import Timer
import time

timeout = 3


def call_uno_timer():
    """Call to start uno timer and return True if user says uno, else return False"""
    t = Timer(timeout, print, ["You didn't call Uno! Draw 2. Enter to continue..."])
    t.start()
    start_time = time.time()
    prompt = f"\nYOU HAVE {timeout} SECONDS TO CALL UNO, TYPE \"UNO\" NOW...\n"
    answer = input(prompt)
    t.cancel()
    end_time = time.time()
    reaction_time = end_time - start_time
    if reaction_time > timeout:
        return False
    else:
        if answer.lower() == "uno":
            print("You called Uno!")
            return True
        print("You failed to type \"uno\"! Draw 2.")
        return False
