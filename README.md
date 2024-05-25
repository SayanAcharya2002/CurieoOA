# CurieoOA
The solution works by extending the idea of a sparse table. 

As the updates are only of appending type and no changes are made to the past data, we can use a modified sparse table for this. 

The QueryHandler is built in a way that, it keeps a running sparse table for each logtypes to better serve query 4 and a global sparse table for all the information to better serve query 3.

As new logs come, they are inserted into the sparse table and the new entries in the sparse table are calculated that would be valid for the new length of the log array. For this a 2d array is used of the format array[number_of_bits][number_of_elements]. Whenever the number of elements crosses the bit-threshold, a new entry is added in the 1st dimension to support longer length queries. 

For example:
l=[1] will only require 1 bit, l=[1,2] will require 2 bits, l=[1,2,3] 2 bits, l= [1,2,3,4] 3 bits. This way, the first dimension of the sparse table is increased.

Afterwards, for min/max simple, sparse table queries are made and for summation, binary lifting technique is used on sparse table. 

This ensures O(logn) search time for each query. On top of that, to find the correct range, upperbound and lowerbound functions are applied on the timestamps array.

This too makes sure that the time complexity remains O(logn) for each query. [n=number of logs]

Space complexity of this solution is O(nlogn) as the sparse table has to be stored.

If queries are made when no logs are available then (0.0,0.0,0.0) is returned.

Instructions to run:
```
python main.py [Optional:input.txt] [Optional:output.txt]
```
A sample_maker too is given that generates random testing data.
To run it, change the hyperparameters within the file and then:
```
python sample_maker.py
```
The docker image is built with:
```
docker build -t app . 
```
The docker solution can be run with 
```
docker build -t app . 
```
