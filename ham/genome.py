from abc import ABCMeta, abstractmethod
from . import abstractgene
import ete3

class Genome(metaclass=ABCMeta):

    """Genome abstract class for genomes.

    Attributes:
        genes    list of genes that belong to this genome
        taxon    related Taxonomy.tree element

    """

    def __init__(self):
        self.genes = []
        self.taxon = None
        self.name = None


    def add_gene(self, gene):
        if not isinstance(gene, abstractgene.AbstractGene):
            raise TypeError("expect subclass obj of '{}', got {}"
                            .format(abstractgene.AbstractGene.__name__,
                                    type(gene).__name__))
        self.genes.append(gene)
        gene.set_genome(self)

    def set_taxon(self, taxon):
        if not isinstance(taxon, ete3.coretype.tree.TreeNode):
            raise TypeError("expect subclass obj of '{}', got {}"
                            .format(ete3.coretype.tree.TreeNode.__name__,
                                    type(taxon).__name__))
        if self.taxon is not None and taxon != self.taxon:
            raise EvolutionaryConceptError("only one taxon can refers to one genome")
        self.taxon = taxon

    def __str__(self):
        return self.name



class AncestralGenome(Genome):

    """AncestralGenome class for ancestral genomes (inherit from Genome).

    Attributes:
        parent    list of genes that belong to this genome
        children    related Taxonomy.tree element

    """

    def __init__(self):
        super(AncestralGenome, self).__init__()
        self.name = None
        self.ancestral_clustering = None # {hog -> [extant genes]}

    def get_name(self):
        return self.name


    def get_ancestral_clustering(self):
        if self.ancestral_clustering is None:
            self.ancestral_clustering = {}
            for hog in self.genes:
                self.ancestral_clustering[hog] = hog.get_all_descendant_genes()
        return self.ancestral_clustering

    def get_number_genes(self):
        return len(self.genes)

class ExtantGenome(Genome):

    """ExtantGenome class for extant genomes (inherit from Genome).

    Attributes:
        name    unique name use by HAM to denote specifically this extant genome
        taxid    related NCBI taxId

    """

    def __init__(self, name, NCBITaxId, **kwargs):
        super(ExtantGenome, self).__init__()
        self.name = name
        self.taxid = NCBITaxId

    def get_number_genes(self, singleton=True):
        if singleton:
            return len(self.genes)
        else:
            nbr = 0
            for g in self.genes:
                if g.parent is not None:
                    nbr += 1
            return nbr


class EvolutionaryConceptError(Exception):
    pass
