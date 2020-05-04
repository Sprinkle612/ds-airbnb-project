import pandas as pd
import numpy as np
from sklearn.externals import joblib
import sklearn.linear_model._ridge

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
df = pd.DataFrame(np.array([neigh]), columns=['neigh'])
df['neigh_encoded'] = df.neigh.apply(lambda x: neigh_le.get(x))

df['room_type'] = np.array([room_type])
df['room_encoded'] = df.room_type.apply(lambda x: room_type_le.get(x))

df['accommodates'] = np.array([accommodates])

df['bathrooms'] = np.array([bathrooms])
df['bedrooms'] = np.array([bedrooms])
df['beds'] = np.array([beds])

df['guests_included'] = np.array([guests_included])

df['cancel'] = np.array([cancellation_policy])
df['cancel_encoded'] = df.cancel.apply(lambda x: cancel_le.get(x))

df['review'] = np.array([review])
df['review_encoded'] = df.review.apply(lambda x: review_le.get(x))

df['property_cat'] = np.array([property_cat])
df['prop_encoded'] = df.property_cat.apply(lambda x: property_cat_le.get(x))


# look up ava from csv
availability_30 = ava_zip_dic.get(zipcode)
ava_temp = ava_30[(ava_30['zipcode'] == zipcode) & (ava_30['bedrooms'] == bedrooms) & (ava_30['beds'] == beds)]
if(ava_temp.empty):
    availability_30 = ava_zip_dic.get(zipcode)
else:
    availability_30 = ava_temp.availability_30.values[0]
# input['avail'] = np.array([availability_30])

del df['neigh']
del df['property_cat']
del df['room_type']
del df['cancel']
del df['review']

df = df.append([df]*4,ignore_index=True)

# dummy
room = df['room_encoded'][0]
room_types = np.zeros(4)
room_types[room] = 1
del df['room_encoded']

neigh = df['neigh_encoded'][0]
neigh_types = np.zeros(223)
neigh_types[neigh] = 1
del df['neigh_encoded']

review = df['review_encoded'][0]
review_types = np.zeros(4)
review_types[review] = 1
del df['review_encoded']

cancel = df['cancel_encoded'][0]
cancel_types = np.zeros(6)
cancel_types[cancel] = 1
del df['cancel_encoded']

prop = df['prop_encoded'][0]
prop_types = np.zeros(4)
prop_types[prop] = 1
del df['prop_encoded']

new_input = np.concatenate((df.to_numpy()[0].reshape(1,-1), room_types.reshape(1,-1), neigh_types.reshape(1,-1), cancel_types.reshape(1,-1), review_types.reshape(1,-1), prop_types.reshape(1,-1)), axis=1)
new_input = np.stack([new_input.reshape(-1)] * 5, axis=0)

# # growth curve
# host_months
# number_of_reviews
part1 = pd.DataFrame(np.array([[cleaning_fee]*5, [0,5,10,20,50], [0,6,12,24,36], 
                               [extra_people]*5, [minimum_nights]*5, [availability_30]*5]
                             ).transpose(1, 0),
                   columns=['cleaning_fee', 'number_of_reviews', 'host_months', 'extra_people','minimum_nights','availability_30'])

part1_scaled = joblib.load('./saved-models/standardize.pkl').transform(part1)
part1_scaled

####################################################################################
# sanity check
# print("\nCurrent user input\n")
# print(new_input.shape)

# print("\nCurrent part1\n")
# print(part1.shape)

new_input = np.concatenate((new_input, part1_scaled), axis=1)
# print(new_input.shape)

####################################################################################
model = joblib.load('./saved-models/ridge.pkl')
pred = model.predict(new_input)
price = np.exp(pred)[0]
print("\n*************************************************************************")
print("Your property has value of ${:.2f} via airbnb!".format(price))
print("Your property will be occupied for {} days per month.\nIn total, you will get ${:.2f} per month!".format(int(30-availability_30), price*(30 - availability_30)))


####################################################################################
# predict rental price
price_index = 60
#36.83

# prompt users to input more 
land_square_feet = int(input("\n\nTo estimate your rental price, we need more information from you.\nPlease enter your property's area (in square feet):\n"))
print('>> You entered {}'.format(land_square_feet))

year_built = int(input("\nPlease enter which year your property was built:\n"))
print('>> You entered {}'.format(year_built))

# model
sales_input = np.array([zipcode, land_square_feet, year_built, property_cat_le[property_cat]]).reshape(1,-1)
sales_r = joblib.load('./saved-models/random_forest_rental.pkl')

monthly_rent = sales_r.predict(sales_input)[0] / (price_index * 12)
print("\n*************************************************************************")
print("If you rent your property, you will get ${:.2f} per month!".format(monthly_rent))

utilities = 145.55
cleaning_fee = 240
broker = 0.15/12
maintenance = 1500/12

airbnb_income = (price * (30 - availability_30) - utilities) * 0.97
rental_income = monthly_rent * (1 - broker) - cleaning_fee - maintenance
print("\n*************************************************************************")
print("Excluding miscellaneous factors, your income from [airbnb] is ${:.2f}.".format(airbnb_income))
print("Excluding miscellaneous factors, your income from [regular rental] is ${:.2f}.".format(rental_income))
print ("We suggest you go with [airbnb]." if (airbnb_income > rental_income)  else "We suggest you go with [regular lease].")
