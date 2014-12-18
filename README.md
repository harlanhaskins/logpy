# logpy
A quick, centralized logging system

## Installation

logpy depends on `peewee` and `flask`.

Install them with `[sudo] pip install peewee flask`

You'll need to have Postgres installed, and a user `logpy` with password
`logpy`

In that, you'll need a database called `logpy`

## API

### POST /logs/:source

### Example Request
```
{
    "text" : "This is a log"
}
```

### Example Response

```
{
    "content" : "This is a log",
    "date" : "2014-08-26 10:42:13AM",
    "id" : "343"
}
```

## GET /logs/:source

### Example Response
```
[
    {
        "content" : "This is a log",
        "date" : "2014-08-26 10:42:13AM",
        "id" : "343"
    }
    {
        "content" : "This is another log",
        "date" : "2014-08-26 10:43:13AM",
        "id" : "344"
    }
]
```

## GET /logs/:source/:id

### GET /logs/somesource/344
### Example Response
```
{
    "content" : "This is another log",
    "date" : "2014-08-26 10:43:13AM",
    "id" : "344"
}
```

## GET /logs/:source/:id

### POST /logs/somesource/344
### Example Request
```
{
    "text" : "This is an update."
}
```
### Example Response
```
{
    "content" : "This is an update.",
    "date" : "2014-08-26 10:43:13AM",
    "id" : "344"
}
```

## DELETE /logs/:source/:id

### DELETE /logs/somesource/344
### Example Response
```
{
    "content" : "This is another log",
    "date" : "2014-08-26 10:43:13AM",
    "id" : "344"
}
```