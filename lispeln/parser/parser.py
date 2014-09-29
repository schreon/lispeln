from lispeln.scheme.constants import Integer, Float, Boolean
from lispeln.scheme.expressions import Symbol
import re

patterns = {
    re.compile(r"^[0-9]+$") : Integer,
    re.compile(r"^[0-9]+.[0-9]+$") : Float,
    re.compile(r"^(?!\#%)(\#)?\.?[^\s\(\)\[\]\{\}\"\,\'\;\#\|\\]+$") : Symbol,
    re.compile(r"false|true") : Boolean
}