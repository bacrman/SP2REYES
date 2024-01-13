import tkinter as tk

class StarRatingWidget(tk.Frame):
    def __init__(self, master=None, num_stars=5, **kwargs):
        super().__init__(master, **kwargs)
        self.num_stars = num_stars
        self.rating = tk.IntVar()

        # Add a border and background color to the frame
        self.config(borderwidth=2, relief="solid", background="black", padx=5, pady=5)

        self.create_stars()
        self.bind("<Motion>", self.on_hover)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)

    def create_stars(self):
        for i in range(1, self.num_stars + 1):
            star_label = tk.Label(self, fg='grey',text='\u2605', font=('Arial', 20), cursor='hand2', background="black")
            star_label.grid(row=0, column=i-1, padx=5)
            star_label.bind("<Enter>", lambda event, rating=i: self.highlight_stars(rating))

    def on_hover(self, event):
        rating = int((event.x / self.winfo_width()) * self.num_stars) + 1
        self.highlight_stars(rating)

    def on_leave(self, event):
        self.highlight_stars(self.rating.get())

    def on_click(self, event):
        rating = int((event.x / self.winfo_width()) * self.num_stars) + 1
        self.set_rating(rating)

    def highlight_stars(self, num_stars):
        self.rating.set(num_stars)
        for i, child in enumerate(self.winfo_children()):
            if i < num_stars:
                child.config(fg='yellow')
            else:
                child.config(fg='grey')

    def set_rating(self, rating):
        self.rating.set(rating)
        # Save the rating value to a file, database, or perform any other action

    def get(self, default=None):
        if self.rating.get() is None:
            return default
        return self.rating.get()

