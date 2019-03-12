# window.py
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

from gi.repository import Gtk, GLib
from .gi_composites import GtkTemplate

import threading
import random
import json

import base64

from .request import Request

from .requestItem import RequestItem
from .argumentItem import ArgumentItem

@GtkTemplate(ui='/org/gnome/Restjoc/ui/window.ui')
class RestjocWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'RestjocWindow'

    popover = GtkTemplate.Child()
    baseURLEntery = GtkTemplate.Child()
    sendRequest = GtkTemplate.Child()
    requestList = GtkTemplate.Child()
    addRequest = GtkTemplate.Child()
    removeRequest = GtkTemplate.Child()
    duplicateRequest = GtkTemplate.Child()
    requestOptions = GtkTemplate.Child()
    requestMethod = GtkTemplate.Child()
    requestWay = GtkTemplate.Child()
    argumentListView = GtkTemplate.Child()
    responseText = GtkTemplate.Child()
    emptyRequest = RequestItem()
    argumentList = Gtk.ListBox()
    responseTextBuffer = GtkTemplate.Child()
    spinner = GtkTemplate.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.init_template()

        self.fileFilter = Gtk.FileFilter()
        self.fileFilter.set_name("RestJoc Files")
        self.fileFilter.add_pattern("*.[rR][eE][sS][tT][jJ][oO][cC]")

        self.filePath = ""

        self.argumentListView.add(self.argumentList)
        self.setOptionsFromRequest(self.emptyRequest)

        self.sendRequest.set_sensitive(False)

    def _setResponse(self,text):
        self.responseTextBuffer.set_text(text)
        self.spinner.stop()
        self.sendRequest.set_sensitive(True)

    def _sendRequest(self):
        request = self.requestList.get_selected_row()

        data = dict()
        headers = dict()

        for i in request.argumentList:
            if i.checkbox.get_active():
                if i.kind.get_active_id() == "text_argument":
                    data[i.key.get_text()] = i.value.get_text()
                elif i.kind.get_active_id() == "file_argument":
                    data[i.key.get_text()] = "data:application/octet-stream;base64,"+str(base64.b64encode(
                        open(i.fileChooser.get_filename(), "rb").read()
                        ),encoding="ascii")
                else:
                    headers[i.key.get_text()] = i.value.get_text()

        request.response = Request(self.baseURLEntery.get_text() + request.way.get_text(),
                                    method = request.method.get_text(),
                                    headers=headers,
                                    data=data).Text()

        GLib.idle_add(self._setResponse,request.response)

    def on_sendRequest_clicked(self,*args):
        self.spinner.start()
        self.sendRequest.set_sensitive(False)
        thread = threading.Thread(target=self._sendRequest)
        thread.daemon = True
        thread.start()



    def on_addRequest_clicked(self,*args):
        new = RequestItem()
        self.requestList.add(new)
        self.requestList.select_row(new)
        self.requestList.show_all()

    def on_removeRequest_clicked(self,*args):
        selected_row = self.requestList.get_selected_row()
        selected_row_index = selected_row.get_index()

        self.requestList.remove(selected_row)

        if len(list(self.requestList)) == 0:
            self.removeRequest.set_sensitive(False)
            self.requestOptions.set_sensitive(False)
            self.duplicateRequest.set_sensitive(False)

            self.setOptionsFromRequest(self.emptyRequest)
        else:
            if selected_row_index > 0:
                self.requestList.select_row(self.requestList.get_row_at_index(selected_row_index-1))
            else:
                self.requestList.select_row(self.requestList.get_row_at_index(0))



    def on_requestList_row_selected(self,listbox,row):
        self.sendRequest.set_sensitive(True)
        self.setOptionsFromRequest(row)

    def setOptionsFromRequest(self,request):
        self.requestWay.set_text(request.way.get_text())
        self.requestMethod.set_active_id(request.method.get_text())

        self._setResponse(request.response)

        self.argumentListView.remove(self.argumentList)
        self.argumentList = request.argumentList
        self.argumentListView.add(self.argumentList)
        self.argumentListView.show_all()
        #Set Requests


    def on_requestWay_changed(self,*args):
        self.requestList.get_selected_row().way.set_text(self.requestWay.get_text())

    def on_requestList_add(self,*args):
        self.requestOptions.set_sensitive(True)
        self.removeRequest.set_sensitive(True)
        self.duplicateRequest.set_sensitive(True)

    def on_duplicateRequest_clicked(self,*args):
        new = RequestItem()
        new.fromDict(self.requestList.get_selected_row().toDict())

        self.requestList.add(new)
        self.requestList.select_row(new)

    def on_requestMethod_changed(self,*args):
        self.requestList.get_selected_row().method.set_text(self.requestMethod.get_active_text())

    def on_addArgument_clicked(self,*args):
        self.argumentList.add(ArgumentItem())
        self.argumentList.show_all()

    def on_new_clicked(self,*args):
        RestjocWindow(application=self.get_application()).show()

    def _save_project(self,path):
        with open(path, 'w') as fp:
            try:

                data = {"base_url": self.baseURLEntery.get_text(),
                        "auto_save": False,
                        "requests": [i.toDict() for i in self.requestList],
                        "headers": [],
                        "cokkies": [],
                        }

                json.dump(data, fp)
                self.filePath = path
            except Exception as e:
                print(e)


    def _open_project(self,fp):
        data = json.load(open(fp,'r'))

        self.baseURLEntery.set_text(data['base_url'])

        for i in self.requestList:
            self.requestList.remove(i)

        for i in data['requests']:
            new = RequestItem()
            new.fromDict(i)
            self.requestList.add(new)
            self.requestList.select_row(new)
            self.requestList.show_all()



    def on_save_clicked(self,*args):
        if self.filePath == "":
            dialog = Gtk.FileChooserDialog("Save", None,
                                           Gtk.FileChooserAction.SAVE,
                                           (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                            Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

            dialog.add_filter(self.fileFilter)

            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                path = dialog.get_filename()
                self._save_project(path)
                dialog.destroy()
            elif response == Gtk.ResponseType.CANCEL:
                dialog.destroy()
        else:
            self._save_project(self.filePath)

    def on_save_as_clicked(self,*args):
        dialog = Gtk.FileChooserDialog("Save", None,
                                           Gtk.FileChooserAction.SAVE,
                                           (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                            Gtk.STOCK_SAVE, Gtk.ResponseType.OK))

        dialog.add_filter(self.fileFilter)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            path = dialog.get_filename()
            self._save_project(path)
            dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()

    def on_open_clicked(self,*args):
        dialog = Gtk.FileChooserDialog("Save", None,
                                           Gtk.FileChooserAction.OPEN,
                                           (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                            Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        dialog.add_filter(self.fileFilter)

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
                path = dialog.get_filename()
                self._open_project(path)
                self.filePath = path
                dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()

        
