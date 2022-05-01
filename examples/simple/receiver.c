#include <stdio.h>
#include "simple_message.h"

static uint8_t buffer[SIMPLE_MESSAGE_TOTAL_SIZE];

static struct simple_message message;

int main(int argc, char** argv) {
  if (argc < 2) {
    printf("You must provide a binary file name to content!\n");
  } else {
    FILE* f = fopen(argv[1], "r");
    if (f) {
      printf("Reading file:\n");
      fread(buffer, SIMPLE_MESSAGE_TOTAL_SIZE, 1, f);
      simple_message_decode(buffer, &message);

      printf(" counter: 0x%.2x\n", message.counter);
      printf(" field_1: 0x%.4x\n", message.field_1);
      for (size_t i = 0; i < SIMPLE_MESSAGE_NUMBERS_SIZE; i++) {
        printf(" numbers[%lu]: 0x%.8x\n", i, message.numbers[i]);
      }

      fclose(f);
    }
  }

  return 0;
}