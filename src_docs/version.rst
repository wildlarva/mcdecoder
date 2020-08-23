####################################
Release cycle and versioniong policy
####################################

********************************
Release cycle
********************************

We have 2 regular releases of mcdecoder in a year, or once in 6 months.
Additionally, we have a bugfix release for the latest version each time we find bugs.

********************************
Deprecation policy
********************************

If some part of the specifications are marked :code:`deprecated`, they will be removed following the next 2 regular releases, that is, 1 year later.

********************************
Versioning policy
********************************

:code:`<major>.<minor>.<micro>`

The number in each part is increased when,

<major>
    A significant change is made to the specifications of mcdecoder.
    :code:`0` means that mcdecoder is under evaluation against a real use case.
<minor>
    Some features are added to or removed from mcdecoder.
<micro>
    Some bugs are fixed or some improvements are taken place.
