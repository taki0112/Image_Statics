import json, sys
from collections import defaultdict
import matplotlib.pyplot as plt

# reference
# https://www.reddit.com/r/learnpython/comments/2y9zwq/adding_value_labels_on_bars_in_a_matplotlib_bar/
# https://pythonspot.com/en/matplotlib-pie-chart/
# https://matplotlib.org/users/text_props.html



"""
Architecture (list type)
image       [identifier], [imsize]
regions     [ansize], [boxcorners] or [vertices], [class], [type]
   - linegroup   [tags], [vertices]
version 
json = list type
regions = list type
linegroup = list type... but may be length = 1
box = dict[0]['regions'][0]['boxcorners']
polygon = dict[0]['regions'][0]['vertices']
line = dict[0]['regions'][0]['linegroup'][0]['vertices']
"""

PATH = "./annotations.raf"

def change_class_name(name) :

    if(name.__eq__("crosswalk")) :
        name = "Cross"
    elif(name.__eq__("Pedestrian1")) :
        name = "Pedes"
    elif(name.__eq__("RoadBoundary")) :
        name = "Road"
    elif(name.__eq__("TrafficLight")) :
        name = "Light"
    elif(name.__eq__("TrafficSign")) :
        name = "Sign"
    elif(name.__eq__("UnidentifiedObjects")) :
        name = "Ufo"
    elif(name.__eq__("Vehicle")) :
        name = "Vehicle"
    return name


def Distribution_class() :
    with open(PATH) as json_file:
        Architecture = json.load(json_file)
        class_count = defaultdict(int)
        for i,_ in enumerate(Architecture):
            for j,_ in enumerate(Architecture[i]['regions']):
                class_name = Architecture[i]['regions'][j]['class']
                class_count[class_name] += 1

        plt.bar(range(len(class_count)), class_count.values(), align='center')
        plt.xticks(range(len(class_count)), class_count.keys())
        for x, y in zip(range(len(class_count)), class_count.values()):
            plt.text(x, y, str(y), horizontalalignment='center') # verticalalignment  option too
        plt.xlabel("Class name")
        plt.ylabel("# of class")
        plt.title("Distribution of Class")
        plt.show()

def Intersection_class() :
    with open(PATH) as json_file :
        Architecture = json.load(json_file)
        image_list = list()
        for i,_ in enumerate(Architecture) :
            class_set = set()
            for j,_ in enumerate(Architecture[i]['regions']) :
                class_name = Architecture[i]['regions'][j]['class']
                class_set.add(class_name)
            class_set = sorted(class_set)
            image_list.append(class_set)

        intersection_count = defaultdict(int)
        for i,_ in enumerate(image_list) :
            intersection_class_str = "∩".join(str(element) for element in image_list[i])
            intersection_count[intersection_class_str] += 1

        # print(len(intersection_count))
        # print(intersection_count)


        plt.title("Intersection of Class", horizontalalignment = 'center', fontsize=20)

        # pie 1
        plt.pie(list(intersection_count.values()), labels=intersection_count.keys(), autopct='%1.1f%%',  startangle=140)
        plt.axis('equal')
        plt.show()

        # pie 2
        """
        patches, texts = plt.pie(list(intersection_count.values()), startangle=90)
        plt.legend(patches, intersection_count.keys(), loc="best")
        plt.axis('equal')
        plt.tight_layout()
        plt.show()
        """

def Pixel_distribution(max=100) :
    with open(PATH) as json_file :
        Architecture = json.load(json_file)
        image_list = list()
        for i,_ in enumerate(Architecture) :
            y_list = list()
            for j,_ in enumerate(Architecture[i]['regions']) :
                if Architecture[i]['regions'][j]['type'].__eq__('line') :
                    y = Get_pixel(Architecture[i]['regions'][j]['linegroup'][0]['vertices'])

                elif Architecture[i]['regions'][j]['type'].__eq__('box') :
                    y = Get_pixel(Architecture[i]['regions'][j]['boxcorners'])

                else :
                    y = Get_pixel(Architecture[i]['regions'][j]['vertices'])
                y_list.append(y)
            image_list.append(y_list)

        pixel_count = defaultdict(int)
        for i,_ in enumerate(image_list) :
            for j,_ in enumerate(image_list[i]) :
                key = image_list[i][j] // 10 * 10
                if key < max :
                    key = str(key)+"~"+str((key+10))
                    pixel_count[key] += 1

        # print(len(pixel_count))
        plt.title("Pixel distribution, max=%d" %max, position=(0.5,1.05),  fontsize=20)

        # pie 1
        plt.pie(list(pixel_count.values()), labels=pixel_count.keys(), autopct='%1.1f%%',  startangle=140)
        plt.axis('equal')
        plt.show()


def Get_pixel(coordinate) :
    y_coordinate = coordinate[1::2]

    return max(y_coordinate) - min(y_coordinate)

if __name__ == "__main__" :
    try :
        method = sys.argv[1]
        if method.lower().__eq__("Distribution".lower()) :
            Distribution_class()
        elif method.lower().__eq__("Intersection".lower()):
            Intersection_class()
        elif method.lower().__eq__("Pixel".lower()):
            try :
                Pixel_distribution(int(sys.argv[2]))
            except :
                print("Please enter the max value")
    except :
        print("Please enter the option...")
        print("For example, (1) Distribution, (2) Intersection, (3) Pixel <Case-insensitive>" )
        print("If you enter \"Pixel\", you must also enter the max value.")


