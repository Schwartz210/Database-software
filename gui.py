__author__ = 'aschwartz - Schwartz210@gmail.com'
from db_interface import add_record, pull_data, update_record
from tkinter import *
from functools import partial
from collections import OrderedDict



def null_entry_handler(entry):
    if len(entry.get()) == 0:
        return ''
    else:
        return entry.get()

class HomeScreen(object):
    def __init__(self):
        self.master = Tk()
        self.build_canvas()
        self.menubar()
        mainloop()

    def build_canvas(self):
        self.master.title('Avi Enterprise Pro')
        self.width = 900
        self.height = 600
        self.canvas = Canvas(self.master, width=self.width, height=self.height)
        self.canvas.grid()

    def menubar(self):
        self.menu = Menu(self.master)
        #File menu
        filemenu = Menu(self.menu, tearoff=0)
        filemenu.add_command(label="Open", command=self.hello)
        filemenu.add_command(label="Save", command=self.hello)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.master.destroy)
        self.menu.add_cascade(label="File", menu=filemenu)
        #Record menu
        recordmenu = Menu(self.menu, tearoff=0)
        recordmenu.add_command(label="New record", command=self.new_record)
        recordmenu.add_command(label="Delete record", command=self.hello)
        self.menu.add_cascade(label="Records", menu=recordmenu)
        #Reporting menu
        reportingmenu = Menu(self.menu, tearoff=0)
        reportingmenu.add_command(label="Show all records", command=self.reporting)
        self.menu.add_cascade(label="Reporting", menu=reportingmenu)
        self.master.config(menu=self.menu)

    def hello(self):
        print('hello')

    def new_record(self):
        record_window = CreateRecordWindow()

    def reporting(self):
        reporting_window = Report('all')



class CreateRecordWindow(object):
    def __init__(self):
        self.master = Tk()
        self.entries = []
        self.build_canvas()
        mainloop()

    def build_canvas(self):
        fields = ['First name', 'Last name','Address 1', 'Address 2','City','State','Zip','Phone']
        self.master.title('Create new record')
        self.width = 150
        self.height = 150
        self.canvas = Canvas(self.master, width=self.width, height=self.height)
        entry_width = 60
        row_num = 1
        for field in fields:
            Label(self.master, text=field).grid(row=row_num, sticky=W)
            entry = Entry(self.master, width=entry_width)
            entry.grid(row=row_num, column=2)
            self.entries.append(entry)
            row_num += 1
        Button(self.master, text='Create Record', command=self.entry_handler).grid(row=9, column=1, sticky=S)
        Button(self.master, text='Cancel', command=self.master.destroy).grid(row=9, column=2, sticky=S)
        self.canvas.grid()

    def entry_handler(self):
        record = [null_entry_handler(entry) for entry in self.entries if entry]
        add_record(record)
        self.master.destroy()


class Report(object):
    def __init__(self, fields):
        if fields == 'all':
            self.fields = ['ID','First_name','Last_name','Address1','Address2','City','State','Zip','Phone']
            self.display_fields = list(self.fields)
        else:
            if 'ID' not in fields:
                self.display_fields = list(fields)
                fields.insert(0,'ID')
                self.fields = fields
            else:
                self.fields = list(fields)
                self.display_fields = list(self.fields)
        self.sorted_by_field = 0
        self.rightmost_column = len(self.display_fields) - 1
        self.width = 600
        self.height = 800
        self.master = Toplevel()
        self.master.title('Reporting')
        self.canvas1 = Canvas(self.master, width=self.width, height=self.height)
        self.canvas2 = Canvas(self.master, width=self.width, height=self.height)
        self.refresh_report()
        mainloop()

    def get_sql_data(self):
        field_query = ''
        for field in self.fields:
            field_query += field + ','
        sql_request = 'SELECT %s FROM test_table4' % (field_query[:-1])
        self.data = pull_data(sql_request)

    def canvas_master_processs(self):
        self.canvas1.destroy()
        self.canvas2.destroy()
        self.canvas1 = Canvas(self.master, width=self.width, height=self.height)
        self.canvas2 = Canvas(self.master, width=self.width, height=self.height)
        self.determine_button_width()
        self.layout_headers()
        self.layout_buttons()
        self.canvas1.grid()
        self.canvas2.grid()

    def layout_headers(self):
        #Button(self.canvas1,width=60,bg='blue').grid(column=0, row=0)
        Button(self.canvas1,
               text='Customize Report',
               width=15,
               height=1,
               borderwidth=1,
               font=('calibri',12,'bold',),
               command=self.customize_report,
               bg='#dcdcdc').grid(column=0, row=0)

        Button(self.canvas1,
               text='Refresh Report',
               width=15,
               height=1,
               borderwidth=1,
               font=('calibri',12,'bold',),
               command=self.refresh_report,
               bg='#dcdcdc').grid(column=1, row=0)
        iterator_column = 0
        for field in self.display_fields:
            text = field.replace('_',' ')
            Button(self.canvas2,
                   text=text,
                   width=self.button_width[iterator_column],
                   height=1,
                   borderwidth=1,
                   font=('arial',12,'bold'),
                   anchor=W,
                   command=partial(self.custom_sort,iterator_column)).grid(row=1, column=iterator_column)
            iterator_column += 1

    def layout_buttons(self):
        iterator_row = 2
        for record in self.data:
            iterator_field = 0
            if 'ID' in self.display_fields:
                for field in record:
                    Button(self.canvas2,text=field,width=self.button_width[iterator_field],height=1,borderwidth=0,command=partial(self.open_record_window,record[0]),anchor=W).grid(row=iterator_row,column=iterator_field,sticky=S)
                    iterator_field += 1
            else:
                for field in record[1:]:
                    Button(self.canvas2,text=field,width=self.button_width[iterator_field],height=1,borderwidth=0,command=partial(self.open_record_window,record[0]),anchor=W).grid(row=iterator_row,column=iterator_field,sticky=S)
                    iterator_field += 1
            iterator_row += 1

    def refresh_report(self):
        self.get_sql_data()
        self.canvas_master_processs()

    def customize_report(self):
        CustomizeReportWindow()

    def open_record_window(self, ID):
        RecordWindow(ID)

    def custom_sort(self, field):
        if 'ID' not in self.display_fields:
            field += 1
        self.data.sort(key=lambda x: x[field])
        if field == self.sorted_by_field:
            self.data.reverse()
            self.sorted_by_field = ''
        else:
            self.sorted_by_field = field
        self.canvas_master_processs()

    def determine_button_width(self):
        self.button_width = []
        for field in self.display_fields:
            ind = self.fields.index(field)
            max_value = self.list_of_list_column_len(self.data, ind)
            self.button_width.append(max_value)

    def list_of_list_column_len(self, list_of_lists, column):
        max_value = 0
        for lst in list_of_lists:
            if len(str(lst[column])) > max_value:
                max_value = len(str(lst[column]))
        return max_value

