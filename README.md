Needle map to GameMaker converter
===

When designing intricate platforming for [guy games](http://delicious-fruit.com/), it's nice to use an editor like RMJ or Jtool to be able to quickly test and iterate on your designs. However, once you've finalized your design, it can be quite tedious to manually copy over every single object into GameMaker. I made this tool to automate that process.

The input file, an RMJ or Jtool map, is a text file containing a list of objects, each with an x coordinate, y coordinate, and type *number*. The output file, a GameMaker room, is an XML file where each object has an x coordinate, y coordinate, and name *string* (and other default values). The GUI lets you choose your input and output files, and also lets you map which object type numbers correspond to which object names in your GM project. It conveniently uses a file selection dialog to choose object names, so you don't have to type them out yourself.

For GameMaker 8.x projects, [Gmksplitter](https://github.com/Medo42/Gmk-Splitter) is used to decompose the binary project file to allow selection objects, and then to recompose the project file with the new room added.

![](http://i.imgur.com/GCyRLwe.png)
