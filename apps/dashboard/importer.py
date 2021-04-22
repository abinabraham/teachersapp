import pandas as pd

from apps.accounts.models import (Teacher,
                                     Subject)

def importer_function(file):
	df=pd.read_csv(file,sep=';')

	row_iter = df.iterrows()

	objs = [

	    Teacher(

	        first_name = row['First Name'],

	        last_name  = row['Last Name'],

	        profile_pic  = row['Profile picture'],

	        email  = row['Email Address'],

	        phone_number = row['Phone Number'],

	        room_number = row['Room Number,']

	    )

	    for index, row in row_iter

	]

	myClass_in_model.objects.bulk_create(objs)