import pandas as pd
import numpy as np

####################################################################################
# read saved label encoder 

temp = pd.read_csv("./saved-models/zipcode-neigh-dic.csv", header=0)
zip_neigh_dic = dict(zip(temp.zipcode, temp.neighbourhood_cleansed))

temp = pd.read_csv("./saved-models/neighbourhood-le.csv", header=0)
neigh_le = dict(zip(temp.neighbourhood_cleansed, temp.temp))

temp = pd.read_csv("./saved-models/room_type-le.csv", header=0)
room_type_le = dict(zip(temp.room_type, temp.temp))

# availability_30
ava_30 = pd.read_csv("./saved-models/aval_30.csv", header=0)

temp = pd.read_csv("./saved-models/aval_30_zip.csv", header=0)
ava_zip_dic = dict(zip(temp.zipcode, temp.availability_30))

temp = pd.read_csv("./saved-models/cancellation_policy-le.csv", header=0)
cancel_le = dict(zip(temp.cancellation_policy, temp.temp))

temp = pd.read_csv("./saved-models/review_cat-le.csv", header=0)
review_le = dict(zip(temp.review_cat, temp.temp))

temp = pd.read_csv("./saved-models/property_cat-le.csv", header=0)
property_cat_le = dict(zip(temp.property_cat, temp.temp))

####################################################################################
# prompt user to input 
zipcode = int(input("Please enter your property's zipcode:\n"))
neigh = zip_neigh_dic.get(zipcode)
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

# we recommend for them
cleaning_fee = 40.0
minimum_nights = 2
extra_people = 0
guests_included = 2
accommodates = 2 * beds
cancellation_policy = "strict_14_with_grace_period"
review = "excellent"

####################################################################################
# construct user input matrix
input = pd.DataFrame(np.array([neigh]), columns=['neigh'])
input['neigh_encoded'] = input.neigh.apply(lambda x: neigh_le.get(x))

input['room_type'] = np.array([room_type])
input['room_encoded'] = input.room_type.apply(lambda x: room_type_le.get(x))

input['accommodates'] = np.array([accommodates])

input['bathrooms'] = np.array([bathrooms])
input['bedrooms'] = np.array([bedrooms])
input['beds'] = np.array([beds])

input['guests_included'] = np.array([guests_included])

input['cancel'] = np.array([cancellation_policy])
input['cancel_encoded'] = input.cancel.apply(lambda x: cancel_le.get(x))

input['review'] = np.array([review])
input['review_encoded'] = input.review.apply(lambda x: review_le.get(x))

input['property_cat'] = np.array([property_cat])
input['prop_encoded'] = input.property_cat.apply(lambda x: property_cat_le.get(x))




# look up ava from csv
availability_30 = ava_zip_dic.get(zipcode)
ava_temp = ava_30[(ava_30['zipcode'] == zipcode) & (ava_30['bedrooms'] == bedrooms) & (ava_30['beds'] == beds)]
if(ava_temp.empty):
    availability_30 = ava_zip_dic.get(zipcode)
else:
    availability_30 = ava_temp.availability_30.values[0]
# input['avail'] = np.array([availability_30])

del input['neigh']
del input['property_cat']
del input['room_type']
del input['cancel']
del input['review']

input = input.append([input]*4,ignore_index=True)
print("\nCurrent user input\n")
print(input)



part1 = pd.DataFrame(np.array([[cleaning_fee]*5, [0,5,10,20,50], [0,2,4,6,8], 
                               [extra_people]*5, [minimum_nights]*5, [availability_30]*5]
                             ).transpose(1, 0),
                   columns=['cleaning_fee', 'number_of_reviews', 'host_months', 'extra_people','minimum_nights','availability_30'])

print("\nCurrent part1\n")
print(part1)

# # growth curve
# host_months
# number_of_reviews
