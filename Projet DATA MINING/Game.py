import pygame
import numpy as np
import numpy as np
import itertools
from itertools import chain, combinations, permutations
import warnings
import os


# generate random integer values
from random import seed
from random import randint
# seed random number generator
seed(1)
warnings.filterwarnings("ignore")

# Window Settings :
pygame.init()
display_width = 1280
display_height = 720
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("DM PROJECT")
crashed = False
path = os.path.dirname(os.path.abspath(__file__))+"\\"


# Apriori settings:
minimal_support = 0.3
minimal_confidence = 0.5
matrix = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0]])

matrix = np.array(matrix)
initmat = False
for row in matrix:
    row = np.array(row)
matrixLabels = ["Apple", "Avocado", "Banana", "Cherry",
                "Orange", "Peach", "Pear", "Strawberry", "Watermelon"]
matrixLabels = np.array(matrixLabels)
labels = np.arange(len(matrix[0]))
unknown = pygame.image.load(path+"Sheet\\Unknown.png")
bg = pygame.image.load(path+"Sheet\\xcx.png")
buyIcon = pygame.image.load(path+"Sheet\\buy.png")
# class :


class Button:
    def __init__(self, x, y, width, height, text):
        self.posx = x
        self.posy = y
        self.width = width
        self.height = height
        self.text = text
        self.color = (125, 125, 125)

    def isOver(self, mouseX, mouseY):
        return (mouseX >= self.posx and mouseX <= self.width+self.posx and mouseY >= self.posy and mouseY <= self.posy+self.height)

    def draw(self):
        pygame.draw.rect(gameDisplay, (0, 0, 0), (self.posx-2,
                                                  self.posy-2, self.width+4, self.height+4), 0)
        pygame.draw.rect(gameDisplay, self.color, (self.posx,
                                                   self.posy, self.width, self.height), 0)
        myfont = pygame.font.SysFont(path+"pixelated.ttf", 40)
        label = myfont.render(self.text, 1, (0, 0, 0))
        # text_rect = label.get_rect(center=(self.posx+(self.width/2), self.posy+(self.height/2)))
        gameDisplay.blit(
            label, (self.posx+15, (self.posy+self.posy+self.height)/2-15))


class Image:
    def __init__(self, src, posx, posy, label='', border=True):
        self.src = path+src
        self.img = pygame.image.load(self.src)
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.checked = False
        self.posx = posx
        self.posy = posy
        self.border = border
        self.label = label
        self.known = True

    def draw(self, x=None, y=None):
        global unknown
        if x == None or y == None:
            x = self.posx
            y = self.posy
        img = self.img
        if not self.known:
            gameDisplay.blit(unknown, (x, y))
        else:
            if self.border:
                if not self.checked:
                    pygame.draw.rect(img, (255, 255, 255),
                                     img.get_rect(), Border_Width)
                else:
                    pygame.draw.rect(img, (0, 255, 0),
                                     img.get_rect(), Border_Width)
            gameDisplay.blit(img, (x, y))

    def __eq__(self, value):
        if isinstance(value, self.__class__) and self.src == value.src:
            return True
        return False

    def clicked(self, mouseX, mouseY):
        return (mouseX >= self.posx and mouseX <= self.width+self.posx and mouseY >= self.posy and mouseY <= self.posy+self.height)


# Background
Darkwood = Image('Sheet\\darkwood.png', 15, 15, border=False)
Lightwood = []
xwood = 200
ywood = 200
for i in range(2):
    for j in range(3):
        Lightwood.append(Image("Sheet\\lightwood.png", j *
                               xwood+15, ywood+i*250, border=False))


def drawBackground():
    '''Draw the background '''
    global bg
    gameDisplay.blit(bg, (-25, 0))
    Darkwood.draw()
    for i in Lightwood:
        i.draw()


def getValue(fruit):
    ''' if fruit is checked returns 1 else 0'''
    return int(fruit.checked)


def writeText(text, x, y, size):
    '''used to write attemps'''
    myfont = pygame.font.SysFont(path+"pixelated.ttf", size)
    label = myfont.render(text, 1, (255, 255, 255))
    labelrect = label.get_rect()
    text_rect = label.get_rect(center=((x+labelrect[0]), (y+labelrect[1])))
    gameDisplay.blit(label, text_rect)


