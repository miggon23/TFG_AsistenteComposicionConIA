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


def ajustarTempo(tematica):
    tempo = 120
    if(tematica == 0):
        tempo = random.randint(80, 110)
    elif(tematica == 1):
        tempo = random.randint(70, 140)
    elif(tematica == 2):
        tempo = random.randint(80, 110)
    elif(tematica == 3):
        tempo = random.randint(80, 110)
    elif(tematica == 4):
        tempo = random.randint(80, 110)
    elif(tematica == 5):
        tempo = random.randint(80, 110)
    elif(tematica == 6):
        tempo = random.randint(80, 110)
    elif(tematica == 7):
        tempo = random.randint(80, 110)
    elif(tematica == 8):
        tempo = random.randint(80, 110)
    elif(tematica == 9):
        tempo = random.randint(80, 110)
    RPR_SetTempoTimeSigMarker(0, -1, 0, -1, -1, tempo, 0, 0, True)

#Melodía instrumento 1 y 2   
def crearPista1(i, tematica, preset):
    pista = 1
    i -= 1

    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "JS: MIDI Transpose Notes", False, -1)
    if(i == 1):
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "octaveUp") 
    
    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Humanisator (x86) (Tobybear)", False, -1)
    RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "humanisator2") 

    if(tematica == 0):
        if(preset <= 0):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK Guitars Acousti (x86) (DSK Music)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 1):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK Guitars Nylon (x86) (DSK Music)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 2):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK Guitars Steel (x86) (DSK Music)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 4):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK AkoustiK GuitarZ (x86) (DSK MusicSZZ)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 5):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK Saxophones (DSK Music) (16 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 7):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK Strings (x86) (DSK)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        else:
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK AkoustiK Keyz (x86) (DSK MusicSZZ)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 1):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Room Piano v3 (SampleScience) (32 out)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pianoSolo0")
    elif(tematica == 2):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 3):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 4):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 5):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 6):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 7):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 8):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 9):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))

    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "ReaComp (Cockos)", False, -1)
    if(tematica != 1):
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "gain"+str(pista))
    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "ReaLimit (Cockos)", False, -1)
    if(tematica != 1):
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 4, "gain"+str(pista))


#Acompañamiento instrumento 3 y 4   
def crearPista3(i, tematica, preset, arpegiado, preset_arpegio):
    pista = 3
    i -= 1
    if(arpegiado == 1):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "BlueArp", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "arpegio"+str(preset_arpegio)) 
    elif(arpegiado == 2):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "BlueArp", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "acordes"+str(preset_arpegio)) 
    elif(arpegiado == 3):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "BlueArp", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "bypass") 
    
    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Humanisator (x86) (Tobybear)", False, -1)
    RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "humanisator1") 

    if(tematica == 0):
        if(preset <= 3):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK AkoustiK Keyz (x86) (DSK MusicSZZ)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 7):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Spicy Guitar (64 bits) (Keolab)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        else:
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK Elektrik Keyz (x86) (DSK)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 1):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Room Piano v3 (SampleScience) (32 out)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pianoSolo0")
    elif(tematica == 2):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DPiano-A (Dead Duck Software)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 3):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 4):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 5):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 6):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 7):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 8):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 9):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))

    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "ReaComp (Cockos)", False, -1)
    if(tematica != 1):
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "gain"+str(pista))
    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "ReaLimit (Cockos)", False, -1)
    if(tematica != 1):
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 4, "gain"+str(pista))

#Pads instrumento 5   
def crearPista5(pista, tematica, preset):
    i = pista-1

    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "JS: MIDI Transpose Notes", False, -1)
    if(tematica == 1):
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "octaveUp") 
    
    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Humanisator (x86) (Tobybear)", False, -1)
    RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "humanisator1") 

    if(tematica == 0):
        if(preset <= 2):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK ChoirZ (x86) (DSK Music)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        else:
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "VSTi: DSK Strings (x86) (DSK)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 1):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Room Piano v3 (SampleScience) (32 out)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pianoSolo0")
    elif(tematica == 2):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 3):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 4):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 5):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 6):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 7):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 8):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 9):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))

    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "ReaComp (Cockos)", False, -1)
    if(tematica != 1):
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "gain"+str(pista))
    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "ReaLimit (Cockos)", False, -1)
    if(tematica != 1):
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 4, "gain"+str(pista))

