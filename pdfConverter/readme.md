## pdfplumber
#### 1. pdf parsing package pdfplumber:
    (1) For any given PDF page, find (a) clearly defined lines and/or (b) lines implied by word alignment on the page.
    (2) Combine overlapping or almost overlapping lines.
    (3) Find the intersection of all these lines.
    (4) Find the finest-grained set of rectangles (ie cells) that use these intersections as their vertices.
    (5) Group consecutive cells into the table.
    
#### 2. Extraction process:
    (1) Analyze the words in the pdf, and the word objects contain coordinate information.
    (2) Use the table title and the next table title to locate the table range
    (3) Find all the words contained in the table in the pdf, and find the words corresponding to the table header and the table content.
    (4) Use the coordinate position of the word in the header and the coordinate position of the row to get the cell, and mark the word contained in each cell.
    (5) Combine the words of the cells into a structured data DataFrame.
    
## paddleocr
#### 1. Analysis process:
    (1) Convert the uploaded pdf into a page image through fitz and create a new file, and store all the pictures in sequence
    (2) Use paddleocr to parse the image to generate a list dictionary containing the coordinates of the four corners of the text block, text content, and accuracy
    (3) Extract the table header from the list dictionary and store it in a dictionary
    (4) Determine which column the table belongs to by comparing the content of the table with the left-aligned coordinates of the table header, and store the information in the dictionary
    (5) Combine the two dictionaries of the table and the header, synthesize the text block into a structured data DataFrame, and use Pandas to output it as excel
