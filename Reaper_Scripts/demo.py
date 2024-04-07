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
    elif(tematica == 12):
        tempo = random.randint(105, 150)
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
        estilo = random.choice(["BASIC", "ROCK", "ROCK"])
    elif(tematica == 11):
        estilo = random.choice(["BASIC", "LATIN", "ROCK"])
    elif(tematica == 12):
        estilo = random.choice(["DISCO", "DISCO", "DISCO"])

    return estilo

def cargarDrums(tematica, patron):
    
    estilo = estiloDrums(tematica)
    for item in patron:
        cargarMidi("midi/output_"+estilo+"_drumPattern"+ item +".mid")
        
    estilo = estiloDrums(tematica)
    for item in patron:
        cargarMidi("midi/output_"+estilo+"_drumPattern"+ item +".mid")

def cargarMelodia(tematica, patron, recortar = False, pos = -1):

    estilo = "output_song"

    if(tematica == 0):
        estilo = "Lydian_output_song"
    elif(tematica == 1):
        estilo = "output_song"
    elif(tematica == 2):
        estilo = "Phrygian_output_song"
    elif(tematica == 3):
        estilo = "Dorian_output_song"
    elif(tematica == 4):
        estilo = "Mixolydian_output_song"
    elif(tematica == 5):
        estilo = "Phrygian_output_song"
    elif(tematica == 6):
        estilo = "Mixolydian_output_song"
    elif(tematica == 7):
        estilo = "Locrian_output_song"
    elif(tematica == 8):
        estilo = "Mixolydian_output_song"
    elif(tematica == 9):
        estilo = "Lydian_output_song"
    elif(tematica == 10):
        estilo = "Dorian_output_song"
    elif(tematica == 11):
        estilo = "output_song"
    elif(tematica == 12):
        estilo = "output_song"

    if not recortar:
        cont = 0
        for item in patron:
            if(pos != -1):
                RPR_SetEditCurPos(pos + cont*4, True, True)
                cont += 1
            cargarMidi("midi/"+estilo+ item +".mid")
    else:
        cargarMidi("midi/"+estilo+"D.mid")

def cargarArmonia(tematica, recortar = False):

    estilo = "output_harmony"

    if(tematica == 0):
        estilo = "Lydian_output_harmony"
    elif(tematica == 1):
        estilo = "output_harmony"
    elif(tematica == 2):
        estilo = "Phrygian_output_harmony"
    elif(tematica == 3):
        estilo = "Dorian_output_harmony"
    elif(tematica == 4):
        estilo = "Mixolydian_output_harmony"
    elif(tematica == 5):
        estilo = "Phrygian_output_harmony"
    elif(tematica == 6):
        estilo = "Mixolydian_output_harmony"
    elif(tematica == 7):
        estilo = "Locrian_output_harmony"
    elif(tematica == 8):
        estilo = "Mixolydian_output_harmony"
    elif(tematica == 9):
        estilo = "Lydian_output_harmony"
    elif(tematica == 10):
        estilo = "Dorian_output_harmony"
    elif(tematica == 11):
        estilo = "output_harmony"
    elif(tematica == 12):
        estilo = "output_harmony"

    cargarMidi("midi/"+estilo+".mid")
    if not recortar:
        cargarMidi("midi/"+estilo+".mid")


#Melodía instrumento 1 y 2   
def crearPista1(i, tematica, preset, dream, ampli, ampli_preset, semitonos):
    pista = 1
    i -= 1


    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "JS: MIDI Transpose Notes", False, -1)
    RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, semitonos) 


    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "JS: MIDI Transpose Notes", False, -1)
    if(i == 1):
        if(tematica == 10):
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "octaveDown") 
        elif(tematica == 11 or tematica == 12):
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "") 
        else:
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "octaveUp")

    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Humanisator (x86) (Tobybear)", False, -1)
    RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "humanisator2") 

    if(tematica == 0):
        if(preset <= 0):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK Guitars Acousti (x86) (DSK Music)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 1):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK Guitars Nylon (x86) (DSK Music)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 2):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK Guitars Steel (x86) (DSK Music)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 4):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK AkoustiK GuitarZ (x86) (DSK MusicSZZ)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 5):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK Saxophones (DSK Music) (16 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 7):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK Strings (x86) (DSK)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        else:
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK AkoustiK Keyz (x86) (DSK MusicSZZ)", False, -1)
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
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pianoSolo2")
        elif(preset <= 7):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DPiano-A (Dead Duck Software)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pianoSolo"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Upright Piano (audiolatry) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pianoSolo"+str(preset))
    elif(tematica == 2):
        if(preset <= 0):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Room Piano v3 (SampleScience) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 2): 
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Zither Renaissance v2 (SampleScience) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 5): 
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Sitar (x86) (Christopher Clews)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 6): 
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK Indian DreamZ (x86) (DSK MusicSZZ)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9): 
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Quilcom SIM-DIZI v1.002 (Rex Basterfield)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 3):
        if(preset <= 1): 
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Virtual Handpan (SampleScience) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 5): 
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Quilcom SIM-DIZI v1.002 (Rex Basterfield)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9): 
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Dulcimator2 (x86) (Rock Hardbuns Global Entertainment)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 4):
        if(preset <= 1): 
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK World String (DSK Music) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 3): 
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Accordion (x86) (Safwan Matni)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 4): 
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK Indian DreamZ (x86) (DSK MusicSZZ)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 5): 
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Ukulele (x86) (Christopher Clews) (mono)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 7): 
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK Strings (x86) (DSK)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9): 
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Keyzone (x86) (Bitsonic LP)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 5):
        if(preset <= 0): 
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "VSCO2 Marimba (bigcat) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 4): 
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "01 Pipa (DSK Music) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 6): 
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK Indian DreamZ (x86) (DSK MusicSZZ)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 7): 
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Sonatina Xylopho (Maizesoft) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9): 
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Quilcom SIM-MBIRA v1.00 (Rex Basterfield)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 6): 
        if(preset <= 2): 
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK Strings (x86) (DSK)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 3): 
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Iowa Alto Flute (bigcat) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 4): 
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Sonatina Oboe (bigcat) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 5): 
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Sonatina Trombon (bigcat) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 6): 
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Iowa Trumpet (bigcat) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9): 
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Iowa Trumpet (bigcat) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 7):
        if(preset <= 4): 
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Darksichord 3 Lite (ESL) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 5): 
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DVS Guitar (x86) (Martin Best)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 7): 
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Keyzone (x86) (Bitsonic LP)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9): 
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK ChoirZ (x86) (DSK Music)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 8):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Toy Keyboard v3 (SampleScience) (32 out)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 9):
        if(preset <= 2): 
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Nu Guzheng v2 (SampleScience) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 5): 
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK World String (DSK Music) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 7): 
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "01 Pipa (DSK Music) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 8): 
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Toy Keyboard v3 (SampleScience) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9): 
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Quilcom SIM-SHENG v1.002 (Rex Basterfield)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 10):
        if(preset <= 1): 
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "OMB2 (x86) (Christopher Clews)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 4): 
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DVS Guitar (x86) (Martin Best)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 5): 
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Karoryfer Cute E (bigcat) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9): 
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "StratAVarious (x86) (Ian Webster)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))   
    elif(tematica == 11):
        if(preset <= 0): 
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK Guitars Acousti (x86) (DSK Music)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 1): 
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Karoryfer Cute E (bigcat) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 2): 
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Upright Piano (audiolatry) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 4): 
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DPiano-A (Dead Duck Software)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 5): 
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Virtual Handpan (SampleScience) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9): 
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Toy Keyboard v3 (SampleScience) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 12):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "TAL-NoiseMaker (TAL-Togu Audio Line)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))

    if(tematica == 10 and ampli):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "FA3 Full (x86) (Fretted Synth)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 4, "ampli"+str(ampli_preset))
    else:
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "ReaEQ (Cockos)", False, -1)

    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "ReaComp (Cockos)", False, -1)
    if(tematica != 1):
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 5, "gain"+str(pista))
    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "ReaLimit (Cockos)", False, -1)
    if(tematica != 1):
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 6, "gain"+str(pista))
    
    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "ReaEQ (Cockos)", False, -1)
    if(tematica != 1):
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 7, "eqPista"+str(pista))

    if dream:        
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Flux Mini 2 (Caelum Audio)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 8, "dream"+str(random.randint(0, 9))) 
    elif (tematica == 12):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Flux Mini 2 (Caelum Audio)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 8, "sidechain1")

