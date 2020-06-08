{# Example usage of user-defined data for the global scope and the machine #}
/*
 * This file is generated for:
 *   - Compiler: {{ extras.compiler }}
 *   - Architecture: {{ machine.extras.arch_type }}
 */

{%- for inst in instructions -%}
    {%- for field in inst.fields -%}
        {# Example usage of user-defined data for fields #}
        {# Check if the attribute 'type' exists #}
        {%- if field.extras.type -%}
            #define FIELD_REG_TYPE_{{ inst.name }}_{{ field.name }} "{{field.extras.type}}"
        {%- endif -%}
    {%- endfor %}
{%- endfor -%}

extern uint8 CLOCKS[];
