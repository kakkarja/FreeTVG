# You have to install FPDF for this module to work.
# You can isntall from https://github.com/reingart/pyfpdf
# Copyright © Mariano Reingart

from fpdf import FPDF 
import time

class Pydf(FPDF):
    # Setting the header and footnote in pdf.
    
    def __init__(self, title):
        super().__init__()
        self.title = title
        self.filename = f'{title}.pdf'
        
    def header(self):
        self.set_y(10)  
        self.set_font('Arial', 'B', 15)  
        self.cell(0, 7, self.title, 1, 0, 'C')
        self.ln(10)
        
    def footer(self):  
        self.set_y(-10)  
        self.set_font('Arial', 'I', 8)
        self.cell(0, 7, f'{time.ctime()}', 'T', 0, 'L')
        self.cell(0, 7, f'{str(self.page_no())} / {"{nb}"}', 'T', 0, 'R')
         
        
if __name__ == '__main__':
    # For testing the Pydf if it is working.
    
    import os
    
    if 'tuto21.pdf' in os.listdir():
        os.remove('tuto21.pdf')
        print('Done')
        
    pdf = Pydf('tuto21')
    pdf.add_font('Corbel', '', r"c:\WINDOWS\Fonts\corbel.ttf", uni=True)
    pdf.alias_nb_pages() 
    pdf.add_page() 
    pdf.set_font('Corbel', '', 12) 
    for i in range(1, 54): 
        pdf.cell(0, 5, f'Printing line number {str(i)}', 0, 1) 
    pdf.output(pdf.filename, 'F') 
    
    #Unblock below script to delete the pdf.
    #
    #if 'tuto21.pdf' in os.listdir():
    #    os.remove('tuto21.pdf')
    #    print('Done')


