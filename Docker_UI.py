import os
from flask import Flask
from flask import render_template
from flask import request
import docker
dic={"cassandra":"spotify/cassandra","wordpress":"wordpress"}
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')


def start_image(image_name):
    docker_client = docker.Client(base_url='unix://var/run/docker.sock',
                                  version='1.12',
                                  timeout=100)
    image = dic[image_name]
    docker_client.images(name=image)
    container = docker_client.create_container(image=image)
    docker_client.start(container=container['Id'])


@app.route('/dropdown', methods=['POST'])
def process():
    if request.method == 'POST':
       selected_image=request.form['docker_image']
       start_image(selected_image)
       return "done"

    
if __name__ == '__main__':
    app.run(debug=True)
