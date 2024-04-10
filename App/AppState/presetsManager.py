from tkinter import ttk
from tkinter import *
from App.AppState.modeState import ModeState
import json

class PresetManager:
    presetsPath = "App/AppPresets"

    def __init__(self):
        self.popup = None

    def _savePreset(self, modeState, presetName):
        jsonMap = modeState.toJSON()
        presetPath = self.presetsPath + "/" + presetName + ".json"

        with open(presetPath, "w") as archivo:    
            json.dump(jsonMap, archivo, indent=4)
        print("Preset guardado con el nombre de " + presetName)

    def recoverPreset(self, presetName):
        jsonPath = self.presetsPath + presetName + ".json"
        recoveredPreset = ModeState.fromJSON(jsonPath)
        return recoveredPreset
    
    def show_save_preset_popup(self, tab, modeState):
        self.popup = Toplevel(tab)
        self.popup.geometry("200x100")
        self.popup.title("Guardar Preset")
        self.modeState = modeState

        label = Label(self.popup, text="Introduce el nombre del preset: ")
        label.pack()

        self.presetName = StringVar()
        Entry(self.popup, textvariable=self.presetName).pack()

        Button(self.popup, text="Guardar", command=self._saveAndClose).pack()

    def _saveAndClose(self):
        self._savePreset(self.modeState, self.presetName.get())
        if self.popup != None:
            self.popup.destroy()
            self.popup = None
        