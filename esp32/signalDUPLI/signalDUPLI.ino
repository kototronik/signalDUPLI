#include <WiFi.h> 
#include <LittleFS.h>
#include <WebServer.h>
#include <ESPmDNS.h>


const char* ssid = "пароль не 12345678"; 
const char* password = "a87654321";      

const int signalPin = 2;  

WebServer server(80);  

void handleFileUpload();
void generateSignalFromFile(const char* filename);
void deleteFile(const char* filename);
void sendMainPage();
void listFiles();

void setup() {
    Serial.begin(115200);


    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.print(".");
    }
    Serial.println("\nWi-Fi connected");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());

 
    if (!LittleFS.begin()) {
        Serial.println("LittleFS initialization failed. Formatting...");
        if (LittleFS.format()) {
            Serial.println("LittleFS formatted successfully");
            ESP.restart();
        } else {
            Serial.println("Failed to format LittleFS");
            return;
        }
    }

    Serial.println("LittleFS is ready");


    if (!MDNS.begin("sigi")) { 
        Serial.println("Error starting mDNS");
    } else {
        Serial.println("mDNS responder started");
        Serial.println("Now you can access the server at http://sigi.local");
    }


    pinMode(signalPin, OUTPUT);


    server.on("/", HTTP_GET, sendMainPage);
    server.on("/upload", HTTP_POST, []() {
        server.send(200, "text/plain", "File uploaded successfully");
    }, handleFileUpload);
    
    server.on("/start", HTTP_GET, []() {
        if (server.hasArg("file")) {
            String filename = server.arg("file");
            generateSignalFromFile(filename.c_str());
            server.send(200, "text/plain", "Signal generation completed for file: " + filename);
        } else {
            server.send(400, "text/plain", "No file specified");
        }
    });


    server.on("/delete", HTTP_GET, []() {
        if (server.hasArg("file")) {
            String filename = server.arg("file");
            deleteFile(filename.c_str());
            server.sendHeader("Location", "/");
            server.send(303); 
        } else {
            server.send(400, "text/plain", "No file specified");
        }
    });

    server.begin();
    Serial.println("Web server started");
}
void loop() {
    server.handleClient();
}


void sendMainPage() {
    String html = "<html><body>"
                  "<h1>ESP32 Signal Generator</h1>"

                  "<h2>Upload New File</h2>"
                  "<form method='POST' action='/upload' enctype='multipart/form-data'>"
                  "<input type='file' name='upload'><input type='submit' value='Upload File'>"
                  "</form>"

                  "<h2>Available Files</h2>"
                  "<ul>";
    
    File root = LittleFS.open("/");
    File file = root.openNextFile();
    while (file) {
        String filename = file.name();
        html += "<li>" + filename + " ";
        html += "<button onclick=\"generateSignal('" + filename + "')\">Generate Signal</button> ";
        html += "<a href='/delete?file=" + filename + "' onclick='return confirm(\"Delete this file?\")'>Delete</a>";
        html += "</li>";
        file.close();
        file = root.openNextFile();
    }

    html += "</ul>"
            "<script>"
            "function generateSignal(filename) {"
            "   fetch('/start?file=' + filename)"
            "   .then(response => response.text())"
            "   .then(data => {"
            "       alert(data);"
            "   })"
            "   .catch(error => {"
            "       alert('Error generating signal: ' + error);"
            "   });"
            "}"
            "</script>"
            "</body></html>";
    server.send(200, "text/html", html);
}


void handleFileUpload() {
    HTTPUpload& upload = server.upload();
    if (upload.status == UPLOAD_FILE_START) {
        String filename = "/" + upload.filename;
        Serial.printf("Uploading file: %s\n", filename.c_str());
        File file = LittleFS.open(filename, "w");
        if (!file) {
            Serial.println("Failed to open file for writing");
            return;
        }
        file.close();
    } else if (upload.status == UPLOAD_FILE_WRITE) {
        String filename = "/" + upload.filename;
        File file = LittleFS.open(filename, "a");
        if (file) {
            file.write(upload.buf, upload.currentSize);
            file.close();
        }
    } else if (upload.status == UPLOAD_FILE_END) {
        Serial.printf("Upload complete: %s, size %d bytes\n", upload.filename.c_str(), upload.totalSize);
        sendMainPage();
    }
}


void generateSignalFromFile(const char* filename) {
    String path = String("/") + filename;
    File file = LittleFS.open(path, "r");
    if (!file) {
        Serial.println("Failed to open file");
        return;
    }

    while (file.available()) {
        uint16_t high_duration;
        uint16_t pause;

        file.read((uint8_t*)&high_duration, sizeof(high_duration));
        file.read((uint8_t*)&pause, sizeof(pause));

        digitalWrite(signalPin, HIGH);
        delayMicroseconds(high_duration);

        digitalWrite(signalPin, LOW);
        delayMicroseconds(pause);
    }

    file.close();
    Serial.println("Signal generation completed");
}


void deleteFile(const char* filename) {
    String path = String("/") + filename;
    if (LittleFS.exists(path)) {
        LittleFS.remove(path);
        Serial.printf("File %s deleted\n", filename);
    } else {
        Serial.printf("File %s not found\n", filename);
    }
}
