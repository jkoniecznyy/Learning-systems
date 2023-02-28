## The pirpose of this project is to build a decision tree from a given dataset


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