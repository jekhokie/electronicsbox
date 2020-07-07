#include <ESP8266WiFi.h>
#include <ESPAsyncTCP.h>
#include <ESPAsyncWebServer.h>
#include <WiFiUdp.h>
#include <FS.h>
#include <WS2812FX.h>
#include <Ticker.h>

// USER CONFIGURATIONS //
const char* ssid = "<WIFI_SSID>";           // WiFi SSID (network name)
const char* passwd = "<WIFI_PASSWORD>";     // WiFi password
const char* expectedRFID = "0E008E9B5B40";  // ID of the RFID card used

// PROGRAM CONFIGURATIONS //
#define LED_PIN 2               // GPIO pin on ESP for LED control
#define LED_COUNT 20            // number of LEDs in LED strip
#define LED_BRIGHTNESS 128      // brightness of LEDs when lit
#define WIRELESS_TIMEOUT 10000  // timeout connecting to wifi triggering ESP reboot
#define SERVER_PORT 80          // web server port
#define UDP_PORT 1234           // port to advertise IP address on
#define ADVERTISE_SECONDS 3     // how often to advertise/send IP broadcast (seconds)
#define NUM_STATUS_BLINKS 3     // number of LED blinks on RFID status check
#define BROADCAST_ADDRESS IPAddress(255, 255, 255, 255) // broadcast address

// VARS //
String cardInput;        // raw input of RFID card ID (contains non-alphanumeric chars)
String cardID;           // string built with only alphanumeric components of card ID
WiFiUDP udp;             // UDP handler for broadcasting IP address
Ticker broadcastTicker;  // async timer for frequency of IP broadcast
int availableStatus = 1; // state management of LEDs (0=busy(red),1=free(green))
int powerStatus = 0;     // whether LEDs are on/off (0=off,1=on)

// INITIALIZATION //
AsyncWebServer server(SERVER_PORT);   // init web server
WS2812FX ws2812fx = WS2812FX(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800); // init LEDs

// FUNCTIONS //
// default 404/not found handling for web server
void notFound(AsyncWebServerRequest *request) {
  request->send(404, "text/plain", "Not found");
}

// advertise location of this availability device - advertised as:
//    AVAILABILITY:<IP_ADDRESS>:<WEB_SERVER_PORT>
void advertiseLocation() {
  String reachme = "AVAILABILITY:" + WiFi.localIP().toString() + ":" + SERVER_PORT + "\n";
  char msg[255];
  reachme.toCharArray(msg, 255);

  udp.beginPacketMulticast(BROADCAST_ADDRESS, UDP_PORT, WiFi.localIP());
  udp.write(msg);
  udp.endPacket();
}

// blink the current status known
void blinkStatus() {
  Serial.println("Blinking status...");
  static int frameCount;

  // calculate the number of times we should blink and do it
  frameCount = 0;
  ws2812fx.setMode(FX_MODE_BLINK);
  ws2812fx.start();
  while (true) {
    ws2812fx.service();

    if (ws2812fx.isFrame()) {
      frameCount++;

      // if we've blinked enough, return to normal operation
      if (frameCount >= (NUM_STATUS_BLINKS*2)) {
        break;
      }
    }
  }

  Serial.println("Done blinking status");
  ws2812fx.setMode(FX_MODE_STATIC);

  // check if LEDs were off
  if (powerStatus == 0) {
    ws2812fx.stop();
  }
}

// connect to wifi
void connectWifi() {
  unsigned long start_of_connection = millis();
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");

    if (millis() - start_of_connection > WIRELESS_TIMEOUT) {
      Serial.println();
      Serial.println("Exceeded wireless timeout - rebooting");
      ESP.reset();
    }
  }

  // print network and IP address lease
  Serial.println();
  Serial.print("Connected to: ");
  Serial.println(ssid);
  Serial.print("My IP address: ");
  Serial.println(WiFi.localIP());
}

