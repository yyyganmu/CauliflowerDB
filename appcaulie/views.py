import datetime
import json
import os
import re
import subprocess

import paramiko
from django.http import FileResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from CauliflowerDB import settings
from appcaulie import models
from appcaulie.utils.pagination import Pagination


# Create your views here.


def downloadfile(request, filename):
    fileio = open(os.path.join(settings.STATIC_ROOT, 'tmp', filename), 'rb')
    response = FileResponse(fileio)
    response['Content-type'] = 'application/octet-stream'
    response['Content-Disposition'] = f'attachment;filename="{filename}"'
    return response


def home(request):
    return render(request, template_name='index.html')


def genome(request):
    return render(request, template_name='genome.html')


def download(request):
    # todo: adjust download links in 'download.html'
    return render(request, template_name='download.html')


def sampleinfo(request):
    rowdata = models.Sampleinfo.objects.all()
    page_object = Pagination(request, rowdata)
    context = {
        'datalist': page_object.page_queryset,
        'page_string': page_object.html()
    }
    return render(request, template_name='sampleinfo.html', context=context)


def revblast(request, path_param):
    return redirect(f'/cauliflowerdb/blast/{path_param}')


class SnpSeek(View):

    @staticmethod
    def paramiko_query(command):
        server = paramiko.SSHClient()
        server.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        server.connect(hostname='taascr.myddns.me', port=7251, username='yyy', password='2020apr23')
        stdin, stdout, stderr = server.exec_command(command=command, get_pty=True)
        results = stdout.read().decode('utf-8')
        results = [i.split('\t') for i in re.split(r'[\r\n]+', results)[0:-1]]  # 将结果做成一个列表列表，里面的每一个列表就是一行数据
        error = ''
        return error, results

    @staticmethod
    def subprocess_query(command):
        # execute the command
        results = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        # deal with the results
        if results.returncode != 0:
            return JsonResponse({'err': f'retrieval failure\n{command}\n{results.stderr}'})
        elif results.returncode == 0 and not results.stdout:
            return JsonResponse({'err': f'No SNPs are located in this block.'})
        else:
            error = ''
            # turn the results into a list of list, each interior list stands for a line of the results
            results = [i.split('\t') for i in re.split(r'[\r\n]+', results.stdout)[0:-1]]
            return error, results

    @staticmethod
    def get(request):
        return render(request, template_name='snpseek.html')

    @staticmethod
    def post(request):

        # parse POST date
        psdata = json.loads(request.body.decode('utf-8'))
        region = psdata.get('region')
        samples = psdata.get('samples')
        genotype = psdata.get('fjyi')  # value: '%GT' or '%TGT'
        biallelic = psdata.get('biallelic')  # value: '-m 2 -M 2 -v snps' or ''

        # verify samples' existence
        with open(os.path.join(settings.STATIC_ROOT, 'webdata', 'zsamplelist820.txt'), 'r') as fi:
            samplelist = [line.strip() for line in fi]  # 820 samples
        samples = ','.join([i for i in samples.split(',') if i in samplelist])
        if not samples:
            return JsonResponse({'err': 'Nonexistent sample(s).'})

        # concatenate a command for SNP query
        vcffile = '/home/yyy/snpvcf/zhuge820.vcf.gz'
        formation = fr'%CHROM\t%POS\t%REF\t%ALT[\t{genotype}]\n'
        command = fr"bcftools view -r {region} -s {samples} {biallelic} {vcffile} -Ou | bcftools query -f '{formation}'"

        # execute the command via either paramiko or subprocess
        # error, results = SnpSeek.subprocess_query(command=command)
        error, results = SnpSeek.paramiko_query(command=command)

        # write the results to a file for downloading
        outputfile = f'zresults_snpseek_{datetime.datetime.now().strftime("%Y%m%d")}.csv'
        with open(os.path.join(settings.STATIC_ROOT, 'tmp', outputfile), 'w') as fo:
            fo.write('CHROM,POS,REF,ALT,' + samples + '\n')
            for line in results:
                fo.write(','.join(line) + '\n')

        # return json response
        return JsonResponse({
            'err': error,
            'samples': samples.split(','),
            'snps': results,
            'link': f'/cauliflowerdb/downloadfile/{outputfile}/'
        })


