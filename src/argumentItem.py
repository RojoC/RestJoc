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


@GtkTemplate(ui='/org/gnome/Restjoc/ui/argumentItem.ui')
class ArgumentItem(Gtk.ListBoxRow):
    __gtype_name__ = 'argument'

    checkbox = GtkTemplate.Child()

    key = GtkTemplate.Child()
    value = GtkTemplate.Child()

    fileChooser = GtkTemplate.Child()
    kind = GtkTemplate.Child()

    delete =  GtkTemplate.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_template()

    def on_kind_changed(self,*args):
        if self.kind.get_active_id() == "text_argument":
            self.value.show()
            self.fileChooser.hide()
        elif self.kind.get_active_id() == "file_argument":
            self.value.hide()
            self.fileChooser.show()
        else: # header
            self.value.show()
            self.fileChooser.hide()


    def on_delete_clicked(self,*args):
        self.get_parent().remove(self)

    def on_argumentFile_file_set(self,*args):
        pass

    def on_argument_event(self,*args):
        pass

    def toDict(self):
        return {
            "isActive":self.checkbox.get_active(),
            "key":self.key.get_text(),
            "kind":self.kind.get_active_id(),
            "value":self.fileChooser.get_filename() if self.fileChooser.get_filename() != None else self.value.get_text()
        }

    def fromDict(self,data):
        self.value.hide()
        self.checkbox.set_active(data['isActive'])

        self.key.set_text(data['key'])
        self.kind.set_active_id(data['kind'])

        if data['kind'] == "file_argument":

            if data['value'] != "":
                self.fileChooser.set_filename(data['value'])

            self.value.hide()
        else:
            self.fileChooser.unselect_all()
            self.value.show()

            self.value.set_text(data['value'])
