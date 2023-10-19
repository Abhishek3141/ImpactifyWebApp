import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from PIL import Image
import io
import base64

# Initialize Firebase
cred = credentials.Certificate('impactify-b2f68-firebase-adminsdk-6r32m-3ed1a596a2.json')
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://impactify-b2f68-default-rtdb.firebaseio.com'
    })

# Create a new Credentials object
creds = None
while not creds:
    try:
        creds = service_account.Credentials.from_service_account_file(
            'impactify-b2f68-firebase-adminsdk-6r32m-3ed1a596a2.json',
            scopes=['https://www.googleapis.com/auth/firebase.database']
        )
        creds.refresh(Request())
    except Exception as e:
        print(e)

# Get a reference to the database
ref = db.reference('/')

# Create text boxes for inputs
title = st.text_input('Title')
location = st.text_input('Location')
organizer = st.text_input('Organizer')
url = st.text_input('URL')
posted_on = st.date_input('Posted on')
appropriate_for = st.multiselect('Appropriate for', ['Students', 'Parents', 'Teachers'])
working_with = st.multiselect('Working with', ['People', 'Animals', 'Environment'])
images = st.file_uploader('Images', accept_multiple_files=True, type=['png', 'jpeg'])
description = st.text_area('Description')

# Save data to Firebase
if st.button('Submit'):
    data = {
        'title': title,
        'location': location,
        'organizer': organizer,
        'url': url,
        'posted_on': str(posted_on),
        'appropriate_for': appropriate_for,
        'working_with': working_with,
        'description': description
    }
    if images:
        for image in images:
            img = Image.open(io.BytesIO(image.read()))
            img = img.convert('RGB')
            img_buffer = io.BytesIO()
            img.save(img_buffer, format='PNG')
            encoded_image = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
            data['image'] = encoded_image
    ref.child('Services').child(title).set(data)
    st.success('Data saved to Firebase!')