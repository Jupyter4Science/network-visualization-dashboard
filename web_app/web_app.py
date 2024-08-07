# AUTOGENERATED! DO NOT EDIT! File to edit: ../WebApp.ipynb.

# %% auto 0
__all__ = ['accordion_welcome', 'accordion_about_dataset', 'accordion_key_features', 'welcome_next_button', 'welcome_tab',
           'authors', 'publications', 'authors_df', 'publications_df', 'author_datagrid', 'publication_datagrid',
           'datagrid', 'dropdown', 'setup_next_button', 'setup_tab', 'G_authors', 'G_publications', 'cyto', 'node_info',
           'title_label', 'graph_next_button', 'graph_tab', 'download_publications', 'download_authors', 'button_stack',
           'html', 'export_tab', 'tabs', 'update_graph', 'log_mouseovers', 'create_button', 'on_button_click',
           'on_node_mode_change']

# %% ../WebApp.ipynb 1
import pprint
from fastcore.basics import patch
import networkx as nx
import ipywidgets as widgets
import ipycytoscape
from ipycytoscape import CytoscapeWidget
from IPython.display import display, clear_output, HTML
from ipywidgets import Output, link, jslink
from pprint import pformat
import pandas as pd
from ipydatagrid import DataGrid
from ipywidgets import Tab, Stack
from itertools import product
import ipyvuetify as v
import base64

# %% ../WebApp.ipynb 2
from preprocessing.objects import create_objects

# %% ../WebApp.ipynb 3
from preprocessing.author import Author

# %% ../WebApp.ipynb 4
########### FIRST TAB #############

# Create accordion widgets for the "Welcome" tab
accordion_welcome = widgets.Accordion(children=[
    widgets.HTML("Welcome to the Agent-Based Modeling Visualization Web App! This interactive tool provides a dynamic way to explore and analyze code sharing and model documentation practices in individual-based and agent-based models since the inception of the field in the 80's. This tool allows user to explore the properties of and relationships among 7500 hand picked articles describing IBMs or ABMs across awide range of research domains up to the year 2018.")
])

accordion_welcome.set_title(0, 'Welcome!')
accordion_welcome.selected_index = 0

accordion_about_dataset = widgets.Accordion(children=[
    widgets.HTML("1. Welcome Tab: Begin your journey by visiting the Welcome tab. Here, you'll find essential information about the web app's features and functionalities. <br> 2. Setup Tab: Switch to the Setup tab to access the dataset configuration options. <br> 3. Graph Tab: Move on to the Graph tab to visualize the network graph representation of authors/nodes and their collaborative connections. Hover over nodes to view author information and click to explore further. <br> 4. Export Tab: In the Export tab, you can choose to download the graph visualization in either Excel (XLSX) or CSV format. While the download functionality is under development, the dropdown menu allows you to select your preferred file format")
])
                
accordion_about_dataset.set_title(0, 'How to Use the Web-App')

accordion_key_features = widgets.Accordion(children=[
    widgets.HTML("Key Features of the Web App: <br> - Network Visualization: Gain insights into collaboration patterns among authors using an interactive network graph. The graph highlights relationships based on shared publications. <br> - Dynamic Exploration: Hover over nodes for author details, click to reveal deeper connections, and analyze the co-authorship network.<br> - Download Options: The 'Export' tab allows you to choose your preferred file format for downloading the network graph visualization. While the functionality is currently static, it will soon enable you to save your insights for further analysis.")
])
accordion_key_features.set_title(0, 'Key Features of the Web App')

# Create a next button
welcome_next_button = widgets.Button(description='Next', layout=widgets.Layout(width='auto', background_color='lightblue', color='black'))

# Create Welcome tab content with accordion widgets
welcome_tab = widgets.VBox([
    accordion_welcome,
    accordion_key_features,
    accordion_about_dataset,
    welcome_next_button
])

# %% ../WebApp.ipynb 6
authors, publications = create_objects('Catalogdatabase-till2018b.xlsx', n=50)

