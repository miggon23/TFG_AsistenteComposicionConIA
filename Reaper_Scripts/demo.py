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
        tempo = random.randint(70, 100)
    elif(tematica == 4):
        tempo = random.randint(105, 150)
    elif(tematica == 5):
        tempo = random.randint(105, 150)
    elif(tematica == 6):
        tempo = random.randint(80, 110)
    elif(tematica == 7):
        tempo = random.randint(70, 140)
    elif(tematica == 8):
        tempo = random.randint(70, 100)
    elif(tematica == 9):
        tempo = random.randint(80, 110)
    elif(tematica == 10):
        tempo = random.randint(90, 135)
    elif(tematica == 11):
        tempo = random.randint(90, 135)
    RPR_SetTempoTimeSigMarker(0, -1, 0, -1, -1, tempo, 0, 0, True)

def estiloDrums(tematica):
    estilo = "BASIC"

    if(tematica == 0):
        estilo = random.choice(["BASIC", "SHAKER", "JAZZ"])
    elif(tematica == 1):
        estilo = "BASIC"
    elif(tematica == 2):
        estilo = random.choice(["BASIC", "CLAP", "SHAKER"])
    elif(tematica == 3):
        estilo = random.choice(["BASIC", "JAZZ", "ROCK"])
    elif(tematica == 4):
        estilo = random.choice(["SHAKER", "LATIN", "ROCK"])
    elif(tematica == 5):
        estilo = random.choice(["METAL", "LATIN", "ROCK"])
    elif(tematica == 6):
        estilo = random.choice(["BASIC", "CLAP", "JAZZ"])
    elif(tematica == 7):
        estilo = random.choice(["SHAKER", "METAL", "ROCK"])
    elif(tematica == 8):
        estilo = random.choice(["CLAP", "SHAKER", "JAZZ"])
    elif(tematica == 9):
        estilo = random.choice(["BASIC", "JAZZ", "ROCK"])
    elif(tematica == 10):
        estilo = random.choice(["BASIC", "CLAP", "ROCK"])
    elif(tematica == 11):
        estilo = random.choice(["CLAP", "SHAKER", "LATIN"])

    return estilo

def cargarDrums(tematica):
       
    estilo = estiloDrums(tematica)
    for i in range(4):
        cargarMidi("midi/output_"+estilo+"_drumPattern"+random.choice(["A", "B", "C"])+".mid")
        
    estilo = estiloDrums(tematica)
    for i in range(4):
        cargarMidi("midi/output_"+estilo+"_drumPattern"+random.choice(["A", "B", "C"])+".mid")




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
        if(preset == 0):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Room Piano v3 (SampleScience) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pianoSolo0")
        elif(preset == 1):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Pianotone 600 v2 (SampleScience) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pianoSolo1")
        elif(preset == 2):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "EVM Grand Piano v1.1 (x86) (Etric van-mayer)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "pianoSolo2")
        elif(preset <= 7):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DPiano-A (Dead Duck Software)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "pianoSolo"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Upright Piano (audiolatry) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "pianoSolo"+str(preset))
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
    
    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "ReaEQ (Cockos)", False, -1)
    if(tematica != 1):
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 5, "eqPista"+str(pista))



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
        if(preset == 0):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Room Piano v3 (SampleScience) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pianoSolo0")
        elif(preset == 1):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Pianotone 600 v2 (SampleScience) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pianoSolo1")
        elif(preset == 2):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "EVM Grand Piano v1.1 (x86) (Etric van-mayer)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "pianoSolo2")
        elif(preset <= 7):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DPiano-A (Dead Duck Software)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "pianoSolo"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Upright Piano (audiolatry) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "pianoSolo"+str(preset))
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

    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "ReaEQ (Cockos)", False, -1)
    if(tematica != 1):
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 5, "eqPista"+str(pista))

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
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Spicy Guitar (64 bits) (Keolab)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        else:
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "VSTi: DSK Strings (x86) (DSK)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 1):
        if(preset == 0):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Room Piano v3 (SampleScience) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pianoSolo0")
        elif(preset == 1):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Pianotone 600 v2 (SampleScience) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pianoSolo1")
        elif(preset == 2):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "EVM Grand Piano v1.1 (x86) (Etric van-mayer)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "pianoSolo2")
        elif(preset <= 7):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DPiano-A (Dead Duck Software)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "pianoSolo"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Upright Piano (audiolatry) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "pianoSolo"+str(preset))
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

    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "ReaEQ (Cockos)", False, -1)
    if(tematica != 1): 
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 5, "eqPista"+str(pista))

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
    if(tematica == 1 or tematica == 8):
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
        if(preset == 0):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Room Piano v3 (SampleScience) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pianoSolo0")
        elif(preset == 1):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Pianotone 600 v2 (SampleScience) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pianoSolo1")
        elif(preset == 2):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "EVM Grand Piano v1.1 (x86) (Etric van-mayer)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "pianoSolo2")
        elif(preset <= 7):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DPiano-A (Dead Duck Software)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "pianoSolo"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Upright Piano (audiolatry) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "pianoSolo"+str(preset))
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

    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "ReaEQ (Cockos)", False, -1)
    if(tematica != 1):
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 6, "eqPista"+str(pista))

