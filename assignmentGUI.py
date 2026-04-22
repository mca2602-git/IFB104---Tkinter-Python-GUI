#-----Statement of Authorship----------------------------------------#
#
# This is an individual assessment task for QUT's teaching unit
# IFB104, "Building IT Systems". By submitting
# this code I agree that it represents my own work. I am aware of
# the University rule that a student must not act in a manner
# which constitutes academic dishonesty as stated and explained
# in QUT's Manual of Policies and Procedures, Section C/5.3
# "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
# Put your student number here as an integer and your name as a
# character string:
#
student_number = 12345678
# ^ NOT REAL STUDENT NUM #
student_name = "Marc Allam"
#
# NB: All files submitted for this assessable task will be subjected
# to automated plagiarism analysis using a tool such as the Measure
# of Software Similarity (http://theory.stanford.edu/~aiken/moss/).
#
#--------------------------------------------------------------------#


#-----Assessment Task 2 Description----------------------------------#
#
#  In this assessment you will combine your knowledge of Python
#  programming, and Graphical User Interface design to produce
#  a robust, interactive "app" that allows user to view 
#  data from a data source.
#
#  See the client's briefings accompanying this file for full
#  details.
#
#  Note that this assessable assignment is in multiple parts,
#  simulating incremental release of instructions by a paying
#  "client".  This single template file will be used for all parts,
#  together with some non-Python support files.
#
#--------------------------------------------------------------------#

#-----Set up---------------------------------------------------------#

# This section imports standard Python 3 modules sufficient to
# complete this assignment.  Don't change any of the code in this
# section, but you are free to import other Python 3 modules
# to support your solution, provided they are standard ones that
# are already supplied by default as part of a normal Python/IDLE
# installation.
#
# However, you may NOT use any Python modules that need to be
# downloaded and installed separately, such as "Beautiful Soup" or
# "Pillow", because the markers will not have access to such modules
# and will not be able to run your code.  Only modules that are part
# of a standard Python 3 installation may be used.

# A function for exiting the program immediately (renamed
# because "exit" is already a standard Python function).
from sys import exit as abort

# Some standard Tkinter functions.  [You WILL need to use
# SOME of these functions in your solution.]  You may also
# import other widgets from the "tkinter" module, provided they
# are standard ones and don't need to be downloaded and installed
# separately.  (NB: Although you can import individual widgets
# from the "tkinter.tkk" module, DON'T import ALL of them
# using a "*" wildcard because the "tkinter.tkk" module
# includes alternative versions of standard widgets
# like "Label" which leads to confusion.  If you want to use
# a widget from the tkinter.ttk module name it explicitly,
# as is done below for the progress bar widget.)
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Progressbar

# Functions for finding occurrences of a pattern defined
# via a regular expression.  [You do not necessarily need to
# use these functions in your solution, because the problem
# may be solvable with the string "find" function, but it will
# be difficult to produce a concise and robust solution
# without using regular expressions.]
from re import *

# All the standard SQLite database functions.  [You WILL need
# to use some of these in your solution.]
from sqlite3 import *


#-----Validity Check-------------------------------------------------#
#
# This section confirms that the student has declared their
# authorship.  You must NOT change any of the code below.
#

if not isinstance(student_number, int):
    print('\nUnable to run: No student number supplied',
          '(must be an integer)\n')
    abort()
if not isinstance(student_name, str):
    print('\nUnable to run: No student name supplied',
          '(must be a character string)\n')
    abort()
#--------------------------------------------------------------------#




#-----Dummy Data----------------------------------------------#
#
# Below is data that you can use in your solution for Part A to
# substitute for database data that you will access and use in Part B.


main_window = Tk()
main_window.title("MoviVision Media Movie Search")
main_window.geometry("200x200")


#-----Student's Solution---------------------------------------------#
# Put your solution below.
# As a starting point, you should consider defining functions for:
# - Cleaning Text
# - Searching Movies
# - Displaying Movie Details
# - Interface Setup for Application Branding
# - Interface Setup for Search Input
# - Interface Setup for Status Label(s)
# - Interface Setup for the Search Results area
# - Interface Setup for the Movie Details area


