{# Example usage of user-defined data for the global scope and the machine #}
/*
 * This file is generated for:
 *   - Compiler: {{ extras.compiler }}
 *   - Architecture: {{ machine_decoder.extras.arch_type }}
 */
#include "{{ ns }}constants.h"

const uint8 CLOCKS[] = {
    {%- for inst in instruction_decoders -%}
        {# Example usage of user-defined data for instructions #}
        {# Check if the attribute 'clocks' exists #}
        {%- if inst.extras.clocks -%}
            {{ inst.extras.clocks }}, /* {{ inst.name }} */
        {%- else -%}
            0, /* {{ inst.name }} */
        {%- endif -%}
    {%- endfor %}
};
