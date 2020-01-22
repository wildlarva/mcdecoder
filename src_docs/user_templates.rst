############################
User templates
############################

Some users need user-specific decoder codes or
some codes to support decoders like constant tables.
mcdecoder allows users to define user-specific code templates
to generate those codes.
This is called user templates.

To use user templates, follow the steps below:

1. Add user-defined data to an MC description
2. Create user-defined template files
3. Generate codes with the created template

Here's a tutorial for user templates.

1. Add user-defined data to an MC description
=============================================

First, you may need to add some user-specific data to your MC description file.
If you don't need any additional information than MC description specification,
you can skip this step.
You can use :code:`extras` or :code:`field_extras` to define user-defined data.
They take any structure, so you can define the structure of your own.
See :doc:`spec_mc_desc` for more details.

Make :code:`arm.yaml` that contains the following content.

.. literalinclude:: ../examples/user_templates/arm.yaml
   :language: yaml
   :caption: arm.yaml

2. Create user-defined template files
=============================================

Second, you must define user-defined templates.
mcdecoder uses :download:`Jinja2 <https://jinja.palletsprojects.com/>` syntax for templates.
See :download:`Template Designer Documentation <https://jinja.palletsprojects.com/templates/>` to understand the template syntax.

You can use template variables in your template, such as
:code:`instruction_decoders` (decoder information about instructions)
or :code:`ns` (namespace prefix)
to access information about decoders and user-defined data.
See :doc:`spec_template_var` for more details.

You need to make a directory and put your template files in it.
Generated files will have the same names as those of template files.
If you use template variables in the names of template files,
the names will be generated in the same way as the contents of generated files.

This time, make :code:`templates` directory and
create the following template files.

.. literalinclude:: ../examples/user_templates/templates/{{ns}}constants.h
   :language: jinja
   :caption: templates/{{ns}}constants.h

.. literalinclude:: ../examples/user_templates/templates/{{ns}}constants.c
   :language: jinja
   :caption: templates/{{ns}}constants.c

3. Generate codes with the created template
=============================================

Finally, you must run a command to generate with the template.
Use :code:`mcdecoder generate` command and
:code:`--template` option to specify the template.
See :doc:`spec_commandline_options` for more details.

Run the command below:

.. code-block:: bash

   mcdecoder generate --template templates --output out arm.yaml

And the generated files will be:

.. literalinclude:: ../examples/user_templates/out/arm_constants.h
   :language: c
   :caption: out/arm_constants.h

.. literalinclude:: ../examples/user_templates/out/arm_constants.c
   :language: c
   :caption: out/arm_constants.c

You can see :download:`example files in this tutorial in github <https://github.com/wildlarva/mcdecoder/blob/master/examples/user_templates>`.

What's next?
=============================================

* :doc:`More details about MC description <spec_mc_desc>`
* :download:`More details about Jinja2 template syntax <https://jinja.palletsprojects.com/templates/>`
* :doc:`More details about template variables <spec_template_var>`
* :doc:`More details about MC decoder model <spec_mcdecoder_model>`
* :doc:`More details about mcdecoder generate <spec_commandline_options>`