#Batería instrumento 7   
def crearPista7(pista, tematica, preset, fill, preset_fill):
    i = pista - 1
    pista = 7

    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "JS: MIDI Transpose Notes", False, -1)
    if tematica == 2 or (tematica == 4 and preset > 5) or tematica == 5:
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "octaveUp") 
    
    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "BlueArp", False, -1)
    if fill:
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "fill"+str(preset_fill))
    else:
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "bypass") 

    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Humanisator (x86) (Tobybear)", False, -1)
    if fill:
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "humanisator4")
    else:
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "humanisator3")
    
    if(tematica == 0):
        if(preset <= 4):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK mini DRUMZ 2 (x86) (DSK Music)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 7):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Apari Tenpan (x86) (Apari)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        else:
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK DrumZ 8bitZ (x86) (DSK Music)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 1):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK mini DRUMZ 2 (x86) (DSK Music)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
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

    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "ReaEQ (Cockos)", False, -1)
    RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 6, "eqPista"+str(pista))


#Transiciones instrumento 8 y 9   
def crearPista8(pista, tematica, preset, preset2, preset3):
    i = pista-1
    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "JS: MIDI Transpose Notes", False, -1)
    RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "octaveUp") 
    
    if(tematica == 0):
        if(preset <= 0):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Room Piano v3 (SampleScience) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "riserTematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 5):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK Strings (x86) (DSK)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "riserTematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Spicy Guitar (64 bits) (Keolab)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "riserTematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 1):
            if(tematica == 0):
                RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Room Piano v3 (SampleScience) (32 out)", False, -1)
                RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "pianoSolo0")
            elif(preset == 1):
                RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Pianotone 600 v2 (SampleScience) (32 out)", False, -1)
                RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "pianoSolo1")
            elif(preset == 2):
                RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "EVM Grand Piano v1.1 (x86) (Etric van-mayer)", False, -1)
                RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "pianoSolo2")
            elif(preset <= 7):
                RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DPiano-A (Dead Duck Software)", False, -1)
                RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "pianoSolo"+str(preset))
            elif(preset <= 9):
                RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Upright Piano (audiolatry) (32 out)", False, -1)
                RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "pianoSolo"+str(preset))
    
    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Flux Mini 2 (Caelum Audio)", False, -1)
    RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "riser"+str(preset2))

    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "ValhallaSupermassive (Valhalla DSP, LLC)", False, -1)
    RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "riser"+str(preset3))


