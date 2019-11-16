from .webserver import WebServer
import time


def getWebServer():
    return WebServer(host="0.0.0.0", port=8080, name="WebServer")

try:
    webserver = getWebServer()
    # Start
    webserver.start()
    while True:
        command = input()
        if command == 'r':
            print("Restarting servers...")
            webserver.end()  # Stop
            webserver = getWebServer()   # Reset
            webserver.start()  # Start
        elif command == 's':
            print("Exiting servers...")
            webserver.end()
            break
except KeyboardInterrupt:
    print("Exiting servers...")
    if webserver:
        webserver.end()
