import requests
from google.cloud import storage


def search(request):
    request_json = request.get_json()
    
    storage_client = storage.Client('big-data-architecture-ricardo')
    bucket = storage_client.get_bucket('bda5-keepcoding-ricardo1')
    blob = bucket.blob('output/recommendation/000000_0')
    results = blob.download_as_string().decode('utf-8')
    
    result = "Los 5 mejores airbnb que te puedo recomendar son: \n"
    for apartment in str(results).split('\n')[0:-6]:
        apartment_parts = apartment.split(';')
        result += '{0}, A {1} mts de {2}\n'.format(apartment_parts[0], apartment_parts[2][0:4], apartment_parts[1])
    
    chat_id = 000000
    
    if request_json is not None and 'message' in request_json:
        chat_id = request_json['message']['chat']['id']
    
    requests.post(
        url='https://api.telegram.org/bot859395001:ENTERAPIKEYHERE/sendMessage',
        data={'chat_id': chat_id, 'text': result}
    ).json()
    
    return "OK"