#Bajo instrumento 6   
def crearPista6(pista, tematica, preset, arpegiado, preset_arpegio):
    i = pista-1
    if(arpegiado == 1):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "BlueArp", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "arpegio"+str(preset_arpegio)) 
    elif(arpegiado == 2):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "BlueArp", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "bajo"+str(preset_arpegio)) 
    elif(arpegiado == 3):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "BlueArp", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "bajo0") 
    

    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "JS: MIDI Transpose Notes", False, -1)
    if(tematica == 1):
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "octaveDown") 
    
    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Humanisator (x86) (Tobybear)", False, -1)
    RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "humanisator1") 

    if(tematica == 0):
        if(preset <= 6):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "OMB2 (x86) (Christopher Clews)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        else:
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK BassZ (x86) (DSK MusicSZZ)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 1):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Room Piano v3 (SampleScience) (32 out)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pianoSolo0")
    elif(tematica == 2):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 3):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 4):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 5):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 6):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 7):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 8):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 9):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))

    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "ReaComp (Cockos)", False, -1)
    if(tematica != 1):
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 4, "gain"+str(pista))
    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "ReaLimit (Cockos)", False, -1)
    if(tematica != 1):
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 5, "gain"+str(pista))

#Batería instrumento 7   
def crearPista7(pista, tematica, preset):
    i = pista-1
    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Humanisator (x86) (Tobybear)", False, -1)
    RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "humanisator1") 
    
    if(tematica == 0):
        if(preset <= 7):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK mini DRUMZ 2 (x86) (DSK Music)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        else:
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK DrumZ 8bitZ (x86) (DSK Music)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 1):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK mini DRUMZ 2 (x86) (DSK Music)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 2):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 3):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 4):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 5):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 6):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 7):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 8):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 9):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "tal-noiseMaker", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))

    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "ReaComp (Cockos)", False, -1)
    if(tematica != 1):
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "gain"+str(pista))
    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "ReaLimit (Cockos)", False, -1)
    if(tematica != 1):
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "gain"+str(pista))


#Transiciones instrumento 8 y 9   
def crearPista8(pista, tematica, preset):
    i = pista-1
    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "JS: MIDI Transpose Notes", False, -1)
    RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "octaveUp") 
    
    if(tematica == 0):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Room Piano v3 (SampleScience) (32 out)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "riser"+str(preset))
    
    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Flux Mini 2 (Caelum Audio)", False, -1)
    RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "riser"+str(preset))

    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "ValhallaSupermassive (Valhalla DSP, LLC)", False, -1)
    RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "riser"+str(preset))



def cargarDrums(tematica):
        
    estilo = "BASIC"

    if(tematica == 0):
        rnd = random.randint(0, 2)
        if(rnd == 0): 
            estilo = "BASIC"
        elif(rnd == 1):
            estilo = "SHAKER"
        elif(rnd == 2):
            estilo = "JAZZ"
    elif(tematica == 1):
        estilo = "BASIC"

    if(tematica != 1):
        cargarMidi("midi/output_"+estilo+"_drumPatternA.mid")
        cargarMidi("midi/output_"+estilo+"_drumPatternB.mid")
        cargarMidi("midi/output_"+estilo+"_drumPatternA.mid")
        cargarMidi("midi/output_"+estilo+"_drumPatternC.mid")

        cargarMidi("midi/output_"+estilo+"_drumPatternA.mid")
        cargarMidi("midi/output_"+estilo+"_drumPatternB.mid")
        cargarMidi("midi/output_"+estilo+"_drumPatternA.mid")
        cargarMidi("midi/output_"+estilo+"_drumPatternC.mid")



for i in range (10):
    RPR_DeleteTrack(RPR_GetTrack(0, 0))
    
for i in range (10):
    RPR_TrackFX_Delete(RPR_GetMasterTrack(0), 0)

n_tracks = 9

for i in range(n_tracks):
    RPR_InsertTrackAtIndex(i, True)
    RPR_SetTrackColor(RPR_GetTrack(0, i), random.randint(0, 0x1000000))

RPR_SetTempoTimeSigMarker(0, -1, 0, -1, -1, 120, 0, 0, True)


