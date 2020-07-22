const uint8 CLOCKS[] = {
    {% for inst in instructions %}
        {{ inst.extras.clocks }}, /* {{ inst.name }} */
    {% endfor %}
};
