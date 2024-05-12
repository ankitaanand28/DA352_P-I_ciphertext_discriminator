# import LFSR
from pylfsr import LFSR
from custom_utility import *

import pandas as pd

# Define the English words list
english_words = [
    "apple", "beach", "happy", "study", "green", "rabbit", "coffee", "monkey", "candle", "window",
    "purple", "flower", "basket", "orange", "pencil", "guitar", "cookie", "kitten", "forest", "potato",
    "castle", "turtle", "cherry", "camera", "travel", "summer", "basket", "pillow", "planet", "doctor",
    "planet", "forest", "garden", "school", "pencil", "cheese", "bottle", "forest", "winter", "flower",
    "rocket", "silver", "circus", "zipper", "jacket", "rocket", "flower", "coffee", "bottle", "doctor",
    "monkey", "purple", "guitar", "garden", "kitten", "potato", "candle", "turtle", "basket", "pillow",
    "camera", "window", "orange", "summer", "rabbit", "cherry", "castle", "coffee", "kitten", "planet",
    "cheese", "bottle", "winter", "zipper", "doctor", "monkey", "camera", "purple", "cherry", "turtle",
    "garden", "planet", "zipper", "rocket", "jacket", "forest", "pencil", "kitten", "bottle", "coffee",
    "pillow", "garden", "winter", "planet", "candle", "castle", "flower", "rocket", "cheese", "guitar",
    "cherry", "rabbit", "summer", "doctor", "silver", "coffee", "bottle", "window", "kitten", "zipper",
    "planet", "monkey", "forest", "winter", "rabbit", "turtle", "castle", "basket", "pillow", "coffee",
    "garden", "camera", "cherry", "pencil", "rocket", "bottle", "kitten", "planet", "doctor", "cheese",
    "zipper", "winter", "monkey", "castle", "forest", "turtle", "basket", "pillow", "coffee", "rocket",
    "cherry", "pencil", "planet", "doctor", "garden", "cheese", "zipper", "winter", "monkey", "forest",
    "turtle", "castle", "basket", "pillow", "coffee", "rocket", "cherry", "pencil", "planet", "doctor",
    "garden", "cheese", "zipper", "winter", "monkey", "forest", "turtle", "castle", "basket", "pillow",
    "coffee", "rocket", "cherry", "pencil", "planet", "doctor", "garden", "cheese", "zipper", "winter",
    "monkey", "forest", "turtle", "castle","ankita","ankle","anger","average","army","below","banana","cat","dog",
    "colour","dolphin","elephant","eagle","vulture","figure","game","chance","table","Dog", "Cow", "Cat", "Horse", "Donkey", "Tiger", "Lion", "Panther",
    "Leopard", "Cheetah", "Bear", "Elephant", "Polar bear", "Turtle", "Tortoise",
    "Crocodile", "Rabbit", "Porcupine", "Hare", "Hen", "Pigeon", "Albatross",
    "Crow", "Fish", "Dolphin", "Frog", "Whale", "Alligator", "Eagle", "Flying squirrel",
    "Ostrich", "Fox", "Goat", "Jackal", "Emu", "Armadillo", "Eel", "Goose", "Arctic fox",
    "Wolf", "Beagle", "Gorilla", "Chimpanzee", "Beaver", "Orangutan", "Antelope",
    "Bat", "Badger", "Giraffe", "Hermit crab", "Giant panda", "Hamster", "Cobra",
    "Hammerhead shark", "Camel", "Hawk", "Deer", "Chameleon", "Hippopotamus", "Jaguar",
    "Chihuahua", "Ibex", "Koala", "Kangaroo", "Llama", "Chinchillas", "Dodo", "Jellyfish",
    "Rhinoceros", "Hedgehog", "Zebra", "Possum", "Wombat", "Bison", "Bull", "Buffalo",
    "Sheep", "Meerkat", "Mouse", "Otter", "Sloth", "Owl", "Vulture", "Flamingo", "Racoon",
    "Mole", "Duck", "Swan", "Lynx", "Monitor lizard", "Elk", "Boar", "Lemur", "Mule",
    "Baboon", "Mammoth", "Blue whale", "Rat", "Snake", "Peacock", "Sparrow", "Blackbird",
    "Magpie", "Robin", "Wren", "Parrot", "Cockatoo", "Toucan", "Macaw", "Budgerigar",
    "Cormorant", "Pelican", "Gull", "Crane", "Pheasant", "Woodpecker", "Kingfisher", "Swift",
    "Hummingbird", "Heron", "Stork", "Egret", "Ibis", "Finch", "Starling", "Quail", "Grouse",
    "Turkey", "Peafowl", "Lark", "Nightingale", "Lapwing", "Curlew", "Stilt", "Oystercatcher",
    "Avocet", "Turnstone", "Sandpiper", "Snipe", "Plover", "Rail", "Coot", "Moorhen", "Bittern",
    "Shoebill", "Secretary bird", "Caracara", "Harrier", "Kestrel", "Merlin", "Falcon",
    "Goshawk", "Buzzard", "Condor", "Raven", "Jay", "Nutcracker", "Magpie", "Rook", "Jackdaw",
    "Chough", "Wagtail", "Pipit", "Bunting", "Sparrowhawk", "Osprey", "Lapwing", "Coot", "Heron",
    "Bittern", "Shelduck", "Teal", "Mallard", "Wigeon", "Pochard", "Shoveler", "Pintail", "Gadwall",
    "Shearwater", "Albatross", "Frigatebird", "Tropicbird", "Booby", "Gannet", "Cormorant",
    "Anhinga", "Pelican", "Heron", "Egret", "Ibis", "Spoonbill", "Flamingo", "Swan", "Goose", "Duck",
    "Merganser", "Grebe", "Gannet", "Petrel", "Storm petrel", "Shearwater", "Tern", "Auk", "Puffin",
    "Guillemot", "Razorbill", "Murrelet", "Dove", "Pigeon", "Quail", "Pheasant", "Grouse",
    "Ptarmigan", "Turkey", "Chukar", "Francolin", "Bulbul", "Sunbird", "Starling", "Oriole",
    "Blackbird", "Sparrow", "Weaver", "Finch", "Lark", "Pipit", "Wagtail", "Bunting", "Warbler",
    "Swallow", "Swift", "Sand martin", "Nightingale", "Cuckoo", "Kingfisher", "Woodpecker",
     "potato", "tomato", "onion", "carrot", "cucumber", "lettuce", "celery", "broccoli",
    "cauliflower", "spinach", "peas", "corn", "beans", "mushrooms", "asparagus", "eggplant",
    "pepper", "zucchini", "squash", "pumpkin", "sweetpotato", "beetroot", "turnip", "radish",
    "cabbage", "sprout", "kale", "artichoke", "leek",
    "fennel", "kohlrabi", "celtuce", "rhubarb", "garlic", "ginger", "horseradish", "parsnip",
    "okra", "artichoke", "acorns", "chayote", "jicama", "rutabaga", "salsify", "celeriac",
    "favabeans", "snowpeas", "broccoli", "watercress",
    "arugula", "endive", "escarole", "radicchio", "dandelion","satisfy","environment","mango"
    ,"pineapple","apricot","date","laptop","chair","clothes","hand","face","smile","flower"
]
set_english_words=set(english_words)

