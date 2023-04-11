'''
Author: Braden Barlean

This module serves as the output of the Lazor Project. It takes the
laser data and displays it using tkinter. 
'''
import tkinter as tk
from PIL import ImageGrab

def visual_board(data):
    '''
    This function takes in the solved board, presents it, and
    saves it as a pdf.
    '''
    chars = data['grid']
    points = data['points']
    lazers = data['lazors']
    filename = data['filename']

    # Create the main window
    root = tk.Tk()
    root.title('Output')

    # Create a frame for the grid
    frame = tk.Frame(root, bd=5, bg='white')
    frame.grid(row=0, column=0)
    
    # Define the size of each square in the grid
    square_size = 25

    # Create a canvas for the grid
    canvas = tk.Canvas(frame, width=(len(chars[0])*square_size), height=(len(chars)*square_size), bg='white')
    canvas.grid(row=0, column=0)

    # Draw the grid of characters
    for row, char_row in enumerate(chars):
        for col, char in enumerate(char_row):
            x0 = col * square_size
            y0 = row * square_size
            x1 = x0 + square_size*2
            y1 = y0 + square_size*2
            if char == 'o':
                canvas.create_rectangle(x0, y0, x1, y1,
                                        fill='grey', outline='white')
            elif char == 'x':
                canvas.create_rectangle(x0, y0, x1, y1,
                                        fill='black', outline='white')
            elif char == 'A' or char == 'a':
                canvas.create_rectangle(x0, y0, x1, y1,
                                        fill='blue', outline='white')
            elif char == 'B' or char == 'b':
                canvas.create_rectangle(x0, y0, x1, y1,
                                        fill='orange', outline='white')
            elif char == 'C' or char == 'c':
                canvas.create_rectangle(x0, y0, x1, y1,
                                        fill='yellow', outline='white')

    # Draw a red line
    for lazor in lazers:
        for i in range(len(lazor)):
            try:
                start_x, start_y = (lazor[i][0]+1) * square_size, (lazor[i][1]+1) * square_size
                end_x, end_y = (lazor[i+1][0]+1) * square_size, (lazor[i+1][1]+1) * square_size
                canvas.create_line(start_x, start_y, end_x, end_y, fill='red', width=3)
            except:
                break

            # Draw a red dot at the start of the line
            # This needs to change to be the starting coordinates of the laser (could do now)
        start_x = (lazor[0][0]+1) * square_size
        start_y = (lazor[0][1]+1) * square_size
        dot_size = 3
        canvas.create_oval(start_x - dot_size,
                        start_y - dot_size,
                        start_x + dot_size,
                        start_y + dot_size,
                        fill='red', outline='white')

    # Draw a red circle where the line needs to intersect
    for coords in points:
        x = (coords[0]+1) * square_size
        y = (coords[1]+1) * square_size
        canvas.create_oval(x - dot_size,
                           y - dot_size,
                           x + dot_size,
                           y + dot_size,
                           fill='white', outline='red')

    # Save canvas as image
    canvas.update()
    img = ImageGrab.grab(bbox=(canvas.winfo_rootx(),
                               canvas.winfo_rooty(),
                               canvas.winfo_rootx()
                               + canvas.winfo_width(),
                               canvas.winfo_rooty()
                               + canvas.winfo_height()))
    cleanname = filename[:-4]
    img.save(cleanname + "_output.png")

    root.destroy()