##### CODING AREA #####
connection = connect(database = 'movies.db')
moviesdb = connection.cursor()

#Fonts for the header and body
header_font = ('Georgia', 24)
body_font = ('Arial', 16)

#Sets the geomtry of the main window to automatically fit your screen, but will not be full screen
screen_width = main_window.winfo_screenwidth()
screen_height = main_window.winfo_screenheight()
main_window.geometry(f"{screen_width}x{screen_height}")

#changing the design/colour of the window to be visually appealling, resembling a movie clapper
main_window.config(bg='#181818')

#Gets the data from what was enter after the search button is press
def get_data():
    ##### SQL AREA #####
    
    occurrences_title = []
    #Code is used repetitively so a cleaning function is made
    def cleaning(results):
            for line in results:
                for item in line:
                #item is each individual entry we found
                    #Within this the stripped_result is cycled through each time
                    #it handles ALL html entities (even ones that do not show up in database)
                    stripped_result = sub(r'<[^>]*>','', item)
                    stripped_result = sub('&amp;','&', stripped_result)
                    stripped_result = sub('&nbsp;', '', stripped_result)
                    stripped_result = sub('&lt;', '<', stripped_result)
                    stripped_result = sub('&gt;', '>', stripped_result)
                    stripped_result = sub('&quot;', '"', stripped_result)
                    stripped_result = sub('&#39;',"'", stripped_result)
                    #Checks for duplicates as some titles have their titles in the description
                    if stripped_result not in occurrences_title:
                        occurrences_title.append(stripped_result)
    
    #Deletes previous entries
    movie_description.config(state=NORMAL)
    movie_description.delete('1.0', END)
    movie_description.config(state=DISABLED)
    movie_titles_found.delete(0, END)
    #Uses get to see what user has entered and adds spaces to make it the same as the titles
    entry_info = movie_searchbar.get()
    entry_info = entry_info.lower()
    entry_info = entry_info.strip()
    #preemptively sets perameters d = description, t = title, dir = director, act = actor
    entry_info_all = f"% {entry_info} %"
    entry_info_dt = f"%>{entry_info} %"
    entry_info_t = f" {entry_info}<%"
    entry_info_d = f"% {entry_info}%<%"
    entry_info_act_dir = f"{entry_info} %"
    entry_info_act_dir2 = f"% {entry_info}"
    entry_info_fulltitle = f"%>{entry_info}<%"
    entry_info_fulldesc = f"%>{entry_info}%<%"
    #LIKE ? allows for variables to be used makes the code look less cluttered
    results_title = moviesdb.execute(
    """SELECT title FROM movies
       WHERE LOWER(title) LIKE ?
       OR LOWER(title) LIKE ?
       OR LOWER(title) LIKE ?
       OR LOWER(title) LIKE ?""",
    (entry_info_all, entry_info_dt, entry_info_t, entry_info_fulltitle))

    #Fetches all results from the query and puts the results through the cleaning to remove HTML entities/tags
    all_results = results_title.fetchall()
    cleaning(all_results)

    #Same process as previous, goes through each table just to check titles   
    results_lead_actor = moviesdb.execute(
    """
    SELECT movies.title FROM actors
    JOIN castings ON actors.actor_id = castings.actor_id
    JOIN movies ON castings.movie_id = movies.movie_id
    WHERE LOWER(actors.full_name) LIKE ?
    OR LOWER(actors.full_name) LIKE ?
    OR LOWER(actors.full_name) LIKE ?
    OR LOWER(actors.full_name) = ?""",
    (entry_info_all, entry_info_act_dir, entry_info_act_dir2, entry_info))
    all_results_actor = results_lead_actor.fetchall()
    cleaning(all_results_actor)

    results_director = moviesdb.execute(
    """
    SELECT movies.title FROM directors
    JOIN direction ON directors.director_id = direction.director_id
    JOIN movies ON direction.movie_id = movies.movie_id
    WHERE LOWER(directors.full_name) LIKE ?
    OR LOWER(directors.full_name) LIKE ?
    OR LOWER(directors.full_name) LIKE ?
    OR LOWER(directors.full_name) = ?""",
    (entry_info_all, entry_info_act_dir, entry_info_act_dir2, entry_info))
    all_results_director = results_director.fetchall()
    cleaning(all_results_director)

    results_description = moviesdb.execute(
    """
    SELECT movies.title FROM movies
    WHERE LOWER(description) LIKE ?
    OR LOWER(description) LIKE ?
    OR LOWER(description) LIKE ?
    OR LOWER(description) LIKE ?""",
    (entry_info_all, entry_info_d, entry_info_dt, entry_info_fulldesc))
    all_results_description = results_description.fetchall()
    cleaning(all_results_description)
    
    for line in occurrences_title:
            movie_titles_found.insert(END, line)

    titles_found = len(occurrences_title)
    
    #Dynamically changes the text instructions to tell the user how many results have occurred 
    text_instructions.config(text="Number of results from search: " +str(titles_found))
    movie_scroll = scrollbar_movies.grid(row = 4, column = 1, pady=10, sticky='nes')
    movie_titles_found.config(yscrollcommand=scrollbar_movies.set)




