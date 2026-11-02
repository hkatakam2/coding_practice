# question
There’s a row of seats. Each is either occupied (1) or empty (0). I pick one empty seat to sit in. Distance between two seats is the difference of their indices. I want the seat where the nearest occupied seat is as far away as possible, and I return that distance.

# clarify
1. is there atleast 1 person and 1 empty seat? yes
2. can i sit at either end of row? yes
3. is distance just abs(index difference)? yes
4. is the imput large? upto 20K seats; O(n^2) is risky

# ideas
