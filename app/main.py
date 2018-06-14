from flask import Flask, render_template, request
from werkzeug import secure_filename
import json, zipfile



def fac_recog(final):
    with open("temp/about_you/face_recognition.json", "r") as read_file:
        final['facial_recognition'] = json.load(read_file)['facial_data']['example_count']
def peer_group(final):
    with open("temp/about_you/friend_peer_group.json", "r") as read_file:
        final['friend_peer_group'] = json.load(read_file)['friend_peer_group']
def address_books(final):
    with open("temp/about_you/your_address_books.json", "r") as read_file:
        final['contact_info'] = len(json.load(read_file)['address_book']['address_book'])
def ads(final):
    with open("temp/ads/ads_interests.json", "r") as read_file:
        final['ad_topics'] = json.load(read_file)['topics']
def advertisers(final):
    with open("temp/ads/advertisers_who_uploaded_a_contact_list_with_your_information.json", "r") as read_file:
        final['advertisers'] = json.load(read_file)['custom_audiences']
def apps(final):
    with open("temp/apps/installed_apps.json", "r") as read_file:
        final['apps'] = [application['name'] for application in json.load(read_file)['installed_apps']]

app = Flask(__name__)

@app.route('/')
def upload_page():
    return render_template('upload.html')

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))

    zipfile.ZipFile(f.filename).extractall(path='temp')

    final = {}

    extraction_pipe = {
        'facial_recognition': fac_recog,
        'peer_group': peer_group,
        'address_books': address_books,
        'ad_interests': ads,
        'advertisers': advertisers,
        'apps': apps
    }

    for label, func in extraction_pipe.items():
        try:
            final[label] = func(final)
        except FileNotFoundError:
            pass

    return json.dumps(final, separators=(',',':'))