// SETUP //
void setup() {
  // some startup things
  Serial.begin(9600);
  delay(500);
  Serial.println("\n\nInitializing...");

  // connect to wifi and obtain IP address
  WiFi.begin(ssid, passwd);
  Serial.print("Connecting to wireless SSID '");
  Serial.print(ssid);
  Serial.print("'");

  // connect to wifi
  connectWifi();

  // start SPIFFS to enable data storage of
  // the html, javascript, and style files
  if (!SPIFFS.begin()) {
    Serial.println("ERROR: Could not mount SPIFFS");
    return;
  }
  
  // initialize/set up the LED light strip
  Serial.println("Initializing the WS2812FX Light Strip...");
  ws2812fx.init();
  ws2812fx.setMode(FX_MODE_STATIC);
  ws2812fx.setColor(GREEN);  // free by default
  ws2812fx.setBrightness(LED_BRIGHTNESS);
  ws2812fx.stop();  // off by default
  Serial.println("Light strip set up.");

  // set up some routes
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request) {
    Serial.println("Received GET request at '/'");
    request->send(SPIFFS, "/index.html");
  });

  server.on("/power", HTTP_GET, [](AsyncWebServerRequest *request) {
    Serial.println("Received GET request at '/power'");
    request->send(200, "text/plain", String(powerStatus));
  });

  server.on("/status", HTTP_GET, [](AsyncWebServerRequest *request) {
    Serial.println("Received GET request at '/status'");
    request->send(200, "text/plain", String(availableStatus));
  });

  server.on("/power", HTTP_POST, [](AsyncWebServerRequest *request) {
    Serial.println("Received POST request at '/power'");
    String message;

    if (request->hasParam("message", true)) {
      message = request->getParam("message", true)->value();
      Serial.println("...Received content: " + message);

      if (message == "0") {
        Serial.println("Requested Power Off");
        powerStatus = 0;
        ws2812fx.stop();
      } else if (message == "1") {
        Serial.println("Requested Power On");
        powerStatus = 1;
        ws2812fx.start();
      } else {
        Serial.println("Unknown state requested!");
      }
    } else {
      Serial.println("...No content received");
    }
  });

  server.on("/status", HTTP_POST, [](AsyncWebServerRequest *request) {
    Serial.println("Received POST request at '/status'");
    String message;
    
    if (request->hasParam("message", true)) {
      message = request->getParam("message", true)->value();
      Serial.println("...Received content: " + message);
      if (message == "0") {
        Serial.println("Requested Busy");
        availableStatus = 0;
        ws2812fx.setColor(RED);
      } else if (message == "1") {
        Serial.println("Requested Free");
        availableStatus = 1;
        ws2812fx.setColor(GREEN);
      } else {
        Serial.println("Unknown state requested!");
      }
    } else {
      Serial.println("...No content received");
    }
    
    request->send(200, "text/plain", "");
  });

  // bind 404/not found handler
  server.onNotFound(notFound);

  // start the server (async - does not use even loop "loop()")
  server.begin();

  // set up ability to advertise location information
  // every XX seconds to avoid over-advertising in loop
  // and/or adding a delay/sleep in loop which would delay
  // the functionality of the LED strip
  broadcastTicker.attach(ADVERTISE_SECONDS, advertiseLocation);
}

// LOOP //
void loop() {
  // accommodate if ESP loses wifi connectivity - attempt to reconnect
  if (WiFi.status() != WL_CONNECTED) {
    connectWifi();
  }
  
  // read values from the RFID reader
  if (Serial.available() > 0) {
    cardID = "";
    cardInput = "";

    // read all characters for message
    cardInput = Serial.readString();
    Serial.print("Card Input (RAW): ");
    Serial.println(cardInput.substring(0));

    // parse only ID components/remove garbage chars
    for (int i = 0; i < cardInput.length(); i++) {
      if (isalnum(cardInput[i])) {
        cardID += cardInput[i];
      }
    }

    // check if card matches our expected ID - if so, take action
    if (cardID == expectedRFID) {
      Serial.print("Received Expected RFID Card ID: ");
      Serial.println(cardID);

      blinkStatus();
    } else {
      Serial.print("Received Unexpected RFID Card ID (ignoring): '");
      Serial.println(cardID);
    }
  } else {
    // drive the LED strip
    ws2812fx.service();
  }
}
