from reactive import Reactive

def test_1():
    obj = Reactive()
    obj.add('var_1', value = 1)
    obj.add('var_2', value = 2)
    obj.add('var_3', value = 3)
    obj.add('var_4', equation = '3 * var_1 + var_2 - 1 * var_3')
    assert obj.var_4 == 2

def test_2():
    obj = Reactive()
    obj.add('var_1', value = 1)
    obj.add('var_2', value = 2)
    obj.add('var_3', value = 3)
    obj.add('var_4', equation = '(3 * var_1 + var_2 - 1) * var_3')
    assert obj.var_4 == 12


def test_3():
    obj = Reactive()
    obj.add('var_1', value = 'abc')
    obj.add('var_2', value = 'd')
    obj.add('var_3', value = 'ghi')
    obj.add('var_4', equation = '3 * var_1 + var_2 + var_3')
    assert obj.var_4 == 'abcabcabcdghi'

def test_4():
    obj = Reactive()
    obj.add('var_1', value = 'abc')
    obj.add('var_2', value = 'd')
    obj.add('var_3', value = 'ghi')
    obj.add('var_4', equation = '3 * (var_1 + var_2) + var_3')
    assert obj.var_4 == 'abcdabcdabcdghi'

def test_5():
    obj = Reactive()
    obj.add('var_1', value = 12)
    obj.add('var_2', value = 'd')
    obj.add('var_3', value = 'ghi')
    obj.add('var_4', equation = '3 * str(var_1) + var_2 + var_3')
    assert obj.var_4 == '121212dghi'
