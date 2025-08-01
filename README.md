# event-management-microservice

COMMUNICATIONS CONTRACT

This is an event management microservice developed by Colin Sonnenberg for CS 361 at Oregon State University.  This microservice was written to support main programs developed by classmates.  It was developed using Python and supporting packages such as zmq, json and time.

## Data storage syntax

Data is stored in a text file located within the repo.  Here is an example of what stored data could look like:

[
    {
      "app_id": "forrest",
      "event": {
          "title": "Netflix",
          "timestamp": "08-01-2025",
          "frequency": "monthly",
          "data": {
              "amount": 14.99,
              "currency": "USD"
          }
      }
    },
    {
      "app_id": "artur",
      "event": {
        "title": "Math 110 Final Exam",
        "timestamp": "08-02-2025",
        "frequency": "one-time",
        "data": {
            "location": "Main Lecture Hall"
        }
      }
    }
]

## Getting started

Ensure you have the latest version of Python installed.

Download the repo and run the server.py file (typically with 'python3 server.py' command).

## Requesting data

Endpoint is automatically established on "tcp://localhost:40699" via ZeroMQ upon running server.py.

You will need to establish a socket connection to this from your main program also using ZeroMQ.  This tool is platform agnostic ([see here for links to documentation on establishing socket connection in your chosen language](https://zeromq.org/get-started/)).

### Create

| Key | Required or optional |
| --- | --- |
| operation | required |
| app_id | required|
| event | required |
| title | required |
| timestamp | required |
| frequency | required |
| data | required |
| amount | optional |
| currency | optional |
| location | optional |

message = {
    "operation": "create",
    "app_id": "forrest",
    "event": {
        "title": "Netflix",
        "timestamp": "08-01-2025",
        "frequency": "monthly",
        "data": {
            "amount": 14.99,
            "currency": "USD"
        }
    }
}

### Read all

| Key | Required or optional |
| --- | --- |
| operation | required |
| app_id | required|

message = {
    "operation": "read",
    "app_id": "forrest"
}

### Read specific

| Key | Required or optional |
| --- | --- |
| operation | required |
| app_id | required|
| event | required |
| title | required |

message = {
    "operation": "read",
    "app_id": "forrest",
    "event": {
        "title": "Netflix"
    }
}

### Update specific (several example depending on attribute attempting to update)

| Key | Required or optional |
| --- | --- |
| operation | required |
| app_id | required|
| event | required |
| title | required |
| timestamp | optional |
| frequency | optional |
| data | required only if providing amount, currency, or location update |
| amount | optional |
| currency | optional |
| location | optional |

message = {
    "operation": "update",
    "app_id": "forrest",
    "event": {
        "title": "Netflix",
        "timestamp": "12-01-2025"
    }
}

message = {
    "operation": "update",
    "app_id": "forrest",
    "event": {
        "title": "Netflix",
        "frequency": "one-time"
    }
}

message = {
    "operation": "update",
    "app_id": "forrest",
    "event": {
        "title": "Netflix",
        "data": {
            "amount": 19.99
        }
    }
}

message = {
    "operation": "update",
    "app_id": "forrest",
    "event": {
        "title": "Netflix",
        "data": {
            "currency": "CAD"
        }
    }
}

message = {
    "operation": "update",
    "app_id": "artur",
    "event": {
        "title": "Math 110 Final Exam",
        "data": {
            "location": "Updated exam location!" 
        }
    }
}

### Delete

| Key | Required or optional |
| --- | --- |
| operation | required |
| app_id | required|
| event | required |
| title | required |

message = {
    "operation": "delete",
    "app_id": "forrest",
    "event": {
        "title": "Netflix",
    }
}

## Receiving data
Data is received back over the same socket you established in your main program.

Create, update and delete requests will reply with a string message that the request was successful or a failure (and errors encountered if failed).
Read will reply with a string message containing the requested event(s) or a failure (and errors encountered if failed).

An example of receiving data back in Python is:
'''
reply = socket.recv()
'''

But again, your chosen language will use its [own syntax per the ZeroMQ documentation](https://zeromq.org/get-started/).

## UML sequence diagram

Coming soon...
