#include <Keypad.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

const uint8_t  ROWS = 4; 
const uint8_t  COLS = 4; 
char keys[ROWS][COLS] = {
  {'1','2','3','A'},
  {'4','5','6','B'},
  {'7','8','9','C'},
  {'*','0','#','D'}
};
uint8_t  rowPins[ROWS] = {2, 3, 4, 5}; 
uint8_t  colPins[COLS] = {6, 7, 8, 9}; 
Keypad keypad = Keypad(makeKeymap(keys), rowPins, colPins, ROWS, COLS);

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
#define OLED_RESET    -1 
#define OLED_I2C_ADDRESS 0x3C 
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);


void setup() {
  // put your setup code here, to run once:
  Serial1.begin(115200);
  Serial1.println("Hello, Raspberry Pi Pico W!");

  if (!display.begin(SSD1306_I2C_ADDRESS, OLED_I2C_ADDRESS)) {
    Serial1.println(F("SSD1306 allocation failed"));
  }
   display.display();
  delay(2000); 
  display.clearDisplay();

  display.setTextSize(1);     
  display.setTextColor(SSD1306_WHITE); 
  display.setCursor(0, 0);   
  display.println(F("Hello, Raspberry Pi Pico W!"));
  Serial1.println("Hello, Display");
  display.display();


}
void loop() {
  // put your main code here, to run repeatedly:
  char key = keypad.getKey();
  if (key != NO_KEY) {
    Serial1.println(key);
  }
  delay(1); // this speeds up the simulation
}