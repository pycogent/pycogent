Evaluate process heterogeneity using a Hidden Markov Model
==========================================================

The existence of rate heterogeneity in the evolution of biological sequences is well known. Typically such an evolutionary property is evaluated using so-called site-heterogeneity models. These models postulate the existence of discrete classes of sites, where sites within a class evolve according to a specific rate that is distinct from the rates of the other classes. These models retain the assumption that alignment columns evolve independently. One can naturally ask the question of whether rate classes occur randomly throughout the sequence or whether they are in fact auto-correlated - meaning sites of a class tend to cluster together. Because we do not have, *a priori*, a basis for classifying the sites the models are specified such that each column can belong to any of the designated site classes and the likelihood is computed across all possible classifications. Post numerical optimisation we can calculate the posterior probability a site column belongs to a specific site class. In ``cogent``, site classes are referred to as ``bins`` and so we refer to bin probabilities etc ...

To illustrate how to evaluate these hypotheses formally we specify 3 nested hypotheses: (i) Ho: no rate heterogeneity; (ii) Ha(1): two classes of sites - fast and slow, but independent sites; (iii) Ha(2): fast and slowly evolving sites are auto-correlated (meaning a sites class is correlated with that of its' immediate neighbours).

In the interests of computational speed for evaluation we use a restricted example consisting of 2 aligned sequences but note that the approach applies to more than 2 sequences too. It is also possible to apply these models to different types of changes and we illustrate this with a single parameterisation at the end.

First import standard components necessary for all of the following calculations. As the likelihood ratio tests (LRT) involve nested hypotheses we will employ the chi-square approximation for assessing statistical significance.

.. doctest::

    >>> from cogent.evolve.substitution_model import Nucleotide, predicate
    >>> from cogent import LoadSeqs, LoadTree
    >>> from cogent.maths.stats import chisqprob

The alignment is read in and, as it consists of only 2 sequences, we construct the tree simply from the sequence names.

.. doctest::

    >>> aln = LoadSeqs("data/long_testseqs.fasta")
    >>> tree = LoadTree(tip_names = aln.getSeqNames())

Model Ho: no rate heterogeneity
-------------------------------

We define a HKY model of nucleotide substitution, which has a transition parameter.

.. doctest::

    >>> MotifChange = predicate.MotifChange
    >>> gap_model = dict(recode_gaps=True, model_gaps=False)
    >>> kappa = (MotifChange('R', 'R') | MotifChange('Y', 'Y')).aliased('kappa')
    >>> model = Nucleotide(predicates=[kappa], **gap_model)

We specify a null model with no bins, and optimise it. (Note that as we have only two sequences and are using a reversible evolutionary model we constrain the 2 branch lengths to be equal by setting ``is_independent=False``.)

.. doctest::

    >>> lf_one = model.makeLikelihoodFunction(tree)
    >>> lf_one.setParamRule('length', is_independent=False)
    >>> lf_one.setAlignment(aln)
    >>> lf_one.optimise(show_progress = False)
    >>> lnL_one = lf_one.getLogLikelihood()
    >>> df_one = lf_one.getNumFreeParams()
    >>> print lf_one
    Likelihood Function Table
    ================
     kappa    length
    ----------------
    7.9961    0.0271
    ----------------
    ===============
    motif    mprobs
    ---------------
        T    0.2369
        C    0.1803
        A    0.3799
        G    0.2029
    ---------------

Model Ha(1): two classes of sites - fast and slow, but independent sites
------------------------------------------------------------------------

Our next hypothesis is that there are two rate classes, or bins. We will specify the parameter boundary between these bins as that estimated from Ho.

.. doctest::

    >>> one_bin = lf_one.getParamValue("length")

We then specify a model with bins but require that alignment columns (``sites``) are independent.

.. doctest::

    >>> bin_submod = Nucleotide(predicates=[kappa], with_rate = True,
    ...      distribution='free', **gap_model)

The additional argument ``with_rate`` is for ###.

.. doctest::

    >>> lf_bins = bin_submod.makeLikelihoodFunction(tree,
    ...      bins = ['slow', 'fast'], sites_independent=True)
    >>> lf_bins.setParamRule("length", is_independent=False, init = one_bin)

Following on from the comment above concerning specifying the boundary between the rate classes using the maximum-likelihood parameter estimate from the one bin model, we shift the initial value of the parameter slightly for each bin.

.. doctest::

    >>> lf_bins.setAlignment(aln)
    >>> lf_bins.optimise(show_progress = False)
    >>> lnL_bins = lf_bins.getLogLikelihood()
    >>> df_bins = lf_bins.getNumFreeParams()
    >>> df_bins == 4
    True
    >>> print lf_bins
    Likelihood Function Table
    ==========================
     kappa    length      rate
    --------------------------
    7.9961    0.0624    0.4350
    --------------------------
    ==============
     bin    bprobs
    --------------
    slow    0.9967
    fast    0.0033
    --------------
    ===============
    motif    mprobs
    ---------------
        T    0.2369
        C    0.1803
        A    0.3799
        G    0.2029
    ---------------

Model Ha(2): fast and slowly evolving sites are auto-correlated
---------------------------------------------------------------

We then specify a model with switches, the HMM part. The setup is almost identical to that for above with the sole difference being setting the ``sites_independent=False``.

.. doctest::

    >>> lf_patches = bin_submod.makeLikelihoodFunction(tree,
    ...      bins = ['slow', 'fast'], sites_independent=False)
    >>> lf_patches.setParamRule('length', is_independent=False)
    >>> lf_patches.setAlignment(aln)
    >>> lf_patches.optimise(show_progress = False)
    >>> lnL_patches = lf_patches.getLogLikelihood()
    >>> df_patches = lf_patches.getNumFreeParams()
    >>> print lf_patches
    Likelihood Function Table
    ========================================
    bin_switch     kappa    length      rate
    ----------------------------------------
        0.5869    7.9961    0.2077    0.1307
    ----------------------------------------
    ==============
     bin    bprobs
    --------------
    slow    0.0333
    fast    0.9667
    --------------
    ===============
    motif    mprobs
    ---------------
        T    0.2369
        C    0.1803
        A    0.3799
        G    0.2029
    ---------------

We use the following short function to perform the LR test and return a formatted string.

.. doctest::

    >>> def LRT(null, alt, df_null, df_alt):
    ...     LR = 2 * (alt - null)
    ...     LR = max(0.0, LR) # avoid small negatives that can arise
    ...     df = df_alt - df_null
    ...     p = chisqprob(LR, df)
    ...     return "LR=%.2f; df=%d; p=%.2f" % (LR, df, p)

We conduct the test between the sequentially nested models.

.. doctest::

    >>> print "LR test of Bins: %s" % LRT(lnL_one, lnL_bins, df_one, df_bins)
    LR test of Bins: LR=0.03; df=2; p=0.99
    >>> print "LR test of Patches: %s" % LRT(lnL_bins, lnL_patches, df_bins,
    ... df_patches)
    LR test of Patches: LR=0.00; df=1; p=1.00

The stationary bin probabilities are labelled as ``bprobs`` and can be obtained as follows.

.. doctest::

    >>> bprobs = lf_patches.getParamValue('bprobs')
    >>> print "%.2f : %.2f" % tuple(bprobs)
    0.04 : 0.96

Also of interest, of course, are the posterior probabilities as those allow classification of sites. The result is a ``DictArray`` class instance, which behaves like a dictionary.

.. doctest::

    >>> pp = lf_patches.getBinProbs()

If we want to know the posterior probability the 21st position belongs to the ``slow`` bin, we can determine it as:

.. doctest::

    >>> print pp['slow'][20]
    0.05...

A model with patches of ``kappa``
---------------------------------

In this example we model sequence evolution where there are 2 classes of sites distinguished by their ``kappa`` parameters. Again, however, we need to know what value of ``kappa`` to specify the delineation of the bin boundaries. We can determine this from the null model's output above. Also, we calibrate these additional parameters by specifying the ``kappa`` for one bin to equal 1.0 and that it is constant.

.. doctest::

    >>> kappa_bin_submod = Nucleotide(predicates=[kappa],
    ...       ordered_param='kappa',
    ...       distribution='free', **gap_model)
    >>> lf_kappa = kappa_bin_submod.makeLikelihoodFunction(tree,
    ...      bins = ['slow', 'fast'], sites_independent=False)
    >>> lf_kappa.setParamRule("length", is_independent=False)
    >>> lf_kappa.setAlignment(aln)
    >>> lf_kappa.optimise(show_progress = False)
    >>> print lf_kappa
    Likelihood Function Table
    ==============================
     bin    bprobs    kappa_factor
    ------------------------------
    slow    0.0701          0.0890
    fast    0.9299          1.0686
    ------------------------------
    ==============================
    bin_switch     kappa    length
    ------------------------------
        0.0226    9.9752    0.0272
    ------------------------------
    ===============
    motif    mprobs
    ---------------
        T    0.2369
        C    0.1803
        A    0.3799
        G    0.2029
    ---------------