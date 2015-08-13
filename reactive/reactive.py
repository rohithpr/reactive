import keyword
import re

reserved = keyword.kwlist[:]
reserved += ['sum', 'range']

def clean_up(parents):

    temp = list(filter(lambda x: x != '' and x not in reserved, parents))
    temp = list(filter(lambda x: '"' not in x, temp))
    parents[:] = temp

class Reactive:
    """
    Reactive
    """
    def get_parents(self, equation):
        parents = re.findall(r'([_A-Za-z][\w]*|"[\w\t\n ]*")*', equation)
        clean_up(parents)
        # print(equation, parents)
        # for parent in parents:
        #     print(parent)
        #     if re.search(r'^\"[\w+\t\n ]*\"$', parent) is not None:
        #         parents.remove(parent)
        return list(parents)

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
        """
        Add a new variable into the reactive object.
        """
        if variable not in self.control:
            if value != '':
                self.__dict__[variable] = value
                self.control[variable] = {
                            'dependents': [],
                            'equation': equation,
                            'parents': [],
                            }
            elif equation != '':
                parents = self.get_parents(equation)
                clean_up(parents)
                for parent in parents:
                    if not self.is_cycle(parent, variable):
                        self.control[parent]['dependents'].append(variable)
                    else:
                        raise Exception('Cyclical references are not allowed.')
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
        # print(self)

    def modify(self, variable, value='', equation=''):
        """
        Modify a variable in the reactive object.
        """
        if variable in self.control:
            if self.control[variable]['equation'] == '' and value != '': # Wasn't equation, not equation
                self.__dict__[variable] = value
            elif self.control[variable]['equation'] == '' and equation != '': # Wasn't equation, now equation
                parents = get_parents()
                for parent in parents:
                    if not self.is_cycle(parent, variable):
                        self.control[parent]['dependents'].append(variable)
                    else:
                        raise Exception('Cyclical references are not allowed.')
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
                new_parents = get_parents
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
        # print(self)

    def is_cycle(self, parent, child):
        """
        Detects any cyclical dependecies.
        """
        if child in self.control[parent]['parents']:
            return True
        for _ in self.control[parent]['parents']:
            if self.is_cycle(_, child):
                return True
        return False

    def update(self, variable):
        """
        Updates all the dependents of a variable once it has been changed.
        """
        for dependent in self.control[variable]['dependents']:
            self.__dict__[dependent] = eval(self.control[dependent]['equation'], self.__dict__)
        