class RecordWindow(object):
    def __init__(self, ID):
        self.ID = ID
        self.width = 200
        self.height = 200
        self.entries = []
        self.master = Toplevel()
        self.get_data()
        self.build_canvas()
        self.master.mainloop()

    def get_data(self):
        sql_request = 'SELECT * FROM test_table4 WHERE ID="%s"' % (self.ID)
        try:
            self.data = pull_data(sql_request)[0]
        except:
            self.data = pull_data(sql_request)

    def build_canvas(self):
        self.canvas = Canvas(self.master, width=self.width, height=self.height)
        fields = ['ID', 'First name', 'Last name','Address 1', 'Address 2','City','State','Zip','Phone']
        iterator = 0
        for field in fields:
            Label(self.canvas, text=field).grid(row=iterator, column=0, sticky=W)
            Label(self.canvas, text=self.data[iterator]).grid(row=iterator, column=1, sticky=W)
            iterator += 1
        Button(self.canvas, text='Edit record', width=10, command=self.edit_record).grid(row=iterator, column=0)
        Button(self.canvas, text='Exit', width=10, command=self.master.destroy).grid(row=iterator, column=1)
        self.canvas.grid()

    def edit_record(self):
        self.canvas.destroy()
        self.canvas = Canvas(self.master, width=self.width, height=self.height)
        fields = ['First name', 'Last name','Address 1', 'Address 2','City','State','Zip','Phone']
        iterator = 0
        for field in fields:
            Label(self.canvas, text=field).grid(row=iterator, column=0, sticky=W)
            iterator += 1
        iterator = 0
        Label(self.canvas, text=self.data[0]).grid(row=iterator, column=1, sticky=W)

        for field in self.data[1:]:
            a = StringVar()
            a.set(field)
            entry = Entry(self.canvas, width=15,textvariable=a)
            entry.grid(row=iterator, column=1)
            self.entries.append(entry)
            iterator += 1
        Button(self.canvas, text='Save', width=10, command=self.save_record).grid(row=iterator, column=0)
        Button(self.canvas, text='Cancel', width=10, command=self.master.destroy).grid(row=iterator, column=1)
        self.canvas.grid()

    def save_record(self):
        record = [null_entry_handler(entry) for entry in self.entries if entry]
        record.append(self.ID)
        update_record(record)
        self.master.destroy()
        self.__init__(self.ID)


class CustomizeReportWindow(object):
    def __init__(self):
        self.master = Toplevel()
        self.check_dict = {}
        self.create_canvas()
        self.master.mainloop()

    def create_canvas(self):
        self.width = 100
        self.height = 100
        self.canvas = Canvas(self.master, width=self.width, height=self.height)
        fields = ['ID', 'First name', 'Last name','Address1', 'Address2','City','State','Zip','Phone']
        iterator = 1
        self.results = []
        for field in fields:
            self.check_dict[field]  = IntVar()
            Checkbutton(self.master, text=field, variable=self.check_dict[field],onvalue = 1, offvalue = 0).grid(row=iterator, sticky=W)
            iterator += 1

        Button(self.master, text='Run Report', command=self.call_report, width=15).grid(row=iterator)
        self.canvas.grid()

    def clean_dict(self):
        for key in self.check_dict.keys():
            self.check_dict[key] = self.check_dict[key].get()

    def call_report(self):
        self.clean_dict()
        fields = [field.replace(' ','_') for field in self.check_dict.keys() if self.check_dict[field] == 1]
        self.master.destroy()
        Report(fields)




def run():
    home = HomeScreen()



run()