#Function for when a listbox item (movie) is selected)    
def selected_list(event):
    #obtains the position the user has selected
    selected_item = movie_titles_found.curselection()
    #Checks if an item was actually selected
    if selected_item:
        #Gets the actual movie name the user has selected
        movie_description.config(state=NORMAL)
        movie_description.delete('1.0', END)
        selected = movie_titles_found.get(selected_item[0])
        #Changes movie titles back to contain html tags or the search will not work
        if " & " in selected:
            selected = sub(' & ',' &amp; ', selected)
        if " < " in selected:
            selected = sub(' < ',' &lt; ', selected)
        if " > " in selected:
            selected = sub(' > ', ' &gt; ', selected)
        if ' " ' in selected:
            selected = sub(' " ', ' &quot; ', selected)
        if " ' " in selected:
            selected = sub(" ' ", ' &#39; ', selected)
        selected = '%' + selected + '%'
        selected = moviesdb.execute(
            """
            SELECT movie_id FROM movies WHERE title LIKE ?
            """,
            (selected,))
        selected = selected.fetchone()
        for line in selected:
            selected = line
        #takes the movie name and obtains the description, lead actor and director.
        movie_info = moviesdb.execute(
            """
            SELECT movies.title, actors.full_name, directors.full_name, movies.description FROM castings
            JOIN actors ON actors.actor_id = castings.actor_id
            JOIN movies ON castings.movie_id = movies.movie_id
            JOIN direction ON movies.movie_id = direction.movie_id
            JOIN directors ON directors.director_id = direction.director_id
            WHERE movies.movie_id= ?""",
            (selected,))
        movie_query = movie_info.fetchall()
        info_found = []
        #Even though only title and description need cleaning all information will be cleaned for speed
        for line in movie_query:
            for item in line:
            #item is each individual entry we found
                #This isn't using cleaning function due to differing table insertions
                stripped_result = sub(r'<[^>]*>','', item)
                stripped_result = sub('&amp;','&', stripped_result)
                stripped_result = sub('&nbsp;', ' ', stripped_result)
                stripped_result = sub('&lt;', '<', stripped_result)
                stripped_result = sub('&gt;', '>', stripped_result)
                stripped_result = sub('&quot;', '"', stripped_result)
                stripped_result = sub('&#39;',"'", stripped_result)
                info_found.append(stripped_result)
        movie_description.insert(END, "Title: " + info_found[0] + "\n")
        movie_description.insert(END, "Lead Actor: " + info_found[1] + "\n")
        movie_description.insert(END, "Director: " + info_found[2] + "\n")
        movie_description.insert(END, "Description: " + info_found[3] + "\n")
        movie_description.config(state=DISABLED)
        scrollbar_descriptions.grid(row = 5, column = 1, pady=10, stick='nes')
        movie_description.config(yscrollcommand=scrollbar_descriptions.set)

