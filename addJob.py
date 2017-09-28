import wx
from wx.lib.rcsizer import RowColSizer
from wx import adv
from utilities import *
import time
from datetime import date
ADD = wx.NewId()
CANCEL = wx.NewId()


class addjob(wx.Dialog):
    def __init__(self, parent, id, title, edit, idu, **kwds):

        # initialisation

        self.title = title
        self.edit = edit
        self.idu = 0
        self.parms = {
            'nosalesorder': '',
            'machine_id': '',
            'jobdate': '',
            'jenisjob': '',
            'makereadytime': '',
            'makereadyoutput': '',
            'productivetime': '',
            'productiveoutput': '',
            'finishtime': '',
            'finishoutput': '',
            'statusjob': '',
        }
        salutations = ['New', 'Rework', 'Test']
        professions = ['Finished', 'Continued', 'Others']
        if edit:
            self.parms = getjobparms(idu)
            self.idu = idu

        wx.Dialog.__init__(self, parent, id, title, **kwds)

        # create the widgets

        self.Salute = wx.RadioBox(self, -1, "Jenis Job: ",
                                  wx.DefaultPosition, wx.DefaultSize, salutations, 1, wx.RA_SPECIFY_ROWS)
        self.Salute.SetStringSelection(self.parms['jenisjob'])
        self.labnosalesorder = wx.StaticText(self, -1, "No Job/SO:")
        self.nosalesorder = wx.TextCtrl(self, -1, self.parms['nosalesorder'])
        self.labmachine_id = wx.StaticText(self, -1, "No Machine:")
        self.machine_id = wx.TextCtrl(self, -1, self.parms['machine_id'])
        self.labjobdate = wx.StaticText(self, -1, "Tanggal job:")
        self.jobdate = wx.adv.DatePickerCtrl(self, -1)

        self.labmakereadytime = wx.StaticText(self, -1, "makereadytime:")
        self.makereadytime = wx.adv.TimePickerCtrl(self, -1)
        self.labmakereadyoutput = wx.StaticText(self, -1, "makereadyoutput:")
        self.makereadyoutput = wx.TextCtrl(self, -1, '0')

        self.labproductivetime = wx.StaticText(self, -1, "productivetime:")
        self.productivetime = wx.adv.TimePickerCtrl(self, -1)
        self.labproductiveoutput = wx.StaticText(self, -1, "productiveoutput:")
        self.productiveoutput = wx.TextCtrl(self, -1, self.parms['productiveoutput'])

        self.labfinishtime = wx.StaticText(self, -1, "finishtime:")
        self.finishtime = wx.adv.TimePickerCtrl(self, -1)

        self.labstatusjob = wx.StaticText(self, -1, "Status Job:")
        self.statusjob = wx.ComboBox(self, -1, choices=professions,
                                      style=wx.CB_DROPDOWN)
        self.statusjob.SetValue(self.parms['statusjob'])
        self.butsave = wx.Button(self, ADD, "Save")
        self.butcancel = wx.Button(self, CANCEL, "Cancel")
        self.nosalesorder.SetSize((380, 26))
        self.nosalesorder.SetMaxLength(60)
        self.jobdate.SetSize((320, 26))
        #self.jobdate.SetMaxLength(40)

        self.__do_layout()

    def __do_layout(self):

        self.SetPosition([300, 250])
        boxl = RowColSizer()
        boxl.Add(self.Salute, row=1, col=1, colspan=2)
        boxl.Add(self.labnosalesorder, row=2, col=1)
        boxl.Add(self.nosalesorder, row=2, col=2)
        boxl.Add(self.labmachine_id, row=2, col=3)
        boxl.Add(self.machine_id, row=2, col=4)
        boxl.Add(self.labjobdate, row=3, col=1)
        boxl.Add(self.jobdate, row=3, col=2)
        self.machine_id.Disable()
        boxl.Add(self.labstatusjob, row=4, col=1)
        boxl.Add(self.statusjob, row=4, col=2)

        box2 = RowColSizer()
        box2.Add(self.labmakereadyoutput, row=1, col=1)
        box2.Add(self.makereadyoutput, row=1, col=2)
        box2.Add(self.labproductiveoutput, row=2, col=1)
        box2.Add(self.productiveoutput, row=2, col=2)
        box2.Add(self.labfinishtime, row=3, col=1)
        box2.Add(self.finishtime, row=3, col=2)

        boxl.Add(box2, row=5, col=1)

        boxb = wx.BoxSizer(wx.HORIZONTAL)
        boxb.Add(self.butsave, 0,
                 wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        boxb.Add(50, 10, 0)
        boxb.Add(self.butcancel, 0,
                 wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 0)
        boxl.Add(boxb, row=6, col=2)

        for x in range(1, 6):
            boxl.AddSpacer(75, 30, pos=(x, 1))
            boxl.AddSpacer(380, 1, pos=(x, 2))

        boxl.AddSpacer(75, 30, pos=(6, 1))
        self.SetAutoLayout(1)
        self.SetSizer(boxl)
        boxl.Fit(self)
        boxl.SetSizeHints(self)

        #self.SetSizer(box2)
        #box2.Fit(self)
        #box2.SetSizeHints(self)

        self.Layout()
        wx.EVT_BUTTON(self, ADD, self.add)
        wx.EVT_BUTTON(self, CANCEL, self.cancel)

    def cancel(self, event):
        self.EndModal(0)

    def add(self, event):
        ok = True
        msg = ''
        parms = self.parms
        parms['statusjob'] = self.statusjob.GetValue().strip()
        # strip to get rid of leading and trailing spaces
        parms['nosalesorder'] = self.nosalesorder.GetValue()
        parms['statusjob'] = self.statusjob.GetValue()
        parms['jenisjob'] = self.Salute.GetStringSelection()
        parms['jobdate'] = self.jobdate.GetValue()
        # check that all fields are filled
        for k, v in parms.items():
            if v == '':
                msg += "Isilah data '%s'." % (k.capitalize())
                ok = False
        # if edit mode
        if self.edit:
            # check for duplicates
            msg, ok = duplicedit(parms['nosalesorder'],
                                 parms['jobdate'], self.idu, msg, ok)
            if ok:
                updatejob(parms, self.idu)  # external program
                self.EndModal(1)
            else:
                # display error message
                error = wx.MessageDialog(self, msg, 'Kesalahan', wx.OK)
                error.ShowModal()
                error.Destroy()
                # if add mode
        else:
            msg, ok = duplic(parms['nosalesorder'], parms['jobdate'], msg, ok)
            if ok:
                enterjob(parms)  # external program
                self.EndModal(1)
            else:
                error = wx.MessageDialog(self, msg, 'Kesalahan', wx.OK)
                error.ShowModal()
                error.Destroy()