import zmq
import json

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:40699")
print("Starting server on port 40699...")

def createEvent(newEvent):
    """
    Attempt to store the event in a text file to support further operations such as Read, Update and Delete.

    :newEvent: Dictionary representing the request payload (minus the "operation" key and associated value)
    :return: List specifying errors encountered during data valiation (return only executes if errors exist, otherwise nothing returned)
    """

    print("Running def createEvent()...")
    errors = []
    
    # Open the text file and attempt to read it
    with open("event-storage.txt", "r") as storageFile:
        try:          
            # Validate whether the file is empty
            allEvents = storageFile.read().strip()
            if allEvents:
                allEvents = json.loads(allEvents)
            else:
                allEvents = []
        except json.JSONDecodeError:
            print("Invalid JSON format in the storage file.")
            errors.append("Invalid JSON format in the storage file.")
            return errors

        # Append the newEvent to the existing list containing events stored as dictionaries
        allEvents.append(newEvent)

        # Open the text file and dump the updated list of events back in
        with open("event-storage.txt", "w") as storageFile:
            json.dump(allEvents, storageFile, indent=2)
        
        # Send errors or indication of successful request back over the socket
        if errors:
            print("Create request errors:")
            for error in errors:
                print(error)
            socket.send_string(f"Request errors: '{errors}'")
        else:
            socket.send_string("Create request was executed successfully!")
            print("Create request was executed successfully!")

def readAllEvent(appId):
    """
    Read the text file for all events which match the request payload

    :appId: String representing the application which is asking to read events
    :return: List specifying errors encountered during data valiation (return only executes if errors exist, otherwise nothing returned)
    """

    print("Running def readAllEvent()...")
    errors = []

    # Attempt to open and read from the text file
    try:
        with open("event-storage.txt", "r") as storageFile:
            allEvents = json.load(storageFile)
    except IOError as error:
        print(f"def readAllEvent(): Error reading the text file: {error}")
        errors.append(f"def readAllEvent(): Error reading the text file: {error}")
        return errors

    # Attempt to filter events which do not match appId param
    try:
        filteredEvents = []
        for event in allEvents:
            if event.get("app_id") == appId:
                filteredEvents.append(event)
    except json.JSONDecodeError as error:
        print(f"def readAllEvent(): Error decoding the JSON object: {error}")
        errors.append(f"def readAllEvent(): Error decoding the JSON object: {error}")
    
    # If errors exist, send the errors back over the socket to close out the request
    if errors:
        print("Read all request errors:")
        for error in errors:
            print(error)
        socket.send_string(f"Errors: '{errors}'")
    
    # If errors do not exist, send success confirmation back over the socket to close out the request
    else:
        socket.send_string(json.dumps(filteredEvents))
        print("Read all request was executed successfully!")

def readSpecificEvent(appId, title):
    """
    Read the text file for the specific event which matches the request payload

    :appId: String representing the application which is asking to read events
    :title: String representing the title of the event to return
    :return: List specifying errors encountered during data valiation (return only executes if errors exist, otherwise nothing returned)
    """

    print("Running def readAllEvent()...")
    errors = []

    # Attempt to open and read from the text file
    try:
        with open("event-storage.txt", "r") as storageFile:
            allEvents = json.load(storageFile)
    except IOError as error:
        print(f"def readSpecificEvent(): Error reading the text file: {error}")
        errors.append(f"def readSpecificEvent(): Error reading the text file: {error}")
        return errors

    # Attempt to filter events which do not match appId and title params
    try:
        filteredEvents = []
        for eventObject in allEvents:
            event = eventObject.get("event")
            if eventObject.get("app_id") == appId and event.get("title") == title:
                filteredEvents.append(event)
    except json.JSONDecodeError as error:
        print(f"def readSpecificEvent(): Error decoding the JSON object: {error}")
        errors.append(f"def readSpecificEvent(): Error decoding the JSON object: {error}")

    # If errors exist, send the errors back over the socket to close out the request
    if errors:
        print("Read specific request errors:")
        for error in errors:
            print(error)
        socket.send_string(f"Errors: '{errors}'")
    
    # If errors do not exist, send success confirmation back over the socket to close out the request
    else:
        socket.send_string(json.dumps(filteredEvents))
        print("Read specific request was executed successfully!")