#Transiciones instrumento 10 y 11   
def crearPista10(pista, tematica, preset, preset2, preset3):
    i = pista-1
    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "JS: MIDI Transpose Notes", False, -1)
    RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "octaveUp") 
    
    if(tematica == 0):
        if(preset <= 0):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Room Piano v3 (SampleScience) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "downriserTematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "TAL-NoiseMaker (TAL-Togu Audio Line)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "downriserTematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 1):
            if(preset == 0):
                RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Room Piano v3 (SampleScience) (32 out)", False, -1)
                RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "pianoSolo0")
            elif(preset == 1):
                RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Pianotone 600 v2 (SampleScience) (32 out)", False, -1)
                RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "pianoSolo1")
            elif(preset == 2):
                RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "EVM Grand Piano v1.1 (x86) (Etric van-mayer)", False, -1)
                RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "pianoSolo2")
            elif(preset <= 7):
                RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DPiano-A (Dead Duck Software)", False, -1)
                RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "pianoSolo"+str(preset))
            elif(preset <= 9):
                RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Upright Piano (audiolatry) (32 out)", False, -1)
                RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "pianoSolo"+str(preset))

    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "ValhallaSupermassive (Valhalla DSP, LLC)", False, -1)
    RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "downriser"+str(preset3))

    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Flux Mini 2 (Caelum Audio)", False, -1)
    RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "downriser"+str(preset2))

#Ear candy instrumento 13, 14 y 15   
def crearPista13(pista, tematica, preset, preset2, preset3, preset4, preset_arpegio):
    i = pista-1
    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "BlueArp", False, -1)
    RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, "candy"+str(preset_arpegio)) 
    
    if(tematica == 0):
        if(preset <= 2):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Ocarina (x86) (Christopher Clews) (mono)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "candyTematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 3):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "VSCO2 Marimba (bigcat) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "candyTematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 5):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Ukulele (x86) (Christopher Clews) (mono)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "candyTematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 7):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "wind (x86) (rurik leffanta)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "candyTematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DPiano-A (Dead Duck Software)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "candyTematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 1):
            if(preset == 0):
                RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Room Piano v3 (SampleScience) (32 out)", False, -1)
                RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "pianoSolo0")
            elif(preset == 1):
                RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Pianotone 600 v2 (SampleScience) (32 out)", False, -1)
                RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "pianoSolo1")
            elif(preset == 2):
                RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "EVM Grand Piano v1.1 (x86) (Etric van-mayer)", False, -1)
                RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "pianoSolo2")
            elif(preset <= 7):
                RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DPiano-A (Dead Duck Software)", False, -1)
                RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "pianoSolo"+str(preset))
            elif(preset <= 9):
                RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Upright Piano (audiolatry) (32 out)", False, -1)
                RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "pianoSolo"+str(preset))


    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Flux Mini 2 (Caelum Audio)", False, -1)
    RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "candy"+str(preset2))
    if tematica == 1:   
        RPR_TrackFX_SetEnabled(RPR_GetTrack(0, i), 2, False)

    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Flux Mini 2 (Caelum Audio)", False, -1)
    RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "candyGate"+str(preset3))

    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "CRMBL (unplugred)", False, -1)
    RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 4, "candy"+str(preset4))

    
    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "ReaComp (Cockos)", False, -1)
    if(tematica != 1):
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 4, "gain13")
    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "ReaLimit (Cockos)", False, -1)
    if(tematica != 1):
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 5, "gain13")



for i in range (20):
    RPR_DeleteTrack(RPR_GetTrack(0, 0))
    
for i in range (10):
    RPR_TrackFX_Delete(RPR_GetMasterTrack(0), 0)

n_tracks = 16

for i in range(n_tracks):
    RPR_InsertTrackAtIndex(i, True)
    RPR_SetTrackColor(RPR_GetTrack(0, i), random.randint(0, 0x1000000))

