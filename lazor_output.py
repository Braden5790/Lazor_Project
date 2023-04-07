'''
Author: Braden Barlean

This module serves as the output of the Lazor Project. It takes the
laser data and displays it using tkinter. 
'''
import tkinter as tk
from tkinter import filedialog
from PIL import Image
from bff_reader import read_bff


data = read_bff('mad_1.bff')
chars = data['grid']
points = data['points']

# Create the main window
root = tk.Tk()
root.title('Output')

# Create a frame for the grid
frame = tk.Frame(root, bd=5, bg='white')
frame.grid(row=0, column=0)

# Create a canvas for the grid
canvas = tk.Canvas(frame, width=500, height=500, bg='white')
canvas.grid(row=0, column=0)

# Define the size of each square in the grid
square_size = 24

# Draw the grid of characters
for row, char_row in enumerate(chars):
    for col, char in enumerate(char_row):
        x0 = col * square_size
        y0 = row * square_size
        x1 = x0 + square_size
        y1 = y0 + square_size
        if char == 'o':
            canvas.create_rectangle(x0, y0, x1, y1, fill='grey', outline='white')
        elif char == 'x':
            canvas.create_rectangle(x0, y0, x1, y1, fill='black', outline='white')
        elif char == 'A' or char == 'a':
            canvas.create_rectangle(x0, y0, x1, y1, fill='blue', outline='white')
        elif char == 'B' or char == 'b':
            canvas.create_rectangle(x0, y0, x1, y1, fill='orange', outline='white')
        elif char == 'C' or char == 'c':
            canvas.create_rectangle(x0, y0, x1, y1, fill='yellow', outline='white')

# Draw a red line
start_x = 2.5 * square_size
start_y = 8.5 * square_size
middle_x = 2 * square_size
middle_y = 1.5 * square_size
end_x = 5 * square_size
end_y = 5.5 * square_size
canvas.create_line(start_x, start_y, middle_x, middle_y, end_x, end_y, fill='red', width=3)

# Draw a red dot at the start of the line
dot_size = 3
canvas.create_oval(start_x - dot_size, start_y - dot_size, start_x + dot_size, start_y + dot_size, fill='red', outline='white')

# Draw a red circle where the line needs to intersect
for coords in points:
    x = (coords[0]+1.5) * square_size
    y = (coords[1]+1.5) * square_size
    canvas.create_oval(x - dot_size, y - dot_size, x + dot_size, y + dot_size, fill='white', outline='red')

# Save the canvas as an image
def save_canvas():
    filename = filedialog.asksaveasfilename()
    if filename:
        canvas.postscript(file=filename + '.eps')

# Add a button to save the canvas as an image
save_button = tk.Button(root, text="Save", command=save_canvas)
save_button.grid(row=1, column=0)

# ^^ This works but idk why the below alone doesn't work 
canvas.postscript(file='output' + '.eps')

root.mainloop()