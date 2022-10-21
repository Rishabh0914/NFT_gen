import os
from typing import List
from PIL import Image
from layer import Layer
import csv


class AvatarGenerator:
    def __init__(self, images_path: str):
        self.layers: List[Layer]= self.load_image_layers(images_path)
        self.output_path: str = "./output"
        os.makedirs(self.output_path, exist_ok=True)

    def load_image_layers(self, images_path: str):
        sub_paths = sorted(os.listdir(images_path))
        layers = []
        for sub_path in sub_paths:
            layer_path = os.path.join(images_path,sub_path)    # /images/Background
            layer = Layer(layer_path)
            layers.append(layer)
        return layers

    def generate_image_sequence(self):
        image_path_sequence = []     # /images/Background/1.png
        for layer in self.layers:
            image_path = layer.get_random_image_path()  # /images/Background/1.png
            image_path_sequence.append(image_path)
        hat_hair = image_path_sequence[3].split('/')
        face = image_path_sequence[4].split('/')
        if hat_hair[3][0] == face[3][0]:
            return image_path_sequence
        else:
            return None
        


    def render_avatar_image(self,image_path_sequence: List[str]):
        image = Image.open(image_path_sequence[0])
        for image_path in image_path_sequence[1:]:
            layer_image = Image.open(image_path)
            image = Image.alpha_composite(image, layer_image)
        return image

            
            

    def save_image(self, image:Image.Image, image_path_sequence, i :int = 0):
        
        bg = image_path_sequence[0].split('/')
        soil = image_path_sequence[1].split('/')
        body_skin = image_path_sequence[2].split('/')
        hat_hair = image_path_sequence[3].split('/')
        face = image_path_sequence[4].split('/')
        neck_bands_scarves = image_path_sequence[5].split('/')
        crops_plants_gems = image_path_sequence[6].split('/')
        image_index = str(i).zfill(4)

        

        image_file_name = f'EarthBuddy_{image_index}_{bg[3][:-4]}_{soil[3][:-4]}_{body_skin[3][:-4]}_{hat_hair[3][:-4]}_{face[3][:-4]}_{neck_bands_scarves[3][:-4]}_{crops_plants_gems[3][:-4]}.png'
        image_save_path = os.path.join(self.output_path,image_file_name)
        image.save(image_save_path)

        
        
        # header = ['Name','Background','Soil','Body Skins','Hat and Hair','Face','Neck Bands and Scarves','Crops and Plants or Gems']
        # data = {'Name':image_file_name,'Background':bg[3],'Soil':soil[3],'Body Skins':body_skin[3],'Hat and Hair':hat_hair[3],'Face':face[3],'Neck Bands and Scarves':neck_bands_scarves[3],'Crops and Plants or Gems':crops_plants_gems[3]}
        data = [image_file_name,bg[3][:-4],soil[3][:-4],body_skin[3][:-4],hat_hair[3][:-4],face[3][:-4],neck_bands_scarves[3][:-4],crops_plants_gems[3][:-4]]
        
        with open('./metadata.csv', 'a',newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(data)
            
            csv_file.close()
        
    def generate_avatar(self, n :int = 1):
        print("AvatarGenerator: Generating Avatar!")
        for i in range(n):
            image_path_sequence = self.generate_image_sequence() # /images/Background/1.png
            image = self.render_avatar_image(image_path_sequence)
            self.save_image(image, image_path_sequence,i)
            
        