# forked from https://github.com/nsadawi/Download-Large-File-From-Google-Drive-Using-Python
#
# from https://github.com/nsadawi/Download-Large-File-From-Google-Drive-Using-Python
import requests

def download_file_from_google_drive(id, destination):
    print('downloading id=' + id + ' from Google Drive...')
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()
    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    
    
    print('finished!')

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 50000
    chunk_counter = 0
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                chunk_counter += 1
                if chunk_counter % 1000 == 0:
                    print('  ' + str(chunk_counter*CHUNK_SIZE/1000) + ' MB downloaded...' )
                    
                f.write(chunk)
