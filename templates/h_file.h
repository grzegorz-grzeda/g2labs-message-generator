#ifndef G2LABS_MESSAGE_GENERATOR_{{name.upper()}}_H
#define G2LABS_MESSAGE_GENERATOR_{{name.upper()}}_H
#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

#define {{name.upper()}}_ID ((uint16_t)({{id}}))
#define {{name.upper()}}_TOTAL_SIZE ((size_t)({{total_size}}))
{% for array in arrays %}
#define {{name.upper()}}_{{array.name.upper()}}_SIZE ((size_t)({{array.size}})){% endfor %}

struct {{name}} { {% for field in fields %}
    {{field.c_type}} {{field.name}};{% endfor %}{% for array in arrays %}
    {{array.c_type}} {{array.name}}[{{name.upper()}}_{{array.name.upper()}}_SIZE];{% endfor %}
};

bool is_buffer_a_{{name}}(const uint8_t *buffer);

bool {{name}}_decode(const uint8_t *buffer, struct {{name}} *msg);

bool {{name}}_encode(const struct {{name}} *msg, uint8_t *buffer);

#endif // G2LABS_MESSAGE_GENERATOR_{{name.upper()}}_H
