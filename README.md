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
Requirements for above:
* git
* virtualenvwrapper

## API

### rooms

```
/rooms/
/rooms/<id>/
```
DRF ModelViewSet, used for examining and creating rooms. A room has an ID and a capacity.

#### Validation
Required fields in POST request to `/rooms/`:
* `capacity` - must be a non-negative integer

### movies
```
/movies/
/movies/<id>/
```
DRF ModelViewSet, used for examining and creating movies. A movie has an ID, title, and duration.

#### Validation
Required fields in POST request to `/movies/`:
* `title` - string

Optional fields in POST request to `/movies`:
* `length` - duration string of the form: "HH:MM:SS", e.g. "01:30:00", 1 hour and 30 minutes.
  * Defaults to 90 minutes if omitted


### screenings
```
/screenings/
/screnings/<id>/
/screenings/<id>/buyticket/
```

DRF ModelViewSet used for listing and creating screenings as well as purchasing tickets. A screening has a movie, a room, and a time. Once a screening is created, the server will allow the purchase of tickets for screenings on any date as long as the screening has not already begun and there are still remaining seats.

#### Validation
Required fields in POST request to `/screenings/`
* `movie` - ID of movie being screened
* `room` - ID of room holding the screening
* `time` - Time of day the screening is booked for of the form: "HH:MM:SS", e.g. "13:30:00", 1:30 PM 
  * When creating a new screening, the server will validate that your proposed screening does not overlap with any existing screenings in the specified room during the time proposed for your new screening.
  
Required fields in POST request to `/screenings/<id>/buytickets/`
* `date` - Date for the screening you'd like to purchase a ticket for.
  * The date and starting time of the screening specified must be in the future, no purchasing tickets for yesterday's screenings or anything that has already begun playing on the current day.
  * The screening must still have available seats for that date. The server will only sell up to the screening's room's capacity for each date it is playing.

## Possible Improvements
* I only really test the GET and POST methods on any of the endpoints in order to show the functionality requested in the challenge. I could also add tests for the other HTTP methods being exposed automatically by DRF, but for now am assuming they work as expected.
* Some of my screenings API tests are slightly coupled to the current time of day. I get around this by making sure we're also buying tickets for a date in the future, but I could likely implement something to completely isolate these tests from TOD as I have done for the screenings model tests.
* I didn't really go all out testing all possible Screening overlap scenarios, like across day/month/year boundaries and what not. Mostly just convinced myself the typical cases were covered.
* I don't expose anything to look at existing tickets. Assumption is that its a one shot deal, you buy your ticket, see your ticket's ID, and bring that the to theatre.
* My error responses for being unable to purchase a ticket are kind of vague. Rather than having a general "Unable to purchase ticket" I could have spent more time returning specific reasons for what went wrong, the screening had already started or it was sold out.
* You can't use the buyticket endpoint through the ApiRoot viewer since it requires a POST instead of the default GET for custom actions. There may be a way to hook this up properly but I didn't take the time to research that since it works through manual POST requests.

## API Usage Examples:

Examples created using `httpie` command line utility. 

You can also explore the API using the DRF auto-generated API View at the root of the server by visiting `http://127.0.0.1:8000/` in your browser.

### rooms

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

### screenings

#### GET list
```
➜  http http://127.0.0.1:8000/screenings/
HTTP/1.1 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 47
Content-Type: application/json
Date: Sat, 23 Nov 2019 20:30:06 GMT
Server: WSGIServer/0.2 CPython/3.7.3
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN

[
    {
        "id": 1,
        "movie": 1,
        "room": 1,
        "time": "17:00:00"
    }
]
```
#### GET detail

```
➜  http http://127.0.0.1:8000/screenings/1/
HTTP/1.1 200 OK
Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
Content-Length: 45
Content-Type: application/json
Date: Sat, 23 Nov 2019 20:30:11 GMT
Server: WSGIServer/0.2 CPython/3.7.3
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN

{
    "id": 1,
    "movie": 1,
    "room": 1,
    "time": "17:00:00"
}
```

#### POST create screening
```
➜  http --json POST http://127.0.0.1:8000/screenings/ movie=1 room=1 time="19:00:00"
HTTP/1.1 201 Created
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 45
Content-Type: application/json
Date: Sat, 23 Nov 2019 20:31:49 GMT
Server: WSGIServer/0.2 CPython/3.7.3
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN

{
    "id": 2,
    "movie": 1,
    "room": 1,
    "time": "19:00:00"
}
```

#### POST create screening overlapping an existing screening, returning error
```
➜  http --json POST http://127.0.0.1:8000/screenings/ movie=1 room=1 time="18:00:00"
HTTP/1.1 400 Bad Request
Allow: GET, POST, HEAD, OPTIONS
Content-Length: 27
Content-Type: text/html; charset=utf-8
Date: Sat, 23 Nov 2019 21:01:37 GMT
Server: WSGIServer/0.2 CPython/3.7.3
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN

Overlaps existing screening

```

#### POST purchase ticket
```
➜  http --json POST http://127.0.0.1:8000/screenings/1/buyticket/ date="2019-12-12"
HTTP/1.1 200 OK
Allow: POST, OPTIONS
Content-Length: 22
Content-Type: application/json
Date: Sat, 23 Nov 2019 20:33:56 GMT
Server: WSGIServer/0.2 CPython/3.7.3
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN

{
    "id": 1,
    "screening": 1
}
```

#### POST purchase ticket for sold out screening, returning error
```
➜  http --json POST http://127.0.0.1:8000/screenings/1/buyticket/ date="2019-12-12" 
HTTP/1.1 400 Bad Request
Allow: POST, OPTIONS
Content-Length: 49
Content-Type: text/html; charset=utf-8
Date: Sat, 23 Nov 2019 21:02:38 GMT
Server: WSGIServer/0.2 CPython/3.7.3
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN

Unable to purchase ticket for specified screening
```

#### POST purchase ticket for screening that has already begin, returning error

```
➜  http --json POST http://127.0.0.1:8000/screenings/1/buyticket/ date="2017-12-12"
HTTP/1.1 400 Bad Request
Allow: POST, OPTIONS
Content-Length: 49
Content-Type: text/html; charset=utf-8
Date: Sat, 23 Nov 2019 21:03:56 GMT
Server: WSGIServer/0.2 CPython/3.7.3
Vary: Accept, Cookie
X-Frame-Options: SAMEORIGIN

Unable to purchase ticket for specified screening
```
