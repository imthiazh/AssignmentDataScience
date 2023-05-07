# Task 1

This is a Python script for extracting text and textual properties such as font size and style, from a PDF document. The script is implemented using PyMuPDF (fitz), which provides a way to extract text, font information, and other layout information from PDF documents. The script can be useful in a variety of applications such as data analysis, natural language processing, and information retrieval.

Requirements
The script requires Python 3.x and the following packages:

fitz (PyMuPDF)
pandas
requests
Usage
To use the script, you can import the functions fonts(), font_tags(), headers_para() and remove_empty() and use them separately, or use the script as is to generate an HTML-formatted text file from a PDF document.

The function fonts() takes a PDF document object as input and returns a tuple with two values: a sorted list of fonts used in the document with their usage count, and a dictionary of font styles found in the document.

The function font_tags() takes the output of the fonts() function as input, and returns a dictionary that maps font sizes to HTML tags. For example, if the most frequently used font in the document has a size of 12, the corresponding tag would be <p> for font sizes smaller than or equal to 12, <h1> for font sizes greater than 12, and <s1> for font sizes smaller than 12.

The function headers_para() takes a PDF document object and the output of the font_tags() function as input, and returns a list of text strings with corresponding HTML tags for each element (paragraph, header, subheader) in the document.

The remove_empty() function takes a dictionary as input and removes empty elements from it.