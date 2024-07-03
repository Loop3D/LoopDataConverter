import numpy 
import beartype


@beartype.beartype
def convert_dipdir_cardinals(cardinal: str):
    """
    Convert cardinal directions to degrees.
    """
    if cardinal == 'N':
        return 0
    elif cardinal == 'NNE':
        return 22.5
    elif cardinal == 'NE':
        return 45
    elif cardinal == 'ENE':
        return 67.5
    elif cardinal == 'E':
        return 90
    elif cardinal == 'ESE':
        return 112.5
    elif cardinal == 'SE':
        return 135
    elif cardinal == 'SSE':
        return 157.5
    elif cardinal == 'S':
        return 180
    elif cardinal == 'SSW':
        return 202.5
    elif cardinal == 'SW':
        return 225
    elif cardinal == 'WSW':
        return 247.5
    elif cardinal == 'W':
        return 270
    elif cardinal == 'WNW':
        return 292.5
    elif cardinal == 'NW':
        return 315
    elif cardinal == 'NNW':
        return 337.5
    else:
        return numpy.nan

def convert_dip_terms(dip_term: str):
    """
    Convert dip terms to degrees.
    """
    if dip_term == 'Vertical':
        return 90
    elif dip_term == 'Horizontal':
        return 0
    elif dip_term == 'Moderate':
        return 45
    elif dip_term == 'Steep':
        return 75
    else:
        return numpy.nan

def convert_tightness_terms(tightness_term: str):
    """
    Convert tightness terms to degrees.
    """
    if tightness_term == 'gentle':
        return 150
    elif tightness_term == 'open':
        return 95
    elif tightness_term == 'close':
        return 50
    elif tightness_term == 'tight':
        return 15
    elif tightness_term == 'isoclinal':
        return 0
    else:
        return numpy.nan