RPR_SetTempoTimeSigMarker(0, -1, 0, -1, -1, 120, 0, 0, True)


tematica = 0
reverb = True
entorno = 0
lofi = False
retro = False
agua = False
espacial = False

lofi_preset = random.randint(0, 9)
espacial_preset = random.randint(0, 9)


if(tematica == 1):
    presetPiano = random.randint(0, 7)        
    
    crearPista1(1, tematica, presetPiano)   
    crearPista1(2, tematica, presetPiano)
    crearPista3(3, tematica, presetPiano, random.randint(1, 3), random.randint(0, 9))
    crearPista3(4, tematica, presetPiano, random.randint(1, 3), random.randint(0, 9))
    crearPista5(5, tematica, presetPiano)
    crearPista6(6, tematica, presetPiano, random.randint(1, 3), random.randint(0, 9))
    presetBateria = random.randint(0, 9)
    crearPista7(7, tematica, presetBateria, False, 0)
    crearPista8(8, tematica, presetPiano, random.randint(0, 9), random.randint(0, 9))
    crearPista8(9, tematica, presetPiano, random.randint(0, 9), random.randint(0, 9))
    crearPista10(10, tematica, presetPiano, random.randint(0, 9), random.randint(0, 9))
    crearPista10(11, tematica, presetPiano, random.randint(0, 9), random.randint(0, 9))
    crearPista7(12, tematica, presetBateria, True, random.randint(0, 9))
    crearPista13(13, tematica, presetPiano, random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9))
    crearPista13(14, tematica, presetPiano, random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9))
    crearPista13(15, tematica, presetPiano, random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9))
    crearPista13(16, tematica, presetPiano, random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9))
else:
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

    presetBateria = random.randint(0, 9)
    #Batería
    crearPista7(7, tematica, presetBateria, False, 0)

    #Transiciones 1
    crearPista8(8, tematica, random.randint(0, 9), random.randint(0, 9), random.randint(0, 9))

    #Transiciones 2
    crearPista8(9, tematica, random.randint(0, 9), random.randint(0, 9), random.randint(0, 9))

    #Transiciones 3
    crearPista10(10, tematica, random.randint(0, 9), random.randint(0, 9), random.randint(0, 9))

    #Transiciones 4
    crearPista10(11, tematica, random.randint(0, 9), random.randint(0, 9), random.randint(0, 9))

    #Drum Fills
    crearPista7(12, tematica, presetBateria, True, random.randint(0, 9))

    #Ear Candy 1
    crearPista13(13, tematica, random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9))

    #Ear Candy 2
    crearPista13(14, tematica, random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9))

    #Ear Candy 3
    crearPista13(15, tematica, random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9))
    
    #Ear Candy 4
    crearPista13(16, tematica, random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9))


for i in range(5):
    RPR_SetMediaTrackInfo_Value(RPR_GetTrack(0, i), "D_PAN", (random.randint(-20, 20)/100))

    
for i in range(4):
    RPR_SetMediaTrackInfo_Value(RPR_GetTrack(0, i + 12), "D_PAN", (random.randint(-90, 90)/100))



if(espacial):
    RPR_TrackFX_AddByName(RPR_GetMasterTrack(0), "ValhallaSupermassive (Valhalla DSP, LLC)", False, -1)
    RPR_TrackFX_SetPreset(RPR_GetMasterTrack(0), 0, "espacial"+str(espacial_preset)) 
else:    
    RPR_TrackFX_AddByName(RPR_GetMasterTrack(0), "OrilRiver (Denis Tihanov)", False, -1)
    if(reverb):
        RPR_TrackFX_SetPreset(RPR_GetMasterTrack(0), 0, "entorno"+str(entorno)) 
    else:
        RPR_TrackFX_SetEnabled(RPR_GetMasterTrack(0), 0, False)


