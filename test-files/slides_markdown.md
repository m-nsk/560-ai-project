# **8 Approximation Algorithms**
### Approximation algorithms don’t always return an optimal solution, but their solutions are often close to optimal. They always run in polynomial time, and they are often relatively simple. (Again, in this chapter, exact running times won’t be essential for our purposes.)




### A α-approximation algorithm is a polynomial-time algorithm that always returns a solution whose value ALG is within a factor α of the optimal value OPT. In other words, for minimization problems, there exists α ≥ 1 such that ALG satisfies the following on every instance: OPT ≤ ALG ≤ α · OPT . The approximation ratio of an algorithm is the smallest α such that the algorithm is an α - approximation algorithm. Proving that an α -approximation algorithm is “correct” means showing that the algorithm satisfies ALG ≤ α · OPT on every instance. (For maximization problems, we flip the inequalities above, so α ≤ 1 and we want OPT ≥ ALG ≥ α · OPT.)
## **8.1 Vertex Cover**



### Algorithm: Set S = ∅ . If G has an edge e = {u, v}, add both endpoints of e to S, and remove u and v from G . (Note that when we remove a ver- tex from a graph, we also remove all edges incident to the vertex.) Repeat this process until G has no edges and return S . Correctness: Notice that the edges considered by the algorithm form a matching M, so | ALG | = 2 · 45


-----

### |M | . Furthermore, each vertex in OPT can cover at most one edge in M, so | OPT | ≥|M | . Thus, | ALG | = 2 · |M | ≤ 2 · | OPT | .
## **8.2 Load Balancing**
### Scheduling is a rich topic with many applications. In a typical scheduling problem, there are n jobs and m machines, and we need to assign each job to a machine. Every job has a length, and the load on a machine is the sum of the lengths of the jobs assigned to that machine. The makespan of an assignment is the maximum load created by that assignment. Algorithm: The algorithm is greedy: iterate through the jobs (in any order), assigning each one to the machine with the smallest load so far.


### Correctness: Suppose ALG achieves a makespan of T, the load of i ∈ [ m ] is T, and k was the last job assigned to i . When ALG assigned k to i, i had the smallest load. This means the load on every machine is at least T − ℓ [ k ], so [�] [n] j =1 [ℓ] [[] [j] []] [ ≥] [m] [(] [T][ −] [ℓ] [[] [k] []). Rearranging yields]

### *T ≤*

### � n j =1 [ℓ] [[] [j] []] + ℓ [ k ] . *m*

### Now let T [∗] denote the optimal makespan. Since the average load in any assignment is [�]

### Now let T [∗] denote the optimal makespan. Since the average load in any assignment is [�] j [ℓ] [[] [j] []] [/m] [,] we have T [∗] ≥ [�] j [ℓ] [[] [j] []] [/m] [. Combining this with the inequality above, we get]

### j [ℓ] [[] [j] []] [/m] [. Combining this with the inequality above, we get]

### *T ≤*

### � n j =1 [ℓ] [[] [j] []] + ℓ [ k ] ≤ T [∗] + T [∗] = 2 T [∗], *m*

### where ℓ [ k ] ≤ T [∗] because OPT must assign job k to some machine. **An im p roved anal y sis** In ALG, since every machine has load at least T − ℓ [ k ] when k was assigned to i, the sum of all job lengths excluding job i is at least m ( T − ℓ [ k ]). Thus, we can improve the analysis from above:

### � n j =1 [ℓ] [[] [j] []]

### =1 [ℓ] [[] [j] []] + 1 − [1] *m m* �

### *m*

### *T [∗] .* �

### *T ≤*

### � n j =1 [ℓ] [[] [j] []] [ −] [ℓ] [[] [k] []] + ℓ [ k ] = *m*

### ℓ [ k ] ≤ 2 − [1] *m* � �

### This implies that the algorithm is a (2 − 1 /m )-approximation algorithm. 46


-----

