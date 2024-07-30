from khnlp.romanize import Romanizer

def test_romanizer():
    romanizer = Romanizer('model.bin')

    name = 'កក់ថន តុលា'
    
    result = romanizer.romanize(name)
    
    print(result)

if __name__ == '__main__':
    test_romanizer()
