import glob
import os
import io
import random
from utils import name_to_tensor
from utils import * #this imports everything
import torch


class NamesDataset:
    def __init__(self, dataset_path):
        self.country_to_names = {}
        filenames = glob.glob(dataset_path)
        for fn in filenames:
            basename = os.path.basename(fn)
            country = os.path.splitext(basename)[0] #gives the country name without the .txt at the end
            names = io.open(fn, encoding='utf-8').read().strip().split('\n') #this creates a list with all the names in it
            names = [name.lower() for name in names] #this makes everything lowercase
            self.country_to_names[country] = names #map country to names

        self.countries = list(self.country_to_names.keys()) #just gives the labels greek and korean in a list
        self.num_countries = len(self.countries) #get length of list of countries



    def country_to_tensor(self, country):
        idx = self.countries.index(country)
        country_tensor = torch.zeros((1,self.num_countries))
        country_tensor[0,idx]=1.
        return country_tensor

    #we want to predict the next character in a character 


    #each time we get a random name and country
    def get_random_sample(self):
        rand_country_idx = random.randint(0,self.num_countries-1) #gives a random country index
        country = self.countries[rand_country_idx]

        rand_name_idx = random.randint(0,len(self.country_to_names[country])-1)
        name = self.country_to_names[country][rand_name_idx] #u have to add self because its refering to the object you pass through

        name_tensor = name_to_tensor(name)
        country_tensor = self.country_to_tensor(country) #this transforms a country into a tensor
        shifted_name = shift_name_right(name)

        #Gives a list of indicies for each letter in shifted name
        indicies = [letter_to_index(letter) for letter in shifted_name] #gives us the indicies of all the letters in a name
        target_tensor = torch.LongTensor(indicies)
        target_tensor.unsqueeze_(0) #this makes the shape 1x3 instead of just 3, this makes it a Rank 1 tensor which is important for utils.py

        return country, name, country_tensor, name_tensor, target_tensor

    def output_to_country(self, output):
        country_idx = torch.argmax(output).item() #which value is bigger?
        return self.countries[country_idx] #return the country


    def output_to_letter(self, output):
        idx = torch.argmax(output) #argmax gives us the index of the highest value in a tensor
        return all_letters[idx]