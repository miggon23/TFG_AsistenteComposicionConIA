from asyncio.windows_events import NULL
import os

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


# RPR_ShowMessageBox("Rodrigo", "Rodrigo", 0)

n_tracks = 6

for i in range(n_tracks):
    RPR_InsertTrackAtIndex(i, True)

# Iterar a través de las pistas y agregar una cadena de efectos

# Seleccionar la pista actual
# RPR_SetTrackSelected(RPR_GetTrack(0, 0), True)

# Agregar un efecto
# El número 0 representa el índice del efecto en la lista de efectos disponibles
RPR_TrackFX_AddByName(RPR_GetTrack(0, 0), "Tal", False, -1)
RPR_TrackFX_SetPreset(RPR_GetTrack(0, 0), 0, "cuerdas prueba")

RPR_TrackFX_AddByName(RPR_GetTrack(0, 1), "BlueArp", False, -1)
RPR_TrackFX_SetPreset(RPR_GetTrack(0, 1), 0, "arpegiador")
RPR_TrackFX_AddByName(RPR_GetTrack(0, 1), "Tal", False, -1)
RPR_TrackFX_SetPreset(RPR_GetTrack(0, 1), 1, "piano")

RPR_TrackFX_AddByName(RPR_GetTrack(0, 2), "Tal", False, -1)
RPR_TrackFX_SetPreset(RPR_GetTrack(0, 2), 0, "piano")

RPR_TrackFX_AddByName(RPR_GetTrack(0, 3), "Tal", False, -1)
RPR_TrackFX_SetPreset(RPR_GetTrack(0, 3), 0, "pad")

RPR_TrackFX_AddByName(RPR_GetTrack(0, 4), "Tal", False, -1)
RPR_TrackFX_SetPreset(RPR_GetTrack(0, 4), 0, "bass")

RPR_TrackFX_AddByName(RPR_GetTrack(0, 5), "MT", False, -1)

# Mover el cursor al inicio de la pista
RPR_SetEditCurPos(0, True, True)
# Obtén el índice de la pista en la que deseas cargar el archivo MIDI
indice_de_pista = 0  # Cambia esto al índice de la pista que deseas seleccionar

# Establecer la pista seleccionada utilizando RPR_SetMediaTrackInfo_Value()
RPR_SetMediaTrackInfo_Value(RPR_GetTrack(0, indice_de_pista), "I_SELECTED", 1)


# Cargar el archivo MIDI en Reaper desde la nueva ubicación
cargarMidi("ejemploDemo/markov_sim_0.mid")

# Cortar el midi
RPR_SplitMediaItem(RPR_GetMediaItem(0, 0), 2)
RPR_SetMediaItemLength(RPR_GetMediaItem(0, 0), 4, False)

RPR_SetMediaItemPosition(RPR_GetMediaItem(0, 1), 4, False)
RPR_SplitMediaItem(RPR_GetMediaItem(0, 1), 6)
RPR_SetMediaItemLength(RPR_GetMediaItem(0, 1), 4, False)

RPR_SetMediaItemPosition(RPR_GetMediaItem(0, 2), 12, False)

RPR_SplitMediaItem(RPR_GetMediaItem(0, 0), 2)
RPR_SetMediaItemLength(RPR_GetMediaItem(0, 0), 4, False)
RPR_SetMediaItemLength(RPR_GetMediaItem(0, 1), 4, False)
RPR_SetMediaItemPosition(RPR_GetMediaItem(0, 1), 8, False)

# Mover el midi
RPR_SetMediaItemPosition(RPR_GetMediaItem(0, 3), 28, False)
RPR_SetMediaItemPosition(RPR_GetMediaItem(0, 2), 24, False)
RPR_SetMediaItemPosition(RPR_GetMediaItem(0, 1), 20, False)
RPR_SetMediaItemPosition(RPR_GetMediaItem(0, 0), 16, False)





RPR_SetEditCurPos(0, True, True)
indice_de_pista = 1

RPR_SetMediaTrackInfo_Value(RPR_GetTrack(0, indice_de_pista), "I_SELECTED", 1)
cargarMidi("ejemploDemo/output_harmony.mid")
RPR_SetMediaItemLength(RPR_GetMediaItem(0, 4), 16, False)
RPR_SetEditCurPos(0, True, True)


RPR_SetEditCurPos(16, True, True)
indice_de_pista = 2

RPR_SetMediaTrackInfo_Value(RPR_GetTrack(0, indice_de_pista), "I_SELECTED", 1)
cargarMidi("ejemploDemo/output_harmony.mid")
RPR_SetMediaItemLength(RPR_GetMediaItem(0, 5), 16, False)


RPR_SetEditCurPos(0, True, True)
indice_de_pista = 3

RPR_SetMediaTrackInfo_Value(RPR_GetTrack(0, indice_de_pista), "I_SELECTED", 1)
cargarMidi("ejemploDemo/output_harmony.mid")
RPR_SetMediaItemLength(RPR_GetMediaItem(0, 6), 32, False)

RPR_SetEditCurPos(0, True, True)
indice_de_pista = 4

RPR_SetMediaTrackInfo_Value(RPR_GetTrack(0, indice_de_pista), "I_SELECTED", 1)
cargarMidi("ejemploDemo/output_bass.mid")
RPR_SetMediaItemLength(RPR_GetMediaItem(0, 7), 32, False)

tr = RPR_GetTrack(0, indice_de_pista)
RPR_SetMediaTrackInfo_Value(tr, "D_VOL", 0.2)



RPR_SetEditCurPos(16, True, True)
indice_de_pista = 5

RPR_SetMediaTrackInfo_Value(RPR_GetTrack(0, indice_de_pista), "I_SELECTED", 1)

cargarMidi("output_BASIC_drumPatternA.mid")
cargarMidi("output_BASIC_drumPatternB.mid")
cargarMidi("output_BASIC_drumPatternA.mid")
cargarMidi("output_BASIC_drumPatternC.mid")

cargarMidi("output_BASIC_drumPatternA.mid")
cargarMidi("output_BASIC_drumPatternB.mid")
cargarMidi("output_BASIC_drumPatternA.mid")
cargarMidi("output_BASIC_drumPatternC.mid")


RPR_SetEditCurPos(0, True, True)







