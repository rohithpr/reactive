import keyword
import re

def clean_up(parents):
    parents[:] = list(filter(lambda x: x not in keyword.kwlist, parents))

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
        if variable not in self.control:
        # if True:
            if value != '':
                self.__dict__[variable] = value
                self.control[variable] = {
                            'dependents': [],
                            'equation': equation,
                            'parents': [],
                            }
            elif equation != '':
                parents = re.findall(r'[_A-Za-z][_\dA-Za-z]*', equation)
                clean_up(parents)
                for parent in parents:
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
            raise Exception('Variable exists. Use modify to change it.')
        print(self)

    def modify(self, variable, value='', equation=''):
        if variable in self.control:
            if self.control[variable]['equation'] == '' and value != '': # Wasn't equation, not equation
                self.__dict__[variable] = value
            elif self.control[variable]['equation'] == '' and equation != '': # Wasn't equation, now equation
                for parent in re.findall(r'[_A-Za-z][_\dA-Za-z]*', equation):
                    if not self.is_cycle(parent, variable):
                        self.control[parent]['dependents'].append(variable)
                        self.__dict__[variable] = eval(equation, self.__dict__)
                self.control[variable]['equation'] = equation
                self.control[variable]['parents'] = [parent for parent in re.findall(r'[_A-Za-z][_\dA-Za-z]*', equation)]
            elif value != '': # Was equation, not equation
                for parent in self.control[variable]['parents']:
                    self.control[parent]['dependents'].remove(variable)
                self.control[variable]['parents'] = []
                self.control[variable]['equation'] = ''
                self.__dict__[variable] = value
            elif equation != '': # Was equation, now equation
                new_parents = re.findall(r'[_A-Za-z][_\dA-Za-z]*', equation)
                old_parents = self.control[variable]['parents'][:]
                for parent in old_parents:
                    if parent not in new_parents:
                        self.control[parent]['dependents'].remove(variable)
                for parent in new_parents:
                    if parent not in new_parents:
                        self.control[parent]['dependents'].append(variable)
                self.control[variable]['parents'] = new_parents
                self.control[variable]['equation'] = equation
                self.__dict__[variable] = eval(equation, self.__dict__)
            else:
                raise Exception('Umm..')
            self.update(variable)
        else:
            raise Exception('Variable does not exists. Use the add function to add a new variable.')

    def is_cycle(self, variable_1, variable_2):
        return False

    def update(self, variable):
        for dependent in self.control[variable]['dependents']:
            self.__dict__[dependent] = eval(self.control[dependent]['equation'], self.__dict__)