#Acompañamiento instrumento 3 y 4   
def crearPista3(i, tematica, preset, arpegiado, preset_acordes, preset_arpegio, dream, ampli, ampli_preset, semitonos):
    pista = 3
    i -= 1

    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "JS: MIDI Transpose Notes", False, -1)
    RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, semitonos) 

    if(arpegiado == 1):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "BlueArp", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "arpegio"+str(preset_arpegio)) 
    elif(arpegiado == 2):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "BlueArp", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "acordes"+str(preset_acordes)) 
    elif(arpegiado == 3):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "BlueArp", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "bypass") 

        
    #if(tematica == 10 and arpegiado == 3):
    #    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Mildon Strummer 3 (x86) (Mildon Maducdoc)", False, -1)
    #    RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "strum1") 
    #else:
    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Humanisator (x86) (Tobybear)", False, -1)
    RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "humanisator1") 


    if(tematica == 0):
        if(preset <= 3):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK AkoustiK Keyz (x86) (DSK MusicSZZ)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 7):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Spicy Guitar (64 bits) (Keolab)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        else:
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK Elektrik Keyz (x86) (DSK)", False, -1)
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
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pianoSolo2")
        elif(preset <= 7):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DPiano-A (Dead Duck Software)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pianoSolo"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Upright Piano (audiolatry) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pianoSolo"+str(preset))

    elif(tematica == 2):
        if(preset <= 3):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK World String (DSK Music) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))

        elif(preset <= 7):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Spicy Guitar (64 bits) (Keolab)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))

        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Toy Keyboard v3 (SampleScience) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
   
    elif(tematica == 3):
        if(preset <= 2):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Dulcimator2 (x86) (Rock Hardbuns Global Entertainment)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Toy Keyboard v3 (SampleScience) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    
    elif(tematica == 4):
        if(preset <= 1):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Keyzone (x86) (Bitsonic LP)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 5):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Spicy Guitar (64 bits) (Keolab)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 6):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "MF Concert Guita (bigcat) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Accordion (x86) (Safwan Matni)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))

    elif(tematica == 5):
        if(preset <= 1):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "VSCO2 Marimba (bigcat) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 2):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "01 Pipa (DSK Music) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 7):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Quilcom SIM-DJEMBE v1.00 (Rex Basterfield)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK Strings (x86) (DSK)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        
    elif(tematica == 6):
        if(preset <= 4):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK Brass (x86) (DSK)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK Strings (x86) (DSK)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))

    elif(tematica == 7):
        if(preset <= 4):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Darksichord 3 Lite (ESL) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Toy Keyboard v3 (SampleScience) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))

    elif(tematica == 8):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Toy Keyboard v3 (SampleScience) (32 out)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    
    elif(tematica == 9):
        if(preset <= 1):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Nu Guzheng v2 (SampleScience) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DPiano-A (Dead Duck Software)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))

    elif(tematica == 10):
        if(preset <= 1):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Dynamic Guitars (DSK Music) (16 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 2):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Karoryfer Cute E (bigcat) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 4):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DVS Guitar (x86) (Martin Best)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "StratAVarious (x86) (Ian Webster)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 11):
        if(preset <= 2):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DPiano-A (Dead Duck Software)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 4):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Spicy Guitar (64 bits) (Keolab)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "TAL-NoiseMaker (TAL-Togu Audio Line)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 12):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "TAL-NoiseMaker (TAL-Togu Audio Line)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))

    if(tematica == 10 and ampli):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "FA3 Full (x86) (Fretted Synth)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 4, "ampli"+str(ampli_preset))
    else:
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "ReaEQ (Cockos)", False, -1)


    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "ReaComp (Cockos)", False, -1)
    if(tematica != 1):
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 5, "gain"+str(pista))
    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "ReaLimit (Cockos)", False, -1)
    if(tematica != 1):
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 6, "gain"+str(pista))

    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "ReaEQ (Cockos)", False, -1)
    if(tematica != 1):
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 7, "eqPista"+str(pista))

    if dream:        
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Flux Mini 2 (Caelum Audio)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 8, "dream"+str(random.randint(0, 9))) 
    elif (tematica == 12):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Flux Mini 2 (Caelum Audio)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 8, "sidechain1")