def delete(array, sets):
    for pos in range(len(array)-1, len(sets)):
        todelete = []
        y = sets[pos]
        for element in range(len(y)):
            if(np.all(np.isin(array, y[element]))):
                todelete.append(element)
        todelete = np.array([todelete])
        sets[pos] = np.delete(sets[pos], todelete, axis=0)
    return sets


def itertoolToNparray(labels, comb):
    if comb:
        x = chain.from_iterable(combinations(labels, r)
                                for r in range(len(labels)+1))
    else:
        x = chain.from_iterable(permutations(labels, r)
                                for r in range(len(labels)+1))
    x = list(x)
    y = []
    x.pop(0)
    for i in x:
        y.append(np.asarray(i))
    # y is all the possible itemsets as array
    y = np.array(y)
    return y
# frequentIS is an array containing all frequent k-itemset


def support(value):
    value = value == 1
    try:
        value = np.all(value, axis=1)
    except:
        # value length = 1
        pass
    return np.mean(value)


def confidence(matrix, rule):
    left = rule[:len(rule)-1]
    value = matrix[:, left]
    a = support(matrix[:, rule])
    b = support(matrix[:, left])
    if b == 0:
        return None
    return a/b


rules = []


def apriori(matrix, buy):
    global rules
    rules = []
    y = itertoolToNparray(labels, True)
    frequentIS = []
    for sett in y:
        value = matrix[:, sett]
        if support(value) >= minimal_support:
            frequentIS.append(sett)
    frequentIS = np.array(frequentIS)
    ###############################
    #######Generate rules##########
    ###############################
    # Get all frequant itemset with size >=2
    frequentIS = frequentIS[list(len(i) >= 2 for i in frequentIS)]
    for IS in frequentIS:
        # for each frequent item set , get all the permutations possible
        all_permu = itertoolToNparray(IS, False)
        all_permu = all_permu[list(len(i) >= 2 for i in all_permu)]
        for permutation in all_permu:
            if confidence(matrix, permutation) >= minimal_confidence:
                rules.append(permutation)

    ############################################
    ###########GENERATE RECOMMENDATION##########
    ############################################
    buy = np.where(buy == 1)[0]
    recom = []
    buy = itertoolToNparray(buy, True)
    for i in buy:
        for rule in rules:
            left = rule[:len(rule)-1]
            if len(left) == len(i) and np.all(left == i):
                recom.append(rule[len(rule)-1])
    recom = np.unique(recom)
    return recom


def accuracy(prediction, transaction):
    x = np.isin(prediction, transaction)
    return np.mean(x)


# Declarations :
vfunc = np.vectorize(getValue)
# Selection border width
Border_Width = 9
# Path to the python file
attempts = 7

# Buttons
BuyButton = Button((display_width+600-200)/2+250,
                   display_height-100, 150, 70, "BUY")


# Fruits :
fruitLabel = ["Apple", 'Avocado', 'Banana', 'Cherry',
              'Orange', 'Peach', 'Pear', 'Strawberry', 'Watermelon']
fruitsList = []
fruitsListMin = []
cpt = 0
for label in fruitLabel:
    fruitsList.append(Image('Sheet/'+label+".png", 37 +
                            int(cpt/3)*200, cpt % 3*250+25, label))
    fruitsListMin.append(pygame.image.load(path+"Sheet\\"+label+"Min.png"))
    cpt = cpt+1
fruitsList = np.array(fruitsList)
fruitsListMin = np.array(fruitsListMin)
counter = attempts

