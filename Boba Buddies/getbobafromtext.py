# run the following code if you haven't installed text2emotion
# pip install text2emotion

import text2emotion as te

import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
    
# Calculates the weighted average
def teaAverage(emotions):
    happy = emotions['Happy']
    angry = emotions['Angry']
    sad = emotions['Sad']
    return 0.5 * happy + 0.3 * sad + 0.2 * angry

flavorPercents = [.95, .90, .85, .80, .75, .70, .65, .60, .55, .50, .45, .40, .35, .30, .25, .20, .15, .10, .05, 0]
flavors = ["Peach", "Strawberry", "Mango", "Honeydew", "Coconut", "Passionfruit", "Blueberry", "Lychee", "Rose", "Grapefruit", "Brown Sugar", "Tiger", "Thai Tea", "Hazelnut", "Taro", "Green", "White", "Coffee", "Oolong", ""]
flavorColors = ["LightPink2", "PaleVioletRed1", "DarkGoldenrod1", "PaleGreen1", "honeydew3", "orange2", "RoyalBlue1", "snow", "HotPink1", "IndianRed1", "red4", "tan2", "sandy brown", "navajo white", "MediumPurple2", "lightGoldenrod3", "blanched almond", "saddle brown", "sienna1", "bisque2"]
# Input the average from teaAverage and it returns the flavor
def returnFlavor(average):
    for i in range(len(flavorPercents)):
        if average >= flavorPercents[i]:
            flavor = flavors[i]
            if average >= 0.5:
                teaType = " Green Tea"
            elif flavor == "Thai Tea":
                teaType = ""
            else:
                teaType = " Milk Tea"
            return flavors[i] + teaType, flavorColors[i]

toppingsPercents = [0.8, 0.6, 0.4, 0.2, 0]
toppings = ["Popping Boba", "Grass Jelly", "Aloe", "Lychee Jelly", "Honey Boba"]
toppingColors = ["Black", "Black", "White", "White", "Black"]

# Input the dictionary of emotions, and it returns the topping 
def returnToppings(emotions):
    fear = emotions["Fear"]
    surprise = emotions["Surprise"]
    for i in range(len(toppings)):
        if fear >= toppingsPercents[i] or surprise >= toppingsPercents[i]:
            return toppings[i], toppingColors[i]


    