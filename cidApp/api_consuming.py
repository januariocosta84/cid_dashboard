import requests
from .models import WebForm, CallAndWebForm, Status
from django.utils.dateparse import parse_datetime
from django.db.utils import IntegrityError

api_url = 'https://cidwebform.tlictprojects.com/web-api/subjects/'

def call_app(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # sei fo  sai status code bainhira iha erro ruma ba koneksaun
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error calling API: {e}")
        return None

def insert_subject():
    # Bolu API lius husi URL
    response = call_app(api_url)
    
    if not response:
        print("Failed to retrieve data from the API")
        return
    
    try:
        # NIa halo pare ba Json file
        content = response.json()
        all_subjects = content
    except ValueError as e:
        print(f"Error parsing JSON response: {e}")
        return

    for subject in all_subjects:
        print(subject)
        try:
            # Chek bainhira subjec data iha ona database 
            web_form, created = WebForm.objects.get_or_create(
                id=subject['id'],  # Assume katak 'id' kata ne id uniku
                defaults={
                    'first_name': subject.get('first_name'),
                    'last_name': subject.get('last_name'),
                    'middle_name': subject.get('middle_name'),
                    'nick_name': subject.get('nick_name'),
                    'description_subject': subject.get('description_subject'),
                    'business_name': subject.get('business_name'),
                    'address': subject.get('address'),
                    'post_code': subject.get('post_code'),
                    'country': subject.get('country'),
                    'phone_num': subject.get('phone_num'),
                    'vehicle': subject.get('vehicle'),
                    'routing': subject.get('routing'),
                    'ferry': subject.get('ferry'),
                    'vessel': subject.get('vessel'),
                    'cargo': subject.get('cargo'),
                    'other_trans': subject.get('other_trans'),
                    'approx_age': subject.get('approx_age'),
                    'dob': subject.get('dob', None),
                    'nationality': subject.get('nationality'),
                    'any_other': subject.get('any_other'),
                    'what': subject.get('what'),
                    'location': subject.get('location'),
                    'quando': subject.get('quando'),
                    'how_happen': subject.get('how_happen'),
                    'how_long': subject.get('how_long'),
                    'other_infor': subject.get('other_infor'),
                    'your_connection': subject.get('your_connection'),
                    'still_connect': subject.get('still_connect'),
                    'how_did': subject.get('how_did'),
                    'others_know_information': subject.get('others_know_information'),
                    'how_many': subject.get('how_many'),
                    'affect_information': subject.get('affect_information'),
                    'if_yes': subject.get('if_yes'),
                    'prefer_anonymous': subject.get('prefer_anonymous'),
                    'an_first_name': subject.get('an_first_name'),
                    'an_last_name': subject.get('an_last_name'),
                    'an_middle_name': subject.get('an_middle_name'),
                    'an_phone_number': subject.get('an_phone_number'),
                    'an_email': subject.get('an_email'),
                    'ligar': subject.get('ligar'),
                    'created_at': parse_datetime(subject.get('created_at'))
                }
            )

            if created:
                # Atu verifika sei CAllandWebform iha ona 
                if not CallAndWebForm.objects.filter(webform=web_form).exists():
                    #Se laiha entaun kria record foun iha bases de dados 
                    #status_instance = Status.objects.first()  # Atu hetan dit status iha linha primeiro
                    #if status_instance:
                        CallAndWebForm.objects.create(
                            hotline=None,  # Set hotline hanesan none
                            webform=web_form,  # Reference ba web form object
                            type='Web Form',
                            status='Report'
                        )
                        print(f"New CallAndWebForm created for WebForm ID: {web_form.id}")
            else:
                print(f"Subject with id {web_form.id} already exists. Skipping.")

        except KeyError as e:
            print(f"Missing key in subject data: {e}")
        except IntegrityError as e:
            print(f"Error saving subject to the database: {e}")