# %% ../WebApp.ipynb 7
## Create a list of dictionaries containing author information
## Create a DataFrame from the author data
authors_df = pd.DataFrame([author.__dict__ for author in authors])
publications_df = pd.DataFrame([publication.__dict__ for publication in publications])

# %% ../WebApp.ipynb 8
## Create the datagrid and display it
author_datagrid = DataGrid(authors_df, editable=False, layout={"height": "200px", "width": '400px'})
publication_datagrid = DataGrid(publications_df, editable=False, layout={"height": "200px", "width": '400px'})
datagrid = widgets.Stack(children = [author_datagrid, publication_datagrid], selected_index=0)

# %% ../WebApp.ipynb 11
########### SECOND TAB #############

# Dropdown widget to switch between types of nodes
dropdown = widgets.Dropdown(options=[('Authors'), ('Publications')], value='Authors', description='Node Mode:')

jslink((dropdown, 'index'), (datagrid, 'selected_index'))

# Create a next button
setup_next_button = widgets.Button(description='Next', layout=widgets.Layout(width='auto', background_color='lightblue', color='black'))

# Add the next button to the setup_tab
setup_tab = widgets.VBox([datagrid, dropdown, setup_next_button])

# %% ../WebApp.ipynb 19
########### CREATE AUTHOR NETWORK ###############
##%time
#### Step 1: Making sure correct matches are found between authors ####

# Create the graph
G_authors = nx.Graph()

# Define the graph with authors as nodes
#G_authors = nx.Graph()

# Add nodes to the graph
for author in authors:
    G_authors.add_node(author, tooltip=author.__repr__())

# Add edge between shared publications
for index_a in range(len(authors)):
    for index_b in range(index_a + 1, len(authors)):
        author_a = authors[index_a]
        author_b = authors[index_b]

        #### WORK?? Should be a publication list
        common_publications = list(set(author_a.publications).intersection(author_b.publications))
        if common_publications:
            # Add the weighted edge to the graph
            
            ##### Can we have both object and weight??
            G_authors.add_edge(author_a, author_b, weight = len(common_publications)) #, weight = len(common_publications)

# %% ../WebApp.ipynb 22
############ CREATE PUBLICATION NETWORK ###########
## %time 
# Define the graph with publications as nodes
G_publications = nx.Graph()

for publication in publications:
    G_publications.add_node(publication, tooltip=publication.__repr__())
    

for index_a in range(len(publications)):
    for index_b in range(index_a + 1, len(publications)):
        publication_a = publications[index_a]
        publication_b = publications[index_b]

        common_authors = [ author_i for author_i , author_j in product(publication_a.authors, publication_b.authors) if author_i.same_name(author_j)]
        if common_authors:  
            G_publications.add_edge(publication_a, publication_b, weight = len(common_authors))
            ##### Can we have both object and weight??
            #for common_author in common_authors:
            #    print(common_author)
            #    G_publications.add_edge(publication_a, publication_b, object = common_author) #, weight = len(common_publications))

            #Comment out this part later
            # print(f"Match found between {publication_a} and {publication_b}")
            # print(f"Matching Authors: {common_authors}")
            # print(f"Weighted Edge: {publication_a} - {publication_b} (Weight: {len(common_authors)})")
            # print(" ")

# %% ../WebApp.ipynb 25
# Create Output widget to show node information

#out = widgets.Output()

# for whatever reason, cytoscape doesn't render if it is a child of the stack
# network_stack = widgets.Stack([author_network, publication_network])
cyto = ipycytoscape.CytoscapeWidget()
cyto.graph.add_graph_from_networkx(G_authors)

def update_graph(change):
    selected_mode = dropdown.value
    if selected_mode == 'Authors':
        cyto.graph.clear()
        cyto.graph.add_graph_from_networkx(G_authors)
        #display(cyto)
    if selected_mode == 'Publications':
        cyto.graph.clear()
        cyto.graph.add_graph_from_networkx(G_publications)
        #display(cyto)

