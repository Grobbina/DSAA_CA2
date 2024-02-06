import os 

class validator():
    def __init__(self):
        pass

    def filevalidation(self, path:str):
        current_directory = os.getcwd()
        file_list = os.listdir(current_directory)
        if path == '':
            return True
        elif path not in file_list:
            print('Invalid File Path')
            return True
        else:
            return False
    
    def __checktxt(self, path:str):
        if path.endswith('.txt'):
            return True
        else:
            print('Invalid File Type')
            return False
        
    def addtxt(self, path:str):
        if self.__checktxt(path) == False:
            addtxt = input(f'Did you mean {path}.txt? y/n: ')
            if addtxt == 'y':
                path += '.txt'
                return path
            else:
                return path
        else:
            return path



if __name__ == '__main__':
    validator = validator()
    validator.filevalidation('fruits.txt')