import sys
from resources.datatables import TerminalType

def setup(core, object):
	object.setAttachment("terminalType", TerminalType.ENTERTAINER)
	core.mapService.addLocation(object.getPlanet(), '@map_loc_cat_n:terminal_mission_entertainer', object.getPosition().x, object.getPosition().z, 41, 75, 0)
	return