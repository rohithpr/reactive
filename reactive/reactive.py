import re

class Reactive:
    """
    Reactive
    """
    def __init__(self):
        self.control = {}
        pass

    def __str__(self):
        keys = list(self.__dict__.keys())
        keys.remove('control')
        if '__builtins__' in keys: keys.remove('__builtins__')
        keys.sort()

        temp = 'Control: ' + str(self.control) + '\n\n'
        for variable in keys:
            temp += 'Variable ' + variable + ': ' + str(eval(variable, self.__dict__)) + '\n\n'
        return temp

    def add(self, variable, value='', equation=''):
        if variable not in self.__dict__:
        # if True:
            if value != '':
                self.__dict__[variable] = value
                self.control[variable] = {
                            'dependents': [],
                            'equation': equation,
                            'parents': [],
                            }
            elif equation != '':
                for parent in re.findall(r'[_A-Za-z][_\dA-Za-z]*', equation):

                    if not self.is_cycle(parent, variable):
                        self.control[parent]['dependents'].append(variable)
                        self.__dict__[variable] = eval(equation, self.__dict__)
                self.control[variable] = {
                            'dependents': [],
                            'equation': equation,
                            'parents': [parent for parent in re.findall(r'[_A-Za-z][_\dA-Za-z]*', equation)],
                }
            else:
                raise Exception('Either value or equation must be defined')
        else:
            if value != '':
                self.__dict__[variable] = value
                self.update(variable)
            # raise KeyError('Variable exists. Use update to change value.')
        print(self)

    def evaluate(self, str):
        l = eval(str, self.__dict__)
        print(l)

    def is_cycle(self, variable_1, variable_2):
        return False

    def update(self, variable):
        for dependent in self.control[variable]['dependents']:
            self.__dict__[dependent] = eval(self.control[dependent]['equation'], self.__dict__)