RPR_TrackFX_AddByName(RPR_GetMasterTrack(0), "Unison Zen Master (Unison)", False, -1)
if(lofi):
    RPR_TrackFX_SetPreset(RPR_GetMasterTrack(0), 1, "lofi"+str(lofi_preset)) 
else:
    RPR_TrackFX_SetEnabled(RPR_GetMasterTrack(0), 1, False)



RPR_TrackFX_AddByName(RPR_GetMasterTrack(0), "DeltaModulator (Xfer Records)", False, -1)
if(retro):
    RPR_TrackFX_SetPreset(RPR_GetMasterTrack(0), 2, "retro1") 
else:
    RPR_TrackFX_SetEnabled(RPR_GetMasterTrack(0), 2, False)

    
RPR_TrackFX_AddByName(RPR_GetMasterTrack(0), "ReaEQ (Cockos)", False, -1)
if(agua):
    RPR_TrackFX_SetPreset(RPR_GetMasterTrack(0), 3, "eqAgua1") 
else:
    RPR_TrackFX_SetEnabled(RPR_GetMasterTrack(0), 3, False)

RPR_TrackFX_AddByName(RPR_GetMasterTrack(0), "ReaComp (Cockos)", False, -1)
if(tematica != 1):
    RPR_TrackFX_SetPreset(RPR_GetMasterTrack(0), 4, "comp1") 

RPR_TrackFX_AddByName(RPR_GetMasterTrack(0), "ReaLimit (Cockos)", False, -1)
if(tematica != 1):
    RPR_TrackFX_SetPreset(RPR_GetMasterTrack(0), 5, "limit1") 

RPR_TrackFX_AddByName(RPR_GetMasterTrack(0), "ReaEQ (Cockos)", False, -1)
if espacial:
    RPR_TrackFX_SetPreset(RPR_GetMasterTrack(0), 6, "eqMixExpacial") 
elif retro:
    RPR_TrackFX_SetPreset(RPR_GetMasterTrack(0), 6, "eqMixRetro") 
else:
    RPR_TrackFX_SetPreset(RPR_GetMasterTrack(0), 6, "eqMixTematica"+str(tematica)) 

RPR_TrackFX_AddByName(RPR_GetMasterTrack(0), "OrilRiver (Denis Tihanov)", False, -1)
RPR_TrackFX_SetPreset(RPR_GetMasterTrack(0), 7, "expansor") 

RPR_TrackFX_AddByName(RPR_GetMasterTrack(0), "AFTER (x86) (TWest Productions)", False, -1)
RPR_TrackFX_SetPreset(RPR_GetMasterTrack(0), 8, "mastering1") 


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

if tematica == 1:
    arreglo[6] = [False]*8

if arreglo[0][0]:
    arreglo[1][0] = False

# Nos aseguramos de que no haya ningún espacio de tiempo en silencio
for col in range(len(arreglo[0])):
    column_values = [row[col] for row in arreglo]
    if all(value == False for value in column_values):
        arreglo[2][col] = True

# Limitamos las casillas de acompañamiento
for col in range(len(arreglo[0])):
    # Si ambas casillas 3 y 4 están marcadas como True, mantener solo la casilla 3
    if arreglo[2][col] and arreglo[3][col]:
        arreglo[3][col] = False

if tematica == 1:
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
        elif column_counts[col] == 1:
            if arreglo[0][col] == True:
                arreglo[3][col] == True
            else:
                arreglo[0][col] == True


# Contar la cantidad de True en la primera columna
first_column_count = sum(1 for row in arreglo if row[0])

# Limitar a tres casillas True en la primera columna, con prioridad en la fila 3 y luego en orden descendente desde la 1
if first_column_count > 3:
    # Obtener las filas que tienen True en la primera columna
    true_rows = [row_idx for row_idx, row in enumerate(arreglo) if row[0]]
    # Ordenar las filas según la prioridad
    true_rows.sort(key=lambda x: x == 2, reverse=True)
    # Mantener las primeras tres filas con True, según la prioridad
    for idx in true_rows[3:]:
        arreglo[idx][0] = False


