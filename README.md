
<img align="right" width="200" height="200" src="https://github.com/GabrielMMelo/pyiot-api/blob/master/docs/logo.png" alt="PyIoT's logo">

# PyIoT
> Your home controller _powered by python_

This project was splitted out in 3 repositories:
- [Api application](https://github.com/GabrielMMelo/pyiot-api.git) - Django, DRF, Django Channels, PostgreSQL & Redis 
- [Front-end application](https://github.com/GabrielMMelo/pyiot-fe.git) - React & Redux
> It's not python, but is okay...

- [MicroPython application](https://github.com/GabrielMMelo/pyiot-mp.git) - MicroPython

**PyIoT** aims to be a scalable home controller application which you can easily add/remove nodes and get the whole controll of your home devices.

## Running

To get started with the PyIoT, just follow this steps below.

#### Install Redis server

```shell
apt install redis-server
redis-server
```

#### Clone this repo
```shell
git clone https://github.com/GabrielMMelo/pyiot-api
cd pyiot-api/
mkvirtualenv pyiot
pip install -r requirements.txt
```

#### Run the application
```shell
python manage.py runserver 0.0.0.0:8000
```

> You'll also need to follow the steps described in the two anothers repos as well

## Deploying
**TODO***

## Testing
**TODO***

## Contributing
**TODO***
