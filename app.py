from flask import Flask, request, render_template
import requests
import base64

app = Flask(__name__)

icons = []


@app.route('/', methods=['GET', 'POST'])
def index():
    global icons
    if request.method == 'POST' and 'appid' in request.form:
        appid = request.form['appid']
        url = f"https://microsoft-store.azurewebsites.net/store/detail/{appid}/image"
        response = requests.get(url, allow_redirects=True)
        if response.status_code == 200:
            image_data = response.content
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            image_data = f"data:image/png;base64,{image_base64}"
            preview_image = f'<img src="{image_data}" alt="Preview" width="100">'
            icons.append({
                'appid': appid,
                'image_data': image_data,
                'preview_image': preview_image
            })
    elif request.method == 'POST' and 'clear' in request.args:
        icons = []
    return render_template('index.html', icons=icons)


if __name__ == '__main__':
    app.run()
