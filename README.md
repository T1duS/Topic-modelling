# Topic-modelling
Gets a current topic based on captions using tf-idf.

# Using
  
`git clone https://github.com/T1duS/Topic-modelling.git`    
`python3 main.py input.txt`  
  
If you want better results, change the corpus.txt file and run     
`python3 main,py input.txt -R`      
-R restarts the preprocess  

<hr>

Here is a random news item from google and its output

# Sample input
Mumbai/Bengaluru: 

Demand for physical gold was robust in India this week as consumers stepped up purchases during the wedding season after domestic rates slipped to a near six-week trough, while gains in global prices weighed on bullion's appeal in other Asian hubs. Demand in India, the second biggest gold consumer after China, usually picks up towards the end of the year going into the wedding and festival season.

The current price level was attracting both jewellers and retail consumers, said Daman Prakash Rathod, a director at MNC Bullion, a wholesaler in Chennai.

Local gold prices were trading near their lowest since October 1, as an appreciation in the rupee made buying overseas cheaper.

# Sample output
Possible topics are ---
gold
prices
india
bullion
consumers
