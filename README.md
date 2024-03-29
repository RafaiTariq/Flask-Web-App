# Deploy Keras Model with Flask as Web App 

> A pretty and customizable multi page web app built on Flask to deploy your DL model with ease. 



## Getting started

- Clone this repo 
- Install requirements
- Run the script
- Go to http://localhost:5000
- Done! :tada:



## Local Installation

It's easy to install and run it on your computer.

```shell
# 1. First, clone the repo
$ git clone https://github.com/RafaiTariq/Flask-Web-App.git
$ cd Flask-Web-App

# 2. Install Python packages
$ pip install -r requirements.txt

# 3. Run!
$ python -m flask run
```

Open http://localhost:5000 and have fun. :smiley:


## Pages

- Image Classifier


<p align="center">
<img src="https://github.com/RafaiTariq/Flask-Web-App/blob/main/Media/Image%20Classifier%20gif.gif" height="395px" width="800px" alt="">
</p>



- Color recognizer 


<p align="center">
<img src="https://github.com/RafaiTariq/Flask-Web-App/blob/main/Media/Color%20Recognizer%20Gif.gif" height="395px" width="800px" alt="">
</p>

------------------

## Customization

It's also easy to customize and include your models in this app.

<details>
 <summary>Details</summary>

### Use your own model

Place your trained `.h5` file saved by `model.save()` under models directory.

### Use other pre-trained model

See [Keras applications](https://keras.io/applications/) for more available models such as DenseNet, MobilNet, NASNet, etc.

Check [this section](https://github.com/RafaiTariq/Flask-Web-App/blob/100b92ca0e2b192c003a4320c2cf11ec54e6c097/app.py#L30) in app.py.
