import os
from lib2to3.pgen2 import driver
import urllib
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
#import requests
from bs4 import BeautifulSoup as bs
#from urllib.request import urlopen as uReq
from selenium import webdriver
import glob
from ImageScrapperService.ImageScrapperService import ImageScrapperService

app = Flask(__name__)
app.config["CACHE_TYPE"] = "simple"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.after_request
def add_header(response):
    response.headers['Pragma'] = 'no-cache'
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Expires'] = '0'
    return response

@app.route('/', methods=['GET'])  # route to display the home page
@cross_origin()
def homePage():
    return render_template("index.html")

@app.route('/searchDownloadImages', methods=['GET','POST'])
def searchDownloadImages():
    global target_folder
    if request.method == 'POST':
        print("entered post")
        search_term = request.form['keyword'] # assigning the value of the input keyword to the variable keyword
        number_images = request.form['num_image']
    else:
        print("did not enter post")
    print('printing = ' + search_term)
    #chrome_options = webdriver.ChromeOptions()
    #driver = webdriver.Chrome(chrome_options=chrome_options)
    DRIVER_PATH = './chromedriver'
    #target_folder = os.path.join('static/images', '_'.join(search_term.lower().split(' '))) # make the folder name inside images with the search string
    target_folder='static/images'
    print("Target Folder: ",target_folder )
    scraper_object = ImageScrapperService() #Instance Of the class
    files = glob.glob('static/images/*')
    for f in files:
        os.remove(f)
    if not os.path.exists(target_folder):
        os.makedirs(target_folder) # make directory using the target path if it doesn't exist already


    with webdriver.Chrome(executable_path=DRIVER_PATH) as wd:
        res = scraper_object.fetch_image_urls(search_term, number_images, wd=wd, sleep_between_interactions=0.5)

    counter = 0
    for elem in res:
        scraper_object.persist_image(target_folder, elem, counter)
        counter += 1

    return show_images(target_folder)

@app.route('/showImages') # route to show the images on a webpage
@cross_origin()
def show_images(target_folder):
    print("Target Folder1: ", target_folder)
    scraper_object=ImageScrapperService() #Instantiating the object of class ImageScrapper
    list_of_jpg_files=scraper_object.list_only_jpg_files(target_folder) # obtaining the list of image files from the static folder
    #print(list_of_jpg_files)
    try:
        if(len(list_of_jpg_files)>0): # if there are images present, show them on a wen UI
            return render_template('showImage.html',user_images = list_of_jpg_files)
        else:
            return "Please try with a different string" # show this error message if no images are present in the static folder
    except Exception as e:
        print('no Images found ', e)
        return "Please try with a different string"

#port = int(os.getenv("PORT"))
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    #app.run(host='0.0.0.0', port=port)
    #app.run(host='127.0.0.1', port=8001, debug=True)

