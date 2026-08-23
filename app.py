from flask import Flask,jsonify,render_template,request
import os
import sys
from flask_cors import CORS,cross_origin
from cnnClassifier.utils.common import decodeImage
from cnnClassifier.pipeline.predict import PredictionPipeline

os.putenv('LANG','en_US.UTF-8')
os.putenv('LC_ALL','en_US.UTF-8')

app=Flask(__name__)
CORS(app)

class ClientApp:
    def __init__(self):
        self.temp_dir = 'temp'
        os.makedirs(self.temp_dir, exist_ok=True)
        self.filename = os.path.join(self.temp_dir, 'inputImage.jpg')
        self.classifier = PredictionPipeline(self.filename)


clApp = ClientApp()

@app.route('/',methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')


@app.route('/train',methods=['GET','POST'])
@cross_origin()
def trainRoute():
    os.system(f'{sys.executable} main.py')
    return "Training done Successfully"

@app.route("/predict",methods=['POST'])
@cross_origin()
def predictRoute():
    image=request.json['image']
    decodeImage(image,clApp.filename)
    result=clApp.classifier.predict()
    if os.path.exists(clApp.filename):
        try:
            os.remove(clApp.filename)
        except Exception:
            pass
    return jsonify(result)

if __name__=='__main__':
    app.run(host='0.0.0.0',port=8080)