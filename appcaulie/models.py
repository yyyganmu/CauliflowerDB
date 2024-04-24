# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Features(models.Model):
    geneid = models.CharField(max_length=20)
    mrnaseq = models.TextField()
    cdsseq = models.TextField()
    proteinseq = models.TextField()

    class Meta:
        managed = False
        db_table = 'features'

    def __str__(self):
        return self.geneid


class GeneAndUpstream(models.Model):
    geneid = models.CharField(max_length=20)
    geneseq = models.TextField()
    upseq = models.TextField()

    class Meta:
        managed = False
        db_table = 'gene_and_upstream'

    def __str__(self):
        return self.geneid


class Geneanno(models.Model):
    seqid = models.CharField(max_length=10)
    source = models.CharField(max_length=15)
    type = models.CharField(max_length=25)
    start = models.IntegerField()
    end = models.IntegerField()
    strand = models.CharField(max_length=1)
    phase = models.CharField(max_length=1)
    attributes = models.CharField(primary_key=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'geneanno'


class Geneinfo(models.Model):
    chromosome = models.CharField(max_length=10)
    start = models.IntegerField()
    end = models.IntegerField()
    strand = models.CharField(max_length=1)
    id = models.CharField(primary_key=True, max_length=20)

    class Meta:
        managed = False
        db_table = 'geneinfo'

    def __str__(self):
        return self.id


class Sampleinfo(models.Model):
    sampleid = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=50)
    clade = models.CharField(max_length=10)
    group = models.CharField(max_length=10)
    taxonomy = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'sampleinfo'

    def __str__(self):
        return self.sampleid


class Targets(models.Model):
    chrom = models.CharField(max_length=10)
    strand = models.CharField(max_length=5)
    start = models.IntegerField()
    end = models.IntegerField()
    ptype = models.CharField(max_length=10)
    pam = models.CharField(max_length=10)
    cleavage = models.CharField(max_length=30)
    ofgene = models.CharField(max_length=20)
    ifcds = models.CharField(max_length=10)
    specificity = models.DecimalField(max_digits=5, decimal_places=2)
    offtargets = models.IntegerField()
    seq = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'targets'

    def __str__(self):
        return f'{self.chrom}, {self.start}'