#!/usr/bin/python
# -*- coding: utf-8 -*-

# Lucas Carrilho Pessoa
# lucascpessoa@gmail.com
#
# Coleta as informações de submissões do SuSy
#
# As turmas estão definidas no arquivo <turmas.csv>
#   A primeira coluna é a sigla da turma (por exemplo mc102abcd)
#   As próximas n colunas são cada uma das turmas da disciplina (por exemplo A,B,C,D)
#
# Para executar, digite python main.py <ID_DO_LABOARTORIO>
# por exemplo, para recuperar dados da tarefa 00, digite <python main.py 00>
#
# Ao fim, é impresso uma tabela contendo um consolidado das submissÕes
# e também um arquivo <subissoesTAREFA.csv> com todos os alunos que submeteram a tarefa

import urllib2
import ssl
import sys

#Encontra substring entre first e last
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

#Coleta as informações das páginas do SuSy
def getInfo(lab):
    print 'Coletando informações do laboratório %s'%lab
    resultado = {}
    with open('turmas.csv','rb') as turmasInput:
        for grupo in turmasInput.readlines():
            grupo = grupo.replace('\n','').split(',')
            url = 'https://susy.ic.unicamp.br:9999/' + grupo[0] + '/' + lab
            for turma in grupo[1:]:
                resultado[turma] = {}

                urlTurma = url + '/relato' + turma + '.html'

                #Pega a página de submissões da turma em questão
                context = ssl._create_unverified_context()
                response = urllib2.urlopen(urlTurma, context=context)
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
                        resultado[turma][usuario] = {'total':total,
                                                     'corretas':corretas,
                                                     'final':final}
    return resultado

#Processa os resultados e gera um dicionários de informações consolidadas, por turma
def consolidaResultados(resultados):
    consolidado = {}
    for turma in resultados.keys():
        consolidado[turma] = {'total':0,'corretas':0,'finais_corretas':0,'alunos':0}
        for aluno in resultados[turma].keys():
            consolidado[turma]['total'] += resultados[turma][aluno]['total']
            consolidado[turma]['corretas'] += resultados[turma][aluno]['corretas']
            consolidado[turma]['finais_corretas'] += resultados[turma][aluno]['final']
            consolidado[turma]['alunos'] += 1

    return consolidado

#Gera csv de saída com resultados das submissoes
def resultadosOutput(resultados,lab):
    filename = 'submissoes' + lab + '.csv'
    with open(filename,'wb') as arq:
        #Imprime cabeçalho
        arq.write('Turma,Aluno,Total,Corretas,Nota Final\n')
        for turma in sorted(resultados.keys()):
            for aluno in sorted(resultados[turma].keys()):
                #Para cada aluno, imprime sua turma, usuario, total de submissoes, total de submissores corretas, e a nota final
                #O calculo da nota final é: 10 se a última submissão foi correta, 0 caso contrário
                arq.write(turma + ',' + aluno + ',' + str(resultados[turma][aluno]['total']) + ',' + str(resultado[turma][aluno]['corretas']) + ',' + str(resultado[turma][aluno]['final'] * 10) + '\n')




#Imprime tabela consilidada
def tabelaConsolidada(consolidado):
    print "---------------------------------------------------------------------------"
    print "| {:<8}| {:<8}| {:<10}| {:<17}| {:<21} |".format('Turma',
                                                   'Total',
                                                   'Corretas',
                                                   'Finais Corretas',
                                                   'Alunos com Submissão')
    print "---------------------------------------------------------------------------"
    total = 0
    corretas = 0
    finais_corretas = 0
    alunos = 0
    for turma in sorted(consolidado.keys()):
        total += consolidado[turma]['total']
        corretas += consolidado[turma]['corretas']
        finais_corretas += consolidado[turma]['finais_corretas']
        alunos += consolidado[turma]['alunos']
        if consolidado[turma]['alunos'] != 0:
            percentual = "(%6.2f%%)"%((float(consolidado[turma]['finais_corretas'])/float(consolidado[turma]['alunos']))*100)
        else:
            percentual = "(  ---  )"
        print "| {:<8}| {:<8}| {:<10}| {:<5}{:<12}| {:<21}|".format(turma,
                                                       consolidado[turma]['total'],
                                                       consolidado[turma]['corretas'],
                                                       consolidado[turma]['finais_corretas'],
                                                       percentual,
                                                       consolidado[turma]['alunos'])
    print "---------------------------------------------------------------------------"
    if alunos != 0:
        percentual = "(%6.2f%%)"%((float(finais_corretas)/float(alunos))*100)
    else:
        percentual = "(  ---  )"
    print "| {:<8}| {:<8}| {:<10}| {:<5}{:<12}| {:<21}|".format('Totais',
                                                   total,
                                                   corretas,
                                                   finais_corretas,
                                                   percentual,
                                                   alunos)
    print "---------------------------------------------------------------------------"

if __name__ == '__main__':
    try:
        lab = sys.argv[1]
        #Coleta as informações
        resultado = getInfo(lab)
        #Gera arquivo com as notas
        resultadosOutput(resultado,lab)
        #Gera relatório consolidado
        consolidado = consolidaResultados(resultado)
        #Imprime tabela consolidada
        tabelaConsolidada(consolidado)

    except IndexError:
        print 'Você deve inserir o numero do laboratorio.\nExemplo: python main.py 00'
