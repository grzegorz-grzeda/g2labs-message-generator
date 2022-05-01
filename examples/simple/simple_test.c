#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "simple_message.h"

static uint8_t buffer[SIMPLE_MESSAGE_TOTAL_SIZE];

static struct simple_message write_message;
static struct simple_message read_message;

int main(int argc, char** argv) {
  // Writting and encoding
  srand(time(NULL));
  write_message.counter = (uint8_t)rand();
  write_message.field_1 = (int16_t)rand();
  for (size_t i = 0; i < SIMPLE_MESSAGE_NUMBERS_SIZE; i++) {
    write_message.numbers[i] = (uint32_t)rand();
  }

  simple_message_encode(&write_message, buffer);

  // Decoding and reading
  simple_message_decode(buffer, &read_message);
  bool are_equal = (read_message.counter == write_message.counter);
  printf("Test results (before and after processing):\n");
  printf(" counter: 0x%.2x --- 0x%.2x%s\n", read_message.counter,
         write_message.counter, are_equal ? "" : " !!!");
  are_equal = (read_message.field_1 == write_message.field_1);
  printf(" field_1: 0x%.4x --- 0x%.4x%s\n", read_message.field_1,
         write_message.field_1, are_equal ? "" : " !!!");
  for (size_t i = 0; i < SIMPLE_MESSAGE_NUMBERS_SIZE; i++) {
    are_equal = (read_message.numbers[i] == write_message.numbers[i]);
    printf(" numbers[%lu]: 0x%.8x --- 0x%.8x%s\n", i, read_message.numbers[i],
           write_message.numbers[i], are_equal ? "" : " !!!");
  }

  // comparing:
  are_equal =
      (memcmp(&write_message, &read_message, sizeof(write_message)) == 0);
  printf("Message content befor and after processing is %sthe same\n",
         are_equal ? "" : "NOT ");

  return 0;
}