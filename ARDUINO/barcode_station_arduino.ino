#include <hidboot.h>
#include <usbhub.h>

typedef enum {NONE, GOT_A, GOT_C, GOT_D} states;
states state = NONE;
unsigned long currentValue;
byte transmEnd  = 0;
unsigned long readCommand;
unsigned long aa;
String readEcho;

//int EchoCount = 0;

char read_barcode[30] ;
String barcode;
int counter = 0;

unsigned long mili1 = 0;
unsigned long mili2 = 0;


class KbdRptParser : public KeyboardReportParser
{
  protected:
    void OnKeyDown  (uint8_t mod, uint8_t key);
};


void KbdRptParser::OnKeyDown(uint8_t mod, uint8_t key)
{
uint8_t c = OemToAscii(1, key);
if (mili1 == 0 && c > 0) {
  mili1 = micros();
}
if ( c  != 19) {
  read_barcode[counter] = read_barcode[counter] + char(c);
  counter ++;
} else {
//Serial.print("scan: "); Serial.println(read_barcode[0]);
for (int i = 7; i < 16; i ++) {

  barcode = barcode + read_barcode[i];
   
}
counter = 0;
//read_barcode[30] = "";
mili1 = 0;
}
};

USB     Usb;

HIDBoot<HID_PROTOCOL_KEYBOARD>    HidKeyboard(&Usb);


KbdRptParser KbdPrs;


void processLastState() {                                                     

  switch (state) {
    case GOT_C:
      readCommand = currentValue;
    break; 
    default:
    break;  
  }
  currentValue = 0;
  
}

void IncomingByte(const byte c) {                                            

  if (isdigit(c)) {
    if ( state == GOT_D) {
      aa *= 10;
      aa += c - '0';
      readEcho = readEcho + aa;
      aa = 0;
    }
    else {
    currentValue *= 10;
    currentValue += c- '0';
    }
  } 
  else {
    processLastState();
    switch (c) {
      case 'A':
        if (transmEnd == 1) {
          transmEnd = 0;
        }
      break;
      case 'C':
        state = GOT_C;
      break;
      case 'D':
        state = GOT_D;
        readCommand = 2;
      break;
      case 'E':
        state = NONE;
        transmEnd = 1;
      break;
      case 10:
        if (transmEnd == 1) {
          transmEnd = 0;
        }
        state = NONE;
      break;
      case 13:
        if (transmEnd == 1) {
          transmEnd = 0;
        }
        state = NONE;
      break;        
      default:
        state = NONE;
      break;
    }
  }
}


void setup()
{
  Serial.begin( 115200 );

  if (Usb.Init() == -1)
    Serial.println("OSC did not start.");

  delay( 200 );

  HidKeyboard.SetReportParser(0, (HIDReportParser*)&KbdPrs);

}



void loop()
{
  Usb.Task();

  while (Serial.available()) {
    IncomingByte(Serial.read());
  }

  if (transmEnd == 1) {
    switch(readCommand) {
      case 1:
        if (read_barcode[3] == 0 ) {
          Serial.println("0");
        } else {
        read_barcode[2] = '0';
        Serial.write("A"); Serial.write(read_barcode); Serial.println("E");Serial.flush();
        } 
      break;
      case 2:
      
        if (readEcho.toInt() == barcode.toInt() && barcode != "") {
          Serial.println("AC2E");
          for (int i = 0 ; i <31; i ++) {
            read_barcode[i] = 0;
          }
          readEcho = "";
          barcode = "";
        } else {
          Serial.println("AC3E");
            readEcho = "";
        }
      break;
    }
    readCommand = 0;
  }
}
