import asyncio
from routes import app  # Imports the Microdot web app configured in routes.py

async def main():
    # Starts the web server
    # '0.0.0.0' means "listen on all network interfaces" (WiFi, Ethernet, etc.)
    # This allows you to control the robot from a different device (phone/laptop)
    print("http:10.65.225.38:5000")
    await app.start_server(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    # Creates the Event Loop and runs the main() function
    asyncio.run(main())