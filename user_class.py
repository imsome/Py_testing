import config
from config import ReportHandler
import json
import requests
import api_requests
import random


class User(object):

    def __init__(self, mail, password, delimeter=None, name="opop"):
        if delimeter:
            self.mail = mail[:mail.find('@')] + "+" + str(delimeter) + mail[mail.find('@'):]
        else:
            self.mail = mail
        self.name = name
        self.password = password
        self.token = None

    def register(self):

        ReportHandler.add_log("Registration", "Registering with user {0}".format(self.mail))
        url = config.url + api_requests.register
        body_register = {'name': self.name, 'email': self.mail, 'password': self.password}
        user_register = requests.post(url, body_register, headers=config.headers_desk)
        data = user_register.json()

        return self.token_builder(data, "Registration")

    def authorize(self):

        ReportHandler.add_log("Authorization", "Authorizing with user {0}".format(self.mail))
        url = config.url + api_requests.authorize
        body_login = {'email': self.mail, 'password': self.password}
        user_login = requests.post(url, body_login, headers=config.headers_desk)
        data = user_login.json()
        return self.token_builder(data, "Authorization")

    def token_builder(self, data, function=False):
        if not data.get('success'):
            if function:
                ReportHandler.add_log(function, "Failed to get right response\n__________________________")
                ReportHandler.add_error(function, "Could not get response:\n{0}".format(data))
            else:
                ReportHandler.add_log("Response", "Failed to get right response\n________________________")
                ReportHandler.add_error("Response", "Could not get response:\n{0}".format(data))
        else:
            data = data.get('data')
            if function:
                ReportHandler.add_log(function, "\n{0}".format(data))
            else:
                ReportHandler.add_log("Response", "\n{0}".format(data))
            try:
                self.token = data.get('token')
            except AttributeError:
                data = data[0]
                self.token = data.get('token')

    def watch_ad(self, ad_id):
        # trying_to_watch_ad
        ReportHandler.add_log("Watching add", "Trying to watch ad with id {0}".format(ad_id))
        url = config.url + api_requests.watch_ad
        param = {'token': self.token}
        view_ad = requests.get(url + str(ad_id), headers=config.headers_desk, params=param)
        if '"success": true' in view_ad:
            ReportHandler.add_log("Watch add", "successfull")
        else:
            ReportHandler.add_log("Watch add", "failed")
            ReportHandler.add_error("Watch add", str(view_ad.json()))

    def watch_random_ad(self):
        ad_id = random.randint(config.min_ad_id, config.max_ad_id)
        ReportHandler.add_log("Watching random add", "Trying to watch random add with id {0}".format(ad_id))
        url = config.url + api_requests.watch_ad
        param = {'token': self.token}
        view_ad = requests.get(url + str(ad_id), headers=config.headers_desk, params=param)
        if view_ad.json().get('success'):
            ReportHandler.add_log("Watch add", "successful")
        else:
            ReportHandler.add_log("Watch add", "failed")
            ReportHandler.add_error("Watch add", str(view_ad))

    def user_upload_image(self):
        ReportHandler.add_log("Upload image", "Trying to upload random image")
        url = config.url + api_requests.upload_image
        with open("venv/Uploads/images.json", "r") as read_file:
            photos = json.load(read_file)
        photo_path = "venv/Uploads/" + photos[0]
        body_upload = {'token': self.token}
        upload_image = requests.post(url, body_upload, headers=config.headers_desk,
                                     files={'image': open(photo_path, 'rb')})
        data = upload_image.json()
        img_id = data.get('data')
        if upload_image.json().get('success'):
            ReportHandler.add_log("Upload image", "successful, image id {0}".format(str(img_id[0].get('id'))))
        else:
            ReportHandler.add_log("Uploading image", "failed")
            ReportHandler.add_error("Watch add", str(upload_image.json()))
        return upload_image.json()

    def create_ad(self):
        ReportHandler.add_log("Creating add", "Trying to create add with your settings")
        url = config.url + api_requests.create_ad
        body_add = {'category_id': config.ad_category_id, 'location_id': config.ad_location_id, 'name': config.ad_name,
                    'description': config.ad_description,
                    'cost': config.ad_cost, 'token': self.token}
        user_register = requests.post(url, body_add, headers=config.headers_desk,
                                      files={'photos[]': open(config.ad_photos[0], 'rb')})
