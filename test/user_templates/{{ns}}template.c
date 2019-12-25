const uint8 CLOCKS[] = {
    {% for inst in instruction_decoders %}
        {{ inst.extras.clocks }}, /* {{ inst.name }} */
    {% endfor %}
};
