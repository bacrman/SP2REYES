import tkinter as tk
from tkcalendar import DateEntry
from datetime import datetime

class DateInputWidget(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)

        # Styling options
        widget_Font = ('Arial Bold', 12)
        widget_TextColor = '#FFF'
        widget_FgColor = 'black'
        widget_BackgroundColor = '#5b7b7a'
        widget_BorderColor = '#5b7b7a'
        widget_DropdownHoverColor='#5b7b7a'
        widget_ButtonColor='#5b7b7a'
        widget_ButtonHoverColor='#5b7b7a'
        widget_BorderWidth = 2
        widget_Cursor = 'hand2'
        widget_CornerRadius = 15
        widget_Width = 25

        # Create DateEntry widget
        self.date_entry = DateEntry(self,
                                    textColor= widget_TextColor,
                                    width=widget_Width,
                                    BorderColor=widget_BorderColor,
                                    background=widget_BackgroundColor,
                                    foreground=widget_FgColor,
                                    borderwidth=widget_BorderWidth,
                                    font=widget_Font,
                                    cursor=widget_Cursor,
                                    corner_radius=widget_CornerRadius,
                                    dropdown_hover_color=widget_DropdownHoverColor,
                                    button_color=widget_ButtonColor,
                                    button_hover_color=widget_ButtonHoverColor)

        # Clear the current date and set the placeholder text
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, "YYYY-MM-DD")

        # Grid layout
        self.date_entry.grid(row=0, column=0)

        # Variable to store the formatted date
        self.formatted_date = ""


    def get_date(self):
        selected_date = self.date_entry.get_date()
        return selected_date

    def set_date(self, date_str):
        print(f"Setting date to: {date_str}")

        try:
            # Clear the existing date entry
            self.date_entry.delete(0, tk.END)

            # Set the new date
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            self.date_entry.set_date(date_obj)
        except ValueError:
            print("Invalid date format")

