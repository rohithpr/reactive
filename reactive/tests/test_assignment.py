from reactive import Reactive

def test_1():
    obj = Reactive()
    obj.add('var_1', value = 1)
    assert obj.var_1 == 1

def test_2():
    obj = Reactive()
    obj.add('var_1', value = 'abc')
    assert obj.var_1 == 'abc'

def test_3():
    obj = Reactive()
    obj.add('var_1', value = [123, 'abc'])
    assert obj.var_1 == [123, 'abc']
