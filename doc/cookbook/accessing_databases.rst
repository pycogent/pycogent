*******************
Accessing databases
*******************

.. Gavin Huttley, Kristian Rother, Patrick Yannul, Rob Knight, Yarden Katz

NCBI
====

EUtils is a web service offered by the NCBI to access the sequence, literature and other databases by a special format of URLs. PyCogent offers an interface to construct the URLs and retrieve the results in text format.

From Pubmed
-----------

Retrieving PubMed records from NCBI by PubMed ID
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The process for getting PubMed records by PubMed ID (PMID) is very similar to that for getting sequences. Basically, you just need to pass in the unique id associated with the article. For example, if you want to get the reference to the original PyCogent paper to see how far we've come since then, you can do this:

.. doctest::

    >>> from cogent.db.ncbi import EFetch
    >>> ef = EFetch(id='17708774', db='pubmed', rettype='brief')
    >>> ef.read()
    '\n1. Genome Biol. 2007;8(8):R171.\n\nPyCogent: a toolkit...

If you want more information, there are other rettypes, e.g.

.. doctest::

    >>> ef = EFetch(id='17708774', db='pubmed', rettype='citation')
    >>> ef.read()
    '\n1. Genome Biol. 2007;8(8):R171.\n\nPyCogent: a toolkit for...

Similarly, if you want something more machine-readable (but quite a lot less human-readable), you can specify XML in the retmode:

.. doctest::

    >>> ef = EFetch(id='17708774', db='pubmed', rettype='citation', retmode='xml')
    >>> cite = ef.read()
    >>> for line in cite.splitlines()[:5]:
    ...     print line
    ... 
    <?xml version="1.0"?>
    <!DOCTYPE PubmedArticleSet PUBLIC "-//NLM//DTD PubMedArticle, 1st January 2016//EN" "http://www.ncbi.nlm.nih.gov/corehtml/query/DTD/pubmed_160101.dtd">
    <PubmedArticleSet>
    <PubmedArticle>
        <MedlineCitation Owner="NLM" Status="MEDLINE">

Only a partial example is shown as there are quite a few lines. As with sequences, you can retrieve multiple accessions at once.

Searching for records using EUtils
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Getting records by their primary identifiers is very nice if you actually have the primary identifiers, but what if you don't? For example, what if you want to do a search based on a keyword, or have a genbank accession number rather than a gi, or want to get a range of records?

Fortunately, the more general EUtils class allows this kind of complex workflow with relatively little intervention. For example, if you want to search for articles that mention PyCogent:

.. doctest::

    >>> from cogent.db.ncbi import EUtils
    >>> eu = EUtils(db='pubmed', rettype='brief')
    >>> res = eu['PyCogent']
    >>> print res.read()
    <BLANKLINE>
    1. J Appl Crystallogr. 2011 Apr 1;44(Pt 2):424-428. Epub 2011 Feb 11.
    <BLANKLINE>
    Abstractions, algorithms and data structures for structural bioinformatics in
    PyCogent.
    <BLANKLINE>
    Cieślik M, Derewenda ZS, Mura C...

...or perhaps you want only the ones with PyCogent in the title, in which case you can use any qualifier that NCBI supports:

.. doctest::

    >>> res = eu['PyCogent[ti]']
    >>> print res.read()
    <BLANKLINE>
    1. J Appl Crystallogr. 2011 Apr 1;44(Pt 2):424-428. Epub 2011 Feb 11.
    <BLANKLINE>
    Abstractions, algorithms and data structures for structural bioinformatics in
    PyCogent.
    <BLANKLINE>
    Cieślik M, Derewenda ZS, Mura C...

The NCBI-supported list of field qualifiers, and lots of documentation generally on how to do pubmed queries, is `here <http://www.ncbi.nlm.nih.gov/bookshelf/br.fcgi?book=helppubmed&part=pubmedhelp>`_.

One especially useful feature is the ability to get a list of primary identifiers matching a query. You do this by setting ``rettype='uilist'`` (not idlist any more, so again you may need to update old code examples). For example:

.. doctest::

    >>> eu = EUtils(db='pubmed', rettype='uilist')
    >>> res = eu['PyCogent']
    >>> print res.read()
    22479120
    18230758
    17708774
    <BLANKLINE>