tematica = 0
entorno = 0
lofi = False
retro = False
agua = False

#Melodía instrumento 1    
crearPista1(1, tematica, random.randint(0, 9))

#Melodía instrumento 2    
crearPista1(2, tematica, random.randint(0, 9))

#Acompañamiento 1
crearPista3(3, tematica, random.randint(0, 9), random.randint(1, 3), random.randint(0, 9))

#Acompañamiento 2
crearPista3(4, tematica, random.randint(0, 9), random.randint(1, 3), random.randint(0, 9))

#Pads o strings
crearPista5(5, tematica, random.randint(0, 9))

#Bajo
crearPista6(6, tematica, random.randint(0, 9), random.randint(1, 3), random.randint(0, 9))

#Batería
crearPista7(7, tematica, random.randint(0, 9))

#Transiciones 1
crearPista8(8, tematica, 0)

#Transiciones 2
crearPista8(9, tematica, 0)


for i in range(5):
    RPR_SetMediaTrackInfo_Value(RPR_GetTrack(0, i), "D_PAN", (random.randint(-20, 20)/100))


lofi_preset = random.randint(0, 9)



RPR_TrackFX_AddByName(RPR_GetMasterTrack(0), "Unison Zen Master (Unison)", False, -1)
if(lofi):
    RPR_TrackFX_SetPreset(RPR_GetMasterTrack(0), 0, "lofi"+str(lofi_preset)) 
else:
    RPR_TrackFX_SetPreset(RPR_GetMasterTrack(0), 0, "bypass") 

RPR_TrackFX_AddByName(RPR_GetMasterTrack(0), "TAL BitCrusher - TAL (TAL - Togu Audio Line)", False, -1)
if(retro):
    RPR_TrackFX_SetPreset(RPR_GetMasterTrack(0), 1, "retro1") 
else:
    RPR_TrackFX_SetPreset(RPR_GetMasterTrack(0), 1, "bypass") 

RPR_TrackFX_AddByName(RPR_GetMasterTrack(0), "ReaEQ (Cockos)", False, -1)
if(agua):
    RPR_TrackFX_SetPreset(RPR_GetMasterTrack(0), 2, "eqAgua1") 
else:
    RPR_TrackFX_SetPreset(RPR_GetMasterTrack(0), 2, "bypass") 

RPR_TrackFX_AddByName(RPR_GetMasterTrack(0), "OrilRiver (Denis Tihanov)", False, -1)
RPR_TrackFX_SetPreset(RPR_GetMasterTrack(0), 3, "entorno"+str(entorno)) 


RPR_TrackFX_AddByName(RPR_GetMasterTrack(0), "ReaComp (Cockos)", False, -1)
if(tematica != 1):
    RPR_TrackFX_SetPreset(RPR_GetMasterTrack(0), 4, "comp1") 

RPR_TrackFX_AddByName(RPR_GetMasterTrack(0), "ReaLimit (Cockos)", False, -1)
if(tematica != 1):
    RPR_TrackFX_SetPreset(RPR_GetMasterTrack(0), 5, "limit1") 

RPR_TrackFX_AddByName(RPR_GetMasterTrack(0), "AFTER (x86) (TWest Productions)", False, -1)
RPR_TrackFX_SetPreset(RPR_GetMasterTrack(0), 6, "mastering1") 


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



arreglo = [[False] * 8 for _ in range(7)]

arreglo = [[random.choice([True, False]) for _ in range(8)] for _ in range(7)]

# Nos aseguramos de que no haya ningún espacio de tiempo en silencio
for col in range(len(arreglo[0])):
    column_values = [row[col] for row in arreglo]
    if all(value == False for value in column_values):
        arreglo[2][col] = True


if(tematica == 1):
    # Contar la cantidad de True en cada columna
    column_counts = [sum(1 for row in arreglo if row[col]) for col in range(len(arreglo[0]))]

    # Limitar a dos casillas True por columna, con prioridad en la fila 3 y luego en orden ascendente desde la 1
    for col in range(len(arreglo[0])):
        if column_counts[col] > 2:
            # Obtener las filas que tienen True en la columna actual
            true_rows = [row_idx for row_idx, row in enumerate(arreglo) if row[col]]
            # Ordenar las filas según la prioridad
            true_rows.sort(key=lambda x: x == 2, reverse=True)
            # Mantener las primeras dos filas con True, según la prioridad
            for idx in true_rows[2:]:
                arreglo[idx][col] = False

