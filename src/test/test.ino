#include <Servo.h>
#include <Adafruit_NeoPixel.h>

#define PIN 13
#define NUMPIXELS 4
#define BRIGHTNESS 180       // 밝기 설정 0(어둡게) ~ 255(밝게) 까지 임의로 설정 가능

Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

Servo SL;
Servo SR;
Servo So;
// SR : 90 - 180
// SL : 90 - 0
// So : 0 - 90(hit)

void setup()
{
  SL.attach(6);
  SR.attach(5);
  So.attach(3);
  Serial.begin(9600);
  Serial.println("Serial and Motor is already");
  strip.setBrightness(BRIGHTNESS);    //  BRIGHTNESS 만큼 밝기 설정 
  strip.begin();
  strip.show();
  So.write(0);
  SR.write(90);
  SL.write(90);
}

void loop()
{
  So.write(0);
  SR.write(90);
  SL.write(90);
/*  delay(1000);
  So.write(90);
  SR.write(180);
  SL.write(0);
  delay(1000);
  */
  strip.begin();
  strip.setPixelColor(0, 255, 255, 255);          //  Neopixel 색상 설정 ( 첫번째 소자위치 , 색상설정(Red) , 0 , 0 )
  strip.setPixelColor(1, 255, 255, 255);          //  ( 두번째 소자위치 , 0 , 색상설정(Green) , 0 )
  strip.setPixelColor(2, 255, 255, 255);          //  ( 세번째 소자위치 , 0 , 0 , 색상설정(Blue) )
  strip.setPixelColor(3, 255, 255, 255);  //  ( 네번째 소자위치 , (Red) , (Green) , (Blue) ) 3가지 색을 다 킨다면 White가 켜짐
  strip.show();                                         //  LED가 켜지는 동작을 하게 합니다
//  delay(2000);
/*
  //  colorWipe 함수를 적용하면 모든 LED를 동일한 색상으로 적용합니다.
  colorWipe(strip.Color(255,0,0),100);   //  strip 색상을 ( 255 (Red) , 0 (Green) , 0 (Blue) , 마지막 100은 딜레이 타임으로 
  delay(1500);
  colorWipe(strip.Color(0,255,0),100);   //  strip 색상을 ( 0 (Red) , 255 (Green) , 0 (Blue) , 100)
  delay(1500);
  colorWipe(strip.Color(0,0,255),100);   //  strip 색상을 ( 0 (Red) , 0 (Green) , 255 (Blue) , 100)
  delay(1500);
  colorWipe(strip.Color(255,255,255),100);  //  strip 색상을 ( 255 (Red) , 255 (Green) , 255 (Blue) , 100)  " White "
  delay(1500);*/
}
/*
void colorWipe(uint32_t c, uint8_t wait){    //  loop에서 사용할 colorWipe 함수를 만든 공식
  for(uint16_t i=0; i<strip.numPixels(); i++){
  strip.setPixelColor(i,c);
  strip.show();
  delay(wait);
  }
}*/