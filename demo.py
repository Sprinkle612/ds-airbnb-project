import pandas as pd
import numpy as np

####################################################################################
# read saved label encoder 

temp = pd.read_csv("./saved-models/zipcode-neigh-dic.csv", header=0)
zip_neigh_dic = dict(zip(temp.zipcode, temp.neighbourhood_cleansed))

temp = pd.read_csv("./saved-models/neighbourhood-le.csv", header=0)
neigh_le = dict(zip(temp.neighbourhood_cleansed, temp.temp))

temp = pd.read_csv("./saved-models/property_cat-le.csv", header=0)
property_cat_le = dict(zip(temp.property_cat, temp.temp))




####################################################################################
# prompt user to input 

# zipcode = '10044'
# property_cat = 'apartment'

zipcode = input("Please enter your property's zipcode:\n")
neigh = zip_neigh_dic.get(int(zipcode))
print('>> You entered {}, so your neighborhood is {}'.format(zipcode, neigh))

property_cat = input("\nPlease enter your property's type (apartment, house, hotel, other):\n")
print('>> You entered {}'.format(property_cat))


####################################################################################
# construct user input matrix
input = pd.DataFrame(np.array([neigh]), columns=['neigh'])
input['neigh_encoded'] = input.neigh.apply(lambda x: neigh_le.get(x))

input['property_cat'] = np.array([property_cat])
input['prop_encoded'] = input.property_cat.apply(lambda x: property_cat_le.get(x))

print("\nCurrent user input\n")
print(input)


# room_type
# bathrooms
# bedrooms
# beds


# input_part1 = 

# # look up ava from csv
# availability_30

# # we recommend for them
# cleaning_fee = 40.0
# minimum_nights = 2
# extra_people = 0
# accommodates = (2*beds)
# guests_included
# cancellation_policy

# # growth curve
# host_months
# number_of_reviews
# review_cat


# # zipcode = input("Please enter your property's zipcode:\n")
# # print(f'You entered {zipcode}')

# # zipcode = input("Please enter your property's zipcode:\n")
# # print(f'You entered {zipcode}')
   