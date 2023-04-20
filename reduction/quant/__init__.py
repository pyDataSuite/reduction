"""
The quantization package is used to reduce the amount of data sent to
a plot without any visual degredation in quality. It has first-class support
for matplotlib plotting, and provides a variety of classes which wrap around
different types of plots.

Using this package, you can generate a performant, interactive plot of 
100 million data points in just a few seconds using most hardware. Unlike
Holoviews or Datashaders, all the data is plotted as a real dataset.

Data produced by this package will be affected by quantization and discretization
errors. The magnitude of which depend on how the classes are configured.
"""