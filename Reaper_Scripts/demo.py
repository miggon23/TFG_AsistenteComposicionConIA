from asyncio.windows_events import NULL
import os
import random

def cargarMidi(ruta):
    bufOut = ""  # Initialize bufOut with an empty string
    bufOut_sz = 1024  # Set an arbitrary size for bufOut_sz, adjust as needed
    
    # Corrected usage of RPR_GetProjectPath
    bufOut, bufOut_sz = RPR_GetProjectPath(bufOut, bufOut_sz)
    
    ruta = os.path.join(bufOut, ruta)  # Use os.path.join to concatenate paths
    
    if os.path.isfile(ruta):
        RPR_InsertMedia(ruta, 0)
    else:
        RPR_ShowMessageBox("El archivo MIDI no existe en la ruta proporcionada: "+ ruta, "Error", 0)


#Melodía instrumento 1 y 2   
def crearPista1(pista, tematica, preset):
    i = pista-1
    if(tematica == 0):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    if(tematica == 1):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    if(tematica == 2):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    if(tematica == 3):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    if(tematica == 4):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    if(tematica == 5):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    if(tematica == 6):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    if(tematica == 7):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    if(tematica == 8):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    if(tematica == 9):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))

#Acompañamiento instrumento 3 y 4   
def crearPista3(pista, tematica, preset, arpegiado, preset_arpegio):
    i = pista-1
    if(arpegiado == 1):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "BlueArp", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "arpegio"+str(preset_arpegio)) 
    elif(arpegiado == 2):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "BlueArp", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "acordes"+str(preset_arpegio)) 

    if(tematica == 0):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 1):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 2):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 3):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 4):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 5):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 6):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 7):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 8):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 9):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))


#Pads instrumento 5   
def crearPista5(pista, tematica, preset):
    i = pista-1
    if(tematica == 0):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    if(tematica == 1):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    if(tematica == 2):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    if(tematica == 3):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    if(tematica == 4):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    if(tematica == 5):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    if(tematica == 6):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    if(tematica == 7):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    if(tematica == 8):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    if(tematica == 9):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))

#Bajo instrumento 6   
def crearPista6(pista, tematica, preset, arpegiado, preset_arpegio):
    i = pista-1
    if(arpegiado == 1):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "BlueArp", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "arpegio"+str(preset_arpegio)) 
    elif(arpegiado == 2):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "BlueArp", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "bajo"+str(preset_arpegio)) 

    if(tematica == 0):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 1):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 2):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 3):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 4):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 5):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 6):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 7):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 8):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 9):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))


#Batería instrumento 7   
def crearPista7(pista, tematica, preset):
    i = pista-1
    if(tematica == 0):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    if(tematica == 1):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    if(tematica == 2):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    if(tematica == 3):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    if(tematica == 4):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    if(tematica == 5):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    if(tematica == 6):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    if(tematica == 7):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    if(tematica == 8):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    if(tematica == 9):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))


n_tracks = 7

for i in range(n_tracks):
    RPR_InsertTrackAtIndex(i, True)

# Iterar a través de las pistas y agregar una cadena de efectos

# Seleccionar la pista actual
# RPR_SetTrackSelected(RPR_GetTrack(0, 0), True)

# Agregar un efecto
# El número 0 representa el índice del efecto en la lista de efectos disponibles
    
tematica = 0

#Melodía instrumento 1    
crearPista1(1, tematica, random.randint(1, 3))

#Melodía instrumento 2    
crearPista1(2, tematica, random.randint(1, 3))

#Acompañamiento 1
crearPista3(3, tematica, random.randint(1, 3), random.randint(1, 3), random.randint(1, 10))

#Acompañamiento 2
crearPista3(4, tematica, random.randint(1, 3), random.randint(1, 3), random.randint(1, 10))

#Pads o strings
crearPista5(5, tematica, random.randint(1, 3))

#Bajo
crearPista6(6, tematica, random.randint(1, 3), random.randint(1, 3), random.randint(1, 10))

#Batería
crearPista7(7, tematica, random.randint(1, 3))

# Mover el cursor al inicio de la pista
RPR_SetEditCurPos(0, True, True)
# Obtén el índice de la pista en la que deseas cargar el archivo MIDI
indice_de_pista = 0  # Cambia esto al índice de la pista que deseas seleccionar