adelantar = [False] * 8

# Determinar las posiciones donde adelantar la entrada de la pista
for col in range(7):
    for fila in range(7):
        if arreglo[fila][col]:  # Si el elemento actual es True
            # comprobar si es False en la siguiente columna
            if not arreglo[fila][col + 1]:
                adelantar[col] = True
            else:
                adelantar[col] = False
                break


# Rellenar un nuevo arreglo con las columnas en las que se adelanta la entrada
arreglo_adelantar = [[False] * 8 for _ in range(7)]
for col in range(7):
    if adelantar[col]:
        if arreglo[5][col+1]: # Priorizamos el bajo
            arreglo_adelantar[5][col] = True
        else:
            for fila in range(5):
                if arreglo[fila][col+1]:
                    arreglo_adelantar[fila][col] = True
                    break  # Salir del bucle interno para asegurarse de marcar solo una casilla por columna



# Calcular posiciones para colocar transiciones
riser = [False] * len(arreglo[0])
downriser = [False] * len(arreglo[0])
drumFill = [False] * len(arreglo[0])

# Calcular posiciones para colocar ear candy
candy = [False] * len(arreglo[0])


# Marcamos las casillas que serán True en la siguiente columna
for col in range(len(arreglo[0]) - 1):
    for row in range(len(arreglo)):
        if row == 6:  # Última fila
            if not arreglo[row][col] and arreglo[row][col+1]:
                drumFill[col] = True


# Contar cuántas casillas serán True en la siguiente columna cuando ahora es False
next_true_counts = [0] * len(arreglo[0])

for col in range(len(arreglo[0]) - 1):
    for row in range(len(arreglo)):
        if not arreglo[row][col] and arreglo[row][col + 1]:
            next_true_counts[col + 1] += 1

# Contar cuántas casillas serán False en la siguiente columna cuando ahora es True
next_false_counts = [0] * len(arreglo[0])

for col in range(len(arreglo[0]) - 1):
    for row in range(len(arreglo)):
        if arreglo[row][col] and not arreglo[row][col + 1]:
            next_false_counts[col + 1] += 1


for col in range(len(arreglo[0]) - 1):
        if arreglo[6][col] and arreglo[6][col + 1]:
            if next_true_counts[col] == next_false_counts[col]:
                drumFill[col] = True

for col in range(len(arreglo[0]) - 1):
    if next_true_counts[col + 1] > next_false_counts[col + 1]:
        riser[col] = True
        drumFill[col] = False

for col in range(len(arreglo[0]) - 1):
    if (next_true_counts[col + 1] + 1) < next_false_counts[col + 1]:
        downriser[col + 1] = True

for col in range(len(arreglo[0])):
    contador_true = sum(arreglo[fila][col] for fila in range(len(arreglo)))
    if contador_true <= 3:
        candy[col] = True


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

i = 0
RPR_SetMediaTrackInfo_Value(RPR_GetTrack(0, 7), "I_SELECTED", 1)
for value in riser:
    if value:
        RPR_SetEditCurPos(i * 16, True, True)
        cargarMidi("midi/output_harmony.mid")
    i += 1

i = 0
RPR_SetMediaTrackInfo_Value(RPR_GetTrack(0, 8), "I_SELECTED", 1)
for value in riser:
    if value:
        RPR_SetEditCurPos(i * 16, True, True)
        cargarMidi("midi/output_harmony.mid")
    i += 1
    
i = 0
RPR_SetMediaTrackInfo_Value(RPR_GetTrack(0, 9), "I_SELECTED", 1)
for value in downriser:
    if value:
        RPR_SetEditCurPos(i * 16, True, True)
        cargarMidi("midi/output_harmony.mid")
    i += 1 

