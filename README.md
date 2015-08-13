# reactive

A Python package for writing functional reactive programs.

### Usage

The following line must be used to import the required class.

```python
from reactive import Reactive
```

Example 1:  

```python
obj = Reactive()
obj.add('var_1', value = 10)
obj.add('var_2', value = 100)
obj.add('var_3', equation = 'var_1 + var_2+1')
print(obj)
print('-'*25)
obj.modify('var_1', value = 20)
print(obj)
```

Output:  

```
Variable var_1: 10

Variable var_2: 100

Variable var_3: 111

-------------------------

Variable var_1: 20

Variable var_2: 100

Variable var_3: 121

```

Example 2:  

```python
obj.add('var_1', value = [[1, 2], [3, 4]])
obj.add('var_2', equation = 'var_1[0][0] * var_1[0][1]')
obj.add('var_3', equation = 'var_2 + 10')
print(obj)
print('-'*25)
obj.modify('var_1', value = [[10, 20], [30, 40]])
print(obj)
```

Output:  

```
Variable var_1: [[1, 2], [3, 4]]

Variable var_2: 2

Variable var_3: 12


-------------------------
Variable var_1: [[10, 20], [30, 40]]

Variable var_2: 200

Variable var_3: 210
```

Example 3:  

```python
obj.add('var_1', value = [[1, 2], [3, 4]])
obj.var_1[0][1] = 20
obj.modify('var_1', value = obj.var_1)
print(obj)
```

Output:  
```
Variable var_1: [[1, 20], [3, 4]]
```

Example 4:  

```python
obj.add('var_1', value = "hello")
obj.add('var_2', equation = 'var_1 + " world."')
obj.add('var_3', equation = 'sum(range(10))')
print(obj)
```

Output:  

```
Variable var_1: hello

Variable var_2: hello world.

Variable var_3: 45
```