##### GUI CODING AREA #####

#GUI used in the main_window
#Label in a bigger font to emphasis what it is
brand_name = Label(main_window,
                   text = "MoviVision Movie Finder",
                   font = header_font,
                   bg = '#181818',
                   fg = 'white'
                )
#Entry widget for user to enter a search term
movie_searchbar = Entry(main_window,
                        width = "75",
                        font = body_font,
                        fg = 'white',
                        bg = '#353535',
                        borderwidth=0,
                        relief="sunken",
                        )
#Button which on click does the 'get_data' function (above)
search_button = Button(main_window,
                       width = "10",
                       text = "Search",
                       font = body_font,
                       command = get_data,
                       fg = 'white',
                       bg = '#175693'
                       )
#Label instructions which change dynamically to help user
text_instructions = Label(main_window,
                         text = "Enter a search term to find movies",
                         font = body_font,
                         bg = '#181818',
                         fg = 'white'
                         )
#Listbox so that user can select each movie which appears
movie_titles_found = Listbox(main_window,
                             font = body_font,
                             width = "80",
                             height = "5",
                             fg = 'white',
                             bg = '#353535',
                             highlightthickness=0,
                             borderwidth=0
                             )
#Text box so that the description paragraph gets indented automatically (using wrap)
movie_description = Text(main_window,
                         wrap = 'word',
                         font = body_font,
                         width = "80",
                         height = "5",
                         fg = 'white',
                         bg = '#353535',
                         borderwidth=0
                            )
#Styling the scrollbar to match dark background
from tkinter import ttk

style = ttk.Style()
style.theme_use('clam')

#Configuring the style of the scrollbar

style.configure('Custom.Vertical.TScrollbar',
                background = '#353535',
                troughcolor = '#181818',
                arrowcolor = '#353535'
                )

                
#Vertical scrollbars which move their respective boxes in the y-axis
scrollbar_movies = ttk.Scrollbar(main_window,
                                 orient=VERTICAL,
                                 command=movie_titles_found.yview,
                                 style='Custom.Vertical.TScrollbar'
                             )
scrollbar_descriptions = ttk.Scrollbar(main_window,
                                   orient=VERTICAL,
                                   command=movie_description.yview,
                                   style='Custom.Vertical.TScrollbar'
                                   )

#Displaying all Tkinter GUI on a grid
#All GUI has the 'sticky' parameter for a dynamic window when resized
brand_name.grid(row=0, column = 1, rowspan=1, padx=10, pady=10, sticky='nesw')

movie_searchbar.grid(row=2, column = 1, rowspan=1, padx=10, pady=10, sticky= 'nws')
movie_searchbar.focus_set()

search_button.grid(row = 2, column = 1, rowspan = 1, padx=(20,0), pady=10, sticky='nes')

text_instructions.grid(row = 3, column = 1, padx = 10, pady = 10, sticky='nesw')

movie_titles_found.grid(row = 4, column = 1, rowspan = 1, padx = 10, pady = 10, sticky='nesw')
movie_titles_found.bind('<<ListboxSelect>>', selected_list)

movie_description.grid(row = 5, column = 1, rowspan = 1, padx = 10, pady = 10, sticky='nesw')
movie_description.config(state=DISABLED)



#Configuring each column used to have the same weight
#this configuration allows for dynamic window when resized 
main_window.columnconfigure(0, weight = 1)
main_window.columnconfigure(1, weight = 1)
main_window.columnconfigure(2, weight = 1)

main_window.rowconfigure(0, weight = 1)
main_window.rowconfigure(1, weight = 1)
main_window.rowconfigure(2, weight = 1)
main_window.rowconfigure(3, weight = 1)
main_window.rowconfigure(4, weight = 1)
main_window.rowconfigure(5, weight = 1)







main_window.mainloop()