#Pads instrumento 5   
def crearPista5(pista, tematica, preset, dream, semitonos):
    i = pista-1


    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "JS: MIDI Transpose Notes", False, -1)
    RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, semitonos) 

    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "JS: MIDI Transpose Notes", False, -1)
    if(tematica == 1):
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "octaveUp") 
    
    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Humanisator (x86) (Tobybear)", False, -1)
    RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "humanisator1") 

    if(tematica == 0):
        if(preset <= 2):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Spicy Guitar (64 bits) (Keolab)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        else:
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "VSTi: DSK Strings (x86) (DSK)", False, -1)
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
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pianoSolo2")
        elif(preset <= 7):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DPiano-A (Dead Duck Software)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pianoSolo"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Upright Piano (audiolatry) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pianoSolo"+str(preset))

    elif(tematica == 2):
        if(preset <= 6):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Abstract Crystal (SampleScience) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK Strings (x86) (DSK)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))

    elif(tematica == 3):
        if(preset <= 4):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Toy Keyboard v3 (SampleScience) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 5):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Sonatina Glocken (Maizesoft) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 6):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Sonatina Xylopho (Maizesoft) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Abstract Crystal (SampleScience) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))

    elif(tematica == 4):
        if(preset <= 2):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "water (x86) (rurik leffanta)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 4):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK Strings (x86) (DSK)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 6):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Quilcom SIM-DJEMBE v1.00 (Rex Basterfield)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Toy Keyboard v3 (SampleScience) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        
    elif(tematica == 5):
        if(preset <= 0):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK ChoirZ (x86) (DSK Music)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 2):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK Strings (x86) (DSK)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 6):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Abstract Crystal (SampleScience) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 7):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "oscine tract (x86) (rurik leffanta)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "TAL-NoiseMaker (TAL-Togu Audio Line)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))

    elif(tematica == 6):
        if(preset <= 7):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK Strings (x86) (DSK)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK B3x (x86) (DSK)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        
    elif(tematica == 7):
        if(preset <= 2):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Keyzone (x86) (Bitsonic LP)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 6):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Darksichord 3 Lite (ESL) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Abstract Crystal (SampleScience) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        
    elif(tematica == 8):
        if(preset <= 4):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Toy Keyboard v3 (SampleScience) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "water (x86) (rurik leffanta)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        
    elif(tematica == 9):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "01 Pipa (DSK Music) (32 out)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    
    elif(tematica == 10):
        if(preset <= 4):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Toy Keyboard v3 (SampleScience) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 7):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK Elektrik Keyz (x86) (DSK)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Spicy Guitar (64 bits) (Keolab)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
           
    elif(tematica == 11):
        if(preset <= 4):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "TAL-NoiseMaker (TAL-Togu Audio Line)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 7):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Spicy Guitar (64 bits) (Keolab)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Toy Keyboard v3 (SampleScience) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
 
    elif(tematica == 12):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "TAL-NoiseMaker (TAL-Togu Audio Line)", False, -1)
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

    if dream:        
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Flux Mini 2 (Caelum Audio)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 7, "dream"+str(random.randint(0, 9))) 
    elif (tematica == 12):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Flux Mini 2 (Caelum Audio)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 7, "sidechain1")

#Bajo instrumento 6   
def crearPista6(pista, tematica, preset, arpegiado, preset_bajo, preset_arpegio, dream, ampli, ampli_preset, semitonos):
    i = pista-1

    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "JS: MIDI Transpose Notes", False, -1)
    RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, semitonos) 

    if(arpegiado == 1):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "BlueArp", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "arpegio"+str(preset_arpegio)) 
    elif(arpegiado == 2):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "BlueArp", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "bajo"+str(preset_bajo)) 
    elif(arpegiado == 3):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "BlueArp", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "bajo0") 
    

    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "JS: MIDI Transpose Notes", False, -1)
    if(tematica == 1 or tematica == 8):
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "octaveDown") 
    
    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Humanisator (x86) (Tobybear)", False, -1)
    RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "humanisator1") 

    if(tematica == 0):
        if(preset <= 6):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "OMB2 (x86) (Christopher Clews)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 4, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        else:
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK BassZ (x86) (DSK MusicSZZ)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 4, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    
    elif(tematica == 1):
        if(preset == 0):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Room Piano v3 (SampleScience) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 4, "pianoSolo0")
        elif(preset == 1):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Pianotone 600 v2 (SampleScience) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 4, "pianoSolo1")
        elif(preset == 2):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "EVM Grand Piano v1.1 (x86) (Etric van-mayer)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 4, "pianoSolo2")
        elif(preset <= 7):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DPiano-A (Dead Duck Software)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 4, "pianoSolo"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Upright Piano (audiolatry) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 4, "pianoSolo"+str(preset))

    elif(tematica == 2):
        if(preset <= 6):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "OMB2 (x86) (Christopher Clews)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 4, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK Strings (x86) (DSK)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 4, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))

    elif(tematica == 3):
        if(preset <= 3):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "OMB2 (x86) (Christopher Clews)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 4, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "TAL-NoiseMaker (TAL-Togu Audio Line)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 4, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))

    elif(tematica == 4):
        if(preset <= 3):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Accordion (x86) (Safwan Matni)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 4, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "OMB2 (x86) (Christopher Clews)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 4, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))

    elif(tematica == 5):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "OMB2 (x86) (Christopher Clews)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 4, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    
    elif(tematica == 6):
        if(preset <= 2):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK Brass (x86) (DSK)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 4, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 6):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK Strings (x86) (DSK)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 4, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Toy Keyboard v3 (SampleScience) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 4, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))

    elif(tematica == 7):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "OMB2 (x86) (Christopher Clews)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 4, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    
    elif(tematica == 8):
        if(preset <= 2):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Virtual Handpan (SampleScience) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 4, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Toy Keyboard v3 (SampleScience) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 4, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        
    elif(tematica == 9):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "OMB2 (x86) (Christopher Clews)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 4, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
     
    elif(tematica == 10):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "OMB2 (x86) (Christopher Clews)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 4, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    
    elif(tematica == 11):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "OMB2 (x86) (Christopher Clews)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 4, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
    
    elif(tematica == 12):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "TAL-NoiseMaker (TAL-Togu Audio Line)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 4, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))



    if(tematica == 10 and ampli):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "FA3 Full (x86) (Fretted Synth)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 5, "ampli"+str(ampli_preset))
    else:
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "ReaEQ (Cockos)", False, -1)


    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "ReaComp (Cockos)", False, -1)
    if(tematica != 1):
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 6, "gain"+str(pista))
    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "ReaLimit (Cockos)", False, -1)
    if(tematica != 1):
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 7, "gain"+str(pista))

    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "ReaEQ (Cockos)", False, -1)
    if(tematica != 1):
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 8, "eqPista"+str(pista))

    if dream:        
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Flux Mini 2 (Caelum Audio)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 8, "dream"+str(random.randint(0, 9))) 


