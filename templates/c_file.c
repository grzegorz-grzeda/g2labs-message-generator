#include <string.h>
#include "{{name}}.h"

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

bool {{name}}_decode(const uint8_t* buffer, struct {{name}}* msg) {
  if (buffer && msg && (GET_U16(buffer) == {{name.upper()}}_ID)) {
    buffer += 2;{%for field in fields %}
    msg->{{field.name}} = GET_{{field.define_type}}(buffer);
    buffer += {{field.byte_count}};{% endfor %}{% for array in arrays %}
    for (size_t i = 0; i < {{name.upper()}}_{{array.name.upper()}}_SIZE; i++) {
      msg->{{array.name}}[i] = GET_{{array.define_type}}(buffer);
      buffer += {{array.byte_count_per_entry}};
    }{% endfor %}
    return true;
  } else {
    return false;
  }
}

bool {{name}}_encode(const struct {{name}}* msg, uint8_t* buffer) {
  if (msg && buffer) {
    SET_U16(buffer, {{name.upper()}}_ID);
    buffer += 2;{%for field in fields %}
    SET_{{field.define_type}}(buffer, msg->{{field.name}});
    buffer += {{field.byte_count}};{% endfor %}{% for array in arrays %}
    for (size_t i = 0; i < {{name.upper()}}_{{array.name.upper()}}_SIZE; i++) {
      SET_{{array.define_type}}(buffer, msg->{{array.name}}[i]);
      buffer += {{array.byte_count_per_entry}};
    }{% endfor %}
    return true;
  } else {
    return false;
  }
}