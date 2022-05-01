#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "simple_message.h"

static uint8_t buffer[SIMPLE_MESSAGE_TOTAL_SIZE];

static struct simple_message message;

int main(int argc, char** argv) {
  if (argc < 2) {
    printf("You must provide a binary file name to content!\n");
  } else {
    FILE* f = fopen(argv[1], "w");
    if (f) {
      printf("Generating data to be stored:\n");
      srand(time(NULL));
      message.counter = (uint8_t)rand();
      message.field_1 = (int16_t)rand();
      for (size_t i = 0; i < SIMPLE_MESSAGE_NUMBERS_SIZE; i++) {
        message.numbers[i] = (uint32_t)rand();
      }

      printf(" counter: 0x%.2x\n", message.counter);
      printf(" field_1: 0x%.4x\n", message.field_1);
      for (size_t i = 0; i < SIMPLE_MESSAGE_NUMBERS_SIZE; i++) {
        printf(" numbers[%lu]: 0x%.8x\n", i, message.numbers[i]);
      }

      simple_message_encode(&message, buffer);
      fwrite(buffer, SIMPLE_MESSAGE_TOTAL_SIZE, 1, f);
      fclose(f);
    }
  }

  return 0;
}