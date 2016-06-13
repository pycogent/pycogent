.. _quick-install:

Quick installation using pip
============================

The following assumes you have ``pip`` on your system (this comes standard with new Macs for instance), that you have made a virtualenv_ or a conda_ environment and that you're connected to the internet.

The key steps for the minimal install are:

#. Install numpy ::

    $ pip install numpy

#. Use pip to download, build and install PyCogent. ::

    $ pip install cogent

If the above fails to download PyCogent you can `download an archive <https://github.com/pycogent/pycogent>`_ to your hard drive and then do. ::
    
    $ pip install path/to/pycogent-master.zip

Optional installs
^^^^^^^^^^^^^^^^^

To use the Ensembl querying code
""""""""""""""""""""""""""""""""

    $ pip install cogent[mysql]

To use the parallel capabilities
""""""""""""""""""""""""""""""""

    $ pip install cogent[mpi]

To install all dependencies
"""""""""""""""""""""""""""

    $ pip install cogent[all]

This will install all the above and matplotlib for drawing

To use the development version of PyCogent
""""""""""""""""""""""""""""""""""""""""""

Just replace the first line of the requirements file with ``git+https://github.com/pycogent/pycogent.git``.


.. _virtualenv: https://pypi.python.org/pypi/virtualenv
.. _conda: http://conda.pydata.org/docs/