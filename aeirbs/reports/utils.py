from enum import Enum

class IncidentLevels(Enum):
    # Fire Alert Levels
    FR_FIRST = 'FR_FIRST'
    FR_SECOND = 'FR_SECOND'
    FR_THIRD = 'FR_THIRD'
    FR_FOURTH = 'FR_FOURTH'
    FR_FIFTH = 'FR_FIFTH'
    FR_TFALPHA = 'FR_TFALPHA'
    FR_TFBRAVO = 'FR_TFBRAVO'
    FR_TFCHARLIE = 'FR_TFCHARLIE'
    FR_TFDELTA = 'FR_TFDELTA'
    FR_TFECHO = 'FR_TFECHO'
    FR_GENERAL = 'FR_GENERAL'
    # Flood Alert Levels
    FL_GUTTER = 'FL_FIRST'
    FL_HALFKNEE = 'FL_HALFKNEE'
    FL_HALFTIRE = 'FL_HALFTIRE'
    FL_KNEE = 'FL_KNEE'
    FL_TIRES = 'FL_TIRES'
    FL_WAIST = 'FL_WAIST'
    FL_CHEST = 'FL_CHEST'
    # Earthqauke Alert Levels
    EQ_I = 'EQ_I'
    EQ_II = 'EQ_II'
    EQ_III = 'EQ_III'
    EQ_IV = 'EQ_IV'
    EQ_V = 'EQ_V'
    EQ_VI = 'EQ_VI'
    EQ_VII = 'EQ_VII'
    EQ_VIII = 'EQ_VIII'
    EQ_IX = 'EQ_IX'
    EQ_X = 'EQ_X'

    @classmethod
    def choices(cls):
        return[(key.value, key.name) for key in cls]

class IncidentCombinations(Enum):
    FR = 'FIRE'
    FL = 'FLOOD'
    EQ = 'EARTHQUAKE'
    FR_FL = 'FIRE_FLOOD'
    FR_EQ = 'FIRE_EARTHQUAKE'
    FL_EQ = 'FLOOD_EARTHQUAKE'
    FR_FL_EQ = 'FIRE_FLOOD_EARTHQUAKE'

    @classmethod
    def choices(cls):
        return[(key.value, key.name) for key in cls]

