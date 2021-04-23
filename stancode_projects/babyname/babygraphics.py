"""
SC101 Baby Names Project
Adapted from Nick Parlante's Baby Names assignment by
Jerry Liao.

YOUR DESCRIPTION HERE
"""

import tkinter
import babynames
import babygraphicsgui as gui

FILENAMES = [
    'data/full/baby-1900.txt', 'data/full/baby-1910.txt',
    'data/full/baby-1920.txt', 'data/full/baby-1930.txt',
    'data/full/baby-1940.txt', 'data/full/baby-1950.txt',
    'data/full/baby-1960.txt', 'data/full/baby-1970.txt',
    'data/full/baby-1980.txt', 'data/full/baby-1990.txt',
    'data/full/baby-2000.txt', 'data/full/baby-2010.txt'
]
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 600
YEARS = [1900, 1910, 1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]
GRAPH_MARGIN_SIZE = 20
COLORS = ['#D5674F', '#F5B945', '#4FD5AA', '#587BE1', '#9C61C9']
TEXT_DX = 2
LINE_WIDTH = 2
MAX_RANK = 1000


def get_x_coordinate(width, year_index):
    """
    Given the width of the canvas and the index of the current year
    in the YEARS list, returns the x coordinate of the vertical
    line associated with that year.

    Input:
        width (int): The width of the canvas
        year_index (int): The index of the current year in the YEARS list
    Returns:
        x_coordinate (int): The x coordinate of the vertical line associated
                              with the specified year.
    """
    for i in range(len(YEARS)):
        if i == year_index:
            x_coordinate = GRAPH_MARGIN_SIZE + (width-GRAPH_MARGIN_SIZE*2)//len(YEARS)*i
            return int(x_coordinate)


def draw_fixed_lines(canvas):
    """
    Erases all existing information on the given canvas and then
    draws the fixed background lines on it.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.

    Returns:
        This function does not return any value.
    """
    canvas.delete('all')            # delete all existing lines from the canvas

    # Write your code below this line
    #################################
    # bottom line
    canvas.create_line(GRAPH_MARGIN_SIZE, CANVAS_HEIGHT-GRAPH_MARGIN_SIZE,
                       CANVAS_WIDTH-GRAPH_MARGIN_SIZE, CANVAS_HEIGHT-GRAPH_MARGIN_SIZE)
    # top line
    canvas.create_line(GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE, CANVAS_WIDTH-GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE)
    # vertical line
    for i in range(len(YEARS)):
        x = get_x_coordinate(CANVAS_WIDTH, i)
        canvas.create_line(x, 0, x, CANVAS_HEIGHT)
        canvas.create_text(x+TEXT_DX, CANVAS_HEIGHT-GRAPH_MARGIN_SIZE,  text=YEARS[i], anchor=tkinter.NW)  # year text


def draw_names(canvas, name_data, lookup_names):
    """
    Given a dict of baby name data and a list of name, plots
    the historical trend of those names onto the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
        name_data (dict): Dictionary holding baby name data
        lookup_names (List[str]): A list of names whose data you want to plot

    Returns:
        This function does not return any value.
    """
    draw_fixed_lines(canvas)        # draw the fixed background grid

    # Write your code below this line
    #################################
    for i in range(len(lookup_names)):
        name = lookup_names[i]

        # curve line color
        if i < len(COLORS):
            color = COLORS[i]
        else:
            color = COLORS[i % len(COLORS)]

        # create curve line
        for j in range(len(YEARS)-1):
            # rank 1-1000, male
            if str(YEARS[j]) in name_data[name]:
                year_1 = YEARS[j]
                rank_1 = name_data[name][str(year_1)]
                y1 = int((CANVAS_HEIGHT-GRAPH_MARGIN_SIZE*2)/MAX_RANK*int(rank_1)+GRAPH_MARGIN_SIZE)
                year_index_1 = YEARS.index(year_1)
                x1 = get_x_coordinate(CANVAS_WIDTH, year_index_1)
            # rank 1000+, male
            else:
                year_1 = YEARS[j]
                rank_1 = MAX_RANK
                y1 = CANVAS_HEIGHT-GRAPH_MARGIN_SIZE
                year_index_1 = YEARS.index(year_1)
                x1 = get_x_coordinate(CANVAS_WIDTH, year_index_1)
            # rank 1-1000, female
            if str(YEARS[j+1]) in name_data[name]:
                year_2 = YEARS[j+1]
                rank_2 = name_data[name][str(year_2)]
                y2 = int((CANVAS_HEIGHT-GRAPH_MARGIN_SIZE*2)/MAX_RANK*int(rank_2)+GRAPH_MARGIN_SIZE)
                year_index_2 = YEARS.index(year_2)
                x2 = get_x_coordinate(CANVAS_WIDTH, year_index_2)
            # rank 1000+, female
            else:
                year_2 = YEARS[j+1]
                rank_2 = MAX_RANK
                y2 = CANVAS_HEIGHT-GRAPH_MARGIN_SIZE
                year_index_2 = YEARS.index(year_2)
                x2 = get_x_coordinate(CANVAS_WIDTH, year_index_2)

            canvas.create_line(x1, y1, x2, y2, width=LINE_WIDTH, fill=color)

            # male
            if rank_1 == MAX_RANK:
                # rank 1000+
                canvas.create_text(x1 + TEXT_DX, y1, text=name + " " + "*", anchor=tkinter.SW, fill=color)
            else:
                # rank 1-1000
                canvas.create_text(x1 + TEXT_DX, y1, text=name + " " + str(rank_1),
                                   anchor=tkinter.SW, fill=color)
            # female
            if rank_2 == MAX_RANK:
                # rank 1000+
                canvas.create_text(x2 + TEXT_DX, y2, text=name + " " + "*", anchor=tkinter.SW, fill=color)
            else:
                # rank 1-1000
                canvas.create_text(x2 + TEXT_DX, y2, text=name + " " + str(rank_2),
                                   anchor=tkinter.SW, fill=color)


# main() code is provided, feel free to read through it but DO NOT MODIFY
def main():
    # Load data
    name_data = babynames.read_files(FILENAMES)

    # Create the window and the canvas
    top = tkinter.Tk()
    top.wm_title('Baby Names')
    canvas = gui.make_gui(top, CANVAS_WIDTH, CANVAS_HEIGHT, name_data, draw_names, babynames.search_names)

    # Call draw_fixed_lines() once at startup so we have the lines
    # even before the user types anything.
    draw_fixed_lines(canvas)

    # This line starts the graphical loop that is responsible for
    # processing user interactions and plotting data
    top.mainloop()


if __name__ == '__main__':
    main()