This is especially useful when you want to do a bunch of queries (whether for journal articles, as shown here, or for sequences), combine the results, then download the actual unique records only once. You could of course do this with an incredibly complex single query, but good luck debugging that query...


For sequences
-------------

Fetching FASTA or Genpept sequences from NCBI using EFetch with GI's
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you already have a list of GI's (the numeric identifiers that are used by GenBank internally as identifers), your job is very easy: you just need to use ``EFetch`` to retrieve the corresponding records. In general, this works for any case where the identifiers you have are the primary keys, e.g. for PubMed you use the PubMed ID (see example below).

Here is an example of getting the nucleotide record that corresponds to one particular id, in this case id # 459567 (chosen arbitrarily). The record arrives as a file-like object that can be read; in this case, we are looking at each line and printing the first 40 characters.

.. doctest::

    >>> from cogent.db.ncbi import EFetch
    >>> ef = EFetch(id='459567', rettype='fasta')
    >>> lines = ef.read().splitlines()
    >>> for line in lines:
    ...     print line[:40]
    ... 
    >gi|459567|dbj|D28543.1|HPCNS5PC Hepatit
    GAGCACGACATCTACCAATGTTGCCAACTGAACCCAGAGG
    GGCTTTACCTTGGTGGTCCCATGTTTAACTCGCGAGGTCA
    CGGGGTTCTTCCAACCAGCATGGGCAATACCCTCACATGT
    GCAGGCCTCACCAATTCTGACATGTTGGTTTGCGGAGATG
    TC
    <BLANKLINE>

Similarly, if your id refers to a protein record, you can get that by setting the ``rettype`` to 'gp'.

.. doctest::

    >>> genpept = EFetch(id='1234567,459567', rettype='gp').read()

The current ``rettypes`` (as of this writing on 4/14/2010) for the 'core' NCBI databases are native, fasta, gb, gp, gbwithparts, gbc, gpc, est, gss, seqid, acc, ft. Formerly, but not currently, 'genbank' was a synonym for 'gb' and 'genpept' was a synonym for 'gp': however, these synonyms no longer work and need to be fixed if you encounter them in old code. For more information check NCBI's `format documentation <http://www.ncbi.nlm.nih.gov/corehtml/query/static/efetchseq_help.html>`_.

Note that there are two separate concepts: ``rettype`` and ``retmode``. rettype controls what kind of data you'll get, and retmode controls how the data will be formatted.

For example:

