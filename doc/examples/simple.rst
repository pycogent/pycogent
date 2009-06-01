The simplest script
===================

This is just about the simplest possible Cogent script. We use a canned nucleotide substitution model: the general time reversible model.

.. doctest::

    >>> from cogent.evolve.models import GTR
    >>> from cogent import LoadSeqs, LoadTree
    >>> model = GTR()
    >>> alignment = LoadSeqs("data/test.paml")
    >>> tree = LoadTree("data/test.tree")
    >>> likelihood_function = model.makeLikelihoodFunction(tree)
    >>> likelihood_function.setAlignment(alignment)
    >>> likelihood_function.optimise(show_progress = False)
    >>> print likelihood_function
    Likelihood Function Table
    ==============================================
       A/C       A/G       A/T       C/G       C/T
    ----------------------------------------------
    0.7120    2.1574    0.0000    0.4457    4.1764
    ----------------------------------------------
    =============================
         edge    parent    length
    -----------------------------
        Human    edge.0    0.0348
    HowlerMon    edge.0    0.0168
       edge.0    edge.1    0.0222
        Mouse    edge.1    0.2047
       edge.1      root    0.0000
    NineBande      root    0.0325
     DogFaced      root    0.0554
    -----------------------------
    ===============
    motif    mprobs
    ---------------
        T    0.1433
        C    0.1600
        A    0.3800
        G    0.3167
    ---------------