#Batería instrumento 7   
def crearPista7(pista, tematica, preset, fill, preset_fill, dream):
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
        if(preset <= 2):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Clap Machine (99Sounds) (16 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Quilcom SIM-DUNUN v1.001 (Rex Basterfield)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
       
    elif(tematica == 2):
        if(preset <= 2):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Clap Machine (99Sounds) (16 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Quilcom SIM-DUNUN v1.001 (Rex Basterfield)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
           
    elif(tematica == 3):
        if(preset <= 3):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DrumPlayer v1 (99Sounds) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 5):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "AfroPlugin (AfroPlug) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 7):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Apari Tenpan (x86) (Apari)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK mini DRUMZ 2 (x86) (DSK Music)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
           
    elif(tematica == 4):
        if(preset <= 2):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "AfroPlugin (AfroPlug) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 4):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Cassette 606 (BPB) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 5):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Cassette 909 (BPB) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Quilcom SIM-DJEMBE v1.00 (Rex Basterfield)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
       
    elif(tematica == 5):
        if(preset <= 6):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Quilcom SIM-DJEMBE v1.00 (Rex Basterfield)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 8):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "01 Pipa (DSK Music) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Clap Machine (99Sounds) (16 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
            
    elif(tematica == 6):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Sonatina Timpani (bigcat) (32 out)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista7tematica6_0")
    
    elif(tematica == 7): 
        if(preset <= 2):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Cassette 606 (BPB) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 4):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Cassette 808 (BPB) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 7):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Cassette 909 (BPB) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Apari Tenpan (x86) (Apari)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
                
    elif(tematica == 8):
        if(preset <= 2):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DrumPlayer v1 (99Sounds) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 5):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "AfroPlugin (AfroPlug) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK mini DRUMZ 2 (x86) (DSK Music)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        
    elif(tematica == 9):
        if(preset <= 5):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DrumPlayer v1 (99Sounds) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 6):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "01 Pipa (DSK Music) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Apari Tenpan (x86) (Apari)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        
    elif(tematica == 10):
        if(preset <= 4):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DrumPlayer v1 (99Sounds) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 7):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Apari Tenpan (x86) (Apari)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Toy Keyboard v3 (SampleScience) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
             
    elif(tematica == 11):
        if(preset <= 2):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DrumPlayer v1 (99Sounds) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 3):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Toy Keyboard v3 (SampleScience) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 5):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Apari Tenpan (x86) (Apari)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 7):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK mini DRUMZ 2 (x86) (DSK Music)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 8):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "MK Drums (bigcat) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Cassette 909 (BPB) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))

    elif(tematica == 12):
        if(preset <= 1):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "AfroPlugin (AfroPlug) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 2):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Cassette 606 (BPB) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 4):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Cassette 808 (BPB) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 6):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Cassette 909 (BPB) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DrumPlayer v1 (99Sounds) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "pista"+str(pista)+"tematica"+str(tematica)+"_"+str(preset))
        

    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "ReaComp (Cockos)", False, -1)
    if(tematica != 1):
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 4, "gain"+str(pista))
    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "ReaLimit (Cockos)", False, -1)
    if(tematica != 1):
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 5, "gain"+str(pista))

    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "ReaEQ (Cockos)", False, -1)
    RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 6, "eqPista"+str(pista))

    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Cymatics Diablo Lite (Cymatics)", False, -1)
    if (tematica == 10):
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 7, "drums2")
    else:
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 7, "drums1")

    if dream:        
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Flux Mini 2 (Caelum Audio)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 8, "dream"+str(random.randint(0, 9))) 
    
#Transiciones instrumento 8 y 9   
def crearPista8(pista, tematica, preset, preset2, preset3, dream, semitonos):
    i = pista-1

    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "JS: MIDI Transpose Notes", False, -1)
    RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, semitonos) 

    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "JS: MIDI Transpose Notes", False, -1)
    RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "octaveUp") 
    
    if(tematica != 1):
        if(preset <= 0):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Room Piano v3 (SampleScience) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "riserTematica0_"+str(preset))
        elif(preset <= 5):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK Strings (x86) (DSK)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "riserTematica0_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Spicy Guitar (64 bits) (Keolab)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "riserTematica0_"+str(preset))
    elif(tematica == 1):
            if(tematica == 0):
                RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Room Piano v3 (SampleScience) (32 out)", False, -1)
                RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pianoSolo0")
            elif(preset == 1):
                RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Pianotone 600 v2 (SampleScience) (32 out)", False, -1)
                RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pianoSolo1")
            elif(preset == 2):
                RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "EVM Grand Piano v1.1 (x86) (Etric van-mayer)", False, -1)
                RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pianoSolo2")
            elif(preset <= 7):
                RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DPiano-A (Dead Duck Software)", False, -1)
                RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pianoSolo"+str(preset))
            elif(preset <= 9):
                RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Upright Piano (audiolatry) (32 out)", False, -1)
                RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pianoSolo"+str(preset))
    
    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Flux Mini 2 (Caelum Audio)", False, -1)
    RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "riser"+str(preset2))

    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "ValhallaSupermassive (Valhalla DSP, LLC)", False, -1)
    RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 4, "riser"+str(preset3))

    if dream:        
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Flux Mini 2 (Caelum Audio)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 5, "dream"+str(random.randint(0, 9))) 

