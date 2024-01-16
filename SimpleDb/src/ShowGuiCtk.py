import customtkinter
import math
from tkinter import *
from tkinter import ttk
from tkinter import font
import tkinter as tk
from tkinter import messagebox
from ShowDbSqlite import ShowDbSqlite
from StarRatingWidget import StarRatingWidget
from DateInputWidget import DateInputWidget 
from datetime import datetime
from tkinter import filedialog





class ShowGuiCtk(customtkinter.CTk):

    def __init__(self, dataBase=ShowDbSqlite('ShowDb.db')):
        super().__init__()
        self.db = dataBase

        self.title('Show Rating App')
        self.geometry('1400x500')
        self.config(bg='#615748')
        self.resizable(False, False)

        self.font1 = ('Times New Roman', 20, 'bold')
        self.font2 = ('Times New Roman', 12, 'bold')

        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        
        # Date Entry Form
        self.date_label = self.newCtkLabel('Date')
        self.date_label.place(x=20, y=40)
        self.date_entry = DateInputWidget(self) 
        self.date_entry.place(x=100, y=40)


        # 'showTitle' Label and Entry Widgets
        self.showTitle_label = self.newCtkLabel('Title')
        self.showTitle_label.place(x=20, y=100)
        self.showTitle_entry = self.newCtkEntry()
        self.showTitle_entry.place(x=100, y=100)

        # 'genre' Label and Combo Box Widgets
        self.genre_label = self.newCtkLabel('Genre')
        self.genre_label.place(x=20, y=160)
        self.genre_cboxVar = StringVar()
        self.genre_cboxOptions = ['Action', 'Comedy', 'Drama', 'Horror', 'Sci-Fi','Thriller','Fantasy','Non-Fiction','Fantasy', 'Adventure']
        self.genre_cbox = self.newCtkComboBox(options=self.genre_cboxOptions, 
                                    entryVariable=self.genre_cboxVar)
        self.genre_cbox.place(x=100, y=160)

        # 'status' Label and Combo Box Widgets
        self.status_label = self.newCtkLabel('Status')
        self.status_label.place(x=20, y=220)
        self.status_cboxVar = StringVar()
        self.status_cboxOptions = ['Currently Airing', 'Finished Airing', 'Hiatus']
        self.status_cbox = self.newCtkComboBox(options=self.status_cboxOptions, 
                                    entryVariable=self.status_cboxVar)
        self.status_cbox.place(x=100, y=220)


        # 'ratings' Label and Combo Box Widgets
        self.rating_label = self.newCtkLabel('Rating')
        self.rating_label.place(x=20, y=280)
        self.rating_cboxVar = StringVar()
        self.rating_cboxOptions = ['G', 'PG', 'PG-13', 'R', 'NC-17']
        self.rating_cbox = self.newCtkComboBox(options=self.rating_cboxOptions, 
                                    entryVariable=self.rating_cboxVar)
        self.rating_cbox.place(x=100, y=280)

        # 'star rating' label
        self.star_rating_label = self.newCtkLabel('Stars')
        self.star_rating_label.place(x=20, y=340)
        self.star_rating_widget = StarRatingWidget(self, num_stars=5)
        self.star_rating_widget.grid(row=0, column=1, padx=5)
        self.star_rating_widget.place(x=80, y=323)

        self.add_button = self.newCtkButton(text='Add show',
                                onClickHandler=self.add_entry)
        self.add_button.place(x=356,y=400)

        self.new_button = self.newCtkButton(text='New show',
                                onClickHandler=lambda:self.clear_form(True))
        self.new_button.place(x=612, y=400)

        self.update_button = self.newCtkButton(text='Update show',
                                    onClickHandler=self.update_entry)
        self.update_button.place(x=868, y=400)

        self.delete_button = self.newCtkButton(text='Delete show',
                                    onClickHandler=self.delete_entry,
                                    fgColor='#E40404',
                                    hoverColor='#AE0000',
                                    borderColor='#E40404')
        self.delete_button.place(x=1130, y=400)
        ###############################################
        self.export_button = self.newCtkButton(text='Export to CSV',
                                    onClickHandler=self.export_to_csv)
        self.export_button.place(x=1130,y=450)

        ##############################################
        self.import_button = self.newCtkButton(text='Import from CSV',
                                        onClickHandler=self.import_data_from_csv)
        self.import_button.place(x=868, y=450)

        ######################################
        self.json_button = self.newCtkButton(text='Export to JSON',
                                        onClickHandler=self.export_to_json)
        self.json_button.place(x=612, y=450)


        # Tree View for Database Entries
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('Treeview', 
                        font=self.font2, 
                        foreground='#fff',
                        background='#000',
                        fieldbackground='#313837')
        
        self.style.map('Treeview', background=[('selected', '#1A8F2D')])

        self.style.configure('Treeview.Heading', font=self.font1, background='#5b7b7a', foreground='#fff')
        self.style.configure('Treeview', rowheight=30)

        self.tree = ttk.Treeview(self, height=15, style='Treeview')


        self.tree['columns'] =  ('date', 'showTitle', 'Genre', 'Status', 'Rating','Stars')
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('date', anchor=tk.CENTER, width=10)
        self.tree.column('showTitle', anchor=tk.CENTER, width=260)
        self.tree.column('Genre', anchor=tk.CENTER, width=65)
        self.tree.column('Status', anchor=tk.CENTER, width=125)
        self.tree.column('Rating', anchor=tk.CENTER, width=10)
        self.tree.column('Stars', anchor=tk.CENTER, width=10)

        self.tree.heading('date', text='Date')
        self.tree.heading('showTitle', text='Title')
        self.tree.heading('Genre', text='Genre')
        self.tree.heading('Status', text='Status')
        self.tree.heading('Rating', text='Rating')
        self.tree.heading('Stars', text='Stars')

        self.tree.place(x=360, y=20, width=1000, height=350)
        self.tree.bind('<ButtonRelease>', self.read_display_data)

        self.add_to_treeview()

    def treeview_sort_column(self, tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        # reverse sort next time
        tv.heading(col, command=lambda: self.treeview_sort_column(tv, col, not reverse))

    def newCtkRatingScale(self, num_stars):
        widget_Font = self.font1
        widget_Length = 200

        widget = ttk.Scale(self, 
                           from_=0, to=num_stars, 
                           orient=HORIZONTAL, 
                           length=widget_Length)
        
        return widget


    def newCtkLabel(self, text = 'CTK Label'):
        widget_Font=self.font1
        widget_TextColor='#FFF'
        widget_BgColor='#615748'

        widget = customtkinter.CTkLabel(self, 
                                    text=text,
                                    font=widget_Font, 
                                    text_color=widget_TextColor,
                                    bg_color=widget_BgColor)
        return widget

    # new Entry Widget
    def newCtkEntry(self, text = 'CTK Label'):
        widget_Font=self.font1
        widget_TextColor='#000'
        widget_FgColor='#FFF'
        widget_BorderColor='#5b7b7a'
        widget_BorderWidth=2
        widget_Width=250

        widget = customtkinter.CTkEntry(self,
                                    font=widget_Font,
                                    text_color=widget_TextColor,
                                    fg_color=widget_FgColor,
                                    border_color=widget_BorderColor,
                                    border_width=widget_BorderWidth,
                                    width=widget_Width)
        return widget

    # new Combo Box Widget
    def newCtkComboBox(self, options=['DEFAULT', 'OTHER'], entryVariable=None):
        widget_Font=self.font1
        widget_TextColor='#000'
        widget_FgColor='#FFF'
        widget_DropdownHoverColor='#5b7b7a'
        widget_ButtonColor='#5b7b7a'
        widget_ButtonHoverColor='#5b7b7a'
        widget_BorderColor='#5b7b7a'
        widget_BorderWidth=2
        widget_Width=250

        widget = customtkinter.CTkComboBox(self,
                                        font=widget_Font,
                                        text_color=widget_TextColor,
                                        fg_color=widget_FgColor,
                                        border_color=widget_BorderColor,
                                        dropdown_hover_color=widget_DropdownHoverColor,
                                        button_color=widget_ButtonColor,
                                        border_width=widget_BorderWidth,
                                        button_hover_color=widget_ButtonHoverColor,
                                        width=widget_Width,
                                        variable=entryVariable,
                                        values=options,
                                        state='readonly')
        
        # set default value to 1st option
        widget.set(options[0])

        return widget

    # new Button Widget
    def newCtkButton(self, text = 'CTK Button', onClickHandler=None, fgColor='#313837', hoverColor='#5b7b7a', bgColor='#313837', borderColor='#313837'):
        widget_Font=self.font1
        widget_TextColor='#FFF'
        widget_FgColor=fgColor
        widget_HoverColor=hoverColor
        widget_BackgroundColor=bgColor
        widget_BorderColor=borderColor
        widget_BorderWidth=2
        widget_Cursor='hand2'
        widget_CornerRadius=2
        widget_Width=230
        widget_Function=onClickHandler

        widget = customtkinter.CTkButton(self,
                                        text=text,
                                        command=widget_Function,
                                        font=widget_Font,
                                        text_color=widget_TextColor,
                                        fg_color=widget_FgColor,
                                        hover_color=widget_HoverColor,
                                        bg_color=widget_BackgroundColor,
                                        border_color=widget_BorderColor,
                                        border_width=widget_BorderWidth,
                                        cursor=widget_Cursor,
                                        corner_radius=widget_CornerRadius,
                                        width=widget_Width)
       
        return widget

    # Handles
    def add_to_treeview(self):
        shows = self.db.fetch_shows()
        self.tree.delete(*self.tree.get_children())
        for show in shows:
            print(show)
            self.tree.insert('', END, values=show)

    def clear_form(self, *clicked):
        if clicked:
            self.tree.selection_remove(self.tree.focus())
            self.tree.focus('')
        self.showTitle_entry.delete(0, END)
        self.genre_cboxVar.set('Action')
        self.status_cboxVar.set('Currently Airing')
        self.rating_cboxVar.set('G')
        self.date_entry.set_date(datetime.now().strftime("%Y-%m-%d"))
        


    def read_display_data(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            row = self.tree.item(selected_item)['values']
            self.clear_form()

            # Use set_date to update the DateInputWidget
            self.date_entry.set_date(row[0])
            self.showTitle_entry.insert(0, row[1])
            self.genre_cboxVar.set(row[2])
            self.status_cboxVar.set(row[3])
            self.rating_cboxVar.set(row[4])
            self.star_rating_widget.get(row[5])
        else:
            pass

    def add_entry(self):
        date_id = self.date_entry.get_date()
        showTitle = self.showTitle_entry.get()
        genre = self.genre_cboxVar.get()
        status = self.status_cboxVar.get()    
        rating = self.rating_cboxVar.get()
        star_rating = self.star_rating_widget.get()

        # Check for valid input and perform the database insertion
        if not (date_id and showTitle and genre and status and rating and star_rating):
            messagebox.showerror('Error', 'Enter all fields.')
        elif self.db.id_exists(showTitle):
            messagebox.showerror('Error', 'Show already exists')
        else:
            self.db.insert_show(date_id, showTitle, genre, status, rating, star_rating)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Show data has been inserted')


    def delete_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose an show to delete')
        else:
            showTitle = self.showTitle_entry.get()
            self.db.delete_show(showTitle)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been deleted')

    def update_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose a show to update')
        else:
            # Get the current values of the selected item
            current_values = self.tree.item(selected_item)['values']
            current_showTitle = current_values[1]

            # Delete the current entry
            self.db.delete_show(current_showTitle)

            # Now, insert the updated entry
            date_id = self.date_entry.get_date()
            showTitle = self.showTitle_entry.get()
            genre = self.genre_cboxVar.get()
            status = self.status_cboxVar.get()
            rating = self.rating_cboxVar.get()
            star_rating = self.star_rating_widget.get()

            # Check for valid input and perform the database insertion
            if not (date_id and showTitle and genre and status and rating and star_rating):
                messagebox.showerror('Error', 'Enter all fields.')
            else:
                self.db.insert_show(date_id, showTitle, genre, status, rating, star_rating)
                self.add_to_treeview()
                self.clear_form()
                messagebox.showinfo('Success', 'Show data has been updated')



    
    
    def export_to_csv(self):
        self.db.export_csv()
        messagebox.showinfo('Success', f'Data exported to {self.db.dbName}')

    def import_data_from_csv(self):
        file_path = filedialog.askopenfilename(title='Select CSV File', filetypes=[('CSV Files', '*.csv')])

        if file_path:
            try:
                self.db.load_from_csv(file_path)
                self.add_to_treeview()
                messagebox.showinfo('Success', 'Data imported from CSV')
            except Exception as e:
                messagebox.showerror('Error', f'Error importing data: {str(e)}')

    def export_to_json(self):
        self.db.export_json()
        messagebox.showinfo('Success', f'Data exported to json')