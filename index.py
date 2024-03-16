from flask import Flask, request, jsonify,render_template
from werkzeug.utils import secure_filename
import os
import pathlib
import textwrap
import PIL.Image
from translate import Translator
import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

app = Flask(__name__)
translator = Translator(to_lang="zh")
# 指定檔案上傳的存儲位置
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 處理檔案上傳的路由
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/uploads" ,methods = ["POST"])
def upload_file():
    if 'fileUpload' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['fileUpload']
    filelist = file.filename.split(".")
    print(filelist[1])
    if filelist[1] != 'jpg' and filelist[1] != 'png':
        return jsonify({'error': '格式錯誤'})
    
    if file:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    
    genai.configure(api_key="AIzaSyCKHTxONFZkCqBBVLALkgDDieckT7VQTTo")

    model = genai.GenerativeModel('gemini-pro')
    query = request.form["symptoms"]
    response1 = model.generate_content(f"當個專業醫生 我的症狀可能是甚麼{query}")
    
    img = PIL.Image.open(os.path.join('uploads', file.filename))

    model = genai.GenerativeModel('gemini-pro-vision')
    response2 = model.generate_content(img)
    translation = translator.translate(response2.text)
    return render_template("result.html",a=f"文字來看:{response1.text}  圖片來看:{translation}")


if __name__ == '__main__':
    app.run(debug=True)
