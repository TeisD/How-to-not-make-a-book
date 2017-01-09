import config
from page import Page
from printer import Printer
from gui import Gui
from job import Job
from processor import Box
import helpers
import threading
import random

import os, sys, getopt, time

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import pickle
import speech_recognition as sr

WIT_AI_KEY = "BMSJFOODR7HW2VFEWLIUEYHNOVWNOC74" # Wit.ai keys are 32-character uppercase alphanumeric strings
r = sr.Recognizer()
m = sr.Microphone()
printer = Printer()
gui = Gui()
instructions = []

def main(argv):
    """ INIT THE SPEECH RECOGNITION """
    print("A moment of silence, please...")
    with m as source: r.adjust_for_ambient_noise(source)
    r.energy_threshold = 100
    print("Set minimum energy threshold to {}".format(r.energy_threshold))

    """ INIT THE JOB """
    if(os.path.isfile('jobs/TGP.conf')):
        with open('jobs/TGP.conf', 'rb') as f:
            p = pickle.load(f)
            printer.safe = True
            printer.init()
            job = Job(p['name'], Job.get_processor(p['processor']), p['lang'])
            job.processor.set_properties(p['processor_properties'])

    """ DO A PAGE """
    page = Page(printer.capture(), printer.getOcr(), job.get_language())
    if config.DEBUGGING:
        gui.setOriginal(page.getImageOriginal())
        gui.setProcessed(page.getImageProcessed())
    text = [Box(w) for w in job.processor.get_text(page)]

    """ SPAWN A PRINTING THREAD """
    def threaded_print():
        while True:
            if len(instructions) > 0:
                instruction = instructions.pop(0)
                printer.plot(instruction)
                if config.DEBUGGING: gui.plot(instruction)
            else:
                time.sleep(1)
                continue


    listener_thread = threading.Thread(target=threaded_print)
    listener_thread.daemon = True
    listener_thread.start()

    """ START LISTENING """
    i = 0
    while True:
        print("LISTENING ({0})").format(i)
        with m as source: audio = r.record(source, duration=10)
        print("ANALYZING ({0})").format(i)
        process(audio, text, i)
        i += 1


def process(source, text, i):
    def threaded_analyze():
        try:
            speech = r.recognize_wit(source, key=WIT_AI_KEY)
            speech = speech.encode("utf-8").split(" ")
            print("MATCHING ({0})").format(i)
            for s_w in speech:
                matches = []
                for t_w in text:
                    if t_w.get() is None: continue
                    if s_w == t_w.getText(): matches.append(t_w)
                if len(matches) > 0:
                    print("found {0} matches for {1}").format(len(matches), s_w)
                    instructions.append(random.choice(matches).strike())
        except sr.UnknownValueError:
            print("UnknownValueError")
        except sr.RequestError as e:
            print("RequestError: {0}".format(e))

    listener_thread = threading.Thread(target=threaded_analyze)
    listener_thread.daemon = True
    listener_thread.start()

if __name__ == "__main__":
    main(sys.argv)
