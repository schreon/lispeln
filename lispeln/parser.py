from lispeln.constants import Integer, Float, Boolean
from lispeln.expressions import Symbol
import re

patterns = {
    re.compile(r"^[0-9]+$") : Integer,
    re.compile(r"^[0-9]+.[0-9]+$") : Float,
    re.compile(r"^(?!\#%)(\#)?\.?[^\s\(\)\[\]\{\}\"\,\'\;\#\|\\]+$") : Symbol,
    re.compile(r"false|true") : Boolean
}