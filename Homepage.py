import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import base64
from PIL import Image
import io
from datetime import datetime

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
ref = db.reference('/Services')

# Get services from Firebase
def get_services():
    services_dict = ref.get()
    services = []
    if services_dict:
        for key, value in services_dict.items():
            value['key'] = key
            services.append(value)
    return services

# Display services on homepage
services = get_services()
if services:
    st.write('## Services')
    for i in range(0, len(services), 2):
        columns = st.columns(2)
        with columns[0]:
            if 'image' in services[i]:
                decoded_image = base64.b64decode(services[i]['image'])
                st.image(Image.open(io.BytesIO(decoded_image)).resize((400, 400)), use_column_width=True)
            else:
                st.image('https://via.placeholder.com/400', width=400)
            st.write(f"### {services[i]['title']}")
            st.write(f"Location: {services[i]['location']}")
            st.write(f"Date: {services[i]['posted_on']}")
            if st.button('Details', key=services[i]['key']):
                st.session_state.service = services[i]
                st.session_state.show_details = True
        if i+1 < len(services):
            with columns[1]:
                if 'image' in services[i+1]:
                    decoded_image = base64.b64decode(services[i+1]['image'])
                    st.image(Image.open(io.BytesIO(decoded_image)).resize((400, 400)), use_column_width=True)
                else:
                    st.image('https://via.placeholder.com/400', width=400)
                st.write(f"### {services[i+1]['title']}")
                st.write(f"Location: {services[i+1]['location']}")
                st.write(f"Date: {services[i+1]['posted_on']}")
                if st.button('Details', key=services[i+1]['key']):
                    st.session_state.service = services[i+1]
                    st.session_state.show_details = True
else:
    st.write('No services found.')

# Display service details on a new page
if 'service' in st.session_state and st.session_state.show_details:
    st.write(f"## {st.session_state.service['title']}")
    if 'image' in st.session_state.service:
        decoded_image = base64.b64decode(st.session_state.service['image'])
        st.image(Image.open(io.BytesIO(decoded_image)).resize((800, 600)), use_column_width=True)
    st.write(f"### Title")
    st.session_state.service['title'] = st.text_input(f"title_{i}", st.session_state.service['title'])
    st.write(f"### Location")
    st.session_state.service['location'] = st.text_input(f"location_{i}", st.session_state.service['location'])
    st.write(f"### Organizer")
    st.session_state.service['organizer'] = st.text_input(f"organizer_{i}", st.session_state.service['organizer'])
    st.write(f"### URL")
    st.session_state.service['url'] = st.text_input(f"url_{i}", st.session_state.service['url'])
    st.write(f"### Date")
    date = datetime.strptime(st.session_state.service['posted_on'], '%Y-%m-%d')
    new_date = st.date_input(f"date_{i}", date)
    st.session_state.service['posted_on'] = new_date.strftime('%Y-%m-%d')
    st.write(f"### Appropriate for")
    st.session_state.service['appropriate_for'] = st.text_input(f"appropriate_for_{i}", ', '.join(st.session_state.service['appropriate_for'])).split(', ')
    st.write(f"### Working with")
    st.session_state.service['working_with'] = st.text_input(f"working_with_{i}", ', '.join(st.session_state.service['working_with'])).split(', ')
    st.write(f"### Description")
    st.session_state.service['description'] = st.text_area(f"description_{i}", st.session_state.service['description'])
    if st.button('Update'):
        ref.child(st.session_state.service['key']).update(st.session_state.service)
        st.write('Service updated successfully!')
    if st.button('Delete'):
        ref.child(st.session_state.service['key']).delete()
        st.write('Service deleted successfully!')
        st.session_state.show_details = False
    if st.button('Back'):
        st.session_state.show_details = False

    # Hide the services on the homepage
    st.markdown("<style>div[data-testid='stHorizontalBlock'] {display: none;}</style>", unsafe_allow_html=True)