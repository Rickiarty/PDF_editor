"""
 * 
 *  Coded by Rei-Chi Lin 
 * 
"""

from PdfEditor.program import WindowProgrm
from PdfEditor.PdfLib.pdf_manipulation import PdfManipulator
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox as mb
from tkinter import simpledialog as s_dialog
#from PIL import ImageTk, Image

class MainWindowProgrm(WindowProgrm):
    _pdf_manipulator = None
    _sort_count      = 0
    _image_path      = ""
    # widgets
    _main_program         = None
    _listbox_src          = None
    _listbox_dest         = None
    _browse_import_button = None
    _browse_export_button = None
    _swap_button          = None
    _remove_button        = None
    _remove_all_button    = None
    _sort_button          = None
    _split_button         = None
    _merge_button         = None
    _refresh_button       = None
    _icon_photo           = None
    _studio_logo          = None
    _logo_banner          = None

    def initialize(self):
        self._pdf_manipulator = PdfManipulator()
        self._main_program = tk.Tk() # an entity of application of Tkinter framework 

        # set title, size, position, event(s), and background color of window
        self._main_program.title('PDF editor - v{} © 2021 {}'.format(self.version, self.author))
        width = 1000
        height = 600
        position_x = int(self._main_program.winfo_screenwidth()/2 - width/2)
        position_y = int(self._main_program.winfo_screenheight()/2 - height/2)
        self._main_program.geometry('{}x{}'.format(width, height)) # size: width x height
        self._main_program.geometry('+{}+{}'.format(position_x, position_y)) # position of left-top of window
        self._main_program.configure(background='gray') # background color
        self._main_program.protocol(name="WM_DELETE_WINDOW", func=self._on_closing) # set event handler on closing window

        # build listboxes
        self._listbox_src = tk.Listbox(self._main_program, selectmode=tk.EXTENDED)
        self._listbox_src.pack(side=tk.LEFT, fill='both')
        self._listbox_dest = tk.Listbox(self._main_program, selectmode=tk.EXTENDED)
        self._listbox_dest.pack(side=tk.RIGHT, fill='both')
        
        # build buttons
        self._browse_import_button = tk.Button(self._main_program, 
                                                width = 64, 
                                                height=2, 
                                                text='Import from PDF file', 
                                                command=self._browse_import_button_pressed, 
                                                relief=tk.RIDGE, 
                                                borderwidth=5)
        self._browse_import_button.pack()
        self._split_button = tk.Button(self._main_program, 
                                        width = 64, 
                                        height=2, 
                                        text='Split 1 to multiple', 
                                        command=self._split_button_pressed, 
                                        relief=tk.RIDGE, 
                                        borderwidth=5)
        self._split_button.pack()
        self._merge_button = tk.Button(self._main_program, 
                                        width = 64, 
                                        height=2, 
                                        text='Merge all to 1', 
                                        command=self._merge_button_pressed, 
                                        relief=tk.RIDGE, 
                                        borderwidth=5)
        self._merge_button.pack()
        self._swap_button = tk.Button(self._main_program, 
                                        width = 64, 
                                        height=2, 
                                        text='Swap', 
                                        command=self._swap_button_pressed, 
                                        relief=tk.RIDGE, 
                                        borderwidth=5)
        self._swap_button.pack()
        self._remove_button = tk.Button(self._main_program, 
                                        width = 64, 
                                        height=2, 
                                        text='Remove', 
                                        command=self._remove_button_pressed, 
                                        relief=tk.RIDGE, 
                                        borderwidth=5)
        self._remove_button.pack()
        self._sort_button = tk.Button(self._main_program, 
                                        width = 64, 
                                        height=2, 
                                        text='Sort', 
                                        command=self._sort_button_pressed, 
                                        relief=tk.RIDGE, 
                                        borderwidth=5)
        self._sort_button.pack()
        self._remove_all_button = tk.Button(self._main_program, 
                                            width = 64, 
                                            height=2, 
                                            text='Remove all', 
                                            command=self._remove_all_button_pressed, 
                                            relief=tk.RIDGE, 
                                            borderwidth=5)
        self._remove_all_button.pack()
        self._browse_export_button = tk.Button(self._main_program, 
                                                width = 64, 
                                                height=2, 
                                                text='Export PDF to folder', 
                                                command=self._browse_export_button_pressed, 
                                                relief=tk.RIDGE, 
                                                borderwidth=5)
        self._browse_export_button.pack()
        self._refresh_button = tk.Button(self._main_program, 
                                            width = 64, 
                                            height=2, 
                                            text='refresh', 
                                            command=self._refresh_button_pressed, 
                                            relief=tk.RIDGE, 
                                            borderwidth=5)
        self._refresh_button.pack()
        # build image widgets
        # app icon
        #self._image_path = "./PdfEditor/resource/image"
        #self._image_path = os.path.abspath(self._image_path)
        #self._icon_photo = tk.PhotoImage(file = open(os.path.join(self._image_path, 'pdf_icon.png'), 'rb'))
        #self._main_program.iconphoto(False, self._icon_photo)
        # logo
        #self._studio_logo = Image.open(os.path.join(self._image_path, 'pdf_icon.png'), 'rb')
        #self._studio_logo = self._studio_logo.resize((250, 250), Image.ANTIALIAS) # resize
        #self._studio_logo = ImageTk.PhotoImage(self._studio_logo)
        #self._logo_banner = tk.Label(self._main_program, image=self._studio_logo)
        #self._logo_banner.image = self._studio_logo
        #self._logo_banner.pack()
    
    def _on_closing(self):
        if mb.askokcancel("Quit", "Do you want to quit?"):
            self._pdf_manipulator.close()
            self._main_program.destroy()
    
    def run(self):
        # run app
        self._main_program.mainloop()

    def _refresh(self):
        self._refresh_import()
        self._refresh_export()
    
    def _refresh_import(self):
        self._listbox_src.delete(0, tk.END)
        obj_list = self._pdf_manipulator.r_pdf_list
        for obj in obj_list:
            # insert items with a string into specific locations 
            self._listbox_src.insert(tk.END, obj.obj_name)
    def _refresh_export(self):
        self._listbox_dest.delete(0, tk.END)
        obj_list = self._pdf_manipulator.w_pdf_list
        for obj in obj_list:
            # insert items with a string into specific locations 
            self._listbox_dest.insert(tk.END, obj.obj_name)

    def _refresh_button_pressed(self):
        self._refresh()

    def _r_get_chosen_items(self):
        return self._listbox_src.curselection()
    def _w_get_chosen_items(self):
        return self._listbox_dest.curselection()

    def _ask_for_splitting_points(self):
        try:
            series_str = s_dialog.askstring(title="splitting points", prompt="Enter number(s) of point(s) which you want to split a specific PDF file.\nexample of format: 2,4,7")
            series_str = WindowProgrm.sanitize_data(series_str)
            if series_str == "":
                return None
            if series_str[-1] == ','[0]:
                series_str = series_str[0:-1]
            series = series_str.split(',')
            series = [int(num_s) for num_s in series] # 'list comprehension' in Python
            return series
        except Exception as ex:
            mb.showerror("Error", str(ex))
            return None
    
    def _browse_import_button_pressed(self): # IMPORT button
        file_path = filedialog.askopenfilename() # open a file browser to let users choose a specific file. 
        err = self._pdf_manipulator.read_pdf_from(file_path)
        self._refresh_import()
        if err != None:
            mb.showerror("Error", str(err))

    def _browse_export_button_pressed(self): # EXPORT button
        dir_path = filedialog.askdirectory() # open a folder browser to let users choose a specific folder. 
        w_list = self._pdf_manipulator.w_pdf_list
        if len(w_list) < 1:
            mb.showerror("Message", "There is no file in list to export.")
        else:
            chosen_items = self._w_get_chosen_items()
            if len(chosen_items) == 0:
                for pdf_obj in w_list:
                    file_path = os.path.join(dir_path, pdf_obj.obj_name)
                    index = w_list.index(pdf_obj)
                    err = self._pdf_manipulator.write_pdf_to(index, file_path)
                    if err != None:
                        mb.showerror("Error", str(err))
            else:
                for index in chosen_items:
                    file_path = os.path.join(dir_path, w_list[index].obj_name)
                    err = self._pdf_manipulator.write_pdf_to(index, file_path)
                    if err != None:
                        mb.showerror("Error", str(err))
        self._refresh_export()

    def _swap_button_pressed(self):
        chosen_items = self._r_get_chosen_items()
        if len(chosen_items) == 2:
            self._pdf_manipulator.r_swap(chosen_items[0], chosen_items[1])
        elif len(chosen_items) != 0:
            mb.showerror("Message", "Choose EXACT 2 imported files.")
        chosen_items = self._w_get_chosen_items()
        if len(chosen_items) == 2:
            self._pdf_manipulator.w_swap(chosen_items[0], chosen_items[1])
        elif len(chosen_items) != 0:
            mb.showerror("Message", "Choose EXACT 2 exported files.")
        self._refresh()

    def _remove_button_pressed(self):
        chosen_items = self._r_get_chosen_items()
        for loc in chosen_items:
            self._pdf_manipulator.r_delete_pdf_at(loc)
        chosen_items = self._w_get_chosen_items()
        for loc in chosen_items:
            self._pdf_manipulator.w_delete_pdf_at(loc)
        self._refresh()

    def _remove_all_button_pressed(self):
        self._pdf_manipulator.r_clear_list()
        self._pdf_manipulator.w_clear_list()
        self._refresh()

    def _sort_button_pressed(self):
        if self._sort_count % 2 == 0: # is even 
            self._pdf_manipulator.r_sort_asc()
            self._pdf_manipulator.w_sort_asc()
        else: # is odd (self._sort_count % 2 == 1) 
            self._pdf_manipulator.r_sort_desc()
            self._pdf_manipulator.w_sort_desc()
        self._sort_count += 1
        self._refresh()

    def _split_button_pressed(self):
        chosen_items = self._r_get_chosen_items()
        if len(chosen_items) != 1:
            mb.showerror("Message", "Choose exact 1 imported files.")
            return
        pages = self._ask_for_splitting_points()
        if pages == None:
            mb.showerror("Message", "bad format")
            return
        self._pdf_manipulator.w_clear_list()
        self._refresh()
        err = self._pdf_manipulator.split_one_to_multiple(chosen_items[0], pages)
        self._refresh()
        if err != None:
            mb.showerror("Error", str(err))

    def _merge_button_pressed(self):
        if len(self._pdf_manipulator.r_pdf_list) < 1:
            return
        self._pdf_manipulator.w_clear_list()
        self._refresh()
        err = self._pdf_manipulator.merge_multiple_to_one()
        self._refresh()
        if err != None:
            mb.showerror("Error", str(err))
