#include <Arduino.h>
#include <Servo.h>

enum rx {
  servo_num,
  command
};

rx state;

Servo s0, s1, s2, s3, s4, s5, s6;

void setup() {
  Serial1.begin(115200);
  state = servo_num;
  s0.attach(-1, 1500, 1900);
  s1.attach(-1, 1500, 1900);
  s2.attach(-1, 1500, 1900);
  s3.attach(-1, 1500, 1900);
  s4.attach(-1, 1500, 1900);
  s5.attach(-1, 1500, 1900);
  s6.attach(-1, 1500, 1900);
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
        switch(snum) {
          case 0:
            s0.writeMicroseconds(cmd);
            break;
          case 1:
            s1.writeMicroseconds(cmd);
            break;
          case 2:
            s2.writeMicroseconds(cmd);
            break;
          case 3:
            s3.writeMicroseconds(cmd);
            break;
          case 4:
            s4.writeMicroseconds(cmd);
            break;
          case 5:
            s5.writeMicroseconds(cmd);
            break;
          case 6:
            s6.writeMicroseconds(cmd);
            break;
          default:
        }
        state = servo_num;
        break;
      default:
    }
  }
}