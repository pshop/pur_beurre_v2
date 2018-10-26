# pur_beurre_v2

![Accueil](https://lh3.googleusercontent.com/amds4fUZXcAkr-lb3DEDTWLyg_sN2PASJIfOXY6vVdWy5RroTQzw6_oMeNf5PpwniNheTWBLGN6s0xVCpr12eNEx_hYXy0GApVvFaLJ2Bl7o-22zmMbSx8amougF-KxVOBd-D8bd7KziC6lUuRPq1KnSW4hnguk6EP5125JnEeejFyXDzPSk0z5WGEuAcyoOnckno4PrL6syRnfZAnKTgSZtkwbW55SX-0lzDbJq53RMDptcpcf7O7vDLV1yUf_i4wROSLXibEjNGpx0edXiHdJYbyxTzc2L3Kis5y66texAh_hvyjuTUq7nQaRShSt-F2LkrlitfMznluhLIQ4_DWlgzPGisUbJkBG9IIPxLVK-41iqfPTaEFIbUwMROprMI4wR-OLzZaJzhDE5AcgN3bF2MumWOSwozfVh3nI0QIOovSzeK0qlLvFZKkVg7RpeCyDghoiehdM3htTszh1gmfCmuoQka22IgfvxRDYAW2kibgwUtH6pmeq3XFG3CAK1bBBwch6Ojq4MqdeCUNMfXZ4LMfaqLJeD54EkJsyfOncnMVocUK7Vw_GTAERd6o9bY7JeCdpz_lIwsS8bMAbt0wh9TKau96PFCG4hahLOgX3MMnhiojxS2szOLXf8qcS1GgP2E9Hy6vYHGVgVvoZBliPP=w1227-h627-no)

Try online : [https://pur-beurre-v2.herokuapp.com](https://pur-beurre-v2.herokuapp.com)

## What is Pur Beurre ?

* Pur Beurre is an application that helps you eat healthier.
* Enter the name of a food in the search engine and Pur Beurre will suggest healthier foods to replace it.
* You can save your favorite products for viewing at any time.

## How to run it yourself ?
### Requirements:
* Python 3.7
* Django 2.1
* Pip 18.1
* Postgresql

### Run it:
* Clone or Download the Git repository.
* I suggest to create a new virtual environment with `python3 -m venv venv` for instance.
* Install all the dependencies with `pip install requirement.txt`.
* In the `settings.py`set the environment variable like this :
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '<YOUR DB NAME>',
        'USER': '<YOUR DB USER>',
        'PASSWORD':<YOUR DB PASSWORD>,
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
Note that if you what to use an other Relational database management system, you can refer to the [Django Doc](https://docs.djangoproject.com/en/2.1/ref/settings/)
* And like this:
````
SECRET_KEY = '<YOUR SECRET KEY>'
````
we are almost done,
* Now run `python manage.py makemigrations`
* And `python manage.py base_init` to fill the database with a bunch of fresh datas.


