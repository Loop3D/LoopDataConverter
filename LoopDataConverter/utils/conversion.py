import logging
import numpy
import re

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

def convert_dipdir_terms(cardinal: str):
    """
    Convert cardinal directions to degrees.

    Parameters:
    cardinal (str): The cardinal direction to convert.

    return (float): The cardinal direction in degrees.
    """
    logger.info(f"convert_dipdir_terms called with cardinal: {cardinal}")
    if cardinal == "NaN":
        result = numpy.nan
    elif cardinal == "N":
        result = 0.0
    elif cardinal == "NNE":
        result = 22.5
    elif cardinal == "NE":
        result = 45.0
    elif cardinal == "ENE":
        result = 67.5
    elif cardinal == "E":
        result = 90.0
    elif cardinal == "ESE":
        result = 112.5
    elif cardinal == "SE":
        result = 135.0
    elif cardinal == "SSE":
        result = 157.5
    elif cardinal == "S":
        result = 180.0
    elif cardinal == "SSW":
        result = 202.5
    elif cardinal == "SW":
        result = 225.0
    elif cardinal == "WSW":
        result = 247.5
    elif cardinal == "W":
        result = 270.0
    elif cardinal == "WNW":
        result = 292.5
    elif cardinal == "NW":
        result = 315.0
    elif cardinal == "NNW":
        result = 337.5
    else:
        result = numpy.nan
    logger.info(f"convert_dipdir_terms returning: {result}")
    return result


def convert_dip_terms(dip_term: str, type: str):
    """
    Convert dip terms to degrees.

    Parameters:
    dip_term (str): The dip term to convert.

    return (float): The dip term in degrees.
    """
    logger.info(f"convert_dip_terms called with dip_term: {dip_term}, type: {type}")
    if type == "fault":
        dip_text = split_string(dip_term)[0]
        if dip_text == "Vertical":
            result = 90.0
        elif dip_text == "Horizontal":
            result = 0.0
        elif dip_text == "Moderate":
            result = 45.0
        elif dip_text == "Steep":
            result = 75.0
        else:
            result = numpy.nan

    elif type == "fold":
        if dip_term == "Upright":
            result = 90.0
        elif dip_term == "Recumbent":
            result = 0.0
        elif dip_term == "Inclined":
            result = 45.0
        elif dip_term == "Reclined":
            result = 75.0
        else:
            result = numpy.nan
    elif type == "structure":
        if dip_term == "0-5":
            result = 2.5
        elif dip_term == "5-15":
            result = 10.0
        elif dip_term == "15-45":
            result = 45.0
        elif dip_term == ">45":
            result = 75.0
        else:
            result = numpy.nan
    logger.info(f"convert_dip_terms returning: {result}")
    return result


def convert_tightness_terms(tightness_term: str):
    """
    Convert tightness terms to degrees.

    Parameters:
    tightness_term (str): The tightness term to convert.

    return (float): The tightness term in degrees,
    which is the average of the interlimb angle range.
    """
    logger.info(f"convert_tightness_terms called with tightness_term: {tightness_term}")
    if tightness_term == "gentle":
        result = 150.0
    elif tightness_term == "open":
        result = 95.0
    elif tightness_term == "close":
        result = 50.0
    elif tightness_term == "tight":
        result = 20.0
    elif tightness_term == "isoclinal":
        result = 5.0
    else:
        result = numpy.nan
    logger.info(f"convert_tightness_terms returning: {result}")
    return result


def convert_displacement_terms(displacement_term: str):
    """
    Convert displacement terms to a float value.

    Parameters:
    displacement_term (str): The displacement term to convert.

    return (float): The displacement term as a float value.
    """
    logger.info(f"convert_displacement_terms called with displacement_term: {displacement_term}")
    if displacement_term == "small":
        result = 1.0
    elif displacement_term == "moderate":
        result = 2.0
    elif displacement_term == "large":
        result = 3.0
    else:
        result = numpy.nan
    logger.info(f"convert_displacement_terms returning: {result}")
    return result


def split_string(input_string):
    """
    Split a string into components.

    Parameters:
    input_string (str): The string to split.

    return (list): The components of the string.
    """
    logger.info(f"split_string called with input_string: {input_string}")
    result = re.split(r'\s+', input_string)
    logger.info(f"split_string returning: {result}")
    return result