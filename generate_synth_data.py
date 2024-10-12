from trdg.generators import (
    GeneratorFromStrings,
)
from tqdm.auto import tqdm
import os
import pandas as pd
import numpy as np
import random

# helper funcs and data to generate images
df = pd.read_csv("openfoodfacts_export_csv.csv",dtype={'column_name': str}, on_bad_lines='skip', sep='\t', low_memory=False)
df[["product_name_nb", "generic_name_nb", "brands"]]
all_words = df[["product_name_nb", "generic_name_nb", "brands"]].to_numpy().flatten()

num_before = len(all_words)
all_words = [x for x in all_words if str(x) != 'nan']
after_nan_filter = len(all_words)
print("removed: ", num_before - after_nan_filter, "words because of nan values")
all_words = list(set(all_words))
print("Removed", len(all_words), "duplicates")
print("Current number of words: ", len(all_words))

# random price generation
number_strings = []
for i in range(len(all_words)*9//10): # 90 percent of all words
    digits = np.random.randint(1, 100, 4)
    before_comma = f"{str(digits[0])}" # before comma is just given as 1 digit if 0-9
    after_comma = f"{str(digits[1])}" if len(str(digits[1])) == 2 else f"0{str(digits[1])}"
    number_string = f"{before_comma},{after_comma}"
    number_strings.append(number_string)

# then create 10 percent of the words with price between 100-999
for i in range(len(all_words)*1//10): # 10 percent of all words
    before_comma = np.random.randint(100, 999, 1)
    after_comma = np.random.randint(1, 99, 1)
    after_comma = f"{str(after_comma[0])}" if len(str(after_comma[0])) == 2 else f"0{str(after_comma[0])}"
    number_string = f"{str(before_comma[0])},{str(after_comma)}"
    number_strings.append(number_string)

# Now given word list and number list, get all combinations
all_combinations = []
for word in tqdm(all_words):
    for number in random.sample(number_strings, 20):  # Only need 20 prices per product for example
        for num_tabs in [1]:
            combined_string = word + "    " * num_tabs + number
            all_combinations.append(combined_string)

            #generate the images
generator = GeneratorFromStrings(
    random.sample(all_combinations, 10000),

    

    # uncomment the lines below for some image augmentation options
    # blur=6,
    # random_blur=True,
    # random_skew=True,
    # skewing_angle=20,
    # background_type=1,
    # text_color="red",
)

# Save images from generator
if not os.path.exists('output'):
    os.makedirs('output')
if not os.path.exists('output/labels.txt'):
    f = open("output/labels.txt", "w")
    f.close()

# Open txt file
current_index = len(os.listdir('output')) - 1  # all images minus the labels file
with open("output/labels.txt", "a", encoding='utf-8') as f:
    for counter, (img, lbl) in tqdm(enumerate(generator), total=1000):
        if counter >= 1000:
            break
        img.save(f'output/image{current_index}.png')
        f.write(f'image{current_index}.png {lbl}\n')
        current_index += 1
f.close()



# ตั้งค่าพารามิเตอร์สำหรับการสร้างข้อมูล
NUM_IMAGES_TO_SAVE = 10
NUM_PRICES_TO_GENERATE = 10000

# รหัสอื่น ๆ จะตามมาที่นี่
