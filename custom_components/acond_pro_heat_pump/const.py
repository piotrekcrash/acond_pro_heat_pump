"""Constants for acond_pro_heat_pump."""

from logging import Logger, getLogger

LOGGER: Logger = getLogger(__package__)

DOMAIN = "acond_pro_heat_pump"
ATTRIBUTION = "Data provided by http://jsonplaceholder.typicode.com/"

URL_LOGIN = "/SYSWWW/LOGIN.XML"
URL_HOME = "/PAGE115.XML"
URL_TIMETABLES_1 = "/PAGE115.XML"
