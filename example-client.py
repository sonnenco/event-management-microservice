import zmq
import json

context = zmq.Context()

print("Connect to the server...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:40699")

##########################################################

# Create event for Forrest
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

print("\nCreate event for Forrest:")
socket.send_string(json.dumps(message))
reply = socket.recv()
print(f"Received reply: {reply}")

##########################################################

# Create event for Artur
message = {
    "operation": "create",
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

print("\nCreate event for Artur:")
socket.send_string(json.dumps(message))
reply= socket.recv()
print(f"Received reply: {reply}")

##########################################################

# Create event which is missing 'operation'
message = {
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

print("\nCreate event which is missing 'operation':")
socket.send_string(json.dumps(message))
reply= socket.recv()
print(f"Received reply: {reply}")

##########################################################

# Create event which is missing 'app_id'
message = {
    "operation": "create",
    "event": {
        "title": "Math 110 Final Exam",
        "timestamp": "08-02-2025",
        "frequency": "one-time",
        "data": {
            "location": "Main Lecture Hall"
        }
    }
}

print("\nCreate event which is missing 'app_id':")
socket.send_string(json.dumps(message))
reply= socket.recv()
print(f"Received reply: {reply}")

##########################################################

# Create event which is missing 'title'
message = {
    "operation": "create",
    "app_id": "artur",
    "event": {
        "timestamp": "08-02-2025",
        "frequency": "one-time",
        "data": {
            "location": "Main Lecture Hall"
        }
    }
}

print("\nCreate event which is missing 'title':")
socket.send_string(json.dumps(message))
reply= socket.recv()
print(f"Received reply: {reply}")

##########################################################

# Create event which is missing 'timestamp'
message = {
    "operation": "create",
    "app_id": "artur",
    "event": {
        "title": "Math 110 Final Exam",
        "frequency": "one-time",
        "data": {
            "location": "Main Lecture Hall"
        }
    }
}

print("\nCreate event which is missing 'timestamp':")
socket.send_string(json.dumps(message))
reply= socket.recv()
print(f"Received reply: {reply}")

##########################################################

# Create event which is missing 'frequency'
message = {
    "operation": "create",
    "app_id": "artur",
    "event": {
        "title": "Math 110 Final Exam",
        "timestamp": "08-02-2025",
        "data": {
            "location": "Main Lecture Hall"
        }
    }
}

print("\nCreate event which is missing 'frequency':")
socket.send_string(json.dumps(message))
reply= socket.recv()
print(f"Received reply: {reply}")

##########################################################

# Create event with invalid 'frequency' value
message = {
    "operation": "create",
    "app_id": "artur",
    "event": {
        "title": "Math 110 Final Exam",
        "timestamp": "08-02-2025",
        "frequency": "this is not an allowed value!",
        "data": {
            "location": "Main Lecture Hall"
        }
    }
}

print("\nCreate event with invalid 'frequency' value:")
socket.send_string(json.dumps(message))
reply= socket.recv()
print(f"Received reply: {reply}")

##########################################################

# Create event which is missing 'data'
message = {
    "operation": "create",
    "app_id": "artur",
    "event": {
        "title": "Math 110 Final Exam",
        "timestamp": "08-02-2025",
        "frequency": "one-time"
    }
}

print("\nCreate event which is missing 'data':")
socket.send_string(json.dumps(message))
reply= socket.recv()
print(f"Received reply: {reply}")

##########################################################

# Create event which has a non-allowed key under 'data'
message = {
    "operation": "create",
    "app_id": "artur",
    "event": {
        "title": "Math 110 Final Exam",
        "timestamp": "08-02-2025",
        "frequency": "one-time",
        "data": {
            "location": "Main Lecture Hall",
            "newKey": "this is definitely not an allowed key!"
        }
    }
}

print("\nCreate event which has a non-allowed key under 'data':")
socket.send_string(json.dumps(message))
reply= socket.recv()
print(f"Received reply: {reply}")

##########################################################

# Read all Forrest events
message = {
    "operation": "read",
    "app_id": "forrest"
}

print("\nRead all Forrest events:")
socket.send_string(json.dumps(message))
reply= socket.recv()
print(f"Received reply: {reply}")

##########################################################

# Read all Artur events
message = {
    "operation": "read",
    "app_id": "artur",
}

print("\nRead all Artur events:")
socket.send_string(json.dumps(message))
reply= socket.recv()
print(f"Received reply: {reply}")

##########################################################

# Read specific Forrest event which exists
message = {
    "operation": "read",
    "app_id": "forrest",
    "event": {
        "title": "Netflix"
    }
}

print("\nRead specific Forrest event which exists:")
socket.send_string(json.dumps(message))
reply= socket.recv()
print(f"Received reply: {reply}")

##########################################################

# Read specific Artur event which exists
message = {
    "operation": "read",
    "app_id": "artur",
    "event": {
        "title": "Math 110 Final Exam"
    }
}

print("\nRead specific Artur event which exists:")
socket.send_string(json.dumps(message))
reply= socket.recv()
print(f"Received reply: {reply}")

##########################################################

# Read specific Forrest event which does not exist
message = {
    "operation": "read",
    "app_id": "forrest",
    "event": {
        "title": "Disney+"
    }
}

print("\nRead specific Forrest event which does not exist:")
socket.send_string(json.dumps(message))
reply= socket.recv()
print(f"Received reply: {reply}")

##########################################################

# Read specific Artur event which does not exist
message = {
    "operation": "read",
    "app_id": "artur",
    "event": {
        "title": "Physics 210 Final Exam"
    }
}

print("\nRead specific Artur event which does not exist:")
socket.send_string(json.dumps(message))
reply= socket.recv()
print(f"Received reply: {reply}")