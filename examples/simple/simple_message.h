
#ifndef SIMPLE_MESSAGE_H
#define SIMPLE_MESSAGE_H
#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>
#define SIMPLE_MESSAGE_ID (uint16_t)1
#define SIMPLE_MESSAGE_TOTAL_SIZE (size_t)45

#define SIMPLE_MESSAGE_NUMBERS_SIZE 10


struct simple_message {
    uint8_t counter;
    int16_t field_1;
    uint32_t numbers[SIMPLE_MESSAGE_NUMBERS_SIZE];
};

bool simple_message_decode(const uint8_t *buffer, struct simple_message *msg);

bool simple_message_encode(const struct simple_message *msg, uint8_t *buffer);

#endif // SIMPLE_MESSAGE_H