def minimumDataValidation(data):
    """
    Validate that the minimum required keys ("operation" and "app_id) are present in the data.

    :data: Dictionary representing the request payload
    :return: List specifying errors encountered during data valiation (can be empty)
    """
    
    print("Running def minimumDataValidation()...")
    requiredParentKeys = ["operation", "app_id"]
    requiredOperationValues = ["create", "read", "update", "delete"]
    errors = []

    # Validate whether required keys are present in the payload
    for key in requiredParentKeys:
        if key not in data:
            errors.append(f"Missing required parent key(s): '{key}'")
        elif key in data and key == "operation" and data.get("operation") not in requiredOperationValues:
            errors.append(f"Invalid value for 'operation' key. Must be 'create', 'read', 'update', or 'delete'.  Provided value was: '{data.get('operation')}'")
    
    return errors

def processRequest(data):
    """
    Route the quest to the appropriate supporting function(s)

    :data: Dictionary object containing request payload
    """
    print("Running def processRequest()...")
    errors = []
    requestType = data.get("operation")

    # Handle "create" requests
    if requestType == "create":        
        print("This is a create request!")

        # Validate whether required 'event' key is present
        if "event" not in data:
            errors.append("Missing required key 'event' for create requests")
        else:
            requiredEventKeys = ["title", "timestamp", "frequency", "data"]
            eventKeys = data.get("event")
            
            allowedFrequencyValues = ["one-time", "monthly", "quarterly", "annually"]
            frequency = eventKeys.get("frequency")
            
            # Validate whether required create 'event' keys are present
            for key in requiredEventKeys:
                if key not in eventKeys:
                    errors.append(f"Missing required child key under 'event' key: '{key}'")
            
            # Validate whether 'frequency' value is allowable
            if frequency not in allowedFrequencyValues:
                errors.append(f"Invalid value for 'frequency' key.  Must be 'one-time', 'monthly', 'quarterly' or 'annually'.  Provided value was: '{frequency}'")

            allowedDataKeys = ["amount", "currency", "location"]
            dataKeys = eventKeys.get("data")
            
            if dataKeys:
                # Validate that only allowed 'data' keys are present
                for key in dataKeys:
                    if key not in allowedDataKeys:
                        errors.append(f"Non-allowed key under 'data' key.  Allowed keys are 'amount', 'currency' or 'location'. Provided key was: '{key}'")

        if errors:
            return errors
        else:
            # Attempt to write the event to a text file (minus the "operation" key/value pair)
            data.pop("operation", None)
            errors = createEvent(data)
            return errors
            
    # Handle "read" requests
    elif requestType == "read":
        app = data.get("app_id")

        # Indicates a read all request
        if "event" not in data:
            errors = readAllEvent(app)
            if errors: return errors
        
        # Indicates a read specific request
        else:
            event = data.get("event")
            title = event.get("title")
            errors = readSpecificEvent(app, title)
            if errors: return errors


def runServer():
    """
    Main function which handles incoming requests via ZeroMQ.

    :return: List specifying error messages encountered in supporting functions (if any)
    """
    
    while True:
        try:
            # Receive incoming message via ZeroMQ
            message = socket.recv()
            print(f"\nReceived incoming message: {message}")

            # Attempt to convert message into Python dictionary
            try:
                data = json.loads(message)
            except json.JSONDecodeError as error:
                print(f"Invalid JSON object format: {error}")
                continue
            
            # Validate minimum required keys and values are present ("operation" and "app_id")
            minErrors = minimumDataValidation(data)

            if minErrors:
                # Send error message back over the socket
                print("Errors:")
                for error in minErrors:
                    print(error)
                socket.send_string(f"Errors: {minErrors}")
            else:
                # Attempt to process the request upon confirmation that minimum keys/values are present
                print("No errors from def minimumDataValidation()")
                processErrors = processRequest(data)
                # Send error message back over the socket
                if processErrors:
                    print("Errors:")
                    for error in processErrors:
                        print(error)
                    socket.send_string(f"Errors: {processErrors}")

        except KeyboardInterrupt:
            print("Server stopped!")
            break

if __name__ == "__main__":
    runServer()
