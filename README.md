# Rafflee

![platform](https://img.shields.io/badge/django%20versions-2.2.8-blue.svg)

Readme of the project Rafflee

Contents

* [Description](#description)
* [Platfrom and requirements](#platform-and-requirements)
* [Getting started](#getting-started)
    * [Installation](#installation)
    * [Configuration](#configuration)
    * [Launch](#launch)
    * [Monitoring](#monitoring)
* [API](#api)

## Description

This part of Rafflee is the backend part of the webplatform that brings our webservices
closer to the users.

* [Documentation](https://rafflee.rafflee-doc.com/rafflee/rafflee_api/)
* [Changelog](CHANGELOG.md)

Authors:
* Killian Bellesoeur

## Platform and requirements

* Python version: 3.5
* Django version: 2.2.8
* Requirements in [Pipfile](Pipfile)

## Getting started

### Installation

##### Clone the project
    git clone git@gitlab.com:rafflee/rafflee.git

##### Install pip
    sudo apt install python-pip     # debian based OS

    sudo yum install python-pip     # redhat/centos

    sudo dnf install python-pip     # fedora

    sudo pacman -S python-pip       # archlinux

    sudo easy_install pip           # macOS

##### Install pipenv
    sudo pip install pipenv

##### Initialize your work space
    cd rafflee

    pipenv install --dev --python=3.5 && pipenv shell   # install python requirements and run virtualenv

### Configuration



#### Database

##### Method 1: use Docker

You need to have Docker installed, up and running (installation: [Ubuntu](https://docs.docker.com/v17.12/install/linux/docker-ce/ubuntu/), [Fedora](https://docs.docker.com/v17.12/install/linux/docker-ce/fedora/), [Debian](https://docs.docker.com/v17.12/install/linux/docker-ce/debian/), [CentOS](https://docs.docker.com/v17.12/install/linux/docker-ce/centos/), [Mac](https://docs.docker.com/v17.12/docker-for-mac/install/))

To run a postgresql container with a `rafflee` (empty) database, `admin` user with password `AdminPaSsWoRd`, use the following command:

*if your current user isn't in the `docker` group, you have to run the command with `sudo`*

    docker run --name postgresql_rafflee -e POSTGRES_DB=rafflee -e POSTGRES_PASSWORD=AdminPaSsWoRd -e POSTGRES_USER=admin -p 5432:5432 -d --mount "source=postgresql-data,target=/var/lib/postgresql/" postgres

Now you have a postgresql server running on `localhost`, port `5432`.
How to manage your container:

    docker container ls                     # list running containers
    docker container ls --all               # list all containers
    docker container stop postgresql_diaas  # stop container
    docker container start postgresql_diaas # start container
    docker container rm postgresql_diaas    # delete container

If you have postgres-client installed, you can run the postrgesql prompt:

    psql -h localhost -U admin -d rafflee


##### Method 2: local PostgreSQL database

   (installation: [debian](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-16-04))    

    # install postgresql in your local environment

    psql -U user_name   # login to postgre console
    CREATE DATABASE rafflee;   # create the database

#### Environment

    # copy the .env.example file
    cp .env.example .env
    # open your .env file and adjust vars to your environment
    vim .env

#### Initialization of the database
    cd rafflee

    pipenv shell    # if you are not in the virtualenv

    python manage.py makemigrations account
    python manage.py makemigrations company
    python manage.py makemigrations promotion
    python manage.py migrate

#### Generate static files

    python manage.py collectstatic

### Launch

    pipenv shell
    python manage.py runserver
    redis-server --port 6380
    celery -A rafflee worker -B -l INFO
    celery -A rafflee beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler

### Monitoring

    sudo apt-get install cockpit
    https://ip:9090/

## Api

Rafflee's rest API uses JWT tokens to confirm the API call by the user. When connecting this one a token is generated which must be stored locally. This token will be used to call the roads.

### Connection

#### /login/

This endpoint connects the user.


#### `POST /{locale}/login/`

###### Parameters entry

```json
{
	"username" : "usertest",
	"password" : "usertestpassword",
    "ip": "192.168.12.19",
    "device_id": "iphone 11"
}
```

###### Responses

> 200 Response

```json
{
    "company": false,
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1LCJvcmlnX2lhdCI6MTU4MjAzOTY3MywiZXhwIjoxNjEzNTc1NjczLCJvdHBfZGV2aWNlX2lkIjpudWxsLCJ1c2VybmFtZSI6InRlc3Rjb21wYW55In0.j5j_2vwyanhxsw1-z8yx33azDhg6H8xwgOB5RwCdpj4",
}
```

If the user account is a company account the company response will be true.
Save the token on the local storage to use it as authorization during the next API calls.

#### /login/facebook/

This endpoint connects the user.


#### `POST /{locale}/login/facebook/`

###### Parameters entry

```json
{
	"access_token" : "EAAIFlcbZC0PkrfPisPxAXEimjBxrs2zyal2E0M5J4cJDUEEKi390ZBoHHVke4j8jkj...",
    "ip": "192.168.12.19",
    "device_id": "iphone 11"
}
```

###### Responses

> 200 Response

```json
{
    "company": false,
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1LCJvcmlnX2lhdCI6MTU4MjAzOTY3MywiZXhwIjoxNjEzNTc1NjczLCJvdHBfZGV2aWNlX2lkIjpudWxsLCJ1c2VybmFtZSI6InRlc3Rjb21wYW55In0.j5j_2vwyanhxsw1-z8yx33azDhg6H8xwgOB5RwCdpj4",
}
```

If the user account is a company account the company response will be true.
Save the token on the local storage to use it as authorization during the next API calls.


#### /login/google/

This endpoint connects the user.


#### `POST /{locale}/login/google/`

###### Parameters entry

```json
{
	"access_token" : "EAAIFlcbZC0PkrfPisPxAXEimjBxrs2zyal2E0M5J4cJDUEEKi390ZBoHHVke4j8jkj...",
    "ip": "192.168.12.19",
    "device_id": "iphone 11",
    "device": "web"
}
```

parameters device can be: ios/android/web

###### Responses

> 200 Response

```json
{
    "company": false,
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1LCJvcmlnX2lhdCI6MTU4MjAzOTY3MywiZXhwIjoxNjEzNTc1NjczLCJvdHBfZGV2aWNlX2lkIjpudWxsLCJ1c2VybmFtZSI6InRlc3Rjb21wYW55In0.j5j_2vwyanhxsw1-z8yx33azDhg6H8xwgOB5RwCdpj4",
}
```

If the user account is a company account the company response will be true.
Save the token on the local storage to use it as authorization during the next API calls.


#### `POST /{locale}/login/google/authorization-url/`

###### Parameters entry

```json
{
  None
}
```

###### Responses

> 200 Response

```json
{
    "authorization_url": "https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=644186892132-tp25ugmpmskn5usvjn509r4otqjds7c5.apps.googleusercontent.com&redirect_uri=https%3A%2F%2Frafflee.io%2Flogin%2Fgoogle%2Fcallback&scope=openid+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile&state=GnMS2oSSzzJgNb35mj7Q7CPCF67kgC&access_type=offline"
}
```

Redirect the user on the authorization url.

#### /login/google/

#### `POST /{locale}/login/google/`

###### Parameters entry

```json
{
	"code" : "EAAIFlcbZC0PkrfPisPxAXEimjBxrs2zyal2E0M5J4cJDUEEKi390ZBoHHVke4j8jkj...",
    "ip": "192.168.12.19",
    "device_id": "iphone 11"
}
```

###### Responses

> 200 Response

```json
{
    "company": false,
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1LCJvcmlnX2lhdCI6MTU4MjAzOTY3MywiZXhwIjoxNjEzNTc1NjczLCJvdHBfZGV2aWNlX2lkIjpudWxsLCJ1c2VybmFtZSI6InRlc3Rjb21wYW55In0.j5j_2vwyanhxsw1-z8yx33azDhg6H8xwgOB5RwCdpj4",
}
```

If the user account is a company account the company response will be true.
Save the token on the local storage to use it as authorization during the next API calls.


#### /twitter/connect/

#### `POST /{locale}/twitter/connect/<int:step>/`

Connection with twitter

###### Parameters entry

params:
    
    step: 1 or 2 it depends on the process

step 1
    
    headers: 'Authorization' : 'JWT ' + token,

```json
    Params: None
```

###### Responses

> 200 Response

```json
{
    "oauth_token": "QF849AAAAAABDH6cAAABcYN5oDU",
    "msg": "MSG_OAUTH_TOKEN_TWITTER",
    "status": 200
}
```

step 2
    
    headers: 'Authorization' : 'JWT ' + token,

```json
    oauth_token: 2z-05AAAAAABDH6cAAABcYNiSz4
    oauth_verifier: xvsovR0MW90drVdB3mZnXxXyozvqNwwr
```

###### Responses

> 200 Response

```json
{
    "status": 200,
    "msg": "MSG_TWITTER_LOGIN_VALIDATED"
}
```

#### /snapchat/connect/

#### `POST /{locale}/snapchat/connect/<int:step>/`

Connection with snapchat

###### Parameters entry

params:
    
    step: 1 or 2 it depends on the process

step 1
    
    headers: 'Authorization' : 'JWT ' + token,

```json
    Params: None
```

###### Responses

> 200 Response

```json
{
    "url": "https://accounts.snapchat.com/login/oauth2/authorize?response_type=code&client_id=23f94f1e-b362-4d7b-a41a-7185762e856d&redirect_uri=https%3A%2F%2Frafflee.io%2Fsnapchat%2Fconnect%2F&scope=snapchat-marketing-api&state=prXak0XrjK1G7uhtCEWvsAJUj3NYLa",
    "msg": "MSG_OAUTH_SNAPCHAT_URL",
    "status": 200
}
```

step 2
    
    headers: 'Authorization' : 'JWT ' + token,

```json
    url: https://rafflee.io/snapchat/connect/?code=uepgctnYFoYTQjgTRIws_TlkqNFRX8GqRJ6AFfsZmFo&state=prXak0XrjK1G7uhtCEWvsAJUj3NYLa
```

###### Responses

> 200 Response

```json
{
    "msg": "MSG_SNAPCHAT_LOGIN_VALIDATED",
    "status": 200
}
```

#### /twitch/connect/

#### `POST /{locale}/twitch/connect/`

Connection with twitch

###### Parameters entry
    
    headers: 'Authorization' : 'JWT ' + token,

```json
    token: 2z-05AAAAAABDH6cAAABcYNiSz4
```

###### Responses

> 200 Response

```json
{
    "status": 200,
    "msg": "MSG_TWITCH_LOGIN_VALIDATED"
}
```

#### /instagram/connect/

#### `POST /{locale}/instagram/connect/`

Connection with twitch

###### Parameters entry
    
    headers: 'Authorization' : 'JWT ' + token,

```json
    token: 2z-05AAAAAABDH6cAAABcYNiSz4
```

###### Responses

> 200 Response

```json
{
    "status": 200,
    "msg": "MSG_INSTAGRAM_LOGIN_VALIDATED"
}
```

#### /facebook/connect/

#### `POST /{locale}/facebook/connect/`

Connection with twitch

###### Parameters entry
    
    headers: 'Authorization' : 'JWT ' + token,

```json
    token: 2z-05AAAAAABDH6cAAABcYNiSz4
```

###### Responses

> 200 Response

```json
{
    "status": 200,
    "msg": "MSG_FACEBOOK_AUTHORIZATION_VALIDATED"
}
```


#### /facebook/connect/instagram_business/

#### `POST /{locale}/facebook/connect/instagram_business/`

Connection with twitch

###### Parameters entry
    
    headers: 'Authorization' : 'JWT ' + token,

```json
    token: 2z-05AAAAAABDH6cAAABcYNiSz4
```

###### Responses

> 200 Response

```json
{
    "status": 200,
    "msg": "MSG_INSTAGRAM_BUSINESS_PAGE_RETURNED"
}
```


#### /facebook/connect/instagram_business/validation/

#### `POST /{locale}/facebook/connect/instagram_business/validation/`

Connection with twitch

###### Parameters entry
    
    headers: 'Authorization' : 'JWT ' + token,

```json
    id: 2726381279318
```

###### Responses

> 200 Response

```json
{
    "status": 200,
    "msg": "MSG_INSTAGRAM_BUSINESS_AUTHORIZATION_VALIDATED"
}
```


#### /logout/

This endpoint disconnects the user.

#### `POST /{locale}/logout/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
    None
```

###### Response

> 200 Response

```json
{
    "msg": "MSG_USER_LOGOUT",
    "status": 200
}
```

Don't forget to remove the token to the localstorage.

### Favorites

#### /favorites/campaign/

This endpoint list all user's favorites.

#### `GET /{locale}/favorites/campaign/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
  None
```

###### Response

> 200 Response

```json
{
    "result_data": [
        {
            "id": 1,
            "promotion": "Adidas Campaign"
        }
    ],
    "is_error": 0,
    "msg": "FAVORITE_FOUNDED",
    "status": 200
}
```

#### /favorites/company/

This endpoint list all user's favorites company.

#### `GET /{locale}/favorites/company/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
  None
```

###### Response

> 200 Response

```json
{
    "msg": "MSG_FAVORITE_FOUNDED",
    "status": 200,
    "result_data": [
        {
            "description": null,
            "type_of_account": "influencer",
            "logo_url": null,
            "id": 1,
            "company_name": "NewBalance",
            "certified": false
        },
        {
            "description": null,
            "type_of_account": "influencer",
            "logo_url": null,
            "id": 2,
            "company_name": "NewBalance2",
            "certified": false
        }
    ],
    "is_error": 0
}
```

#### /favorites/update/campaign/

This endpoint create a new user's favorite or delete it if favorite exist.

#### `POST /{locale}/favorites/update/campaign/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
{
    "promotion_id" : "1"
}
```

###### Response

> 200 Response

```json
{
    "promotion_id": 12,
    "msg": "FAVORITE_ADDED",
    "status": 200
}
```

#### /favorites/remove/follow/

This function permit to remove follow subscription for an user.

#### `POST /{locale}/favorites/remove/follow/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
{
    "company_id" : "1"
}
```

###### Response

> 200 Response

```json
{
    "company_id": 12,
    "msg": "MSG_SUBSCRIPTION_FOLLOW_DELETED",
    "status": 200
}
```

#### /favorites/remove/newsleter/

This function permit to remove newsletter subscription for an user.

#### `POST /{locale}/favorites/remove/newsletter/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
{
    "company_id" : "1"
}
```

###### Response

> 200 Response

```json
{
    "company_id": 12,
    "msg": "MSG_SUBSCRIPTION_NEWSLETTER_DELETED",
    "status": 200
}
```

### Account

#### /account/register/

This endpoint register a new user.

#### `POST /{locale}/account/register/`

###### Parameters entry


```json
{
    "username": "testuser",
    "email": "testuser@test.com",
    "password1": "PasswordTestUser",
    "password2": "PasswordTestUser"
}
```

###### Response

> 200 Response

```json
{
    "msg": "USER_CREATED",
    "status": 200
}
```

#### /account/profile/

This endpoint return the user's profile.

#### `GET /{locale}/account/profile/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
  None
```

###### Response

> 200 Response

```json
{
    "user_informations": {
        "city": "Paris",
        "email": "test@test.com",
        "country_code": 33,
        "profile_picture": "",
        "firstname": "killian",
        "birth_date": "1992-04-23",
        "twitter": true,
        "lastname": "bellesoeur",
        "address": "21 rue de la liberte",
        "national_number": 655230615,
        "country": "France",
        "gender": "male",
        "region": "Ile de france",
        "username": "ewokewokw"
    },
    "msg": "USER_INFORMATION_RETRIEVED"
}
```

#### /account/profile/username/

This endpoint return true if the username exist and false if the username not exist.

#### `GET /{locale}/account/profile/username`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
{
    "username": "ewuidjewoicjw"
}
```

###### Response

> 200 Response

```json
{
    "exist": true,
    "msg": "MSG_USERNAME_EXIST"
}
```





#### `GET /{locale}/account/wall/settings/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
{
}
```

###### Response


> 200 Response

```json
{
    "msg": "MSG_WALL_SETTINGS_RETURNED",
    "instagram": true,
    "twitter": true,
    "facebook": {
        "activate": true,
        "id": "reververv"
    },
    "status": 200
}
```


#### `POST /{locale}/account/wall/settings/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
{
  "twiter": true,
  "instagram": true,
  "facebook": {
    "id": "eeercjoejcoiwjiejw",
    "activate": true
  }
}
```

###### Response


> 200 Response

```json
{
  "msg": "MSG_WALL_SETTINGS_UPDATED",
  "status": 200
}
```


#### `GET /{locale}/account/wall/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
  None
```

###### Response


> 200 Response

```json
{
    "msg": "MSG_SOCIAL_WALL",
    "wall": {
        "twitter": {
            "error": false,
            "verified": false,
            "name": "JEan Valgeant",
            "followers": 201,
            "tweets": [
                {
                    "retweeted": false,
                    "created_at": "Fri Apr 17 12:40:42 +0000 2020",
                    "text": "test 5 #test"
                },
                {
                    "retweeted": false,
                    "created_at": "Fri Apr 17 12:36:28 +0000 2020",
                    "text": "test 4 https://t.co/mcQnOENdzf"
                },
                {
                    "retweeted": false,
                    "created_at": "Fri Apr 17 12:34:42 +0000 2020",
                    "text": "Test 3"
                }
            ],
            "profile_image_url": "https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png",
            "friends": 26
        },
        "instagram": {
            "publication": [
                {
                    "username": "killianbelles",
                    "text": "#morningview #bahrain",
                    "created_at": "2019-02-01T11:33:10+0000",
                    "permalink": "https://www.instagram.com/p/BtVwm7OmgIFn/"
                },
                {
                    "username": "killianbelles",
                    "text": "#sunset #bahrain",
                    "created_at": "2018-10-20T13:02:35+0000",
                    "permalink": "https://www.instagram.com/p/BpJ-fGUvgFs8/"
                },
                {
                    "username": "killianbelles",
                    "text": "#holydays #thailand #phuket 🇹🇭",
                    "created_at": "2018-08-21T11:33:45+0000",
                    "permalink": "https://www.instagram.com/p/BmvUnw9PBZP0/"
                },
        },
        "facebook": {
            "page_informations": {
                "picture": {
                    "data": {
                        "url": "https://scontent-cdg2-1.xx.fbcdn.net/v/t1.0-1/cp0/p50x50/106488973_101514908298029_3737235319359090931_o.png?_nc_cat=104&_nc_sid=dbb9e7&_nc_ohc=hZGJRdMR3z8AX9dKjqv&_nc_ht=scontent-cdg2-1.xx&oh=354b26487aeedd2101f2c439aea8a72d&oe=5F2A24C0"
                    }
                },
                "id": "101514858298034",
                "fan_count": 1,
                "website": "https://rafflee.io",
                "link": "https://www.facebook.com/101514858298034",
                "verification_status": "not_verified"
            },
            "error": false,
            "publication": [
                {
                    "created_time": "2020-07-01T16:18:01+0000",
                    "story": "Rafflee, surexcité(e).",
                    "id": "101514858298034_101580514958135",
                    "message": "test1"
                },
                {
                    "created_time": "2020-07-01T14:24:46+0000",
                    "id": "101514858298034_101515328297987",
                    "message": "On test l'api"
                }
            ]
        },
    },
    "status": 200
}
```

#### /account/profile/update/

This endpoint return the user's profile.

#### `POST /{locale}/account/profile/update/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
{
    "profile_picture": "/9j/4gIcSUNDX1BST0ZJTEUAAQEAAgAAP/tADZQaG90b3Nob3AgMy4wADhCSU0EBAAAAAAAKMYML5n/2Q==",
    "phone_number": "656243918",
    "prefix_number": "+33",
    "country": "France",
    "region": "Ile de france",
    "birth_date": "1994-08-22",
    "first_name": "Jean",
    "last_name": "Bouvier",
    "city": "Paris",
    "gender": "male",
    "address": "21 avenue de la liberte",
    "username": "wiwjdiwjw"
}
```

###### Response

> 200 Response

```json
{
    "msg": "USER_INFORMATION_UPLOADED",
    "status": 200
}
```

#### /account/password/reset/email/

This endpoint send a reset email with a code.

#### `POST /{locale}/account/password/reset/email/`

###### Parameters entry

```json
{
    "email": "testuser@test.com"
}
```

###### Response

> 200 Response

```json
{
    "msg": "EMAIL_RESET_PASSWORD_SENDED",
    "status": 200
}
```

#### /account/password/reset/

This endpoint permit to reset the user password.

#### `POST /{locale}/account/password/reset/`

###### Parameters entry

```json
{
    "email": "testuser@test.com",
    "password": "newSuperPassword",
    "password_confirmation": "newSuperPassword",
    "token": "5dy-ca6df2602465cd1b8c96"

}
```

###### Response

> 200 Response

```json
{
    "msg": "PASSWORD_UPDATED",
    "status": 200
}
```

#### /account/follow/<int:id>/

This endpoint permit to follow a company account.

#### `POST /{locale}/account/follow/<int:id>/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
{
    "joign_cercle": true,
    "newsletter": true
}
```

###### Response

> 200 Response

```json
{
    "msg": "MSG_SUBSCRIPTION_CREATED",
    "status": 200
}
```

#### /account/unfollow/<int:id>/

This endpoint permit to unfollow a company account.

#### `POST /{locale}/account/unfollow/<int:id>/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
{
  None
}
```

###### Response

> 200 Response

```json
{
    "msg": "MSG_UNFOLLOW_CIRCLE",
    "status": 200
}
```

#### /account/result/{int:id}/

This endpoint returns the result of participation in a campaign.

#### `GET /{locale}/account/result/{int:id}/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
    id: id of the campaign
```

###### Response

> 200 Response

```json
{
    "is_error": 0,
    "msg": "PROMOTION_FOUNDED",
    "status": 200,
    "result_data": [
        {
            "name": "50%",
            "user": "test1",
            "description": "50% of reduction",
            "expiration_date": "2020-05-20",
            "promotion": "Promotion Basket"
        }
    ]
}
```

#### /account/number/send-sms/

This endpoint send a sms to the user with a token.

#### `POST /{locale}/account/number/send-sms/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
{
    "number": "+33103040596"
}
```

###### Response

> 200 Response

```json
{
    "msg": "SMS_SENDED",
    "status": 200
}
```

#### /account/number/verification/

This endpoint permit to confirm the validity of a phone number.

#### `POST /{locale}/account/number/verification/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
{
    "number": "+33103040596",
    "code": "449515"
}
```

###### Response

> 200 Response

```json
{
    "msg": "PHONE_NUMBER_CONFIRMED",
    "status": 200
}
```

#### /account/profile/deactivate/

This endpoint permit to deactivate user profile.

#### `POST /{locale}/account/profile/deactivate/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
{
    "password": "superPAssword"
}
```

###### Response

> 200 Response

```json
{
    "msg": "USER_DEACTIVATE",
    "status": 200
}
```

### Company

#### /company/register/

This endpoint register a new company.

#### `POST /{locale}/company/register/`

###### Parameters entry


```json
{
    "username": "testuser",
    "email": "testuser@test.com",
    "password1": "PasswordTestUser",
    "password2": "PasswordTestUser",
    "entity_name": "Rafflee",
    "is_company": "true"
}
```

is_company: can be true or false. True if it is a company and false if it is an influencer.

###### Response

> 200 Response

```json
{
    "status": 200,
    "msg": "USER_AND_COMPANY_CREATED"
}
```

#### /company/contact-form/

Create a contact form to get in touch with the company.

#### `POST /{locale}/company/contact-form/`

###### Parameters entry


```json
{
    "email": "contactuser@test.com",
    "phone_number": "0192837465",
    "company_name": "Adidas",
    "message": "Hi..."
}
```

###### Response

> 200 Response

```json
{
    "status": 200,
    "msg": "SAVED_REQUEST"
}
```

#### `GET /{locale}/company/wall/<int:id>/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
    id: id of the company
```

###### Response

> 200 Response

```json
{
    "msg": "MSG_SOCIAL_WALL",
    "wall": {
        "twitter": {
            "error": false,
            "verified": false,
            "name": "JEan Valgeant",
            "followers": 201,
            "tweets": [
                {
                    "retweeted": false,
                    "created_at": "Fri Apr 17 12:40:42 +0000 2020",
                    "text": "test 5 #test"
                },
                {
                    "retweeted": false,
                    "created_at": "Fri Apr 17 12:36:28 +0000 2020",
                    "text": "test 4 https://t.co/mcQnOENdzf"
                },
                {
                    "retweeted": false,
                    "created_at": "Fri Apr 17 12:34:42 +0000 2020",
                    "text": "Test 3"
                }
            ],
            "profile_image_url": "https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png",
            "friends": 26
        },
        "instagram": {
            "publication": [
                {
                    "username": "killianbelles",
                    "text": "#morningview #bahrain",
                    "created_at": "2019-02-01T11:33:10+0000",
                    "permalink": "https://www.instagram.com/p/BtVme7OmgIFn/"
                },
                {
                    "username": "killianbelles",
                    "text": "#sunset #bahrain",
                    "created_at": "2018-10-20T13:02:35+0000",
                    "permalink": "https://www.instagram.com/p/BpJ-fGdUgFs8/"
                },
                {
                    "username": "killianbelles",
                    "text": "#holydays #thailand #phuket 🇹🇭",
                    "created_at": "2018-08-21T11:33:45+0000",
                    "permalink": "https://www.instagram.com/p/BmfvUn9PBZP0/"
                },
        },
    },
    "status": 200
}
```

#### /company/bills/

List all the company bills.

#### `GET /{locale}/company/bills/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
    None
```

###### Response

> 200 Response

```json
{
    "is_error": 0,
    "status": 200,
    "result_data": [
        {
            "price": "100.00",
            "emission_date": "2020-02-18T16:23:58.904Z",
            "id": 1,
            "promotion": "Promotion Basket"
        }
    ],
    "msg": "PROMOTION_FOUNDED"
}
```

#### /company/{int:id}/

This endpoint return returns the all informations about a company.

#### `POST /{locale}/company/{int:id}/`

###### Parameters entry

```json
    id: id of the company
```

```json
    params

    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJ4ODSz4jzv-jajQig..." 
```

token need to appear on the parameters, if user is not connected token will be None

###### Response

> 200 Response

```json
{
    "status": 200,
    "msg": {
        "company": {
            "instagram_page_url": null,
            "type_of_account": "influencer",
            "certified": false,
            "newsletter": null,
            "number_of_follower": 0,
            "logo_url": null,
            "website_url": null,
            "twitter_page_url": null,
            "pk": 1,
            "youtube_channel": null,
            "description": null,
            "member_since": "2020-05-19T14:47:26.293667Z",
            "follow": null,
            "company_name": "NewBalance",
            "facebook_page_url": null
        },
        "social_wall": {
            "twitter": {
                "friends": 0,
                "profile_image_url": "https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png",
                "followers": 1,
                "verified": false,
                "tweets": [
                    {
                        "retweeted": false,
                        "created_at": "Tue Apr 21 14:33:05 +0000 2020",
                        "text": "J'ai participe au super nouveau tirage au sort de rafflee sur https://t.co/X3am1kv2B6"
                    },
                    {
                        "retweeted": false,
                        "created_at": "Fri Apr 17 12:40:42 +0000 2020",
                        "text": "test 5 #test"
                    },
                    {
                        "retweeted": false,
                        "created_at": "Fri Apr 17 12:36:28 +0000 2020",
                        "text": "test 4 https://t.co/mcQnOENdzf"
                    },
                    {
                        "retweeted": false,
                        "created_at": "Fri Apr 17 12:34:42 +0000 2020",
                        "text": "Test 3"
                    }
                ],
                "error": false,
                "name": "killian bellesoeur"
            }
        }
    }
}
```

#### /company/bill/{int:id}/

This endpoint return returns the invoice for the campaign given as a parameter with the PDF document.

#### `GET /{locale}/company/bill/{int:id}/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
    id: id of the campaign
```

###### Response

> 200 Response

```json
{
    "is_error": 0,
    "status": 200,
    "result_data": "JVBERi0xLjQKJZOMi54FnZQo+PgplbmRvYmoKNSAwIG9iago8PAovUGFnZU1vZGUgL1VzZU5vbmUgL1BhZ2VzIDcgMCBSIC9UeXBlIC9DYXRhbG9nCj4+CmVuZG9iago2IDAgb2JqCjw8Ci9BdXRob3IgKCkgL0NyZWF0aW9uRGF0ZSAoRDoyMDIwMDIxODE2MjM1OSswMCcwMCcpIC9DcmVhdG9yIChcKHVuc3BlY2lmaWVkXCkpIC9LZXl3b3JkcyAoKSAvTW9kRGF0ZSAoRDoyMDIwMDIxODE2MjM1OSswMCcwMCcpIC9Qcm9kdWNlciAoeGh0bWwycGRmIDxodHRwczovL2dpdGh1Yi5jb20veGh0bWwycGRmL3hodG1sMnBkZi8+KSAKICAvU3ViamVjdCAoKSAvVGl0bGUgKFRpdGxlKSAvVHJhcHBlZCAvRmFsc2UKPj4KZW5kb2JqCjcgMCBvYmoKPDwKL0NvdW50IDEgL0tpZHMgWyA0IDAgUiBdIC9UeXBlIC9QYWdlcwo+PgplbmRvYmoKOCAwIG9iago8PAovRmlsdGVyIFsgL0FTQ0lJODVEZWNvZGUgL0ZsYXRlRGVjb2RlIF0gL0xlbmd0aCAzOTkKPj4Kc3RyZWFtCkdhc0pOOWkmVmsmO0taTi8pREtoPWEiRkJdJmEsXk41Z2RdI0h1SmlLOyEqSE9NQzdrSmpBPGMtPmZWQWdVR01YPF5VbGtwMD8rXzBWVU1XZCJGQjZbYUg/YGlcbFpPUWJvX1o+NGZnSztubyxyLzJBL0w9VlJQVGtHTmQzbztqRkpUWkRuKTo2JSMjaWVfRyZvXGpLdVVwOGQmQTZDTjYybD1cWU5POzg4ODlcMSNjPm8jYT84Lm9LanM/MGspOHF0Ki0mRUxhMHBXcTRHciZDLipoSGxvNnBdUGJNJE1INjE8czshTVUpMWMsOyJjW3E/bGElbkpeNiwuLypaInJmKDYwV1UtOEwxKFZzQ24zOyUzNkModTRlcj5jN2s2Z0xRY3I+V1w+Vik1b1ZFUDRHVTdBcyxuLXNlWTpvRSxhZ1pNY1RXbmYibU5DTUI2ZV01MWc4YSgqcTtQXT8kcyZvM1JuZz9EIm1lTSllciFebnFAYiFAb1M3MVlJKS4rcExCdTsmVyFCOTFvPFd+PmVuZHN0cmVhbQplbmRvYmoKeHJlZgowIDkKMDAwMDAwMDAwMCA2NTUzNSBmIAowMDAwMDAwMDczIDAwMDAwIG4gCjAwMDAwMDAxMDQgMDAwMDAgbiAKMDAwMDAwMDIxMSAwMDAwMCBuIAowMDAwMDAwNjEwIDAwMDAwIG4gCjAwMDAwMDA4NzYgMDAwMDAgbiAKMDAwMDAwMDk0NCAwMDAwMCBuIAowMDAwMDAxMjAxIDAwMDAwIG4gCjAwMDAwMDEyNjAgMDAwMDAgbiAKdHJhaWxlcgo8PAovSUQgCls8OWNkMGEwMGFjYjgxMGU0MTc3YWYwNTQ2MmUwZDFlMjI+PDljZDBhMDBhY2I4MTBlNDE3N2FmMDU0NjJlMGQxZTIyPl0KJSBSZXBvcnRMYWIgZ2VuZXJhdGVkIFBERiBkb2N1bWVudCAtLSBkaWdlc3QgKGh0dHA6Ly93d3cucmVwb3J0bGFiLmNvbSkKCi9JbmZvIDYgMCBSCi9Sb290IDUgMCBSCi9TaXplIDkKPj4Kc3RhcnR4cmVmCjE3NDkKJSVFT0YK",
    "msg": "BILL_PDF_FOUNDED"
}
```

#### /company/profile/update/

This endpoint permit to get the company informations.

#### `POST /{locale}/company/profile/update/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
{
    "logo": "testuser@test.com",
    "country": "France",
    "region": "Ile de france",
    "prefix_number": "+33",
    "address": "21 avenue de la liberte",
    "city": "Paris",
    "phone_number": "603948573",
    "username": "dwdkowko"
}
```

###### Response

> 200 Response

```json
{
    "status": 200,
    "msg": "COMPANY_INFORMATION_UPLOADED"
}
```

#### /company/profile/

This endpoint returns the result of participation in a campaign.

#### `GET /{locale}/company/profile/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
    None
```

###### Response

> 200 Response

```json
{
    "user_informations": {
        "city": "Paris",
        "national_number": 651243517,
        "address": "21 avenue de la liberte",
        "company_name": "NewBalance",
        "country": null,
        "region": "Ile de France",
        "logo": "",
        "country_code": 33,
        "email": "newbalance@test.com",
        "username": "eokcowekc"
    },
    "msg": "COMPANY_INFORMATION_RETRIEVED"
}
```

#### /company/campaign/

This endpoint returns all the campaign of a company.

#### `GET /{locale}/company/campaign/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
    None
```

###### Response

> 200 Response

```json
{
    "status": 200,
    "msg": "PROMOTIONS_FOUNDED",
    "result_data": [
        {
            "campaign_name": "Promotion Basket10",
            "pk": 52,
            "end_date": "2020-02-20T00:00:00Z",
            "release_date": "2020-02-13T00:00:00Z",
            "number_of_participants": 0,
            "number_of_eligible_people": 250,
            "type_of_promotion": "public",
            "description": "Promotion for the release of new basket"
        }
    ],
    "is_error": 0
}
```

#### `GET /{locale}/company/campaign/{int:pk}/`

This endpoint returns all the public and private informations about one campaign of a company.

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
    pk: id of the campaign
```

###### Response

> 200 Response

```json
{
    "status": 200,
    "result_data": {
        "company_id": 1,
        "company_name": "NewBalance",
        "long_description": "",
        "end_date": "2020-05-20T00:00:00Z",
        "winnings": [
            "50%",
            "gazelle"
        ],
        "type_of_distribution": "reward",
        "campaign_image": "https://storage.gra.cloud.ovh.net/v1/AUTH_f5a2983ff1034d118ff000c8bd64c010/rafflee-devlopment/images/46/campaign_logo/1590502576.png",
        "description": "Promotion for the release of new basket",
        "user_actions": {
            "website": false,
            "video": false,
            "twitter_tweet": false,
            "facebook_comment": false,
            "instagram_profile": false,
            "facebook_follow": false,
            "youtube_follow": false,
            "twitter_retweet": false,
            "youtube_like": false,
            "twitch_follow": false,
            "entries_user": 0,
            "twitter_like": false,
            "facebook_like": false,
            "instagram_publication": false,
            "poll": false,
            "twitter_follow": false
        },
        "favorite": false,
        "categories": [
            "Tech",
            "Clothing"
        ],
        "live_draw": true,
        "release_date": "2020-02-13T00:00:00Z",
        "action_participate": [
            {
                "website": {
                    "mandatory": false,
                    "url": "https://google.com",
                    "entries": 1
                },
                "social_action": [
                    {
                        "facebook_comment_mandatory": false,
                        "facebook_like_mandatory": false,
                        "facebook_like_entries": 1,
                        "facebook_comment": true,
                        "facebook_like": true,
                        "facebook_comment_entries": 1,
                        "facebook_follow_mandatory": false,
                        "facebook_follow": false,
                        "facebook_follow_entries": 1
                    },
                    {
                        "youtube_like": true,
                        "youtube_follow_entries": 3,
                        "youtube_like_mandatory": false,
                        "youtube_like_entries": 1,
                        "youtube_follow": true,
                        "youtube_follow_mandatory": true
                    },
                    {
                        "instagram_publication_url": "https://www.instagram.com/p/CADLFvHAQ1S/",
                        "instagram_profile_entries": 1,
                        "instagram_profile_url": "https://www.instagram.com/nike/",
                        "instagram_publication_mandatory": false,
                        "instagram_profile_mandatory": false,
                        "instagram_publication_entries": 1,
                        "instagram_profile": true,
                        "instagram_publication": true
                    },
                    {
                        "twitter_retweet_mandatory": false,
                        "twitter_retweet_entries": 1,
                        "twitter_like_entries": 1,
                        "twitter_tweet": true,
                        "twitter_tweet_mandatory": false,
                        "twitter_tweet_entries": 1,
                        "twitter_retweet": true,
                        "twitter_follow_entries": 1,
                        "twitter_like": true,
                        "twitter_tweet_model": "I participated in the new rafflee raffle on https://www.rafflee.io",
                        "twitter_follow_mandatory": false,
                        "twitter_follow": true
                    },
                    {
                        "twitch_follow_mandatory": false,
                        "twitch_follow_entries": 1,
                        "twitch_follow": true
                    }
                ],
                "poll": {
                    "mandatory": false,
                    "responses": [
                        "yes",
                        "no"
                    ],
                    "multiple_choices": false,
                    "entries": 1,
                    "question": "Do you like cat?"
                },
                "video": {
                    "url_video_mobile": null,
                    "video_name": "test name",
                    "mandatory": false,
                    "entries": 1,
                    "url_video": "https://www.youtube.com/watch?v=O8kZUeYyrmk"
                }
            }
        ],
        "pk": 46,
        "number_of_eligible_people": 5,
        "company_logo": null,
        "campaign_name": "Promotion Basket TEST"
    },
    "is_error": 0,
    "msg": "MSG_PROMOTIONS_FOUNDED"
}
```

### Campaign

#### /campaign/all-campaigns/informations/

This endpoint list campaign information for the analytics.

#### `GET /{locale}/campaign/all-campaigns/informations/`

###### Parameters entry


headers: 'Authorization' : 'JWT ' + token,

###### Response

> 200 Response

```json
{
    "status": 200,
    "list_of_promotions": [
        {
            "id": 46,
            "name": "Promotion Basket TEST"
        }
    ],
    "msg": "MSG_PROMOTION_FOUNDED"
}
```

#### /campaign/all-campaigns/

This endpoint list all the public campaigns.

#### `POST /{locale}/campaign/all-campaigns/`

###### Parameters entry


```json
    "token": "cvokerpckzeckpezkpc..."
```

###### Response

> 200 Response

```json
{
    "result_data": {
        "categories": [
            "Tech",
            "Clothing"
        ],
        "action_participate": [
            {
                "poll": {
                    "multiple_choices": false,
                    "responses": [
                        "yes",
                        "no"
                    ],
                    "question": "Do you like cat?"
                },
                "social_action": [
                    {
                        "facebook_like": false,
                        "facebook_follow": false,
                        "facebook_comment": false
                    },
                    {
                        "youtube_like": false,
                        "youtube_follow": false
                    },
                    {
                        "instagram_profile": false,
                        "instagram_publication": false
                    },
                    {
                        "twitter_like": false,
                        "twitter_tweet": false,
                        "twitter_retweet": false,
                        "twitter_follow": false
                    },
                    {
                        "twitch_follow": false
                    }
                ]
            }
        ],
        "description": "Promotion for the release of new basket",
        "pk": 17,
        "number_of_eligible_people": 250,
        "release_date": "2020-02-13T00:00:00Z",
        "type_of_promotion": "public",
        "winnings": [
            "50%",
            "gazelle"
        ],
        "end_date": "2020-03-31T00:00:00Z",
        "favorite": true,
        "campaign_image": "/9j/4gIc....",
        "campaign_name": "Promotion Basket10"
    },
    "status": 200,
    "msg": "PROMOTION_FOUNDED",
    "is_error": 0
}
```

#### /campaign/{int:id}/

List all the informations about one campaign.

#### `POST /{locale}/campaign/{int:id}/`

###### Parameters entry


```json
    id: id of the campaign
    token: "ieozjcoiezjceiozj..."
```

###### Response

> 200 Response

```json
{
    "result_data": {
        "categories": [
            "Tech",
            "Clothing"
        ],
        "action_participate": [
            {
                "poll": {
                    "multiple_choices": false,
                    "responses": [
                        "yes",
                        "no"
                    ],
                    "question": "Do you like cat?"
                },
                "social_action": [
                    {
                        "facebook_like": false,
                        "facebook_follow": false,
                        "facebook_comment": false
                    },
                    {
                        "youtube_like": false,
                        "youtube_follow": false
                    },
                    {
                        "instagram_profile": false,
                        "instagram_publication": false
                    },
                    {
                        "twitter_like": false,
                        "twitter_tweet": false,
                        "twitter_retweet": false,
                        "twitter_follow": false
                    },
                    {
                        "twitch_follow": false
                    }
                ]
            }
        ],
        "description": "Promotion for the release of new basket",
        "pk": 17,
        "number_of_eligible_people": 250,
        "release_date": "2020-02-13T00:00:00Z",
        "type_of_promotion": "public",
        "winnings": [
            "50%",
            "gazelle"
        ],
        "end_date": "2020-03-31T00:00:00Z",
        "favorite": true,
        "campaign_image": "/9j/4gIc....",
        "campaign_name": "Promotion Basket10"
    },
    "status": 200,
    "msg": "PROMOTION_FOUNDED",
    "is_error": 0
}
```

#### /campaign/create/

This endpoint create a new campaign.

#### `POST /{locale}/campaign/create/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

form-data file: promotion_picture

```json
{
    "promotion_name": "Promotion Basket10",
    "promotion_picture": PROMOTION_IMAGE_FILE,
    "promotion_description": "Short description for my promotion",
    "promotion_long_description": "Long description for my promotion",
    "public_promotion": "public",
    "winnings": [
        {
            "name": "50%",
            "number_of_people": 100,
            "description": "50% of reduction",
            "image": WINNING_IMAGE_FILE
        },
        {
            "name": "gazelle",
            "number_of_people": 150,
            "description": "New model of basket",
            "image": WINNING_IMAGE_FILE
        }
    ],
    "categories": [
        {
            "name": "Tech"
        },
        {
            "name": "Clothing"
        }
    ],
    "promotion_option": {
        "live_draw": true,
        "limitation_participation": 0
    },
    "promotion_type": "giveway",
    "start_date": "2020-02-13",
    "end_date": "2020-02-20",
    "poll": {
        "question": "Do you like cat?",
        "response": [
            "yes",
            "no"
        ],
        "mutiples_choices": false,
        "entries": 1,
        "mandatory": false
    },
    "twitter": [
        {
            "action": "tweet",
            "model": "I participated in the new rafflee raffle on https://www.rafflee.io",
            "entries": 1,
            "mandatory": false
        },
        {
            "action": "like",
            "id": "1252606286228750337",
            "entries": 1,
            "mandatory": false
        },
        {
            "action": "retweet",
            "id": "1252606286228750337",
            "entries": 1,
            "mandatory": false
        },
        {
            "action": "follow",
            "type": "screen_name",
            "id": "rafflee",
            "entries": 1,
            "mandatory": false
        }
    ],
    "facebook": [
        {
            "action": "post",
            "entries": 1,
            "mandatory": false,
            "url": "https://www.facebook.com/101514858298034/posts/101580514958135/",
            "like": true,
            "comment": true,
            "share": true
        },
        {
            "action": "url",
            "entries": 1,
            "mandatory": false,
            "url": "https://rafflee.io",
            "like": true,
            "share": true
        },
        {
            "action": "page",
            "entries": 1,
            "mandatory": false,
            "follow": true,
            "share": true,
            "url": "https://www.facebook.com/Rafflee-101514858298034/"
        }
    ],
    "instagram": [
        {
            "action": "instagram_profile",
            "url": "https://instagram/exemple",
            "entries": 1,
            "mandatory": false
        },
        {
            "action": "instagram_publication",
            "url": "https://instagram/exemple",
            "entries": 1,
            "mandatory": false
        }
    ],
    "youtube": [
        {
            "action": "like",
            "entries": 1,
            "mandatory": false
        },
        {
            "action": "follow",
            "entries": 1,
            "mandatory": false
        }
    ],
    "twitch": [
        {
            "action": "follow",
            "follow_name" : "rafflee",
            "entries": 1,
            "mandatory": false
        }
    ],
    "url_video": {
        "url": "https://www.youtube.com/watch?v=O8kZUeYyrmk",
        "video_name": "test video",
        "url_mobile": "https://www.youtube.com/watch?v=O8kZUeYyrmk",
        "entries": 1,
        "mandatory": false
    },
    "url_website": {
        "url": "https://raffle.io",
        "entries": 1,
        "mandatory": false
    }
}
```

```
promotion can be:
    - private : if the promotion is limited
    - public : open for all
```
```
distribution can be:
    - raffle : users cannot have results before promotion end date
    - giveaway : users can have the result directly
    - reward : users will have the result during the live draw
```
```
Poll can be:
    - null : if the company don't need to create a poll
```
```
Categories can be:
    - null : if the company don't need to add category
```
```
Twitter follow_type can be:
    - screen_name : public name of the account
    - user_id : user id of the account
```

###### Response

> 200 Response

```json
{
    "promotion_id": 51,
    "status": 200,
    "msg": "MSG_PROMOTION_CREATED"
}
```

#### campaign/close/

This endpoint permit to complete a promotion in progress.

#### `POST /{locale}/campaign/close/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
{
    "promotion_id": 2,
    "password": "SuperPassword1234@"
}
```

###### Response

> 200 Response

```json
{
    "msg": "MSG_PROMOTION_IS_STOPPED",
    "promotion_id": 2,
    "end_date": "2020-02-13T00:00:00Z",
    "status": 200
}
```

#### campaign/participate/instagram/publication/

This endpoint permit to allows the user to validate the instagram publication action.

#### `POST /{locale}/campaign/participate/instagram/publication/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
{
    "promotion_id": 2
}
```

###### Response

> 200 Response

```json
{
    "msg": "MSG_VALIDATED_PUBLICATION_INSTAGRAM",
    "status": 200
}
```

#### campaign/participate/instagram/profile/

This endpoint permit to allows the user to validate the instagram profile action.

#### `POST /{locale}/campaign/participate/instagram/profile/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
{
    "promotion_id": 2
}
```

###### Response

> 200 Response

```json
{
    "msg": "MSG_VALIDATED_PROFILE_INSTAGRAM",
    "status": 200
}
```


#### campaign/participate/facebook/url/

This function permit to do the url publication with facebook.

#### `POST /{locale}/campaign/participate/facebook/url/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
{
    "promotion_id": 2,
    "action": "like"
}
```

action: like/share

###### Response

> 200 Response

```json
{
    "msg": "MSG_FACEBOOK_URL_VALIDATED",
    "status": 200
}
```


#### campaign/participate/facebook/page/

This function permit to do the page publication with facebook.

#### `POST /{locale}/campaign/participate/facebook/page/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
{
    "promotion_id": 2,
    "action": "follow"
}
```

action: follow/share

###### Response

> 200 Response

```json
{
    "msg": "MSG_FACEBOOK_PAGE_VALIDATED",
    "status": 200
}
```


#### campaign/participate/facebook/post/

This function permit to do the post publication with facebook.

#### `POST /{locale}/campaign/participate/facebook/post/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
{
    "promotion_id": 2,
    "action": "comment"
}
```

action: comment/like/share

###### Response

> 200 Response

```json
{
    "msg": "MSG_FACEBOOK_POST_VALIDATED",
    "status": 200
}
```


#### campaign/participate/url_video/

This endpoint permit to allows the user to validate the url_video action.

#### `POST /{locale}/campaign/participate/url_video/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
{
    "promotion_id": 2
}
```

###### Response

> 200 Response

```json
{
    "msg": "MSG_VALIDATED_VIDEO",
    "status": 200
}
```

#### campaign/participate/url_website/

This endpoint permit to allows the user to validate the url_website action.

#### `POST /{locale}/campaign/participate/url_website/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
{
    "promotion_id": 2
}
```

###### Response

> 200 Response

```json
{
    "msg": "MSG_VALIDATED_URL_WEBSITE",
    "status": 200
}
```

#### campaign/participate/poll/

This endpoint permit to allows the user to validate the poll action.

#### `POST /{locale}/campaign/participate/poll/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
{
    "promotion_id": 2,
    "response": "Yes"
}
```

###### Response

> 200 Response

```json
{
    "msg": "MSG_VALIDATED_RESPONSE",
    "status": 200
}
```

#### campaign/participate/twitter/comment/

This endpoint permit to allows the user to verify the twitter comment action.

#### `POST /{locale}/campaign/participate/twitter/comment/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
{
    "promotion_id": 2
}
```

###### Response

> 200 Response

```json
{
    "tweet_template": "I participate in the new promotion on https://rafflee.io",
    "msg": "MSG_ACTION_EXIST",
    "status": 200
}
```

#### campaign/participate/twitter/comment/validation/

This endpoint permit to validate the twitter comment action.

#### `POST /{locale}/campaign/participate/twitter/comment/validation`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
{
    "promotion_id": 2,
    "tweet": "I participate in the new promotion on https://rafflee.io"
}
```

###### Response

> 200 Response

```json
{
    "status": 200,
    "msg": "MSG_VALIDATED_TWEET"
}
```

#### campaign/participate/twitter/retweet/

This endpoint permit to allows the user to verify the twitter retweet action.

#### `POST /{locale}/campaign/participate/twitter/retweet/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
{
    "promotion_id": 2
}
```

###### Response

> 200 Response

```json
{
    "status": 200,
    "msg": "MSG_YOU_HAVE_ALREADY_RETWEETED_THIS_TWEET"
}
```

```json
{
    "name": "killian bellesoeur",
    "text": "test 4 https://t.co/mcQnOENdzf",
    "verified": false,
    "profile_img": "https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png",
    "msg": "MSG_ACTION_EXIST",
    "like": 1,
    "status": 200,
    "retweet": 1,
    "created_at": "Fri Apr 17 12:36:28 +0000 2020"
}
```

#### campaign/participate/twitter/retweet/validation/

This endpoint permit to validate the twitter retweet action.

#### `POST /{locale}/campaign/participate/twitter/retweet/validation`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
{
    "promotion_id": 2
}
```

###### Response

> 200 Response

```json
{
    "status": 200,
    "msg": "MSG_RETWEET_VALIDATED"
}
```

#### campaign/participate/twitch/follow/

This endpoint permit to allows the user to verify the twitch follow action.

#### `POST /{locale}/campaign/participate/twitch/follow/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
{
    "promotion_id": 2
}
```

###### Response

> 200 Response

```json
{
    "status": 200,
    "msg": "MSG_YOU_ARE_ALREADY_FOLLOWING_THIS_ACCOUNT"
}
```

```json
{
    "profile_img": "https://pbs.twimg.com/profile_images/786524487334883328/en3aceYGy_normal.jpg",
    "verified": false,
    "status": 200,
    "followers": 13,
    "name": "Jean Valgeant",
    "msg": "MSG_ACTION_EXIST"
}
```

#### campaign/participate/twitch/follow/validation/

This endpoint permit to validate the twitch follow action.

#### `POST /{locale}/campaign/participate/twitch/follow/validation`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
{
    "promotion_id": 2
}
```

###### Response

> 200 Response

```json
{
    "status": 200,
    "msg": "MSG_FOLLOW_VALIDATED"
}
```

#### campaign/participate/twitter/follow/

This endpoint permit to allows the user to verify the twitter follow action.

#### `POST /{locale}/campaign/participate/twitter/follow/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
{
    "promotion_id": 2
}
```

###### Response

> 200 Response

```json
{
    "status": 200,
    "msg": "MSG_YOU_ARE_ALREADY_FOLLOWING_THIS_ACCOUNT"
}
```

```json
{
    "profile_img": "https://pbs.twimg.com/profile_images/786524487334883328/en3aceYGy_normal.jpg",
    "verified": false,
    "status": 200,
    "followers": 13,
    "name": "Jean Valgeant",
    "msg": "MSG_ACTION_EXIST"
}
```

#### campaign/participate/twitter/follow/validation/

This endpoint permit to validate the twitter follow action.

#### `POST /{locale}/campaign/participate/twitter/follow/validation`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
{
    "promotion_id": 2
}
```

###### Response

> 200 Response

```json
{
    "status": 200,
    "msg": "MSG_FOLLOW_VALIDATED"
}
```

#### campaign/participate/twitter/like/

This endpoint permit to allows the user to verify the twitter like action.

#### `POST /{locale}/campaign/participate/twitter/like/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
{
    "promotion_id": 2
}
```

###### Response

> 200 Response

```json
{
    "status": 200,
    "msg": "MSG_YOU_HAVE_ALREADY_LIKE_THIS_TWEET"
}
```

```json
{
    "like": 0,
    "msg": "MSG_LIKE_VALIDATED",
    "retweet": 0,
    "profile_img": "https://abs.twimg.com/sticky/default_profile_images/default_profile_normal.png",
    "name": "Jean Valgeant",
    "created_at": "Fri Apr 17 12:36:28 +0000 2020",
    "status": 200,
    "verified": false,
    "text": "test 4 https://t.co/mcQnOENdzf"
}
```

#### campaign/participate/twitter/like/validation/

This endpoint permit to validate the twitter like action.

#### `POST /{locale}/campaign/participate/twitter/like/validation`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
{
    "promotion_id": 2
}
```

###### Response

> 200 Response

```json
{
    "status": 200,
    "msg": "MSG_LIKE_VALIDATED"
}
```

#### /campaign/participate/

This endpoint permit to a user to participate to a promotion.

#### `POST /{locale}/campaign/participate/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
{
    "promotion_id": 2
}
```

###### Response

> 200 Response

```json
{
    "status": 200,
    "msg": "PARTICIPATION_ACCEPTED"
}
```

#### /campaign/participate/subscription/<int:id>/

This endpoint permit to a user to subscribe/follow to a company.

#### `POST /{locale}/campaign/participate/subscription/<int:id>/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

params: id = id of the promotion

```json
{
    "joign_cercle": true,
    "newsletter": true 
}
```

###### Response

> 200 Response

```json
{
    "status": 200,
    "msg": "MSG_SUBSCRIPTION_UPDATED"
}
```

#### /campaign/prizes/details/<int:id>/<str:name>/

This endpoint permit to get the informations about a winnings object.

#### `GET /{locale}/campaign/prizes/details/<int:id>/<str:name>/

###### Parameters entry

params: id = id of the promotion
        name = name of the prize

```json
{

}
```

###### Response

> 200 Response

```json
{
    "name": "50%",
    "number_of_eligible_people": 100,
    "description": "50% of reduction",
    "image_url": null
}
```

#### /campaign/user/in-progress/

This endpoint returns the promotions in which the user has participated and which are not finished.

#### `POST /{locale}/campaign/user/in-progress/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
    None
```

###### Response

> 200 Response

```json
{
    "is_error": 0,
    "status": 200,
    "result_data": [
        {
            "pk": 2,
            "description": "Promotion for the release of new basket",
            "end_date": "2020-02-20T00:00:00Z",
            "campaign_name": "Promotion Basket",
            "type_of_promotion": "public",
            "number_of_eligible_people": 250,
            "release_date": "2020-02-13T00:00:00Z"
        }
    ],
    "msg": "PROMOTION_FOUNDED"
}
```

#### /campaign/user/historical/

This endpoint returns the promotions in which the user has participated and which have ended.

#### `GET /{locale}/campaign/user/historical/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
    None
```

###### Response

> 200 Response

```json
{
    "is_error": 0,
    "status": 200,
    "result_data": [
        {
            "pk": 2,
            "description": "Promotion for the release of new basket",
            "end_date": "2020-02-15T00:00:00Z",
            "campaign_name": "Promotion Basket",
            "type_of_promotion": "public",
            "number_of_eligible_people": 250,
            "release_date": "2020-02-13T00:00:00Z"
        }
    ],
    "msg": "PROMOTION_FOUNDED"
}
```

#### /campaign/user/inventory/

API endpoint for getting all the user prizes object in the inventory.

#### `GET /{locale}/campaign/user/inventory/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
    None
```

###### Response

> 200 Response

```json
{
    "result_data": [
        {
            "campaign_image": "https://storage.gra.cloud.ovh.net/v1/AUTH_f5a2983ff1034d118ff000c8bd64c010/rafflee-devlopment/images/46/campaign_logo/1590502576.png",
            "campaign_description": "Promotion for the release of new basket",
            "giveaway_name": "gazelle",
            "campaign_name": "Promotion Basket TEST",
            "giveaway_description": "New model of basket",
            "number_of_eligible_people": 3,
            "giveaway_image_url": null
        }
    ],
    "status": 200,
    "msg": "MSG_PROMOTIONS_FOUNDED",
    "is_error": 0
}
```

#### /campaign/live/pick/<int:pk>/

This endpoint returns the winner from a promotion by winning name.

#### `POST /{locale}/campaign/live/pick/<int:pk>/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
pk : pk of the campaign

{
  winning_name: gazelle
}
```

###### Response

> 200 Response

```json
{
    "username": "test2",
    "picture_profile": "efizefdopazjkiahjioejhcdezc...",
    "winning": "gazelle",
    "msg": "WINNER_FOUNDED",
    "status": 200
}
```

#### /campaign/live/pick/<int:pk>/

This endpoint returns one random winner from a promotion.

#### `POST /{locale}/campaign/<int:pk>/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
pk : pk of the campaign

{
  winning_name: gazelle
}
```

###### Response

> 200 Response

```json
{
    "username": "test2",
    "picture_profile": "efizefdopazjkiahjioejhcdezc...",
    "winning": "gazelle",
    "msg": "WINNER_FOUNDED",
    "status": 200
}
```

#### /campaign/live/all/<int:pk>/

This endpoint returns all the winners from a promotion by winning name.

#### `POST /{locale}/campaign/live/all/<int:pk>/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
pk : pk of the campaign

{
  winning_name: 50%
}
```

###### Response

> 200 Response

```json
{
    "is_error": 0,
    "msg": "WINNERS_FOUNDED",
    "result_data": [
        {
            "username": "rvervaervervea",
            "picture_profile": "efizefdopazjkiahjioejhcdezc...",
            "winning": "gazelle"
        },
        {
            "username": "test3",
            "picture_profile": "efizefdopazjkiahjioejhcdezc...",
            "winning": "gazelle"
        }
    ],
    "status": 200
}
```

#### /campaign/live/finish/<int:pk>/

This endpoint returns all the winners from a promotion.

#### `POST /{locale}/campaign/live/finish/<int:pk>/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
pk : pk of the campaign
```

###### Response

> 200 Response

```json
{
    "is_error": 0,
    "msg": "WINNERS_FOUNDED",
    "result_data": [
        {
            "username": "rvervaervervea",
            "winning": "gazelle",
            "picture_profile": "efizefdopazjkiahjioejhcdezc...",
        },
        {
            "username": "test3",
            "winning": "gazelle",
            "picture_profile": "efizefdopazjkiahjioejhcdezc..."
        },
        {
            "username": "test2",
            "winning": "50%",
            "picture_profile": "efizefdopazjkiahjioejhcdezc..."
        }
    ],
    "status": 200
}
```

#### campaign/participants/<int:pk>/

This endpoint returns all the participants and the number of participants.

#### `POST /{locale}/campaign/participants/<int:pk>/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
pk : pk of the campaign
```

###### Response

> 200 Response

```json
{
    "msg": "PARTICIPANT_FOUNDED",
    "number_of_participants": 1,
    "participants": [
        {
            "email": "rtazbtybteeab@yopmail.com",
            "username": "test1"
        }
    ]
}
```

### Homepage

#### /homepage/new/

This endpoint permit to return all the promotion order by release date.

#### `POST /{locale}/homepage/new/`

###### Parameters entry


```json
    "token": "referzfzeofpze...."
```

###### Response

> 200 Response

```json
{
    "is_error": 0,
    "result_data": [
        {
            "type_of_promotion": "public",
            "end_date": "2020-03-19T00:00:00Z",
            "description": "Promotion for the release of new basket",
            "pk": 51,
            "release_date": "2020-02-13T00:00:00Z",
            "campaign_name": "Promotion Basket10",
            "number_of_eligible_people": 250
        },
        {
            "type_of_promotion": "public",
            "end_date": "2020-04-23T00:00:00Z",
            "description": "Promotion for the release of new basket",
            "pk": 50,
            "release_date": "2020-02-13T00:00:00Z",
            "campaign_name": "Promotion Basket3",
            "number_of_eligible_people": 250
        }
    ],
    "status": 200,
    "msg": "PROMOTION_FOUNDED"
}
```

#### /homepage/end-soon/

This endpoint permit to return all the promotion order by end date.

#### `POST /{locale}/homepage/end-soon/`

###### Parameters entry


```json
    "token": "referzfzeofpze...."
```

###### Response

> 200 Response

```json
{
    "is_error": 0,
    "result_data": [
        {
            "type_of_promotion": "public",
            "end_date": "2020-03-19T00:00:00Z",
            "description": "Promotion for the release of new basket",
            "pk": 51,
            "release_date": "2020-02-13T00:00:00Z",
            "campaign_name": "Promotion Basket10",
            "number_of_eligible_people": 250
        },
        {
            "type_of_promotion": "public",
            "end_date": "2020-04-23T00:00:00Z",
            "description": "Promotion for the release of new basket",
            "pk": 50,
            "release_date": "2020-02-13T00:00:00Z",
            "campaign_name": "Promotion Basket3",
            "number_of_eligible_people": 250
        }
    ],
    "status": 200,
    "msg": "PROMOTION_FOUNDED"
}
```

#### /homepage/hot/

This endpoint permit to return all the promotion order by interest for the user.

#### `POST /{locale}/homepage/hot/`

###### Parameters entry


```json
    "token": "referzfzeofpze...."
```

###### Response

> 200 Response

```json
{
    "msg": "PROMOTION_FOUNDED",
    "status": 200,
    "is_error": 0,
    "result_data": [
        {
            "number_of_eligible_people": 250,
            "type_of_promotion": "public",
            "campaign_name": "Promotion Basket10",
            "pk": 51,
            "release_date": "2020-02-13T00:00:00Z",
            "end_date": "2020-03-19T00:00:00Z",
            "description": "Promotion for the release of new basket"
        },
        {
            "number_of_eligible_people": 250,
            "type_of_promotion": "public",
            "campaign_name": "Promotion Basket3",
            "pk": 50,
            "release_date": "2020-02-13T00:00:00Z",
            "end_date": "2020-04-23T00:00:00Z",
            "description": "Promotion for the release of new basket"
        }
    ]
}
```

#### /homepage/highlights/

This endpoint permit to return all the promotion order by priority of highlight.

#### `POST /{locale}/homepage/highlights/`

###### Parameters entry


```json
    "token": "referzfzeofpze...."
```

###### Response

> 200 Response

```json
{
    "msg": "PROMOTION_FOUNDED",
    "status": 200,
    "is_error": 0,
    "result_data": [
        {
            "number_of_eligible_people": 250,
            "type_of_promotion": "public",
            "campaign_name": "Promotion Basket3",
            "pk": 50,
            "release_date": "2020-02-13T00:00:00Z",
            "end_date": "2020-04-23T00:00:00Z",
            "description": "Promotion for the release of new basket"
        },
        {
            "number_of_eligible_people": 250,
            "type_of_promotion": "public",
            "campaign_name": "Promotion Basket10",
            "pk": 51,
            "release_date": "2020-02-13T00:00:00Z",
            "end_date": "2020-03-19T00:00:00Z",
            "description": "Promotion for the release of new basket"
        }
    ]
}
```

### Categories

#### /categories/

This endpoint permit to return all the categories activated.

#### `GET /{locale}/categories/`

###### Parameters entry


```json
    None
```

###### Response

> 200 Response

```json
{
    "result_data": [
        {
            "description": "Technologic product",
            "name": "Tech"
        },
        {
            "description": "Clothing",
            "name": "Clothing"
        }
    ],
    "is_error": 0,
    "status": 200,
    "msg": "CATEGORIES_FOUNDED"
}
```

### Analytics

#### /analytics/followers/<str:time>/

This endpoint permit to return all the followers of a company/influencer depends of the date.

#### `GET /{locale}/analytics/followers/<str:time>/`

###### Parameters entry


headers: 'Authorization' : 'JWT ' + token,

```json
  time :
    - day: return the last number of followers
    - week: returns the number of followers over the last 7 days
    - month: returns the number of followers over the last month
    - year: returns the number of followers over the year
```

###### Response

> 200 Response

```json
{
    "result_data": [
        {
            "description": "Technologic product",
            "name": "Tech"
        },
        {
            "description": "Clothing",
            "name": "Clothing"
        }
    ],
    "is_error": 0,
    "status": 200,
    "msg": "CATEGORIES_FOUNDED"
}
```

#### /analytics/click/<int:promotion_id>/<str:time>/

This endpoint permit to return all the click of a campaign, depends of the date.

#### `GET /{locale}/analytics/click/<str:promotion_id>/<str:time>/`

###### Parameters entry


headers: 'Authorization' : 'JWT ' + token,

```json
  promotion_id:
    - promotion_id: referral for a particular promotion 
  time :
    - day: return the last click of day
    - week: returns the click of a promotion over the last 7 days
    - month: returns the click of a promotion over the last month
    - year: returns the click of a promotion over the year
```

###### Response

> 200 Response

```json
{
    "status": 200,
    "msg": "MSG_OVERVIEW_ANALYTICS_FOUNDED",
    "is_error": 0,
    "result_data": [
        {
            "date": "2020-06-08T18:28:22.178Z",
            "click_actions": 0,
            "product_benefit_by_participations": "325.53",
            "product_benefit_by_view": "-26.83",
            "product_benefit_by_action": "325.53",
            "click_actions_total": 0,
            "click_participations_total": 0,
            "click_views_total": 0,
            "click_views": 0,
            "product_benefit_by_total": "325.53",
            "click_participations": 0
        }
      ...
    ]
}
```

#### /analytics/age/<str:id>/<str:type>/

This endpoint return analytics for the range of the age of the participants.

#### `GET /{locale}/analytics/age/<str:id>/<str:type>/

###### Parameters entry


headers: 'Authorization' : 'JWT ' + token,

```json
  id:
    - id: referral for a particular promotion
    - all: referral for all promotion
  time :
    - men: return the number of men who s participate to the promotions
    - girl: return the number of girl who s participate to the promotions
    - all: return the number of people who s participate to the promotions
```

###### Response

> 200 Response

```json
{
    "range_percentage": {
        "25_34": 100.0,
        "18_24": 0.0,
        "13_17": 0.0,
        "35_44": 0.0,
        "45_54": 0.0,
        "55_65": 0.0,
        "65": 0.0
    },
    "range": {
        "25_34": 1,
        "18_24": 0,
        "13_17": 0,
        "35_44": 0,
        "45_54": 0,
        "55_65": 0,
        "65": 0
    }
}
```


#### /analytics/gender/<str:id>/

This endpoint permit to return the sexe of the participants.

#### `GET /{locale}/analytics/gender/<str:id>/`

###### Parameters entry


headers: 'Authorization' : 'JWT ' + token,

```json
  id :
    - 12: you can put id of the campaign
    - all: returns the data for all the campaigns
```

###### Response

> 200 Response

```json
{
    "unknow": 1,
    "female_percentage": 0.0,
    "male": 1,
    "male_percentage": 50.0,
    "unknow_percentage": 50.0,
    "female": 0
}
```

#### /analytics/map/<str:id>/<str:type>/

This endpoint permit to return the map of the participants depends of action or participation and filter by one promotion or by all.

#### `GET /{locale}/analytics/map/<str:id>/<str:type>/`

###### Parameters entry


headers: 'Authorization' : 'JWT ' + token,

```json
  id :
    - 12: you can put id of the campaign
    - all: returns the data for all the campaigns
  type:
    - action: filter by action
    - participation: filter by participation
```

###### Response

> 200 Response

```json
{
    "datas": [
        {
            "number": 1,
            "longitude": 2.4,
            "country": "France",
            "continent": "Europe",
            "city": "Ivry-sur-Seine",
            "latitude": 48.8
        }
        ...
    ],
}
```

number parameter is the number of people on the city

#### /beta/report/

This endpoint permit to return the report for the tests.

#### `POST /{locale}/beta/report/`

###### Parameters entry


```json
  context:
    - wich page/action is the context
  type:
    - bug: if it is a bug
    - feedback: if it is a feeback
  description: description of the issue
```

###### Response

> 200 Response

```json
{

}
```

#### /twitter/users/search/

This endpoint permit to the twitter users by a research.

#### `POST /{locale}/twitter/users/search/`

###### Parameters entry


```json
{
  "search": 'mic'
}
```

###### Response

> 200 Response

```json
{
    "status": 200,
    "msg": "MSG_TWITTER_USER_RETURNED",
    "search": [
        {
            "screen_name": "mic",
            "followers_count": 183620,
            "verified": true,
            "profile_image_url": "https://pbs.twimg.com/profile_images/847387488872050688/_wCkqCje_normal.jpg"
        },
        {
            "screen_name": "brokenbottleboy",
            "followers_count": 19470,
            "verified": true,
            "profile_image_url": "https://pbs.twimg.com/profile_images/1267523776713052161/kPM9q2Y0_normal.jpg"
        },
        {
            "screen_name": "WeAreMicLowry",
            "followers_count": 46442,
            "verified": true,
            "profile_image_url": "https://pbs.twimg.com/profile_images/1269653667470344192/drHUb4r4_normal.jpg"
        },
        {
            "screen_name": "DavMicRot",
            "followers_count": 69626,
            "verified": true,
            "profile_image_url": "https://pbs.twimg.com/profile_images/671049754369888257/54JoZrei_normal.jpg"
        },
        {
            "screen_name": "MasterTheMic",
            "followers_count": 16024,
            "verified": false,
            "profile_image_url": "https://pbs.twimg.com/profile_images/697757863855304704/AV0gNRnU_normal.jpg"
        },
        {
            "screen_name": "DjMicSmith",
            "followers_count": 156237,
            "verified": false,
            "profile_image_url": "https://pbs.twimg.com/profile_images/1275132976016351237/mZjPHSgw_normal.jpg"
        },
        {
            "screen_name": "ExposureOpenMic",
            "followers_count": 15965,
            "verified": false,
            "profile_image_url": "https://pbs.twimg.com/profile_images/1260008666524155909/KZJ-QgOY_normal.jpg"
        },
        {
            "screen_name": "MIC_Military",
            "followers_count": 107457,
            "verified": false,
            "profile_image_url": "https://pbs.twimg.com/profile_images/1275560581253103616/PMQP-RMl_normal.jpg"
        },
        {
            "screen_name": "PAOnTheMic",
            "followers_count": 182437,
            "verified": false,
            "profile_image_url": "https://pbs.twimg.com/profile_images/1270430695966617602/7OUKqUyO_normal.jpg"
        },
        {
            "screen_name": "sliccmic",
            "followers_count": 37031,
            "verified": false,
            "profile_image_url": "https://pbs.twimg.com/profile_images/1274815513710014467/Jgrwub9o_normal.jpg"
        }
    ]
}
```

#### /facebook/page/search/

This endpoint permit to return the page of the account.

#### `GET /{locale}/facebook/page/search/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
{

}
```

###### Response

> 200 Response

```json
{
    "status": 200,
    "search": [
        {
            "id": "1015148529806534",
            "name": "Rafflee",
            "access_token": "EAAIFlcbZC0PkBAFyBXT1Ebyh7KFXYlalG4cg9TE959mIKmOaH3msOZBRvWen00UqpZCe6DIGA6tVCP4pU5DXpBmDuAwbFcZB78QT8hmr4kFH8xJoZBXUsHTmsZBrw64UOTjKCC9P0gNslLHDpZAqr8XZBVwOHY3EDTtIqxZAKp8TGSi5Golo9ZAVx8TGID5NK0kZD"
        }
    ],
    "msg": "MSG_FACEBOOK_PAGE_RETURNED"
}
```

#### /facebook/publication/search/

This endpoint permit to return the facebook publications.

#### `POST /{locale}/facebook/publication/search/`

###### Parameters entry

headers: 'Authorization' : 'JWT ' + token,

```json
{
  "page_id": '10151234148582980',
  "page_access_token":  'EAAIFlcbZC0PkBAFT1Ebyh7KFXhgYlalG4cg9TE959mIKmOaH3msOZBRvWen00UqpZCe6DIGA6tVCP4pU5DXpBmDuAwbFcZB78QT8hmr4kFH8xJoZBXUsHTmsZBrw64UOTjKCC9P0gNslLHDpZAqr8XZBVwOHY3EDTtIqxZAKp8TGSi5Golo9ZAVx8TGID5NK0kZD'
}
```

###### Response

> 200 Response

```json
{
    "search": [
        {
            "message": "test1",
            "created_time": "2020-07-01T16:18:01+0000",
            "id": "101514858298034_101580514958135",
            "story": "Rafflee, surexcité(e)."
        },
        {
            "message": "On test l'api",
            "created_time": "2020-07-01T14:24:46+0000",
            "id": "101514858298034_101515328297987"
        }
    ],
    "msg": "MSG_FACEBOOK_PUBLICATION_RETURNED",
    "status": 200
}
```