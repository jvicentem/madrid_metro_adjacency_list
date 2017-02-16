# madrid_metro_adjacency_list
The purpose of this project is to generate an adjacency list from the metro system serving the city of Madrid, capital of Spain. 

Version with line colors and names plus travel time between stations: https://github.com/jvicentem/madrid_metro_adjacency_list/releases/tag/v3.2.1

Simple version (only vertices): https://github.com/jvicentem/madrid_metro_adjacency_list/releases/tag/v1.0.0

Gephi's nodes and edges csv files:  https://github.com/jvicentem/madrid_metro_adjacency_list/releases/tag/v3.2.3 -> The ids of the stations are real CRTM station ids. Weight = 1 / travel_seconds

There's a Gephi's project file too. I strongly recommend to install "Give Color To Edges" plugin so you can paint the edges with the color of each Metro line. 

The size of vertix: the higher its degree is, the bigger the vertix is.
According to the size of edges: higher weight (faster time between two stations) equals thicker edges.
About the color of each vertix: the higher its closeness centrality value is, the darker it is.