foo1 = ["None"]
foo2 = ["None"]
recommendation = []
tofind = []
tofindd = []
recommendationToShow = []
lastbuyToShow = []
guessingToShow = []
guessing = 0
guess = False
allowed = 0
pygame.mixer.init()
pygame.mixer.music.load(path+'Sheet\\bgsound (online-audio-converter.com).wav')
pygame.mixer.music.play(-1)
while not crashed:
    drawBackground()
    for event in pygame.event.get():
        X = pygame.mouse.get_pos()
        Y = X[1]
        X = X[0]
        if event.type == pygame.QUIT:
            crashed = True
        # Left click
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Select fruits
                for fruit in fruitsList:
                    if fruit.clicked(X, Y):
                        if guess and attempts < 1:
                            if not fruit.checked and allowed < len(toshowt):
                                fruit.checked = True
                                allowed += 1
                            elif fruit.checked:
                                fruit.checked = False
                                allowed = -1
                        else:
                            fruit.checked = not fruit.checked
                # Press but
                if BuyButton.isOver(X, Y):
                    if not guess:
                        toadd = vfunc(fruitsList)
                        matrix = np.concatenate([matrix, [vfunc(fruitsList)]])
                        recommendation = apriori(matrix, toadd)
                        try:
                            recommendationToShow = fruitsListMin[recommendation]
                            lastbuyToShow = fruitsListMin[np.where(toadd == 1)[
                                0]]
                            # tofind=np.xor1d(toadd,recommendation)
                            tofind = recommendation
                        except:
                            print("No recomendation")
                            recommendation = []
                        if not initmat:
                            initmat = True
                            matrix = np.delete(matrix, 0, axis=0)
                        k = len(recommendation)
                        toshow = []
                        for _ in range(k):
                            toshow.append(unknown)
                    else:
                        guessing = vfunc(fruitsList)
                        guessing = np.where(guessing == 1)[0]
                        guessingToShow = fruitsListMin[guessing]
                        guessing = np.isin(recommendation, guessing)
                        guessing = np.mean(guessing)
                        if np.isnan(guessing):
                            guessing = 0
                        allowed = 0
                    guess = not guess
                    for fruit in fruitsList:
                        fruit.checked = False
                        fruit.known = True
                    if attempts > 0:
                        attempts = attempts-1
                        counter = attempts
                        if attempts == 0:
                            counter = ""
                    else:
                        counter = ""

        # Buy button hover
        if event.type == pygame.MOUSEMOTION:
            if BuyButton.isOver(X, Y):
                BuyButton.color = (0, 255, 0)
            else:
                BuyButton.color = (255, 255, 255)
        for fruit in fruitsList:
            fruit.draw()
        if(attempts < 1):
            # else :
            #     writeText("Attempts :",(display_width+600)/2,100,50)
            writeText("Accuracy : "+str(np.round(guessing*100, decimals=0)
                                        )+"%", (display_width+600)/2-180, 650, 30)
            # writeText(str(np.size(recommendation)),(display_width+600)/2,100,50)
            if guess:
                toshowt = toshow.copy()
                toshowt.reverse()
                limit = len(toshow)
                added = 0
                for i in fruitsList:
                    if len(recommendation) > 2:
                        # for k in lastbuyToShow:
                        buylist = []
                        for buy in np.where(toadd == 1)[0]:
                            buylist.append(fruitLabel[buy])
                        if i.label in buylist:
                            i.checked = True
                    if i.checked == True and added < limit:
                        toshowt[added] = i
                        added += 1
                k = len(recommendation)
                kk = 0
                for i in toshowt:
                    setx = 700+150*(kk % 3)
                    sety = 100+150*(int(kk/3))
                    try:
                        gameDisplay.blit(i, (setx, sety))
                    except:
                        i.draw(setx, sety)
                    kk = kk+1
            else:
                writeText("Recommendation :", 700, 480, 18)
                writeText("Last Purchase  :", 700, 530, 18)
                writeText("Last Guess     :", 700, 600, 18)
                kk = 0
                for i in recommendationToShow:
                    setx = 800+(kk*75)
                    sety = 450
                    kk += 1
                    gameDisplay.blit(i, (setx, sety))
                kk = 0
                for i in lastbuyToShow:
                    setx = 800+(kk*75)
                    sety = 510
                    kk += 1
                    gameDisplay.blit(i, (setx, sety))
                kk = 0
                for i in guessingToShow:
                    setx = 800+(kk*75)
                    sety = 570
                    kk += 1
                    gameDisplay.blit(i, (setx, sety))

        else:
            writeText("Attempts :", (display_width+600)/2, 100, 50)

        writeText(str(counter), (display_width+600)/2, 300, 170)
        BuyButton.draw()
        gameDisplay.blit(buyIcon, (1170, display_height-100))
        pygame.display.update()
pygame.quit()

quit()
