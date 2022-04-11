# The Sparks Foundation: IoT and Computer Vision Internship
# Name: Hesham Mohamed Abd El-Hamed Ali
# Task: Color Identification in Images
# Batch: #GRIPAPR22

# python Color_Identification.py -i Image_2.jpg

import argparse
import cv2
import pandas as pd
import matplotlib.pyplot as plt

# Creating argument parser to take image path from command line

arg = argparse.ArgumentParser()
arg.add_argument(
    '-i', '--image', default=r"Image_1.jpg", help="Image Path")
args = vars(arg.parse_args())

csv_path = "colors.csv"
img_path = "Images/" + args['image']

# read the csv file

Columns_Names = ["Color", "Name of color", "Hexadecimal code", "R", "G", "B"]
colorsDataSet = pd.read_csv(csv_path, names=Columns_Names, header=None)

# read the image

img = cv2.imread(img_path)
img = cv2.resize(img, (1080, 720))
imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Now to declare global variables

clicked_flag = False  # Clicked Value
r = g = b = x_coordinate = y_coordinate = 0

# The function to calculate the min distance from all colors & get the most matching color


def get_color_name(R, G, B):
    minimum_distance = 10000

    for i in range(len(colorsDataSet)):
        distance = abs(R - int(colorsDataSet.loc[i, "R"])) + abs(
            G - int(colorsDataSet.loc[i, "G"])) + abs(B - int(colorsDataSet.loc[i, "B"]))

        if distance <= minimum_distance:
            minimum_distance = distance
            color_name = colorsDataSet.loc[i, "Name of color"]
    return color_name

# The function to get x , y coordinates of mouse double click


def getClickedParams(event, x_coordinate, y_coordinate, flags, parameters):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, x_position, y_position, clicked_flag

        clicked_flag = True
        x_position = x_coordinate
        y_position = y_coordinate

        b, g, r = img[y_coordinate, x_coordinate]
        b = int(b)
        g = int(g)
        r = int(r)


# create window

cv2.namedWindow("Color Identification in Images")
cv2.setMouseCallback("Color Identification in Images", getClickedParams)

while True:

    cv2.imshow("Color Identification in Images", img)
    if clicked_flag:

        # Draw the Rectangle Filled With the Specified Color
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), cv2.FILLED)

        # Getting the color Name along with the R, G and B Values
        color_name = get_color_name(
            r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

        # cv2.putText(img,text,origin,font,fontScale,color,thickness)
        cv2.putText(img, color_name, (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                    0.8, (255, 255, 255), 2)

        # If we have the Light color it will display the text in black
        if r + g + b >= 600:
            cv2.putText(img, color_name, (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, (0, 0, 0), 2)

        # After all the cation the Clicked Event will be set to False
        clicked_flag = False

    # Break the loop when user hits 'q' key
    if cv2.waitKey(20) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
