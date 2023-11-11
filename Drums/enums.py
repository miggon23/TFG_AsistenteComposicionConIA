from enum import Enum

class Style(Enum):
    BASIC = 1
    KICK = 2
    CLAP = 3
    SHAKER = 4
    JAZZ = 5
    DISCO = 6
    METAL = 7
    LATIN = 8
    ROCK = 9

class Note(Enum):
    BassDrum = 36
    SideStick = 37
    AcousticSnare = 38
    AcousticClap = 39
    ElectricSnare = 40
    LowFloorTom = 41
    ClosedHiHat = 42
    HighFloorTom = 43
    PedalHiHat = 44
    LowTom = 45
    OpenHiHat = 46
    LowMidTom = 47
    HiMidTom = 48
    CrashCymbal = 49
    HighTom = 50
    RideCymbal = 51