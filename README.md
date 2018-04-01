# nissan
A basic application to track your [and your friends'] phones (read:cars).

# environment
python 2.7
with flask, flask_mqtt, sqlite3 packages installed

# to run
1. Navigate to the "nissan" directory where app.py is situated from your terminal.
2. Specify the application to run: $ export FLASK_APP=app.py
3. Run the app: $ flask run
4. navigate to the URL displayed.

# Implementation
### run time
**home**
![home](/home.png)

**login**                  |  **wrong login**
:-------------------------:|:-------------------------:
![login](/login.png)       |  ![wrong](/wrong.png)

**car 1**                  |  **admin**
:-------------------------:|:-------------------------:
![car](/mahim.png)         |  ![admin](/admin.png)

### back end
 A mobile app (Owntracks) sends the location data to a private MQTT broker (on cloud). The connection is established when we are logged in to the application and the MQTT isntance, then, subscribe to the topic of the corresponding user (or all topics if we are logged in as admin). The mqtt keeps running in the background waiting for any message to be published to the topic it has subscribed. Anytime a message is published, it extracts out the location attribute from that message and updates the variable containing map marker coordinates.
 The map is refreshed every 3 seconds, automatically, to update the display according to the new coordinates.
 
 Login authorisation is being maintained in the "users" table in "database.db". This table also has topic names corresponding to each user, where they publishe the message, on MQTT broker.
