# madrid_metro_adjacency_list
The purpose of this project is to create an adjacency list from the metro system serving the city of Madrid, capital of Spain. 

I'd like to thank Jesús Sánchez-Oro and Daniel de Santos Sierra for their help in this project.

Version with line colors and names plus travel time between stations: https://github.com/jvicentem/madrid_metro_adjacency_list/releases/tag/v3.2.1

Simple version (only vertices): https://github.com/jvicentem/madrid_metro_adjacency_list/releases/tag/v1.0.0

Gephi's nodes and edges csv files: Ids are real CRTM station ids. Weight = 1 / travel_seconds


I'm currently working on a graph analysis of Madrid Metro network so checkout branch "new-analysis" and visit the Jupyter Notebook on folder "analysis". 
There's a Gephi's project file too. I strongly recommend to install "Give Color To Edges" plugin so you can paint the edges with the color of each Metro line. 

The size of vertix: the higher its degree is, the bigger the vertix is.

According to the size of edges: higher weight (it takes less time to travel between two stations) -> thicker edges.

About the color of each vertix: the higher its closeness centrality value is, the darker it is.

![Madrid Metro Viz](https://github.com/jvicentem/madrid_metro_adjacency_list/raw/master/analysis/with-coordinates.png)


