#include <string.h>
#include "simple_message.h"

#define GET_U8(ptr) ((uint8_t) * (ptr))
#define GET_U16(ptr)             \
  (((uint16_t)(GET_U8((ptr)))) + \
   (((uint16_t)(GET_U8((ptr + 1)))) << 8))
#define GET_U32(ptr)              \
  (((uint32_t)(GET_U16((ptr)))) + \
   (((uint32_t)(GET_U16((ptr + 2)))) << 16))

#define GET_I8(ptr) (int8_t) * (ptr)
#define GET_I16(ptr)              \
  (((int16_t)(GET_I8((ptr)))) + \
   (((int16_t)(GET_I8((ptr + 1)))) << 8))
#define GET_I32(ptr)               \
  (((int32_t)(GET_I16((ptr)))) + \
   (((int32_t)(GET_I16((ptr + 2)))) << 16))

#define SET_U8(ptr, value) *((uint8_t*)(ptr)) = (value)
#define SET_U16(ptr, value)                   \
  {                                          \
    SET_U8(ptr, (uint8_t)(value));            \
    SET_U8(ptr + 1, (uint8_t)((value) >> 8)); \
  }
#define SET_U32(ptr, value)                      \
  {                                             \
    SET_U16(ptr, (uint16_t)(value));             \
    SET_U16(ptr + 2, (uint16_t)((value) >> 16)); \
  }

#define SET_I8(ptr, value) *((int8_t*)(ptr)) = (value)
#define SET_I16(ptr, value)                  \
  {                                         \
    SET_I8(ptr, (int8_t)(value));            \
    SET_I8(ptr + 1, (int8_t)((value) >> 8)); \
  }
#define SET_I32(ptr, value)                     \
  {                                            \
    SET_I16(ptr, (int16_t)(value));             \
    SET_I16(ptr + 2, (int16_t)((value) >> 16)); \
  }

bool simple_message_decode(const uint8_t* buffer, struct simple_message* msg) {
  if (buffer && msg && (GET_U16(buffer) == SIMPLE_MESSAGE_ID)) {
    buffer += 2;
    msg->counter = GET_U8(buffer);
    buffer += 1;
    msg->field_1 = GET_I16(buffer);
    buffer += 2;
    for (size_t i = 0; i < SIMPLE_MESSAGE_NUMBERS_SIZE; i++) {
      msg->numbers[i] = GET_U32(buffer);
      buffer += 4;
    }
    return true;
  } else {
    return false;
  }
}

bool simple_message_encode(const struct simple_message* msg, uint8_t* buffer) {
  if (msg && buffer) {
    SET_U16(buffer, SIMPLE_MESSAGE_ID);
    buffer += 2;
    SET_U8(buffer, msg->counter);
    buffer += 1;
    SET_I16(buffer, msg->field_1);
    buffer += 2;
    for (size_t i = 0; i < SIMPLE_MESSAGE_NUMBERS_SIZE; i++) {
      SET_U32(buffer, msg->numbers[i]);
      buffer += 4;
    }
    return true;
  } else {
    return false;
  }
}