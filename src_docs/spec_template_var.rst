###############################
Template variable specification
###############################

.. table::

    ==================== =========================== ===================================================
    Variable name        Type                        Description
    ==================== =========================== ===================================================
    mcdecoder            :code:`McDecoder`           Root element of decoder model.
    machine              :code:`MachineDecoder`      Decoding information about machine.
                                                     Shorthand for :code:`mcdecoder.machine`
    machine_decoder      :code:`MachineDecoder`      Decoding information about machine.
                                                     Shorthand for :code:`mcdecoder.machine`.

                                                     Deprecated and will be removed in version 0.1b1
    instructions         Sequence of                 Decoding information about instructions
                         :code:`InstructionDecoder`  Shorthand for :code:`mcdecoder.instructions`
    instruction_decoders Sequence of                 Decoding information about instructions.
                         :code:`InstructionDecoder`  Shorthand for :code:`mcdecoder.instructions`.

                                                     Deprecated and will be removed in version 0.1b1
    ns                   string                      Namespace prefix for generated codes.
                                                     Shorthand for :code:`mcdecoder.namespace_prefix`
    extras               any (user-specific)         User-defined data for the global scope.
                                                     Shorthand for :code:`mcdecoder.extras`
    ==================== =========================== ===================================================

See :doc:`spec_mcdecoder_model`
to understand the types of template variables.
