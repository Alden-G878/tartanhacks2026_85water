#include <Arduino.h>
#include <Servo.h>

enum rx {
  servo_num,
  command
};

rx state;

Servo s0, s1, s2, s3, s4;

int remap(int angle) {
  int source_span = 199;
  int source_min = 0;
  int target_span = 400;
  int target_min = 1500;
  double scale_factor = (double)target_span / (double)source_span;
  return (int)(target_min + (angle-source_min) * scale_factor);
}

void setup() {
  Serial1.begin(115200);
  state = servo_num;
  s0.attach(24, 1500, 1900);
  s1.attach(28, 1500, 1900);
  s2.attach(37, 1500, 1900);
  s3.attach(36, 1500, 1900);
  s4.attach(33, 1500, 1900);
  }

void loop() {
  int x = Serial1.read();
  int snum = -1;
  int cmd = -1;
  s0.write(0);
  s1.write(0);
  s2.write(0);
  s3.write(0);
  s4.write(0);
  /*if(x!=-1) {
    switch(state) {
      case servo_num:
        snum = x;
        state = command;
        break;
      case command:
        cmd = remap(x);
        Serial.printf("commanding %i microseconds\n", cmd);
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
          default:
        }
        state = servo_num;
        break;
      default:
    }
  }*/
}