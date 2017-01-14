# Homework assignment for Nizkocenovci d.o.o

## Homework

### Description

Your homework assignment is to develop a application that takes in `departure location`, `arrival location` and `date and time of departure` and returns all possible routes on certain date that start in `departure location` and finish in `arrival location`. The data for routes can be found on Deutschebahn (DB) website.

Application must accept input from two different sources:
* API `/search?departure=Berlin+HBF&arrival=Frankfurt(M)Flughafen&date=2016-03-01+13:37:00`
* Command line `php search.php --departure="Berlin+HBF" --arrival="Frankfurt(M)Flughafen" --date="2016-03-01 13:37:00"`

_Names of GET parameters (`departure=...`), command line script (`search.php`) and script arguments (`--departure=...`) can be renamed as you like. Just provide me with a proper usage commands._

The application has to consists of three main parts:
* Getting search params from the user.
* Executing search on DB and parsing the HTML data.
* Returning result in human readable matter.

### Example

The data for the example can be found at:

 http://reiseauskunft.bahn.de/bin/query.exe/en?S=Berlin+HBF&Z=Frankfurt(M)Flughafen&date=01.03.2016&time=13:37&start=1&from_gt=1&dbkanal_004=L01_S01_D001_KPK0054_anreiselink_LZ03

Keep in mind that to get all the data for the whole day, you have to click _"Later"_ button a couple of times.

So for the example data, the response should look something like.

__For the command line__
```bash
$ php search.php --departure="Berlin HBF" --arrival="Frankfurt(M)Flughafen" --date="2016-03-01 13:37:00"

Berlin Hbf   Frankfurt(M)Flughafen   13:34   18:04   89 EUR   125 EUR
Berlin Hbf   Frankfurt(M)Flughafen   13:49   18:21   49 EUR   125 EUR
....

The search returned 17 routes in 12.23 seconds.
```

__For the API__
```json
{
    "data": {
        "routes": [
            {
                "departure": "Berlin Hbf",
                "location": "Frankfurt(M)Flughafen",
                "departure_time": "13:34",
                "arrival_time": "18:04",
                "price_low": 89,
                "price_high": 125,
                "currency": "EUR",
            },
            {
                "departure": "Berlin Hbf",
                "location": "Frankfurt(M)Flughafen",
                "departure_time": "13:49",
                "arrival_time": "18:21",
                "price_low": 49,
                "price_high": 125,
                "currency": "EUR",
            },...
        ]
    },
    "found": 17,
    "time_taken": 12.23
}
```

The number of routes fetched and number of seconds that the script took, should also be provided.

### What tech can you use?
* __PHP__:  5.5.*
* __Database__: MySQL / MariaDB or PostgreSQL. _(if needed)_
* __Framework__: Laravel5, Symfony3, Lumen or Silex. (You can also use custom solution without a framework. But usage of external libraries is encouraged.)
* __Composer__ for installing external libraries.
* __Git__ for tracking code changes
* Application has to work on __Ubuntu 14.04 LTS__ (but can be developed on any other OS).

<sup><sub>__Disclaimer__: If needed you can use different tech stack, but has to be confirmed by me first. So contact me if needed.</sup></sub>

### What should you send back?
* Working code (on some git repository). I encourage usage of public github projects. So just fork this repo.
* Manual on how to set up the application on the linux system. (add this below)
* Short example of usage. (add this below)

### What is evaluated?

* Fully working application
* Simplicity of application
* Architecture of application
* Smart usage of external libraries.
* Performance of application
* Coding style & standard
* Code documentation
* Proper usage of Git with meaningful messages.
* General impression on the solution.

__For some extra points__

* _Automated Tests (unit and/or functional)_
* _Caching of searches (so the second search with same params is faster than the previous one)_

## Your application

Describe here how to install and use your application.

### How to set up application:

```bash
$ echo "Add your install process here."
$ git clone git@github.com:goavio/homework.git homework
$ cd homework
# Install composer like stated here https://getcomposer.org/download/.
$ php composer.phar install
```

### How use the application:

```bash
$ echo "Add your usage info here."
```
