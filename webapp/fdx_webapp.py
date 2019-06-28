from PIL import Image
from flask import Flask, flash, request, redirect, url_for, render_template, abort, session
import http, sys, traceback, os, uuid
from jinja2 import Environment, FileSystemLoader
# app.py

# inserts the path of core package to system path
sys.path.insert(0, 'E:/fashiondx/fdx_color_extractor/core')
from compute_results import compute_results
from flask_dropzone import Dropzone
app = Flask(__name__)
dropzone = Dropzone(app)
from flask_uploads import UploadSet, configure_uploads, IMAGES

# Uploads settings
app.config['UPLOADED_PHOTOS_DEST'] = os.getcwd() + '/static/uploads/photos'
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

# Dropzone settings
app.config['DROPZONE_UPLOAD_MULTIPLE'] = True
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*'
app.config['DROPZONE_REDIRECT_VIEW'] = 'results'
app.config['SECRET_KEY'] = 'supersecretkeygoeshere'
app.config['DROPZONE_MAX_FILE_SIZE']=1024  # set max size limit to a large number, here is 1024 MB
app.config['DROPZONE_TIMEOUT']=5 * 60 * 1000

@app.route('/swatch', methods=['GET', 'POST'])
def index_swatch():
    
    # set session for image resul
    if "file_urls" not in session:
        session['file_urls'] = []
    # list to hold our uploaded image urls
    file_urls = session['file_urls']
    # handle image upload from Dropzone
    if request.method == 'POST':
        session['swatch'] = True
        file_obj = request.files
        for f in file_obj:
            file = request.files.get(f)
            
            # save the file with to our photos folder
           
            filename = photos.save(
                file,
                name= str(uuid.uuid4().hex)+'.'+file.filename.split('.')[1]  
            )
            
            # append image urls
            file_urls.append({'image_url':'./static/'+'_'.join(photos.url(filename).split('_')[1:]), 'image_name':file.filename})
            
        session['file_urls'] = file_urls
       
        
        return "uploading..."
    # return dropzone template on GET request and clear the session
    else:
        session.clear()    
        return render_template('index_swatch.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    # set session for image results
    
    if "file_urls" not in session:
        session['file_urls'] = []
    # list to hold our uploaded image urls
    file_urls = session['file_urls']
    # handle image upload from Dropzone
    if request.method == 'POST':
        file_obj = request.files
        for f in file_obj:
            file = request.files.get(f)
            
            # save the file with to our photos folder
            filename = photos.save(
                file,
                name= str(uuid.uuid4().hex)+'.'+file.filename.split('.')[1]   
            )
            # append image urls
            file_urls.append({'image_url':'./static/'+'_'.join(photos.url(filename).split('_')[1:]), 'image_name':file.filename})
            
        session['file_urls'] = file_urls
        return "uploading..."
    # return dropzone template on GET request and clear the session
    else:
        session.clear()    
        return render_template('index.html')


@app.route('/results')
def results():
    # redirect to home if no images to display
    if "file_urls" not in session or session['file_urls'] == []:
        return redirect(url_for('index'))
    results=None
    # try:
    #     results = compute_results(session['file_urls'], session.get('swatch'))
    # except Exception as e:
    #     error_logs = open('./error_logs.txt', 'w')
    #     print(traceback.print_tb(e.__traceback__), file=error_logs)
    #     error_logs.close()
    #     session.clear()
    results = compute_results(session['file_urls'], session.get('swatch'))
    
    if results:
    # set the file_urls and remove the session variable
        session.pop('file_urls', None)
        session.clear()
        return render_template('results.html', results = results)
    else:
        return abort(500)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=1)




    