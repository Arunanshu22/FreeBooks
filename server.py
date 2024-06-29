from flask import Flask, render_template, request, redirect, url_for
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium import webdriver


app = Flask(__name__)
options = Options()
options.add_argument("--headless")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=options)

# Global variable to store the book name
book_name = None

@app.route('/')
def index():
    return render_template('search_book_name.html')

@app.route('/set_book', methods=['POST'])
def set_book():
    global book_name
    book_name = request.form.get('book')
    return redirect(url_for('show_book'))

@app.route('/show_book')
def show_book():
    if book_name:
        pdfs = []
        book = book_name + ' filetype:pdf'
        url = f"https://www.google.com/search?q={book}"
        print(url)
        driver.get(url)
        elements = driver.find_elements("xpath","//a[@jsname='UWckNb']")
        for i, element in enumerate(elements, 1):
            href = element.get_attribute('href')
            if href.endswith('pdf'):
                pdfs.append(href)
        # return pdfs
        # return redirect(url_for('new_page'))
        enumerated_pdfs = list(enumerate(pdfs, 1))
        print(enumerated_pdfs)
        return render_template('Results.html', enumerated_pdfs=enumerated_pdfs)
    else:
        return "No book name has been set."
    

@app.route('/reader')
def reader():
    return render_template('readerTrial.html')

@app.route('/results')
def results():
    # Render the results page template
    return render_template('results.html')

if __name__ == '__main__':
    app.run(port=5000)