.. doctest::

    >>> from cogent.db.ncbi import EFetch
    >>> ef = EFetch(id='459567', rettype='fasta', retmode='text')
    >>> lines = ef.read().splitlines()
    >>> for line in lines:
    ...     print line[:40]
    ... 
    >gi|459567|dbj|D28543.1|HPCNS5PC Hepatit
    GAGCACGACATCTACCAATGTTGCCAACTGAACCCAGAGG
    GGCTTTACCTTGGTGGTCCCATGTTTAACTCGCGAGGTCA
    CGGGGTTCTTCCAACCAGCATGGGCAATACCCTCACATGT
    GCAGGCCTCACCAATTCTGACATGTTGGTTTGCGGAGATG
    TC
    <BLANKLINE>
    >>> ef = EFetch(id='459567', rettype='fasta', retmode='html')
    >>> lines = ef.read().splitlines()
    >>> for line in lines:
    ...     print line[:40]
    ... 
    Seq-entry ::= set {
      level 1 ,
      class nuc-prot ,
      descr {
        pub {
          pub {
            sub {
              authors {
                names
                  std {
                    {...
    >>> ef = EFetch(id='459567', rettype='fasta', retmode='xml')
    >>> lines = ef.read().splitlines()
    >>> for line in lines:
    ...     print line[:40]
    ... 
    <?xml version="1.0"?>
     <!DOCTYPE TSeqSet PUBLIC "-//NCBI//NCBI
     <TSeqSet>
    <TSeq>
      <TSeq_seqtype value="nucleotide"/>
      <TSeq_gi>459567</TSeq_gi>
      <TSeq_accver>D28543.1</TSeq_accver>
      <TSeq_taxid>11103</TSeq_taxid>
      <TSeq_orgname>Hepatitis C virus</TSeq_
      <TSeq_defline>Hepatitis C virus gene f
      <TSeq_length>282</TSeq_length>
      <TSeq_sequence>GAGCACGACATCTACCAATGTTG...

You'll notice that the second case is some funny-looking html. Thanks, NCBI! This is not our fault, please don't file a bug report. To figure out whether something is actually surprising behavior at NCBI, you can always capture the command-line and run it in a web browser. You can do this by calling ``str()`` on the ``ef``, or by printing it. For example:

.. doctest::

    >>> print ef
    http://www.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?retmax=100&retmod...

If you paste the resulting string into your web browser and you get the same incorrect result that you get using PyCogent, you know that you should direct your support requests NCBI's way. If you want to use your own email address instead of leaving it as the default (the module developer), you can do that just by passing it in as a parameter. For example, in the unlikely event that I want NCBI to contact me instead of Mike if something goes wrong with my script, I can achieve that as follows:

.. doctest::

    >>> ef = EFetch(id='459567', rettype='fasta', retmode='xml', email='rob@spot.colorado.edu')
    >>> print ef
    http://www.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?retmax=100&retmod...

You can also select multiple ids (pass in as comma-delimited list):

.. doctest::

    >>> ef = EFetch(id='459567,459568', rettype='summary', retmode='xml')
    >>> print ef.read()
    <?xml version="1.0"?>
     <!DOCTYPE Bioseq-set PUBLIC "-//NCBI//NCBI Seqset/EN" "http://www.ncbi.nlm.nih.gov/dtd/NCBI_Seqset.dtd">
     <Bioseq-set>
     <Bioseq-set_seq-set>
    <Seq-entry>
      <Seq-entry_set>
        <Bioseq-set>
          <Bioseq-set_level>1</Bioseq-set_level>
          <Bioseq-set_class value="nuc-prot"/>
          <Bioseq-set_descr>...
    

Retrieving GenPept files from NCBI via Eutils
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We query for just one accession to illustrate the process. A more general query can be executed by replacing ``'BAB52044`` with ``'"lysyl tRNA-synthetase"[ti] AND bacteria[orgn]'`` in the snippet below.

.. doctest::

    >>> from cogent.db.ncbi import EUtils
    >>> e = EUtils(numseqs=100, db='protein', rettype='gp')
    >>> result = e['BAB52044']
    >>> print result.read()
    LOCUS       BAB52044                 548 aa            linear   BCT 16-MAY-2009
    DEFINITION  lysyl tRNA synthetase [Mesorhizobium loti MAFF303099].
    ACCESSION   BAB52044
    VERSION     BAB52044.1  GI:14025444
    DBLINK      BioProject: PRJNA18
    DBSOURCE    accession BA000012.4
    KEYWORDS    .
    SOURCE      Mesorhizobium loti MAFF303099...

Retrieving and parsing GenBank entries
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. doctest::

    >>> from cogent.parse.genbank import RichGenbankParser
    >>> from cogent.db.ncbi import EUtils
    >>> e = EUtils(numseqs=100, db='protein', rettype='gp')
    >>> result = e['"lysyl tRNA-synthetase"[ti] AND bacteria[orgn]']
    >>> parser = RichGenbankParser(result.readlines())
    >>> gb = [(accession, seq) for accession, seq in parser]

Printing the resulting list (``gb``) will generate output like:

.. code-block:: python
    
    [('AAA83071', Sequence(MSEQHAQ... 505)), ('ACS40931', ...


Parsing in more detail:  a single GenBank entry
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. TODO you could select these from each sequence using the getFeaturesMatching

.. doctest::

    >>> from cogent.db.ncbi import EUtils
    >>> from cogent.parse.genbank import RichGenbankParser
    >>> e = EUtils(db="nucleotide", rettype="gb")
    >>> record = e['154102'].readlines()
    >>> parser = RichGenbankParser(record)
    >>> accession, seq = [record for record in parser][0]
    >>> accession
    'STYHEMAPRF'
    >>> type(seq)
    <class 'cogent.core.sequence.DnaSequence'>
    >>> def gene_and_cds(f):
    ...     return f['type'] == 'CDS' and 'gene' in f
    ... 
    >>> cds_features = [f for f in seq.Info.features if gene_and_cds(f)]
    >>> for cds_feature in cds_features:
    ...     print cds_feature['gene'], cds_feature['location']
    ... 
    ['hemA'] 732..1988
    ['prfA'] 2029..3111

Retrieving a bacterial genome file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To obtain a full bacterial genome, run the following to get the complete *Salmonella typhimurium* genome sequence (Genbank) file. (For this documentation, we include a partial file for illustration purposes.)

.. code-block:: python
    
    from cogent.db.ncbi import EUtils
    e = EUtils(db="nucleotide", rettype="gb")
    outfile = open('data/ST.genome.gb','w')
    outfile.write(e['AE006468'].read())
    outfile.close()

For larger files, you might want to dump them directly into a file on your hard drive rather than reading them into memory first, e.g.

.. code-block:: python

    e.filename='ST.genome.gb'
    f = e['AE006468']

dumps the result into the file directly, and returns you a handle to the open file where you can read the result, get the path, or do any of the other standard file operations. Now do the analysis:

.. doctest::
    
    >>> from cogent.parse.genbank import RichGenbankParser
    >>> infile = open('data/ST_genome_part.gb', 'r')
    >>> parser = RichGenbankParser(infile)
    >>> accession, seq = [record for record in parser][0]
    >>> gene_and_cds = lambda f: f['type'] == 'CDS' and 'gene' in f
    >>> gene_name = lambda f: f['gene']
    >>> all_cds = [f for f in seq.Info.features if gene_and_cds(f)]
    >>> for cds in sorted(all_cds, key=gene_name):
    ...     print cds['gene'][0].ljust(6),
    ...     print cds['protein_id'], cds['location']
    ... 
    mog    ['AAL18972.1'] 8729..9319
    talB   ['AAL18971.1'] 7665..8618
    thrA   ['AAL18966.1'] 337..2799
    thrB   ['AAL18967.1'] 2801..3730
    thrC   ['AAL18968.1'] 3734..5020
    thrL   ['AAL18965.1'] 190..255
    yaaA   ['AAL18969.1'] complement(5114..5887)
    yaaH   ['AAL18973.1'] complement(9376..9942)
    yaaJ   ['AAL18970.1'] complement(5966..7396)

The EUtils modules are generic, so additional databases like OMIM can be accessed using similar mechanisms.

Retrieving PubMed abstracts from NCBI via EUtils
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. doctest::
    :options: +NORMALIZE_WHITESPACE
    
    >>> from cogent.db.ncbi import EUtils
    >>> e = EUtils(db='pubmed',rettype='brief')
    >>> result = e['Simon Easteal AND Von Bing Yap'].read()
    >>> print result
    <BLANKLINE>
    1. Mol Biol Evol. 2010 Mar;27(3):726-34. doi: 10.1093/molbev/msp232. Epub 2009 Oct
    8.
    <BLANKLINE>
    Estimates of the effect of natural selection on protein-coding content.
    <BLANKLINE>
    Yap VB(1), Lindsay H, Easteal S, Huttley G...

Retrieving PubMed abstracts via PMID
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. doctest::

    >>> from cogent.db.ncbi import EUtils
    >>> e = EUtils(db='pubmed',rettype='abstract')
    >>> result = e['14983078'].read()

KEGG
====

Complete genomes
----------------

*To be written.*

Orthologs
---------

*To be written.*

Functional assignments
----------------------

*To be written.*

Pathway assignments
-------------------

*To be written.*

Ensembl
=======

.. include:: ensembl.rst

PDB
===

For structures
--------------

The PDB module is very simple and basically gets a pdb coordinates file by accession number. Searches, etc. are not currently implemented because it's easier to get the pdb ids from NCBI than to scrape PDB's html results format.

.. doctest::

    >>> from cogent.db.pdb import Pdb
    >>> p = Pdb()
    >>> result = p['3L0U']

returns a handle to a file containing the PDB coordinates (that you can, for example, pass to the PDB parser in a fashion analogous to how you pass the GenBank record above to the RichGenbankParser). See the pdb parser documentation for more info. To send results directly to a file, you can use the retrieve() method of the Pdb object.

Rfam
====

For RNA secondary structures, alignments, functions
---------------------------------------------------

*To be written.*

GoldenPath (not yet implemented)
================================

*To be written.*

Whole-genome alignments, orthologs, annotation tracks
-----------------------------------------------------

*To be written.*

.. following cleans up files

.. doctest::
    :hide:
    
    >>> from cogent.util.misc import remove_files
    >>> remove_files('ST.genome.gb', error_on_missing=False)