# Create a widgets.Textarea to display author information
node_info = widgets.Textarea(
    value='',
    disabled = True,
    placeholder='Hover over a node to see author information.',
    layout=widgets.Layout(width='50%', height='200px', editable=False)  # Adjust width and height as needed
)

# Create a label for the title with big, bold, and centered style
title_label = widgets.HTML(
    value = "<h2>Network Graph</h2>"
)

_graph_tab = widgets.HBox([node_info, (cyto)], layout=widgets.Layout(width='100%', height='100%', align_items='stretch'))
graph_next_button = widgets.Button(description='Next', layout=widgets.Layout(width='auto', background_color='lightblue', color='black'))
graph_tab = widgets.VBox([_graph_tab, graph_next_button])

# %% ../WebApp.ipynb 27
def log_mouseovers(node):
    node_info.value = node['data']['id']

# Attach the mouseover and click callbacks to the Cytoscape widget
cyto.on('node', 'mouseover', log_mouseovers)

# %% ../WebApp.ipynb 29
def create_button(filename):

    with open(filename+'.csv', 'r', encoding='utf-8') as file:
        res = file.read()
    
    b64 = base64.b64encode(res.encode())
    payload = b64.decode()
    
    button_template = '''<html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    </head>
    <body>
    <a download="{filename}.csv" href="data:text/csv;base64,{payload}" download>
    <button class="p-Widget jupyter-widgets jupyter-button widget-button mod-success">{filename}.csv</button>
    </a>
    </body>
    </html>
    '''
    
    download_text = button_template.format(payload=payload,filename=filename)
    download_button = widgets.HTML(download_text)
    return download_button

# %% ../WebApp.ipynb 30
download_publications = create_button('publications')
download_authors = create_button('authors')

# %% ../WebApp.ipynb 31
######### EXPORT TAB ##########
button_stack = Stack(children = (download_publications, download_authors))
html = widgets.HTML("<p>For more information about how the database was created and how model descriptions were categorized, visit <a href='https://doi.org/10.1016/j.envsoft.2020.104873' style='color: blue;'>On code sharing and model documentation of published individual and agent-based models</a>.</p>")
html.style
export_tab = widgets.VBox(children=[button_stack, html])

# %% ../WebApp.ipynb 33
# Create the Tabs widget with Welcome, Setup, Graph, and Export tabs
tabs = widgets.Tab(children=[welcome_tab, setup_tab, graph_tab, export_tab])
tabs.set_title(0, 'Welcome')
tabs.set_title(1, 'Setup')
tabs.set_title(2, 'Graph')
tabs.set_title(3, 'Export')

# %% ../WebApp.ipynb 35
# Create a next button
def on_button_click(button):
    # Switch to the second tab (index 1) when the button is clicked
    tabs.selected_index = tabs.selected_index + 1

welcome_next_button.on_click(on_button_click)
setup_next_button.on_click(on_button_click)
graph_next_button.on_click(on_button_click)

# %% ../WebApp.ipynb 36
# Temporary download function:
def on_node_mode_change(change):

    title = "Download CSV file"
    selected_mode = change['new']
    if selected_mode == 'Authors':
        setup_next_button.disabled = True
        cyto.graph.clear()
        cyto.graph.add_graph_from_networkx(G_authors)
        button_stack.selected_index = 0
        tabs.selected_index = 2
        setup_next_button.disabled = False
    if selected_mode == 'Publications':
        setup_next_button.disabled = True
        cyto.graph.clear()
        cyto.graph.add_graph_from_networkx(G_publications)
        button_stack.selected_index = 1
        tabs.selected_index = 2
        setup_next_button.disabled = False
        

# Attach the event handler to the next button
dropdown.observe(on_node_mode_change, names='value')

# %% ../WebApp.ipynb 37
# Make sure that all the setup things get triggered
dropdown.select = 'Author'
