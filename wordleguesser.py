import copy
import json
from operator import itemgetter


def findword(guessed, g=None, y=None, gray=''):

    words_ = []
    with open('fivewords.txt','r',encoding='utf-8') as f:
        for word in f.readlines():
            words_.append(word.strip('\n'))
    wordle = copy.deepcopy(words_)
    
    green = ''
    yellow = ''
    position_ = []
    greenpos = [] #list of dics
    yellowpos = [] #list of dics
    #change green to be a string
    #g = 'k3,j4'
    if g == '':
        pass
    else:
        g = g.split(',')
        for x in g:
            dic = {'char':str(x[0]),
                   'pos':int(x[1])}
            greenpos.append(dic)
            green += x[0]

    #y = 'k3,j4'
    if y == '':
        pass
    else:
        y = y.split(',')
        for x in y:
            dic = {'char':str(x[0]),
                   'pos':int(x[1])}
            yellowpos.append(dic)
            yellow += x[0]
        
    
    #remove all guessed words
    guessed = guessed.lower().split(',')
    for word in guessed:
        for char in word:
            if char not in green and char not in yellow:
                gray = gray + char
        try:
            wordle.remove(word.lower())
        except ValueError:
            print(f'The word {word} is not in dic')
            pass
                
    #remove words that contain gray
    gray = ''.join(sorted(set(gray), key=gray.index))
    print(f'Gray letters are {gray}')
    for word in words_:
        if any(i in gray for i in word):
            try:
                wordle.remove(word)
            except ValueError:
                pass
        else:
            pass
    
    #remove words that contain yellow wrong position
    yellow = ''.join(sorted(set(yellow), key=yellow.index))
    if yellow == '':
        pass
    else:
        for word in words_:
            if any(i in yellow for i in word):
                pass
            else:
                try:
                    wordle.remove(word)
                except ValueError:
                    pass

        for dic in yellowpos:
            pos = int(dic['pos']) - 1           
            char = str(dic['char'])
            
            for word in words_:
                if word[pos] == char:
                    try:
                        wordle.remove(word)
                    except ValueError:
                        continue
                else:
                    pass

    #remove words that contain green wrong position
    green = ''.join(sorted(set(green), key=green.index))
    if green == '':
        pass
    else:
        for word in words_:
            if any(i in green for i in word):
                pass
            else:
                try:
                    wordle.remove(word)
                except ValueError:
                    pass
                
        for dic in greenpos:
            pos = int(dic['pos']) - 1           
            char = str(dic['char'])
            
            for word in words_:
                if word[pos] != char:
                    try:
                        wordle.remove(word)
                    except ValueError:
                        continue
                else:
                    pass
    
    #open json get frequency list
    with open('freq_map.json','r') as j:
        weights = json.load(j)
    sortedlist = []
    for word in wordle:
        try:
            weight = weights[word.lower()]
        except KeyError:
            weight = 0
        dic = {'word':word,
               'weight':weight
               }
        sortedlist.append(dic)
        
    sortedlist = sorted(sortedlist, key=itemgetter('weight'), reverse=True)
    
    return sortedlist        



while True:
    guessed = input("Input words you guessed? Format: word1,word2,word3\n")
    g = input("Input GREEN letters and their positions? If none press enter. Format: h1,j4,k5\n")
    y = input("Input YELLOW letters and their positions? If none press enter. Format: h1,j4,k5\n")
    results = findword(guessed=guessed,g=g,y=y)
    for count, dic in enumerate(results, 1):
        print(f"{count}, {dic['word']}, {dic['weight']}")
    
##    print('Possible Words To Use:', *results, sep='\n- ')