# Establecer la pista seleccionada utilizando RPR_SetMediaTrackInfo_Value()
RPR_SetMediaTrackInfo_Value(RPR_GetTrack(0, indice_de_pista), "I_SELECTED", 1)



RPR_SetEditCurPos(16, True, True)

# Cargar el archivo MIDI en Reaper desde la nueva ubicación
cargarMidi("midi/markov_melody_0.mid")

## Cortar el midi
#RPR_SplitMediaItem(RPR_GetMediaItem(0, 0), 2)
#RPR_SetMediaItemLength(RPR_GetMediaItem(0, 0), 4, False)
#
#RPR_SetMediaItemPosition(RPR_GetMediaItem(0, 1), 4, False)
#RPR_SplitMediaItem(RPR_GetMediaItem(0, 1), 6)
#RPR_SetMediaItemLength(RPR_GetMediaItem(0, 1), 4, False)
#
#RPR_SetMediaItemPosition(RPR_GetMediaItem(0, 2), 12, False)
#
#RPR_SplitMediaItem(RPR_GetMediaItem(0, 0), 2)
#RPR_SetMediaItemLength(RPR_GetMediaItem(0, 0), 4, False)
#RPR_SetMediaItemLength(RPR_GetMediaItem(0, 1), 4, False)
#RPR_SetMediaItemPosition(RPR_GetMediaItem(0, 1), 8, False)
#
## Mover el midi
#RPR_SetMediaItemPosition(RPR_GetMediaItem(0, 3), 28, False)
#RPR_SetMediaItemPosition(RPR_GetMediaItem(0, 2), 24, False)
#RPR_SetMediaItemPosition(RPR_GetMediaItem(0, 1), 20, False)
#RPR_SetMediaItemPosition(RPR_GetMediaItem(0, 0), 16, False)





RPR_SetEditCurPos(0, True, True)
indice_de_pista = 2

RPR_SetMediaTrackInfo_Value(RPR_GetTrack(0, indice_de_pista), "I_SELECTED", 1)
cargarMidi("midi/output_harmony.mid")
RPR_SetMediaItemLength(RPR_GetMediaItem(0, 4), 16, False)
RPR_SetEditCurPos(0, True, True)


RPR_SetEditCurPos(16, True, True)
indice_de_pista = 3

RPR_SetMediaTrackInfo_Value(RPR_GetTrack(0, indice_de_pista), "I_SELECTED", 1)
cargarMidi("midi/output_harmony.mid")
RPR_SetMediaItemLength(RPR_GetMediaItem(0, 5), 16, False)


RPR_SetEditCurPos(0, True, True)
indice_de_pista = 4

RPR_SetMediaTrackInfo_Value(RPR_GetTrack(0, indice_de_pista), "I_SELECTED", 1)
cargarMidi("midi/output_harmony.mid")
RPR_SetMediaItemLength(RPR_GetMediaItem(0, 6), 32, False)

RPR_SetEditCurPos(0, True, True)
indice_de_pista = 5

RPR_SetMediaTrackInfo_Value(RPR_GetTrack(0, indice_de_pista), "I_SELECTED", 1)
cargarMidi("midi/output_bass.mid")
RPR_SetMediaItemLength(RPR_GetMediaItem(0, 7), 32, False)

tr = RPR_GetTrack(0, indice_de_pista)
RPR_SetMediaTrackInfo_Value(tr, "D_VOL", 0.2)



RPR_SetEditCurPos(16, True, True)
indice_de_pista = 6

RPR_SetMediaTrackInfo_Value(RPR_GetTrack(0, indice_de_pista), "I_SELECTED", 1)

cargarMidi("midi/output_BASIC_drumPatternA.mid")
cargarMidi("midi/output_BASIC_drumPatternB.mid")
cargarMidi("midi/output_BASIC_drumPatternA.mid")
cargarMidi("midi/output_BASIC_drumPatternC.mid")

cargarMidi("midi/output_BASIC_drumPatternA.mid")
cargarMidi("midi/output_BASIC_drumPatternB.mid")
cargarMidi("midi/output_BASIC_drumPatternA.mid")
cargarMidi("midi/output_BASIC_drumPatternC.mid")


RPR_SetEditCurPos(0, True, True)







