#include <Adafruit_NeoPixel.h>

#define PIN 6

#include <ros.h>
#include <std_msgs/String.h>
Adafruit_NeoPixel strip = Adafruit_NeoPixel(16, PIN, NEO_GRB + NEO_KHZ800);

ros::NodeHandle  nh;


std_msgs::String str_msg;
ros::Publisher neo("neo_state", &str_msg);

int mode = 0;
void messageCb( const std_msgs::String& toggle_msg){
  String str = toggle_msg.data;
  if(str == "speaking")
  {
    mode = 1;
    digitalWrite(LED_BUILTIN, LOW);
//    digitalWrite(LED_BUILTIN, HIGH);
//    rainbowCycle(5);
//    delay(3000);  
//    strip.begin();
  }
  else if(str == "wait")
  {
    mode = 0;
    digitalWrite(LED_BUILTIN, HIGH);
//    digitalWrite(LED_BUILTIN, LOW);
//    rainbow(20);
//    delay(3000);  
//    strip.begin();
  }
}


ros::Subscriber<std_msgs::String> sub("EMOTI/neo", messageCb );


void setup() {
  nh.initNode();
//  nh.advertise(neo_state);sp
  nh.subscribe(sub);
  pinMode(LED_BUILTIN, OUTPUT);
//  Serial.begin(57600);
  strip.begin(); //네오픽셀을 초기화하기 위해 모든LED를 off시킨다
  strip.show(); 
}

void loop() {
  if (mode == 0) {
    rainbow(20);
  } else {
    digitalWrite(LED_BUILTIN, HIGH);
    // colorWipe(strip.Color(255, 0, 0), 20);
    rainbowCycle(20);
  }
  nh.spinOnce();
  
}

//NeoPixel에 달린 LED를 각각 주어진 인자값 색으로 채워나가는 함수
void colorWipe(uint32_t c, uint8_t wait) {
  for(uint16_t i=0; i<strip.numPixels(); i++) {
      strip.setPixelColor(i, c);
      strip.show();
      delay(wait);
  }
}

//모든 LED를 출력가능한 모든색으로 한번씩 보여주는 동작을 한번하는 함수
void rainbow(uint8_t wait) {
  uint16_t i, j;

  for(j=0; j<256; j++) {
    for(i=0; i<strip.numPixels(); i++) {
      strip.setPixelColor(i, Wheel((i+j) & 255));
    }
    strip.show();
    delay(wait);
  }
}

//NeoPixel에 달린 LED를 각각 다른색으로 시작하여 다양한색으로 5번 반복한다
void rainbowCycle(uint8_t wait) {
  uint16_t i, j;

  for(j=0; j<256; j++) {
    for(i=0; i<strip.numPixels(); i++) {
      strip.setPixelColor(i, Wheel(((i * 256 / strip.numPixels()) + j) & 255));
    }
    strip.show();
    delay(wait);
  }
}

//255가지의 색을 나타내는 함수
uint32_t Wheel(byte WheelPos) {
  if(WheelPos < 85) {
   return strip.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
  } else if(WheelPos < 170) {
   WheelPos -= 85;
   return strip.Color(255 - WheelPos * 3, 0, WheelPos * 3);
  } else {
   WheelPos -= 170;
   return strip.Color(0, WheelPos * 3, 255 - WheelPos * 3);
  }
}