#Transiciones instrumento 10 y 11   
def crearPista10(pista, tematica, preset, preset2, preset3, dream, semitonos):
    i = pista-1

    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "JS: MIDI Transpose Notes", False, -1)
    RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, semitonos) 

    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "JS: MIDI Transpose Notes", False, -1)
    RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "octaveUp") 
    
    if(tematica != 0):
        if(preset <= 0):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Room Piano v3 (SampleScience) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "downriserTematica0_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "TAL-NoiseMaker (TAL-Togu Audio Line)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "downriserTematica0_"+str(preset))
    elif(tematica == 1):
            if(preset == 0):
                RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Room Piano v3 (SampleScience) (32 out)", False, -1)
                RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pianoSolo0")
            elif(preset == 1):
                RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Pianotone 600 v2 (SampleScience) (32 out)", False, -1)
                RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pianoSolo1")
            elif(preset == 2):
                RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "EVM Grand Piano v1.1 (x86) (Etric van-mayer)", False, -1)
                RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pianoSolo2")
            elif(preset <= 7):
                RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DPiano-A (Dead Duck Software)", False, -1)
                RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pianoSolo"+str(preset))
            elif(preset <= 9):
                RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Upright Piano (audiolatry) (32 out)", False, -1)
                RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pianoSolo"+str(preset))

    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "ValhallaSupermassive (Valhalla DSP, LLC)", False, -1)
    RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "downriser"+str(preset3))

    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Flux Mini 2 (Caelum Audio)", False, -1)
    RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 4, "downriser"+str(preset2))

    if dream:        
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Flux Mini 2 (Caelum Audio) ", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 5, "dream"+str(random.randint(0, 9))) 

#Ear candy instrumento 13, 14 y 15   
def crearPista13(pista, tematica, preset, preset2, preset3, preset4, preset_arpegio, semitonos):
    i = pista-1

    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "JS: MIDI Transpose Notes", False, -1)
    RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 0, semitonos) 

    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "BlueArp", False, -1)
    RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 1, "candy"+str(preset_arpegio)) 
    
    if(tematica == 0):
        if(preset <= 2):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Ocarina (x86) (Christopher Clews) (mono)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "candyTematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 3):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "VSCO2 Marimba (bigcat) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "candyTematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 5):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Ukulele (x86) (Christopher Clews) (mono)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "candyTematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 7):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "wind (x86) (rurik leffanta)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "candyTematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DPiano-A (Dead Duck Software)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "candyTematica"+str(tematica)+"_"+str(preset))
    elif(tematica == 1):
            if(preset == 0):
                RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Room Piano v3 (SampleScience) (32 out)", False, -1)
                RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pianoSolo0")
            elif(preset == 1):
                RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Pianotone 600 v2 (SampleScience) (32 out)", False, -1)
                RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pianoSolo1")
            elif(preset == 2):
                RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "EVM Grand Piano v1.1 (x86) (Etric van-mayer)", False, -1)
                RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pianoSolo2")
            elif(preset <= 7):
                RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DPiano-A (Dead Duck Software)", False, -1)
                RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pianoSolo"+str(preset))
            elif(preset <= 9):
                RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Upright Piano (audiolatry) (32 out)", False, -1)
                RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "pianoSolo"+str(preset))

    elif(tematica == 2):
        if(preset <= 2):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Clap Machine (99Sounds) (16 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "candyTematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 4):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Sitar (x86) (Christopher Clews)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "candyTematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 6):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK World String (DSK Music) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "candyTematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Quilcom SIM-MIJWIZ v1.00 (Rex Basterfield)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "candyTematica"+str(tematica)+"_"+str(preset))

    elif(tematica == 3):
        if(preset <= 1):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Virtual Handpan (SampleScience) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "candyTematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Toy Keyboard v3 (SampleScience) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "candyTematica"+str(tematica)+"_"+str(preset))

    elif(tematica == 4):
        if(preset <= 3):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "water (x86) (rurik leffanta)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "candyTematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 4):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK Guitars Acousti (x86) (DSK Music)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "candyTematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 5):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK Guitars Nylon (x86) (DSK Music)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "candyTematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 7):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Accordion (x86) (Safwan Matni)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "candyTematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Quilcom SIM-DJEMBE v1.00 (Rex Basterfield)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "candyTematica"+str(tematica)+"_"+str(preset))

    elif(tematica == 5):
        if(preset <= 2):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Quilcom SIM-DJEMBE v1.00 (Rex Basterfield)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "candyTematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 3):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "VSCO2 Marimba (bigcat) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "candyTematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "oscine tract (x86) (rurik leffanta)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "candyTematica"+str(tematica)+"_"+str(preset))

    elif(tematica == 6):
        if(preset <= 2):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK Strings (x86) (DSK)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "candyTematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 4):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Quilcom SIM-MBIRA v1.00 (Rex Basterfield)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "candyTematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 5):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Sonatina Glocken (Maizesoft) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "candyTematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 6):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Sonatina Xylopho (Maizesoft) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "candyTematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 7):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Sonatina Oboe (bigcat) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "candyTematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 8):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Sonatina Timpani (bigcat) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "candyTematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Sonatina Trombon (bigcat) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "candyTematica"+str(tematica)+"_"+str(preset))

    elif(tematica == 7):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "TAL-NoiseMaker (TAL-Togu Audio Line)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "candyTematica"+str(tematica)+"_"+str(preset))

    elif(tematica == 8):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "water (x86) (rurik leffanta)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "candyTematica"+str(tematica)+"_"+str(preset))

    elif(tematica == 9):
        if(preset <= 7):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "01 Pipa (DSK Music) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "candyTematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 8):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Upright Piano (audiolatry) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "candyTematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Ocarina (x86) (Christopher Clews) (mono)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "candyTematica"+str(tematica)+"_"+str(preset))
        
    elif(tematica == 10):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Toy Keyboard v3 (SampleScience) (32 out)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "candyTematica"+str(tematica)+"_"+str(preset))

    elif(tematica == 11):
        if(preset <= 0):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "DSK Guitars Acousti (x86) (DSK Music)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "candyTematica"+str(tematica)+"_"+str(preset))
        elif(preset <= 9):
            RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Toy Keyboard v3 (SampleScience) (32 out)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "candyTematica"+str(tematica)+"_"+str(preset))

    elif(tematica == 12):
        RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "TAL-NoiseMaker (TAL-Togu Audio Line)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 2, "candyTematica"+str(tematica)+"_"+str(preset))

    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Flux Mini 2 (Caelum Audio)", False, -1)
    RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 3, "candy"+str(preset2))
    if tematica == 1:   
        RPR_TrackFX_SetEnabled(RPR_GetTrack(0, i), 3, False)

    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "Flux Mini 2 (Caelum Audio)", False, -1)
    RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 4, "candyGate"+str(preset3))

    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "CRMBL (unplugred)", False, -1)
    RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 5, "candy"+str(preset4))
    if tematica == 1:   
        RPR_TrackFX_SetEnabled(RPR_GetTrack(0, i), 5, False)

    
    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "ReaComp (Cockos)", False, -1)
    if(tematica != 1):
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 5, "gain13")
    RPR_TrackFX_AddByName(RPR_GetTrack(0, i), "ReaLimit (Cockos)", False, -1)
    if(tematica != 1):
        RPR_TrackFX_SetPreset(RPR_GetTrack(0, i), 6, "gain13")


