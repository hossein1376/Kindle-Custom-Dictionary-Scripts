# Kindle Custom Dictionary Scripts

Here you can find scripts to automate the preparation of the dictionary data. This is a sub-project of [English-Persian Kindle Custom Dictionary](https://github.com/hossein1376/English-Persian-Kindle-Custom-Dictionary).  
Scripts are written in Python and you can modify them based on your needs and database.

## content.py

The data will be transformed into multiple HTML files based on the given template of [official Amazon guide](https://kdp.amazon.com/en_US/help/topic/G2HXJS944GL88DNV).

When you run the script, it will ask for the source file. Both the script and the source file need to be in the same folder.  
I had a .txt file so I proceeded with that, you may need some modifications based on your situation. As long as the source file is iterable and each entry is on its own seprate line, it should work.

In the script body, you can change the number of entries per each HTML file (`counter` variable value). I suggest to choose a number that keeps the size of each file under 5mb.  
Also, you can hardcode the input and output files path.

What the code does is essentially, it reads each line of the source file, detects the main term (entry) and all of its inflections which all are separated with a `|` in my case (ofc you can change it). The term and the definitions are seprated by a tab character, so I introduced the `break_point` variable to let the script know when to stop looking for inflections.  
The code calls multiple functions that are defined at the top, most of these are the HTML code that the data is being parsed into.

## content_rtl.py

It's pretty much same as the content.py file, with the exception that it is intended for RTL language.  
Since .mobi format has issues with RTL, as in the words are displayed in reverse order, so I preemptively reversed the words' order.

Example:
Usual text: `سلام من حسین هستم`  
What will script will do to it: `هستم حسین من سلام`  
What will kindle show: `سلام من حسین هستم`

There is the possibility of issues with this method, so you may need to consider beforehand or modify the script (or your data).

## opf.py

You will need an .opf file to create your dictionary. Run this script and provide the requested information. You can find the ISO 639-1 codes [from here](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes).  
That's pretty much all to it. Put this file in the same folder of HTML file(s) and open it with the Kindle Previewer.  
Congratulations!
