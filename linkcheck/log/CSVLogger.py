# -*- coding: iso-8859-1 -*-
# Copyright (C) 2000-2003  Bastian Kleineidam
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

import time, csv
from linkcheck.log import strtime
from StandardLogger import StandardLogger
from Logger import Logger
from linkcheck import Config, i18n

class CSVLogger (StandardLogger):
    """ CSV output. CSV consists of one line per entry. Entries are
    separated by a semicolon.
    """
    def __init__ (self, **args):
        StandardLogger.__init__(self, **args)
        self.separator = args['separator']
        self.lineterminator = "\n"

    def init (self):
        Logger.init(self)
        if self.fd is None: return
        self.starttime = time.time()
        if self.has_field("intro"):
            self.fd.write("# "+(i18n._("created by %s at %s%s") % (Config.AppName, strtime(self.starttime), self.lineterminator)))
            self.fd.write("# "+(i18n._("Get the newest version at %s%s") % (Config.Url, self.lineterminator)))
            self.fd.write("# "+(i18n._("Write comments and bugs to %s%s%s") % \
	                    (Config.Email, self.lineterminator, self.lineterminator)))
            self.fd.write(
                      i18n._("# Format of the entries:")+self.lineterminator+\
                      "# urlname;"+self.lineterminator+\
                      "# recursionlevel;"+self.lineterminator+\
                      "# parentname;"+self.lineterminator+\
                      "# baseref;"+self.lineterminator+\
                      "# errorstring;"+self.lineterminator+\
                      "# validstring;"+self.lineterminator+\
                      "# warningstring;"+self.lineterminator+\
                      "# infostring;"+self.lineterminator+\
                      "# valid;"+self.lineterminator+\
                      "# url;"+self.lineterminator+\
                      "# line;"+self.lineterminator+\
                      "# column;"+self.lineterminator+\
                      "# name;"+self.lineterminator+\
                      "# dltime;"+self.lineterminator+\
                      "# dlsize;"+self.lineterminator+\
                      "# checktime;"+self.lineterminator+\
                      "# cached;"+self.lineterminator)
            self.fd.flush()
        self.writer = csv.writer(self.fd, dialect='excel', delimitor=self.separator, lineterminator=self.lineterminator)


    def newUrl (self, urlData):
        if self.fd is None: return
        row = [urlData.urlName, urlData.recursionLevel,
               urlData.parentName, urlData.baseRef,
               urlData.errorString, urlData.validString,
               urlData.warningString, urlData.infoString,
               urlData.valid, urlData.url,
               urlData.line, urlData.column,
               urlData.name, urlData.dltime,
               urlData.dlsize, urlData.checktime,
               urlData.cached]
        self.writer.writerow(row)
        self.fd.flush()


    def endOfOutput (self, linknumber=-1):
        if self.fd is None: return
        self.stoptime = time.time()
        if self.has_field("outro"):
            duration = self.stoptime - self.starttime
            name = i18n._("seconds")
            self.fd.write("# "+i18n._("Stopped checking at %s") % strtime(self.stoptime))
            if duration > 60:
                duration = duration / 60
                name = i18n._("minutes")
            if duration > 60:
                duration = duration / 60
                name = i18n._("hours")
            self.fd.write(" (%.3f %s)%s" % (duration, name, self.lineterminator))
            self.fd.flush()
        self.fd.close()
        self.fd = None