def crearMasterFX(tematica, retro, lofi, lofi_preset, espacial, espacial_preset, reverb, entorno, vintage, dream, agua):
    RPR_TrackFX_AddByName(RPR_GetMasterTrack(0), "DeltaModulator (Xfer Records)", False, -1)
    if retro:
        RPR_TrackFX_SetPreset(RPR_GetMasterTrack(0), 0, "retro1") 
    else:
        RPR_TrackFX_SetEnabled(RPR_GetMasterTrack(0), 0, False)


    RPR_TrackFX_AddByName(RPR_GetMasterTrack(0), "Unison Zen Master (Unison)", False, -1)
    if(lofi):
        RPR_TrackFX_SetPreset(RPR_GetMasterTrack(0), 1, "lofi"+str(lofi_preset)) 
    else:
        RPR_TrackFX_SetEnabled(RPR_GetMasterTrack(0), 1, False)


    if(espacial):
        RPR_TrackFX_AddByName(RPR_GetMasterTrack(0), "ValhallaSupermassive (Valhalla DSP, LLC)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetMasterTrack(0), 2, "espacial"+str(espacial_preset)) 
    else:    
        RPR_TrackFX_AddByName(RPR_GetMasterTrack(0), "OrilRiver (Denis Tihanov)", False, -1)
        if(reverb and not vintage):
            RPR_TrackFX_SetPreset(RPR_GetMasterTrack(0), 2, "entorno"+str(entorno)) 
        else:
            RPR_TrackFX_SetEnabled(RPR_GetMasterTrack(0), 2, False)

    if(dream or agua): 
        RPR_TrackFX_AddByName(RPR_GetMasterTrack(0), "Cymatics Deja Vu (Cymatics)", False, -1)
        if agua:
            RPR_TrackFX_SetPreset(RPR_GetMasterTrack(0), 3, "dejaVuAqua1") 
        elif dream:
            RPR_TrackFX_SetPreset(RPR_GetMasterTrack(0), 3, "dream1") 
    else:
        RPR_TrackFX_AddByName(RPR_GetMasterTrack(0), "ReaEQ (Cockos)", False, -1)
        RPR_TrackFX_SetEnabled(RPR_GetMasterTrack(0), 3, False)

    RPR_TrackFX_AddByName(RPR_GetMasterTrack(0), "ReaComp (Cockos)", False, -1)
    if(tematica != 1 and not vintage):
        RPR_TrackFX_SetPreset(RPR_GetMasterTrack(0), 4, "comp1") 

    RPR_TrackFX_AddByName(RPR_GetMasterTrack(0), "ReaLimit (Cockos)", False, -1)
    if(tematica != 1 and not vintage):
        RPR_TrackFX_SetPreset(RPR_GetMasterTrack(0), 5, "limit1") 

    RPR_TrackFX_AddByName(RPR_GetMasterTrack(0), "ReaEQ (Cockos)", False, -1)
    if espacial:
        RPR_TrackFX_SetPreset(RPR_GetMasterTrack(0), 6, "eqMixExpacial") 
    elif vintage:
        RPR_TrackFX_SetPreset(RPR_GetMasterTrack(0), 6, "eqMixVintage") 
    elif retro:
        RPR_TrackFX_SetPreset(RPR_GetMasterTrack(0), 6, "eqMixRetro") 
    else:
        RPR_TrackFX_SetPreset(RPR_GetMasterTrack(0), 6, "eqMixTematica"+str(tematica)) 

    if not dream and not vintage:
        RPR_TrackFX_AddByName(RPR_GetMasterTrack(0), "OrilRiver (Denis Tihanov)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetMasterTrack(0), 7, "expansor") 
    elif dream:
        RPR_TrackFX_AddByName(RPR_GetMasterTrack(0), "Cymatics Memory (Cymatics)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetMasterTrack(0), 7, "dream1")
    else:
        RPR_TrackFX_AddByName(RPR_GetMasterTrack(0), "ReaEQ (Cockos)", False, -1)
        RPR_TrackFX_SetEnabled(RPR_GetMasterTrack(0), 7, False)

    if not vintage:
        if(tematica == 12):
            RPR_TrackFX_AddByName(RPR_GetMasterTrack(0), "AFTER (x86) (TWest Productions)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetMasterTrack(0), 8, "mastering2")
        else:
            RPR_TrackFX_AddByName(RPR_GetMasterTrack(0), "AFTER (x86) (TWest Productions)", False, -1)
            RPR_TrackFX_SetPreset(RPR_GetMasterTrack(0), 8, "mastering1")
    else:
        RPR_TrackFX_AddByName(RPR_GetMasterTrack(0), "OverHeat (Sampleson)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetMasterTrack(0), 8, "vintage1") 
        RPR_TrackFX_AddByName(RPR_GetMasterTrack(0), "Ratshack Reverb (Audio Damage, Inc.)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetMasterTrack(0), 9, "vintage1") 
        RPR_TrackFX_AddByName(RPR_GetMasterTrack(0), "DevilSpring (Lostin70s)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetMasterTrack(0), 10, "vintage1") 
        RPR_TrackFX_AddByName(RPR_GetMasterTrack(0), "BPB Dirty VHS (Bedroom Producers Blog)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetMasterTrack(0), 11, "vintage1") 
        RPR_TrackFX_AddByName(RPR_GetMasterTrack(0), "freeTILT (Mixland)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetMasterTrack(0), 12, "vintage1") 
        RPR_TrackFX_AddByName(RPR_GetMasterTrack(0), "AFTER (x86) (TWest Productions)", False, -1)
        RPR_TrackFX_SetPreset(RPR_GetMasterTrack(0), 13, "mastering2") 



for i in range (20):
    RPR_DeleteTrack(RPR_GetTrack(0, 0))
    
for i in range (20):
    RPR_TrackFX_Delete(RPR_GetMasterTrack(0), 0)

n_tracks = 16

for i in range(n_tracks):
    RPR_InsertTrackAtIndex(i, True)
    RPR_SetTrackColor(RPR_GetTrack(0, i), random.randint(0, 0x1000000))

RPR_SetTempoTimeSigMarker(0, -1, 0, -1, -1, 120, 0, 0, True)



tematica = 1
tematica_pistas = [0,1,2,3,4,5,6]
tematicas_aleatorias = False
mezclar_tematicas = False
mezclar_melodias = True
semitonos = -1
reverb = True
entorno = 1
lofi = True
retro = False
agua = False
espacial = False
dream = False
vintage = False

lofi_preset = random.randint(0, 9)
espacial_preset = random.randint(0, 9)

if(tematicas_aleatorias):
    tematica = random.randint(0, 12)
    tematica_pistas = [random.randint(0, 12)] * len(tematica_pistas)

if(not mezclar_tematicas):
    tematica_pistas = [tematica] * len(tematica_pistas)

if(semitonos < -5):
    semitonos = "minus6semitones" 
elif(semitonos == -5):
    semitonos = "minus5semitones" 
elif(semitonos == -4):
    semitonos = "minus4semitones" 
elif(semitonos == -3):
    semitonos = "minus3semitones" 
elif(semitonos == -2):
    semitonos = "minus2semitones" 
elif(semitonos == -1):
    semitonos = "minus1semitones" 
elif(semitonos == 1):
    semitonos = "plus1semitones" 
elif(semitonos == 2):
    semitonos = "plus2semitones" 
elif(semitonos == 3):
    semitonos = "plus3semitones" 
elif(semitonos == 4):
    semitonos = "plus4semitones" 
elif(semitonos == 5):
    semitonos = "plus5semitones" 
elif(semitonos > 5):
    semitonos = "plus6semitones"


if(tematica == 1 and not mezclar_tematicas):
    presetPiano = random.randint(0, 7)        
    
    crearPista1(1, tematica, presetPiano, dream, False, 0, semitonos)   
    crearPista1(2, tematica, presetPiano, dream, False, 0, semitonos)
    crearPista3(3, tematica, presetPiano, random.randint(1, 3), random.randint(0, 9), random.randint(0, 49), dream, False, 0, semitonos)
    crearPista3(4, tematica, presetPiano, random.randint(1, 3), random.randint(0, 9), random.randint(0, 49), dream, False, 0, semitonos)
    crearPista5(5, tematica, presetPiano, dream, semitonos)
    crearPista6(6, tematica, presetPiano, random.randint(1, 3), random.randint(0, 9), random.randint(0, 49), dream, False, 0, semitonos)
    presetBateria = random.randint(0, 9)
    crearPista7(7, tematica, presetBateria, False, 0, dream)
    crearPista8(8, tematica, presetPiano, random.randint(0, 9), random.randint(0, 9), dream, semitonos)
    crearPista8(9, tematica, presetPiano, random.randint(0, 9), random.randint(0, 9), dream, semitonos)
    crearPista10(10, tematica, presetPiano, random.randint(0, 9), random.randint(0, 9), dream, semitonos)
    crearPista10(11, tematica, presetPiano, random.randint(0, 9), random.randint(0, 9), dream, semitonos)
    crearPista7(12, tematica, presetBateria, True, random.randint(0, 9), dream)
    crearPista13(13, tematica, presetPiano, random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), semitonos)
    crearPista13(14, tematica, presetPiano, random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), semitonos)
    crearPista13(15, tematica, presetPiano, random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), semitonos)
    crearPista13(16, tematica, presetPiano, random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), semitonos)
else:
    #Melodía instrumento 1    
    crearPista1(1, tematica_pistas[0], random.randint(0, 9), dream, random.choice([True, False]), random.randint(0, 9), semitonos)

    #Melodía instrumento 2    
    crearPista1(2, tematica_pistas[1], random.randint(0, 9), dream, random.choice([True, False]), random.randint(0, 9), semitonos)

    #Acompañamiento 1
    crearPista3(3, tematica_pistas[2], random.randint(0, 9), random.randint(1, 3), random.randint(0, 9), random.randint(0, 49), dream, random.choice([True, False, False]), random.randint(0, 9), semitonos)

    #Acompañamiento 2
    crearPista3(4, tematica_pistas[3], random.randint(0, 9), random.randint(1, 3), random.randint(0, 9), random.randint(0, 49), dream, random.choice([True, False, False]), random.randint(0, 9), semitonos)

    #Pads o strings
    crearPista5(5, tematica_pistas[4], random.randint(0, 9), dream, semitonos)

    #Bajo
    crearPista6(6, tematica_pistas[5], random.randint(0, 9), random.randint(1, 3), random.randint(0, 9), random.randint(0, 49), dream, random.choice([True, False]), random.randint(0, 9), semitonos)

    presetBateria = random.randint(0, 9)
    #Batería
    crearPista7(7, tematica_pistas[6], presetBateria, False, 0, dream)

    #Transiciones 1
    crearPista8(8, tematica, random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), dream, semitonos)

    #Transiciones 2
    crearPista8(9, tematica, random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), dream, semitonos)

    #Transiciones 3
    crearPista10(10, tematica, random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), dream, semitonos)

    #Transiciones 4
    crearPista10(11, tematica, random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), dream, semitonos)

    #Drum Fills
    crearPista7(12, tematica_pistas[6], presetBateria, True, random.randint(0, 9), dream)

    #Ear Candy 1
    crearPista13(13, tematica, random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), semitonos)

    #Ear Candy 2
    crearPista13(14, tematica, random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), semitonos)

    #Ear Candy 3
    crearPista13(15, tematica, random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), semitonos)
    
    #Ear Candy 4
    crearPista13(16, tematica, random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), semitonos)


