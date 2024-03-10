from tkinter import ttk
from tkinter import *

class GenerationTab:

    def __init__(self, tab):
        self.tab = tab

    def setUp(self):
        self.setBackground()

    def setBackground(self):
        self.canvas = Canvas(self.tab, width = 800, height = 600)