# Calcular posiciones para colocar transiciones
riser = [False] * len(arreglo[0])

for col in range(len(arreglo[0]) - 1):
    for row in range(len(arreglo)):
        if (arreglo[row][col] and not arreglo[row][col + 1]) or (not arreglo[row][col] and arreglo[row][col + 1]):
            riser[col] = True
            break




# Mover el cursor al inicio de la pista
RPR_SetEditCurPos(0, True, True)



RPR_SetMediaTrackInfo_Value(RPR_GetTrack(0, 0), "I_SELECTED", 1)
i = 0
for value in arreglo[0]:
    if value:
        RPR_SetEditCurPos(i * 16, True, True)
        cargarMidi("midi/markov_melody_0.mid")
    i += 1


RPR_SetMediaTrackInfo_Value(RPR_GetTrack(0, 1), "I_SELECTED", 1)
i = 0
for value in arreglo[1]:
    if value:
        RPR_SetEditCurPos(i * 16, True, True)
        cargarMidi("midi/markov_melody_0.mid")
    i += 1
i = 0

RPR_SetMediaTrackInfo_Value(RPR_GetTrack(0, 2), "I_SELECTED", 1)
for value in arreglo[2]:
    if value:
        RPR_SetEditCurPos(i * 16, True, True)
        cargarMidi("midi/output_harmony.mid")
    i += 1
i = 0

RPR_SetMediaTrackInfo_Value(RPR_GetTrack(0, 3), "I_SELECTED", 1)
for value in arreglo[3]:
    if value:
        RPR_SetEditCurPos(i * 16, True, True)
        cargarMidi("midi/output_harmony.mid")
    i += 1
i = 0

RPR_SetMediaTrackInfo_Value(RPR_GetTrack(0, 4), "I_SELECTED", 1)
for value in arreglo[4]:
    if value:
        RPR_SetEditCurPos(i * 16, True, True)
        cargarMidi("midi/output_harmony.mid")
    i += 1

i = 0
RPR_SetMediaTrackInfo_Value(RPR_GetTrack(0, 5), "I_SELECTED", 1)
for value in arreglo[5]:
    if value:
        RPR_SetEditCurPos(i * 16, True, True)
        cargarMidi("midi/output_harmony.mid")
    i += 1

i = 0
RPR_SetMediaTrackInfo_Value(RPR_GetTrack(0, 6), "I_SELECTED", 1)
for value in arreglo[6]:
    if value:
        RPR_SetEditCurPos(i * 16, True, True)
    
        cargarDrums(tematica)

    i += 1


#RPR_SetMediaItemLength(RPR_GetMediaItem(0, 2), 24, False)



i = 0
pista = 7 
for value in riser:
    if value:
        
        RPR_SetMediaTrackInfo_Value(RPR_GetTrack(0, pista), "I_SELECTED", 1)
        RPR_SetEditCurPos(i * 16, True, True) 
        cargarMidi("midi/output_harmony.mid")



        RPR_SetTrackAutomationMode(RPR_GetTrack(0, pista), 3)

        RPR_SetEditCurPos(i * 16 + 0.1, True, True) 
        RPR_SetTrackUIVolume(RPR_GetTrack(0, pista), 0.0, False, False, 0)
        RPR_SetEditCurPos(i * 16 + 12, True, True) 
        RPR_SetTrackUIVolume(RPR_GetTrack(0, pista), 1.0, False, False, 0)
        RPR_SetEditCurPos(i * 16 + 16, True, True) 
        RPR_SetTrackUIVolume(RPR_GetTrack(0, pista), 1.0, False, False, 0)
        RPR_SetEditCurPos(i * 16 + 16.1, True, True) 
        RPR_SetTrackUIVolume(RPR_GetTrack(0, pista), 0.0, False, False, 0)

        RPR_SetTrackAutomationMode(RPR_GetTrack(0, pista), 0)

        #if(pista == 7):
        #    pista = 8
        #else:
        #    pista = 7

    i += 1
                



ajustarTempo(tematica)


RPR_SetEditCurPos(0, True, True)