for i in range(5):
    RPR_SetMediaTrackInfo_Value(RPR_GetTrack(0, i), "D_PAN", (random.randint(-20, 20)/100))

    
for i in range(4):
    RPR_SetMediaTrackInfo_Value(RPR_GetTrack(0, i + 12), "D_PAN", (random.randint(-90, 90)/100))

crearMasterFX(tematica, retro, lofi, lofi_preset, espacial, espacial_preset, reverb, entorno, vintage, dream, agua)



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


#Generamos patrones de melodía variados
n_patrones = 3
patrones_melodia = []
patrones_melodia.append(["A", "B", "C", "D"])

for _ in range(n_patrones - 1):
    patron_melodia = []

    if mezclar_melodias:
        most_probable = random.choice(["A", "B", "C", "D"])
        for _ in range(4):
            if random.randint(1, 10) <= 6:
                patron_melodia.append(most_probable)
            else:
                patron_melodia.append(random.choice(["A", "B", "C", "D"]))
    else:
        patron_melodia = ["A", "B", "C", "D"]

    patrones_melodia.append(patron_melodia)

patrones_orden = [random.randint(0, n_patrones-1) for _ in range(8)]

RPR_SetMediaTrackInfo_Value(RPR_GetTrack(0, 0), "I_SELECTED", 1)
i = 0
for value in arreglo[0]:
    if value:
        RPR_SetEditCurPos(i * 16, True, True)
        cargarMelodia(tematica, patrones_melodia[patrones_orden[i]], pos = i * 16)
    i += 1


