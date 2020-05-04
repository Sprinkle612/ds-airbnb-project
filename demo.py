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

temp = pd.read_csv("./saved-models/room_type-le.csv", header=0)
room_type_le = dict(zip(temp.room_type, temp.temp))



####################################################################################
# prompt user to input 

# zipcode = '10044'
# property_cat = 'apartment'

zipcode = input("Please enter your property's zipcode:\n")
neigh = zip_neigh_dic.get(int(zipcode))
print('>> You entered {}, so your neighborhood is {}'.format(zipcode, neigh))

property_cat = input("\nPlease enter your property's type (apartment, house, hotel, other):\n")
print('>> You entered {}'.format(property_cat))

room_type = input("\nPlease describe how you want to use your property (Entire home, Private room, Shared room, Hotel room):\n")
print('>> You entered {}'.format(room_type))

bathrooms = int(input("\nPlease enter how many bathroom is included with your property:\n"))
print('>> You entered {}'.format(bathrooms))

bedrooms = int(input("\nPlease enter how many bedroom is included with your property:\n"))
print('>> You entered {}'.format(bedrooms))

beds = int(input("\nPlease enter how many bed is included with your property:\n"))
print('>> You entered {}'.format(beds))

####################################################################################
# construct user input matrix
input = pd.DataFrame(np.array([neigh]), columns=['neigh'])
input['neigh_encoded'] = input.neigh.apply(lambda x: neigh_le.get(x))

input['property_cat'] = np.array([property_cat])
input['prop_encoded'] = input.property_cat.apply(lambda x: property_cat_le.get(x))

input['room_type'] = np.array([room_type])
input['room_encoded'] = input.room_type.apply(lambda x: room_type_le.get(x))

input['bathrooms'] = np.array([bathrooms])
input['bedrooms'] = np.array([bedrooms])
input['beds'] = np.array([beds])
# but need scale


print("\nCurrent user input\n")
print(input)


# we recommend for them
cleaning_fee = 40.0
minimum_nights = 2
extra_people = 0
guests_included = 2
cancellation_policy = "strict_14_with_grace_period"
accommodates = 2 * beds


# # look up ava from csv
# availability_30

# # growth curve
# host_months
# number_of_reviews
# review_cat