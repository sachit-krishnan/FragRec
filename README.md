# FragRec: A Cologne & Perfume Recommender
This repository contains an API that enables a user to get cologne and perfume recommendations based on their desired fragrance attributes. The recommendations are made from a pool of 533 fragrances whose information was acquired from Fragrantica.com via web crawling and scraping using Python. The acquired data was processed using custom Python data structures 'Fragrance' and 'Graph'; this process allowed for efficient user input attribute mapping with the perfume data. The user interacts with the program and gets their fragrance recommendations on an HTML page. The relay of input and output data between the backend and the HTML page is done via the Python library 'flask'. Try out the program to know which perfume suits you! 

## Python Library Dependencies
- flask
- splinter
- BeautifulSoup
- time
- webdriver_manager
- requests
- csv
- json
- selenium
- werkzeug
- random

All the above libraries can be installed by running ``pip install <library_name>`` in the terminal.

## Program Files & Directories
1. ``classes.py``: Python file containing all the class definitions used in the program.
2. ``scraping.py``: Python file containing all the functions pertaining to the crawling and scraping of Fragrantica pages.
3. ``datahandling.py``: Python file containing all the functions pertaining to caching, accessing, and processing of the data.
4. ``main.py``: The main control file making all the necessary function calls for the proper running of the program.
5. ``graph_read.py``: Standalone Python file to read the graph from the JSON cache ``fragraph.json``.
5. ``data``: Directory containing the cached data and graph.
    - ``PerfumesFinal.json``: JSON cache containing the processed perfumed data acquired via web crawling and scraping.
    - ``fragraph.json``: JSON cache containing the graph information (node and edge information).
6. ``templates``: Directory containing the HTML template to be rendered using flask
    - ``userinput3.html``: HTML template to be rendered to the user
7. ``complete.ipynb``: Jupyter Notebook containing the entire program code. (To be used alternatively to the .py files.)

## Program Execution
1. The program can be run via command line by navigating to the program directory and executing the command ``python3 main.py``.
2. Once the program is run, the user will be shown the IP address of the local host in the Terminal. The user is then requested to open a web browser of their choice and navigate to the page by adding `/inputPage` to the local host's address.
3. Upon arriving at the Fragrance Recommender page, the user is encouraged to select the fragrance attributes of their choice and click the `Submit` button. The user is also encouraged to use the `Jump to:` hyperlinks to navigate the page seamlessly.
4. Upon clicking `Submit`, the user is given a list of recommendations with a comprehensive account of each fragrance. If the user wishes for another recommendation, they may submit a new form; else they may close the browser. Upon closing the browser, ``Ctrl + C`` (or ``command + C`` on Mac decives) in the Terminal will end the program.

Alternately, the user may run the program on Jupyter Notebook.
