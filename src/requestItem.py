# request.py
#
# Copyright 2018 Mehmet Özbağcı
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import Gtk
from .gi_composites import GtkTemplate

from .argumentItem import ArgumentItem

@GtkTemplate(ui='/org/gnome/Restjoc/ui/requestItem.ui')
class RequestItem(Gtk.ListBoxRow):
    __gtype_name__ = 'request'

    way = GtkTemplate.Child()
    method = GtkTemplate.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_template()

        self.response = ""
        self.argumentList = Gtk.ListBox()

    def toDict(self):
        return {"way":self.way.get_text(),
        "method":self.method.get_text(),
        "arguments":[i.toDict() for i in self.argumentList],
        "response":self.response}

    def fromDict(self,data):
        self.way.set_text(data["way"])
        self.method.set_text(data["method"])


        for i in self.argumentList:
            self.argumentList.remove(i)

        for i in data['arguments']:
            new = ArgumentItem()
            new.fromDict(i)
            self.argumentList.add(new)
            self.argumentList.show_all()

        self.response = data["response"]
