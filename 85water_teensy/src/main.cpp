#include <Arduino.h>

enum rx {
  servo_num,
  command
};

rx state;
void setup() {
  Serial1.begin(115200);
  state = servo_num;
}

void loop() {
  int x = Serial1.read();
  int snum = -1;
  int cmd = -1;
  if(x!=-1) {
    switch(state) {
      case servo_num:
        snum = x;
        state = command;
        break;
      case command:
        cmd = x;
        state = servo_num;
        break;
    }
  }
}