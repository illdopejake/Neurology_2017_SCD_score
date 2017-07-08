# Neurology_2017_SCD_score
Command-line executable script to convert itemized GDS responses into SCD and affective variables
You feed it your spreadsheet with itemized GDS scores, it will convert those into factor scores as
described in the [yet to be published] Vogel et al. 2017 Neurology. [Link coming soon]

# Dependencies
Python
Pandas library

>>>But how do I get that! I don't know python! Or computers!<<<<
No worries. Here is how to get the stuff you need to run this script.

1. If you are working with a mac or on a cluster, you may already have python installed. Open a command line and type which python. 
If you get a response pointing to an existing python path, you can skip to step 3.

2. If you don't have python, its a breeze to install. You can download it here https://www.python.org/downloads/
Don't worry, it won't hurt your computer. 
Alternatively, download python through anacaonda distribution, here: https://www.continuum.io/downloads
Anaconda is perhaps a bit more user-friendly an already comes with the pandas library
Either way you go, make sure do use Python 3 (3.x.x). The newest stable version should be good enough.

If you don't have write access to your system and your system does not have Python, talk to your sys admin for help.
If you don't have write access to your system and your system does have Python, do this: 
Python: http://thelazylog.com/install-python-as-local-user-on-linux/
Anaconda: https://www.continuum.io/blog/developer-blog/python-packages-and-environments-conda section Creating and Using Environments

3. Unless you used Anaconda, python does not necessarily come with the pandas library (at least it didn't used to).
If you don't have pandas, its simple to install. 
Open a command window
If using Python, type: pip install pandas
Press enter. That's it.
Note, if you're working on a cluster, you may have to instead type: pip install --user pandas
anaconda should already have python, but if not, type: conda install pandas

# Accessing the script
This repository contains a script that does all the legwork, a script that executes the function from a command line (the wrapper), 
and a spreadsheet containing information necessary for the factor scores. 

If you have git, just clone the repository
If not, you can download it manually off of the site and save it onto your computer

# Using the script
Open a command line. Navigate to the directory where you saved this repository.
GDS_SCD_conversion_wrapper.py is the actual command-line function you will use to execute the script.

To understand how the script works, just type: python GDS_SCD_conversion_wrapper.py
If you want reliable results, please make sure you read and understand the documentation this provides.
For a short prompt to remind you of the options, just type python GDS_SCD_conversion_wrapper.py --help

Example usage:
python GDS_SCD_conversion_wrapper.py /User/jakevogel/GDS.xlsx 3 -out ../tmp/ -header True -encode True

This will open spreadsheet /User/jakevogel/GDS.xlsx, and will look for the first GDS question at the 4th column.
This will also tell the script to output the scores to ../tmp, that the spreadsheet does contain column names, and that I want the
script to automatically invert several GDS questions (because we want the depressed answers =1).

# Troubleshooting
If the script errors:
    does it say something about not being able to find pandas? Then install pandas, see dependencies above
    did you make sure that col_start is actually the column number -1? So the first column is 0, second is 1, etc.
Otherwise, 
    send me an email.

If your values are unusual (i.e. many factor values >2 or 3), you probably did something wrong with the "encoding" argument. Make sure icols corresponds to the correct columns, or make sure -encode is set to True if you want to change the value (default is False, assumes
GDS questions are already coded so that depressed = 1).

Don't hesitate to send me an email with your input spreadsheet and the explicit error message you got. I will be more than happy to help
and I won't judge you <3