#Order of feedback polynomial can not be less than 2 or greater than length of state vector.
#  Polynomial also can not have negative or zeros powers
# Define the polynomial and initial state
polynomial = [5, 4, 3, 2]
initial_state = [1, 0, 1, 0, 1]

# Encrypt each word and store in a DataFrame
word_data = []
for word in set_english_words:
    encrypted_text = encrypt(word, polynomial, initial_state)
    decrypted_text = decrypt(encrypted_text, polynomial, initial_state)
    binary_encrypted_text = encrypted_text
    binary_decrypted_text = decrypted_text
    alphabet_encrypted_text = binary_to_text(encrypted_text)
    alphabet_decrypted_text = binary_to_text(decrypted_text)
    initial_state_string="5432"
    polynomial_coefficient="11111"
    word_data.append([word,binary_encrypted_text, binary_decrypted_text, alphabet_decrypted_text,initial_state_string,polynomial_coefficient])
#encrypted_text, decrypted_text,
# Create DataFrame
columns = ["English Word", "Encrypted Text (Binary)", "Decrypted Text (Binary)", "Decrypted Text (Alphabet)","Initial State"," Polynomial"]
df = pd.DataFrame(word_data, columns=columns)

# Display the DataFrame
print(df)
df_save=df.to_csv("Dataset_LFSR/ciphertext_set01.csv")