class ConsensusSeq(View):

    @staticmethod
    def get(request):
        return render(request, template_name='consensusseq.html')

    @staticmethod
    def post(request):

        # parse POST date
        psdata = json.loads(request.body.decode('utf-8'))
        region = psdata.get('region')
        samples = psdata.get('samples')

        # verify samples' existence
        with open(os.path.join(settings.STATIC_ROOT, 'webdata', 'zsamplelist820.txt'), 'r') as fi:
            samplelist = [line.strip() for line in fi]  # 820 samples
        samples = [i for i in samples.split(',') if i in samplelist]
        if not samples:
            return JsonResponse({'err': 'Nonexistent sample(s).'})

        # generate consensus sequences
        genomefile = '/home/yyy/caulie/appcaulie/static/webdata/Cauliflower_genome_start3.fasta'
        vcffile = '/home/yyy/snpvcf/zhuge820.vcf.gz'
        resdic = {}  # store result data for response to front-end
        server = paramiko.SSHClient()
        server.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        server.connect(hostname='taascr.myddns.me', port=7251, username='yyy', password='2020apr23')
        for sample in samples:
            command = fr"samtools faidx {genomefile} {region} | bcftools consensus -s {sample} {vcffile}"
            stdin, stdout, stderr = server.exec_command(command=command, get_pty=True)
            result = stdout.read().decode('utf-8')
            lor = re.split(r'[\n\r]+', result)  # 'lor' for list of 'result'
            lor = [line for line in lor if not line.startswith('Warning')]
            seqid, seqseq, av = '_'.join([lor[0], sample]), ''.join(lor[1:-2]), lor[-2]  # 'av' for 'applied variants'
            resdic[seqid] = [seqseq, av]  # store the data of one sample into the dict

        # write the results to a file for downloading
        outputfile = f'zresults_consensusseq_{"_".join(samples)}_{datetime.datetime.now().strftime("%Y%m%d")}.fasta'
        with open(os.path.join(settings.STATIC_ROOT, 'tmp', outputfile), 'w') as fo:
            for key, value in resdic.items():
                fo.write(key + '\n' + value[0] + '\n')

        # return json response
        return JsonResponse({'err': '', 'seqs': resdic, 'link': f'/cauliflowerdb/downloadfile/{outputfile}/'})


class Search(View):

    @staticmethod
    def get(request):
        return render(request, 'search.html')

    @staticmethod
    def post(request):
        # parse POST date
        psdata = json.loads(request.body.decode('utf-8'))
        chrom = psdata.get('chrom')
        start = int(psdata.get('start'))
        end = int(psdata.get('end'))

        # database query
        datalist = models.Geneinfo.objects.filter(chromosome=chrom, start__gte=start, end__lte=end).values()
        datalist = list(datalist)

        # return json response
        if not datalist:
            return JsonResponse({'err': 'No genes are located in this block.'})
        return JsonResponse({'err': '', 'genes': datalist})


class SearchById(View):

    @staticmethod
    def post(request):
        """Responsible for verification for AJAX"""
        # parse POST date
        psdata = json.loads(request.body.decode('utf-8'))
        geneid = psdata.get('geneid')

        # database query
        rawdata = models.Geneinfo.objects.filter(id=geneid).first()

        if not rawdata:
            return JsonResponse({'err': f'Gene {geneid} does not exist.'})
        return JsonResponse({'err': ''})

    @staticmethod
    def get(request):
        """Responsible for data query"""
        # parse GET parameters
        geneid = request.GET.get('geneid')

        seqsdic = {}  # a dict for storing the data for response

        # data query of the table Geneinfo for information of chromosome and position, etc
        rawdata = models.Geneinfo.objects.filter(id=geneid).first()
        chrom = rawdata.chromosome
        start = rawdata.start
        end = rawdata.end

        # data query for gene and upstream sequences, results are unique for one gene ID
        rawdata = models.GeneAndUpstream.objects.filter(geneid=geneid).first()
        seqid = f'>gene_{geneid}_{len(rawdata.geneseq)}b'
        seqsdic[seqid] = rawdata.geneseq
        seqid = f'>1kb_upstream_{geneid}_{len(rawdata.upseq)}b'
        seqsdic[seqid] = rawdata.upseq

        # data query for features sequences, results are not unique for one gene ID
        rawdata = models.Features.objects.filter(geneid__contains=geneid).all()
        for feature in rawdata:
            seqsdic[f'>mRNA_{feature.geneid}_{len(feature.mrnaseq)}b'] = feature.mrnaseq
            seqsdic[f'>CDS_{feature.geneid}_{len(feature.cdsseq)}b'] = feature.cdsseq
            seqsdic[f'>protein_{feature.geneid}_{len(feature.proteinseq)}b'] = feature.proteinseq

        # write the results to a file for downloading
        outputfile = f'zresults_featureseqs_{geneid}_{datetime.datetime.now().strftime("%Y%m%d")}.fasta'
        with open(os.path.join(settings.STATIC_ROOT, 'tmp', outputfile), 'w') as fo:
            for k, v in seqsdic.items():
                fo.write(k + '\n' + v + '\n')

        # render the template
        context = {
            'geneid': geneid,
            'chrom': chrom,
            'start': start,
            'end': end,
            'filename': outputfile,
            'seqsdic': seqsdic
        }
        return render(request, template_name='genefeature.html', context=context)


