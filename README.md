# Theatre

API-only implementation of a simple theatre. Allows users to create Rooms, Movies, Screenings, and purchase Tickets.

## Initial Setup

To get the server up and running:
```sh
git clone https://github.com/taylodactyl/theatre.git
cd theatre
mkvirtualenv -r requirements.txt theatre
cd challenge
python manage.py migrate
python manage.py runserver
```

## API

### rooms

```
/rooms/
/rooms/<id>/
```
DRF ModelViewSet, used for examining and creating rooms:

#### GET list
```
➜ http http://127.0.0.1:8000/rooms/     
HTTP/1.1 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 23
Content-Type: application/json
Date: Sat, 23 Nov 2019 20:13:00 GMT
Server: WSGIServer/0.2 CPython/3.7.3
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN

[
    {
        "capacity": 1,
        "id": 1
    }
]
```

#### GET detail
```
➜  http http://127.0.0.1:8000/rooms/1/   
HTTP/1.1 200 OK
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 21
Content-Type: application/json
Date: Sat, 23 Nov 2019 20:22:10 GMT
Server: WSGIServer/0.2 CPython/3.7.3
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN

{
    "capacity": 1,
    "id": 1
}
```
#### POST create new room
```
➜  http --json POST http://127.0.0.1:8000/rooms/ capacity=20          
HTTP/1.1 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 22
Content-Type: application/json
Date: Sat, 23 Nov 2019 20:23:21 GMT
Server: WSGIServer/0.2 CPython/3.7.3
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN

{
    "capacity": 20,
    "id": 2
}
```

### movies
```
/movies/
/movies/<id>/
```
DRF ModelViewSet, used for examining and creating rooms:

#### GET list
```
➜ http http://127.0.0.1:8000/movies/                       
HTTP/1.1 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 47
Content-Type: application/json
Date: Sat, 23 Nov 2019 20:25:00 GMT
Server: WSGIServer/0.2 CPython/3.7.3
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN

[
    {
        "id": 1,
        "length": "01:30:00",
        "title": "Taylor"
    }
]
```

#### GET detail
```
➜  http http://127.0.0.1:8000/movies/1/
HTTP/1.1 200 OK
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 45
Content-Type: application/json
Date: Sat, 23 Nov 2019 20:25:08 GMT
Server: WSGIServer/0.2 CPython/3.7.3
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN

{
    "id": 1,
    "length": "01:30:00",
    "title": "Taylor"
}
```

#### POST create new movie
```
➜  http --json POST http://127.0.0.1:8000/movies/ title="Weekend at Bernie's"
HTTP/1.1 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 58
Content-Type: application/json
Date: Sat, 23 Nov 2019 20:26:27 GMT
Server: WSGIServer/0.2 CPython/3.7.3
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN

{
    "id": 2,
    "length": "01:30:00",
    "title": "Weekend at Bernie's"
}
```