RPR_SetMediaTrackInfo_Value(RPR_GetTrack(0, 1), "I_SELECTED", 1)
i = 0
for value in arreglo[1]:
    if value:
        RPR_SetEditCurPos(i * 16, True, True)
        cargarMelodia(tematica, patrones_melodia[patrones_orden[i]], pos = i * 16)
    i += 1
i = 0

RPR_SetMediaTrackInfo_Value(RPR_GetTrack(0, 2), "I_SELECTED", 1)
for value in arreglo[2]:
    if value:
        RPR_SetEditCurPos(i * 16, True, True)
        cargarArmonia(tematica)
    i += 1
i = 0

RPR_SetMediaTrackInfo_Value(RPR_GetTrack(0, 3), "I_SELECTED", 1)
for value in arreglo[3]:
    if value:
        RPR_SetEditCurPos(i * 16, True, True)
        cargarArmonia(tematica)
    i += 1
i = 0

RPR_SetMediaTrackInfo_Value(RPR_GetTrack(0, 4), "I_SELECTED", 1)
for value in arreglo[4]:
    if value:
        RPR_SetEditCurPos(i * 16, True, True)
        cargarArmonia(tematica)
    i += 1

i = 0
RPR_SetMediaTrackInfo_Value(RPR_GetTrack(0, 5), "I_SELECTED", 1)
for value in arreglo[5]:
    if value:
        RPR_SetEditCurPos(i * 16, True, True)
        cargarArmonia(tematica)
    i += 1



patron_drums = [random.choice(["A", "B", "C"]) for _ in range(4)]

i = 0
RPR_SetMediaTrackInfo_Value(RPR_GetTrack(0, 6), "I_SELECTED", 1)
for value in arreglo[6]:
    if value:
        RPR_SetEditCurPos(i * 16, True, True)

        cargarDrums(tematica_pistas[6], patron_drums)

    i += 1

i = 0
RPR_SetMediaTrackInfo_Value(RPR_GetTrack(0, 7), "I_SELECTED", 1)
for value in riser:
    if value:
        RPR_SetEditCurPos(i * 16, True, True)
        cargarArmonia(tematica)
    i += 1

i = 0
RPR_SetMediaTrackInfo_Value(RPR_GetTrack(0, 8), "I_SELECTED", 1)
for value in riser:
    if value:
        RPR_SetEditCurPos(i * 16, True, True)
        cargarArmonia(tematica)
    i += 1
    
i = 0
RPR_SetMediaTrackInfo_Value(RPR_GetTrack(0, 9), "I_SELECTED", 1)
for value in downriser:
    if value:
        RPR_SetEditCurPos(i * 16, True, True)
        cargarArmonia(tematica)
    i += 1 

i = 0
RPR_SetMediaTrackInfo_Value(RPR_GetTrack(0, 10), "I_SELECTED", 1)
for value in downriser:
    if value:
        RPR_SetEditCurPos(i * 16, True, True)
        cargarArmonia(tematica)
    i += 1

fill_n = 0
RPR_SetMediaTrackInfo_Value(RPR_GetTrack(0, 11), "I_SELECTED", 1)
for i in range(8):
    if drumFill[i]:
        RPR_SetEditCurPos(i * 16 + 14, True, True)
        cargarMidi("midi/fillTemplate.mid")
        fill_n += 1
    if arreglo[6][i]:
        
        if(i < 6):
            RPR_SetEditCurPos(i * 16 + 7, True, True)
            cargarMidi("midi/fillTemplate.mid")
            RPR_SetMediaItemLength(RPR_GetTrackMediaItem(RPR_GetTrack(0, 11), fill_n), 1, False)
        else:
            RPR_SetEditCurPos(i * 16 + 6, True, True)
            cargarMidi("midi/fillTemplate.mid")
        fill_n += 1

        if(i < 4):
            RPR_SetEditCurPos(i * 16 + 14, True, True)
            cargarMidi("midi/fillTemplate.mid")
        elif(i < 6):
            RPR_SetEditCurPos(i * 16 + 13, True, True)
            cargarMidi("midi/fillTemplate.mid")
            RPR_SetMediaItemLength(RPR_GetTrackMediaItem(RPR_GetTrack(0, 11), fill_n), 3, False)
        else:
            RPR_SetEditCurPos(i * 16 + 12, True, True)
            cargarMidi("midi/fillTemplate.mid")
            RPR_SetMediaItemLength(RPR_GetTrackMediaItem(RPR_GetTrack(0, 11), fill_n), 4, False)
        
        fill_n += 1

i = 0
pista = 12
for value in candy:
    if value:
        
        RPR_SetOnlyTrackSelected(RPR_GetTrack(0, pista))
        RPR_SetEditCurPos(i * 16, True, True)
        cargarArmonia(tematica)
        
        pista += 1
        if pista == 16:
            pista = 12

    i += 1

for col in range(8):
    for fila in range(7):
        if arreglo_adelantar[fila][col]:
            if(fila < 2):
                RPR_SetOnlyTrackSelected(RPR_GetTrack(0, fila))
                RPR_SetEditCurPos(col * 16 + 12, True, True)
                cargarMelodia(tematica, patrones_melodia[patrones_orden[col]], recortar = True)

                cont = 0
                for i in range(col):
                    if arreglo[fila][i]:
                        cont += 4

                RPR_SplitMediaItem(RPR_GetTrackMediaItem(RPR_GetTrack(0, fila), cont), col * 16 + 14)
                RPR_DeleteTrackMediaItem(RPR_GetTrack(0, fila), RPR_GetTrackMediaItem(RPR_GetTrack(0, fila), cont))

            else:
                RPR_SetOnlyTrackSelected(RPR_GetTrack(0, fila))
                RPR_SetEditCurPos(col * 16 + 8, True, True)

                cargarArmonia(tematica, True)

                cont = 0
                for i in range(col):
                    if arreglo[fila][i]:
                        cont += 2

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