class Batch(View):

    @staticmethod
    def get(request):
        return render(request, template_name='batch.html')

    @staticmethod
    def post(request):
        # parse POST data
        psdata = json.loads(request.body.decode('utf-8'))
        genes = psdata.get('genes')
        genes = genes.split(',')
        features = psdata.get('features')  # 前端返回的features是一个列表，包含了需要查询的特征序列
        features.remove('geneseq')  # 基因序列是一定要查询的，先把他从列表里去掉
        features.insert(0, 'geneid')  # 然后把geneid这个字段放到列表的开头，这个时候这个列表就变成了需要查询的字段的列表

        # open output file
        outputfile = f'zresults_batch_download_{datetime.datetime.now().strftime("%Y%m%d")}.fasta'
        fo = open(os.path.join(settings.STATIC_ROOT, 'tmp', outputfile), 'w')

        errgenes = []  # a list to store the nonexistent gene IDs for response
        for gene in genes:
            # data query for gene and upstream sequences
            genedata = models.GeneAndUpstream.objects.filter(geneid=gene).first()

            # the gene ID is mistaken if there are no results
            if not genedata:
                errgenes.append(gene)
                continue

            # write the results to the output file if there are results of gene and upstream sequences
            # write the gene and upstream sequences firstly
            fo.write(f'>gene_{genedata.geneid}\n{genedata.geneseq}\n')
            fo.write(f'>1kb_upstream_{genedata.geneid}\n{genedata.upseq}\n')
            # 判断是否需要查询特征序列。这个时候feature列表里总是有一个元素叫geneid，因此如果列表长度大于1，那就是还需要查询其他的特征序列
            if len(features) > 1:
                # 查询数据，前端返回的数据“features”是一个列表，里面就是要查询的字段，以列表解包的形式输给values()方法
                featuredata = models.Features.objects.filter(geneid__contains=gene).values(*features)
                for row in featuredata:
                    for feature in list(row.keys())[1:]:  # 第一个字段是geneid，所以从第二个开始，是序列的字段名
                        fo.write(f'>{feature}_{row["geneid"]}\n{row[feature]}\n')

        fo.close()
        return JsonResponse({'err': errgenes, 'link': f'/cauliflowerdb/downloadfile/{outputfile}'})


class Target(View):

    @staticmethod
    def get(request):
        return render(request, template_name='target.html')

    @staticmethod
    def post(request):
        # parse POST data
        psdata = json.loads(request.body.decode('utf-8'))
        geneid = psdata.get('geneid')
        block = psdata.get('block')  # maybe empty string
        ptype = psdata.get('pam')
        number = psdata.get('number')

        # verify the gene's existence
        if not models.Geneinfo.objects.filter(id=geneid).exists():
            return JsonResponse({'err': f'Gene {geneid} does not exist.'})

        # data query
        if not block:
            # search targets whole-gene wide if no block is specified
            datalist = models.Targets.objects.filter(ofgene=geneid, ptype__contains=ptype).order_by('-specificity')[:number].values()
        else:
            start = list(models.Targets.objects.filter(ofgene=geneid).values('start'))[0]['start']  # 靶点数据中某个基因最开始有靶点的位置
            end1 = list(models.Targets.objects.filter(ofgene=geneid).values('end'))[-1]['end']  # 靶点数据中某个基因上最后一个靶点的结束位置
            end2 = int(start) + int(block.split('-')[1])  # 前端页面返回的要查询的基因上的范围
            end = end1 if end1 <= end2 else end2  # 如果要查询的范围大于的基因的长度，就依然查整个基因的范围，否则就查目标区间的
            datalist = models.Targets.objects.filter(ofgene=geneid, start__gte=start, end__lte=end, ptype__contains=ptype).order_by('-specificity')[:number].values()
        datalist = list(datalist)

        # write the results to a file for downloading
        outputfile = f'z{datetime.datetime.now().strftime("%Y%m%d")}_crispr_targets_of_{geneid}.csv'
        with open(os.path.join(settings.STATIC_ROOT, 'tmp', outputfile), 'w') as fo:
            try:
                fo.write(','.join(datalist[0].keys()) + '\n')
                for line in datalist:
                    fo.write(','.join(str(i) for i in line.values()) + '\n')
            except IndexError:
                print(datalist)

        # return json response
        return JsonResponse({'err': '', 'targets': datalist, 'link': f'/cauliflowerdb/downloadfile/{outputfile}/'})