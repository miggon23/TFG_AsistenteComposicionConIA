import subprocess
import time
import json
from Utils import globalConsts

class ReaperStream:
    def SetUp(self):
        with open(globalConsts.Paths.appConfigPath, "r") as archivo:
            data = json.load(archivo)

        reaper_executable = data["reaperPath"]

        reaper_proyect = ".\\miProyectoAsistente.rpp"
        reascript_script = ".\\Reaper_Scripts\\ok.lua"

        #Crear proyecto
        command = [reaper_executable, reaper_proyect, reascript_script, "-saveas", reaper_proyect, "-nosplash"]
        subprocess.Popen(command)

        #time.sleep(10)

        #Lanzar script de lua
        #command = [reaper_executable, reaper_proyect, reascript_script, "-saveas", reaper_proyect]
        #subprocess.Popen(command)

        #time.sleep(10)

        #Guardar el proyecto
        #command = [reaper_executable, reaper_proyect, "-saveas", reaper_proyect]
        #subprocess.Popen(command)
