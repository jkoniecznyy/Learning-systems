# Code from the Learning Systems classes

## The purpose of this program is to build a decision tree from a given dataset

To do so, the program performs th following steps:
1. Load the data from a file
2. Calculate occurrences of each attribute value
3. Calculate probabilities of each attribute value
4. Calculate entropy of each attribute
5. Calculate gain ratio of each attribute
6. Choose the attribute with the highest gain ratio
7. Split the dataset into subsets based on the chosen attribute
8. Repeat steps 2-7 for each subset
9. Print the decision tree


## Example:
### Input: 
```
old,yes,swr,down
old,no,swr,down
old,no,hwr,down
mid,yes,swr,down
mid,yes,hwr,down
mid,no,hwr,up
mid,no,swr,up
new,yes,swr,up
new,no,hwr,up
new,no,swr,up
```
### Output:
```
 Atrybut: 1
	 old -> D: down
	 mid -> Atrybut: 2
		 yes -> D: down
		 no -> D: up
	 new -> D: up
```