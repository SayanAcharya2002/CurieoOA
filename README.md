# CurieoOA
The solution works by extending the idea of a sparse table. It is a fully online solution that serves the queries as they come without making any extra assumptions about the length of the queries, the maximum number of queries, or the number of timestamps. Although, a sparse table is generally considered a fixed data structure, here it is modified to be able to add new entries at the back of the table, making the whole data structure online. On top of that, the queries are run iteratively. Therefore, no extra recursive overhead is applied. So the number of operations done and the total runtime are very optimized.

As the updates are only of appending type and no changes are made to the past data, we can use a modified sparse table for this. 

The QueryHandler is built in a way such that it keeps a running sparse table for each logtypes to better serve query 4 and a global sparse table for all the information to better serve query 3.

As new logs come, they are inserted into the sparse table and the new entries in the sparse table are calculated that would be valid for the new length of the log array. For this purpose, a 2d array is used of the format array[number_of_bits][number_of_elements]. Whenever the number of elements crosses the bit-threshold, a new entry is added in the 1st dimension to support longer range queries. 

For example:
l=[1] will only require 1 bit, l=[1,2] will require 2 bits, l=[1,2,3] 2 bits, l= [1,2,3,4] 3 bits. This way, the first dimension of the sparse table is increased.

Afterwards, for min/max simple, sparse table queries are made and for summation, binary lifting technique is used on sparse table. 

If queries are made when no logs are available then (0.0,0.0,0.0) is returned.

## Working idea
   For each logtype a QueryHandler object is kept that is used to answer queries of that logtype. A python dict is utilized for this feature. Other than this, a global QueryHandler object is kept that stores the information of all the logs. This helps to answer queries of type 3. 

## Complexity classes
1. Time Complexity
   1. To service each query of type 3 and 4, upperbound or lowerbound functions are applied on the timestamps array which requires O(logn) time. Then calculation of the min/max requires O(1) time and mean calculation requires O(logn) time. Therefore, in total it requires O(logn) time. [n=number of entries of that logtype {worst case: total number of queries}]
   2. To service query 2, it gives the pre-compiled globalAns value. Therefore, takes O(1) time.
   3. To service query 1, it has to add the entry to the table which requires setting up the sparsetable correctly. Therefore, a total of logn entries need to be entered in the full table. This takes O(logn) time. [n=number of entries of that logtype {worst case: total number of queries}]

2. Space complexity: The space complexity of this solution is O(nlogn) as the sparse table has to be stored which has logn lists each having a maximum of n entries. [n=number of entries of that logtype {worst case: total number of queries}]


## Brief overview of the classes and functions
1. QueryTuple: It is a custom made dataclass that holds the min, max, sum values for the ranges. It has a combine function to combine the results with other QueryTuple objects and a str representation for formatted output
2. QueryHandler: This class handles the queries and saves the log information in the form of a sparse table. Each QueryHandler class stores the information of a specific log type.
   1. Data members:
      1. timeStamps: This list stores all the timestamps of the given log type. It is used for finding out the effective query indices of the before and after type query
      2. globalAns: This QueryTuple holds the min, max, sum for the whole range. Therefore, for "2 logtype" queries the answers can be given instantly without requiring any range search operation
      3. bitwiseArrays: This is a list of lists that is simply the sparse table. This 2d matrix is of the size number_of_bits x number_of_elements. The number of bits is log(number of elements). It increases in size depending on the number of elements inserted. The idea is that the number of bits will be such that 2**number_of_bits > number_of_elements. This way, ranges of length 2\**k can be searched effectively. With each new entry, corresponding array entries are calculated such that the new whole range is covered. Each entry only changes the number of rows in the bitwiseArrays by a maximum of 1 time.
   2. Methods:
      1. addEntry: This function adds an entry to the sparsetable, timeStamps array, and updates the globalAns.
      2. getWholeRange: Returns the ans to the "2 logtype" query
      3. __query_internal_range: This is an internal function supposed to be used as the range query function. For the min/max, it simply uses the overlapping range combination technique that is famously used in sparse tables. For the summation, it starts adding segments until the full length is reached. This technique is taken from the famous Binary Lifting technique. The whole complexity of this process is O(logN). [N= number of entries in the QueryHandler {worst case: total number of queries}]
      4. queryBefore: It calculates the valid range to query given a timestamp t. The valid range is the range of timestamps that comes before the timestamp t. It uses lowerbound function's idea internally. Therefore, it can handle multiple entries at the same timestamp. When no valid range is found, it returns the default (0.0,0.0,0.0) value.
      5. queryAfter: It calculates the valid range to query given a timestamp t. The valid range is the range of timestamps that comes after the timestamp t. It uses upperbound function's idea internally. Therefore, it can handle multiple entries at the same timestamp. When no valid range is found, it returns the default (0.0,0.0,0.0) value.


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
docker run app 
```