i = 0
RPR_SetMediaTrackInfo_Value(RPR_GetTrack(0, 10), "I_SELECTED", 1)
for value in downriser:
    if value:
        RPR_SetEditCurPos(i * 16, True, True)
        cargarMidi("midi/output_harmony.mid")
    i += 1

i = 0
RPR_SetMediaTrackInfo_Value(RPR_GetTrack(0, 11), "I_SELECTED", 1)
for value in drumFill:
    if value:
        RPR_SetEditCurPos(i * 16 + 14, True, True)
        cargarMidi("midi/fillTemplate.mid")
    i += 1

i = 0
pista = 12
for value in candy:
    if value:
        
        RPR_SetOnlyTrackSelected(RPR_GetTrack(0, pista))
        RPR_SetEditCurPos(i * 16, True, True)
        cargarMidi("midi/output_harmony.mid")
        
        pista += 1
        if pista == 16:
            pista = 12

    i += 1

for col in range(8):
    for fila in range(7):
        if arreglo_adelantar[fila][col]:
            RPR_SetOnlyTrackSelected(RPR_GetTrack(0, fila))
            RPR_SetEditCurPos(col * 16, True, True)

            if(fila < 2):
                cargarMidi("midi/markov_melody_0.mid")
            else:
                cargarMidi("midi/output_harmony.mid")

            cont = 0
            for i in range(col):
                if arreglo[fila][i]:
                    cont += 1

            RPR_SplitMediaItem(RPR_GetTrackMediaItem(RPR_GetTrack(0, fila), cont), col * 16 + 14)
            RPR_DeleteTrackMediaItem(RPR_GetTrack(0, fila), RPR_GetTrackMediaItem(RPR_GetTrack(0, fila), cont))





i = 0
pista = 7 
for value in riser:
    if value:

        RPR_SetTrackAutomationMode(RPR_GetTrack(0, pista), 3)

        RPR_SetEditCurPos(i * 16 + 0.1, True, True) 
        RPR_SetTrackUIVolume(RPR_GetTrack(0, pista), 0.0, False, False, 0)
        RPR_SetEditCurPos(i * 16 + 8, True, True) 
        RPR_SetTrackUIVolume(RPR_GetTrack(0, pista), 1.0, False, False, 0)
        RPR_SetEditCurPos(i * 16 + 16, True, True) 
        RPR_SetTrackUIVolume(RPR_GetTrack(0, pista), 1.0, False, False, 0)
        RPR_SetEditCurPos(i * 16 + 16.1, True, True) 
        RPR_SetTrackUIVolume(RPR_GetTrack(0, pista), 0.0, False, False, 0)

        RPR_SetTrackAutomationMode(RPR_GetTrack(0, pista), 0)

        if(pista == 7):
            pista = 8
        else:
            pista = 7

    i += 1
              
i = 0
pista = 9 
for value in downriser:
    if value:

        RPR_SetTrackAutomationMode(RPR_GetTrack(0, pista), 3)

        RPR_SetEditCurPos(i * 16 - 0.1, True, True) 
        RPR_SetTrackUIVolume(RPR_GetTrack(0, pista), 0.0, False, False, 0)
        RPR_SetEditCurPos(i * 16, True, True) 
        RPR_SetTrackUIVolume(RPR_GetTrack(0, pista), 1.0, False, False, 0)
        RPR_SetEditCurPos(i * 16 + 8, True, True) 
        RPR_SetTrackUIVolume(RPR_GetTrack(0, pista), 1.0, False, False, 0)
        RPR_SetEditCurPos(i * 16 + 8.1, True, True) 
        RPR_SetTrackUIVolume(RPR_GetTrack(0, pista), 0.0, False, False, 0)

        RPR_SetTrackAutomationMode(RPR_GetTrack(0, pista), 0)

        if(pista == 9):
            pista = 10
        else:
            pista = 9

    i += 1
                



ajustarTempo(tematica)


RPR_SetEditCurPos(0, True, True)







