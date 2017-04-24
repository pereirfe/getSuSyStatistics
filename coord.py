#!/usr/bin/python
# -*- coding: utf-8 -*-

# Lucas Carrilho Pessoa
# lucascpessoa@gmail.com
#
# Coleta as informações da turma de coordenação


import urllib2
import ssl
import sys
from unicodedata import normalize



#Codigos de coloração do terminal

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#Encontra substring entre first e last
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""
    
def remover_acentos(txt, codif='utf-8'):
    return normalize('NFKD', txt.decode(codif)).encode('ASCII','ignore')

#Coleta as informações das páginas do SuSy
def getInfo(lab):
    print 'Coletando informações do laboratório %s'%lab
    resultado = {}
    url = 'https://susy.ic.unicamp.br:9999/mc102coord/' + lab


    urlTurma = url + '/relatocoord.html'

    #Pega a página de submissões da turma em questão
    context = ssl._create_unverified_context()
    response = urllib2.urlopen(urlTurma,context=context)
    html = response.read()

    #Testa se a página é vazia
    if 'Página inexistente ou inacessível' in html:
        print 'Não há submissões para a turma ',turma

    else:
        #Isola a tabela de submissoes
        tabela = find_between(html,"<TABLE border=1>","</TABLE>")
        #Separa cada linha da tabela
        tabela = tabela.replace('\n','').replace('</TR>','').split('<TR>')
        #Retira cabeçalho da tabela
        tabela = tabela[2:]
        #Itera sobre cada aluno, levantando as informações de submissoes
        for linha in tabela:
            aluno = linha.replace('</TD>','').split('<TD align=center>')[1:]
            usuario = aluno[0]
            total = int(aluno[1])
            corretas = int(aluno[2])
            if aluno[3] == 'Correta':
                final = 1
            else:
                final = 0
            resultado[usuario] = {'total':total,
                                 'corretas':corretas,
                                 'final':final}
    return resultado

                
                
#Imprime tabela consilidada
def tabela(resultado):
    alunos = {}
    with open("turmacoord","rb") as arq:
        for aluno in arq.readlines():
            aluno = aluno.replace('\n','').split(':')
            alunos[aluno[0]] = remover_acentos(aluno[1])
    
    print "----------------------------------------------------------------------------------------"
    print "| {:<40}| {:<8}| {:<17}| {:<14}|".format('Nome',
                                                   'Total',
                                                   'Finais Corretas',
                                                   'Estado Final')
    print "----------------------------------------------------------------------------------------"
    total = 0
    corretas = 0
    finais_corretas = 0

    for aluno in sorted(alunos.keys()):
        if aluno not in resultado.keys():
            color = bcolors.FAIL
            print color + "| {:<40}| {:<8}| {:<17}| {:<14}|".format(alunos[aluno],
                                                       '--',
                                                       '--',
                                                       '--') + bcolors.ENDC
        else:
            total += resultado[aluno]['total']
            corretas += resultado[aluno]['corretas']
            finais_corretas += resultado[aluno]['final']

            if resultado[aluno]['final'] == 0:
                color = bcolors.WARNING
            else:
                color = ''

            print color + "| {:<40}| {:<8}| {:<17}| {:<14}|".format(alunos[aluno],
                                                           resultado[aluno]['total'],
                                                           resultado[aluno]['corretas'],
                                                           resultado[aluno]['final']) + bcolors.ENDC
    
    
    print "----------------------------------------------------------------------------------------"
  
    print "| {:<40}| {:<8}| {:<17}| {:<14}|".format('Totais',
                                                   total,
                                                   corretas,
                                                   finais_corretas)
    print "----------------------------------------------------------------------------------------"
            
if __name__ == '__main__':
    try:
        lab = sys.argv[1]
        #Coleta as informações
        resultado = getInfo(lab)
        #Imprime tabela de resultados
        tabela(resultado)
        
    except IndexError:
        print 'Você deve inserir o numero do laboratorio.\nExemplo: python main.py 00'