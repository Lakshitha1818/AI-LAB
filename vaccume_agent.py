def vacuum_agent(location, status):
    if status == "Dirty":
        return "Suck"
    elif status == "Clean":
        return "No Action"

    if location == "P":
        return "left"
    elif location == "Q":
        return "right"
    else:
        return "Invalid Location"

while True:
    location = input("Enter the location (P or Q, or 'exit' to stop): ")
    if location.lower() == 'exit':
        break
    status = input("Enter the status (Dirty or Clean): ")

    action = vacuum_agent(location, status)
    print(f"Location: {location}, Status: {status}, Action: {action}")
