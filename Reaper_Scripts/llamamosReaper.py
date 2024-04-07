import subprocess
import time


reaper_executable = "C:\\Program Files\\REAPER (x64)\\reaper.exe"

reaper_proyect = ".\\Reaper_Proyect\\miProyectoAsistente.rpp"
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
