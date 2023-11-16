#Exercício 1
def limpa_texto(cad_carateres):
    """Esta função recebe uma cadeia de carateres qualquer e devolve a cadeia de carateres
    correspondente à remoção de carateres brancos da mesma, conforme descrito no enunciado.

    :param cad_carateres: cadeia de carateres a limpar.
    :return: cadeia de carateres limpa (após a remoção dos espaços brancos).
    """
    lista_palavras = cad_carateres.split()
    cadeia_limpa = " ".join(lista_palavras)
    return cadeia_limpa

def corta_texto(cad_carateres, larg_coluna):
    """Esta função recebe uma cadeia de carateres e um inteiro positivo
    e devolve duas cadeias de carateres limpas.

    A cadeia de carateres e o inteiro positivo fornecidos como argumentos correspondem
    a um texto limpo e a uma largura de coluna, respetivamente. A primeira cadeia devolvida
    contém todas as palavras completas desde o inicio da cadeia original até um comprimento
    máximo igual à largura fornecida e a segunda contém o resto do texto de entrada.

    :param cad_carateres: cadeia correspondente a texto limpo.
    :param larg_coluna: inteiro positivo correspondente a largura de coluna.
    :return: duas cadeias de cararateres limpas.
    """
    primeira_cadeia, segunda_cadeia = "", ""

    if larg_coluna < len(cad_carateres):
        if cad_carateres[larg_coluna - 1] == " ":
            primeira_cadeia = cad_carateres[:larg_coluna]
            segunda_cadeia = cad_carateres[larg_coluna:]
        else:
            carater = larg_coluna
            while cad_carateres[carater] != " ":
                carater -= 1
            primeira_cadeia = cad_carateres[:carater + 1]
            segunda_cadeia = cad_carateres[carater + 1:]
    else:
        primeira_cadeia += cad_carateres

    return primeira_cadeia.strip(), segunda_cadeia.strip()

def insere_espacos(cad_carateres, larg_coluna):
    """Esta função recebe uma cadeia de carateres e um inteiro positivo e devolve uma
    cadeia de carateres.

    A cadeia de carateres e o inteiro positivo fornecidos correspondem a um texto limpo e a
    uma largura de coluna, respetivamente. A cadeia de carateres devolvida tem comprimento
    igual à largura de coluna fornecida com espaços entre palavras conforme descrito no enunciado
    caso a cadeia original contenha duas ou mais palavras. Caso contrário, é devolvida uma cadeia
    de comprimento igual à largura da coluna formada pela original seguida de espaços.

    :param cad_carateres: cadeia correspondente a texto limpo.
    :param larg_coluna: inteiro positivo correspondente a largura de coluna.
    :return: cadeia de carateres com espaços inseridos tal como é pedido.
    """
    lista_palavras = cad_carateres.split()
    cadeia_nova = ""
    lista_nova = []

    #Caso o número de palavras do texto de entrada seja maior ou igual a 2
    if len(lista_palavras) >= 2:
        #Lista com palavras e espaços
        for i in range(len(lista_palavras)):
            lista_nova += [lista_palavras[i], " "]
        lista_nova.pop()

        # Lista com posição dos espaços (números ímpares)
        posicao = []
        for i in range(len(lista_nova)):
            if " " in lista_nova[i]:
                posicao.append(i)

        #Cálculo de espaços restantes
        num_espacos = len(posicao)
        tamanho_restante = larg_coluna - len("".join(lista_nova))

        #Inserção de espaços na lista
        for i in posicao:
            lista_nova[i] = " " + " " * int(tamanho_restante // num_espacos)
            # lista_nova[i] = " " * (1 + int(tamanho_restante / num_espacos))
        # Inserção de Espaços restantes
        if tamanho_restante % num_espacos != 0:
            resto = tamanho_restante % num_espacos
            for i in posicao:
                if resto > 0:
                    lista_nova[i] += " "
                resto -= 1
        #Conversão da lista obtida para string
        cadeia_nova = "".join(lista_nova)

    # Caso o texto de entrada só tenha uma palavra
    else:
        cadeia_nova += cad_carateres
        while len(cadeia_nova) < larg_coluna:
            cadeia_nova += " "

    return cadeia_nova

def justifica_texto(cad_carateres, larg_coluna):
    """Esta função recebe uma cadeia de carateres não vazia e um inteiro positivo
    e devolve um tuplo de cadeias de carateres justificadas.

    A cadeia de carateres e o inteiro positivo fornecidos correspondem a um texto
    qualquer e a uma largura de coluna, respetivamente. O tuplo devolvido contém
    cadeias de carateres de comprimento igual à largura da coluna especificada com
    espaços entre palavras conforme o descrito no enunciado.

    :param cad_carateres: cadeia correspondente a um texto qualquer.
    :param larg_coluna: inteiro positivo correspondente a uma largura de coluna.
    :return: tuplo que contém cadeias de carateres justificadas.
    """
    #Validação de Argumentos
    if type(cad_carateres) != str or type(larg_coluna) != int or len(cad_carateres) == 0:
        raise ValueError("justifica_texto: argumentos invalidos")
    lista_palavras = cad_carateres.split()
    for i in lista_palavras:
        if len(i) > larg_coluna:
            raise ValueError("justifica_texto: argumentos invalidos")

    #Limpar o texto
    texto_limpo = limpa_texto(cad_carateres)

    #Cortar o texto
    linhas = []
    while True:
        texto_cortado, resto = corta_texto(texto_limpo, larg_coluna)
        linhas.append(texto_cortado)
        texto_limpo = resto
        if texto_limpo == "":
            break

    #Inserção de espaços em cada uma das linhas do texto
    linhas_justificadas = ()
    for l in range(len(linhas) - 1):
        linhas_justificadas += (insere_espacos(linhas[l], larg_coluna),)

    #Última linha
    tamanho_restante = larg_coluna - len(linhas[-1])
    ultima_linha = linhas[-1]
    while tamanho_restante > 0:
        ultima_linha += " "
        tamanho_restante -= 1
    linhas_justificadas += (ultima_linha,)

    return linhas_justificadas

#Exercício 2
def calcula_quocientes(votos, deputados):
    """Esta função recebe um dicionário e um inteiro positivo e devolve um dicionário.

    O dicionário e o inteiro positivo fornecidos correspondem aos votos apurados num
    círculo eleitoral e ao número de deputados desse mesmo círculo, respetivamente.
    O dicionário devolvido tem as mesmas chaves do dicionário fornecido, cada uma para
    um partido, e os valores que lhes correspondem são listas com os quocientes calculados
    pelo método de Hondt ordenados em ordem decrescente.

    :param votos: dicionário com os votos aputados num círculo eleitoral.
    :param deputados: inteiro positivo correspondente ao número de deputados.
    :return: dicionário com os quocientes calculados pelo método de Hondt.
    """
    partidos = {}
    for i in votos:
        lista_quocientes, n = [], 1
        while n <= deputados:
            lista_quocientes.append(votos[i]/n)
            n += 1
        partidos[i] = lista_quocientes
    return partidos

#Função adicional que verifica o número de ocorrências de um valor numa dada lista
def ocorrencia_lista(lista, valor):
    """Esta função verifica o número de ocorrências de um certo elemento numa lista
    e devolve esse número.

    :param lista: lista de elementos a ser analisada.
    :param valor: valor cujo número de ocorrências se quer verificar.
    :return: número de ocorrências do valor dado na lista fornecida.
    """
    cont = 0
    for i in lista:
        if i == valor:
            cont += 1
    return cont

#Função adicional que ordena as chaves de um dicionário pelos respetivos valores
def ordenar_dic(dic):
    """Esta função ordena as chaves de um dicionário pelos respetivos valores.

    :param dic: dicionário a ser ordenado.
    :return: dicionário com as chaves ordenadas pelo seu valor.
    """
    valores_ordenados = sorted(dic.values(), reverse=True)
    dic_ordenado = {}

    for v in valores_ordenados:
        for c in dic.keys():
            if dic[c] == v:
                dic_ordenado[c] = dic[c]

    return dic_ordenado

def atribui_mandatos(votos, deputados):
    """Esta função recebe um dicionário e um inteiro e devolve uma lista ordenada.

    O dicionário e o inteiro fornecidos correspondem aos votos apurados num círculo
    e a um número de deputados, respetivamente. A lista devolvida tem tamanho igual
    ao número de deputados fornecido e contém as cadeias de carateres dos partidos
    que obtiveram cada mandato, correspondendo a primeira posição desta lista ao
    primeiro deputado, a segunda posição ao segundo deputado, assim sucessivamente.

    :param votos: dicionário correspondente aos votos apurados num círculo.
    :param deputados: inteiro corresponde ao número de deputados.
    :return: lista ordenada dos partidos que obtiveram cada mandato.
    """
    partidos = calcula_quocientes(votos, deputados)
    lista_quocientes = []

    #Lista com todos os quocientes
    for p in partidos:
        for q in partidos[p]:
            lista_quocientes.append(q)
    #Ordenação da lista com todos os quocientes
    lista_quocientes.sort(reverse=True)

    #Verificação a que partido corresponde cada um dos quocientes
    lista_partidos, cont, iguais = [], 0, []

    while len(lista_partidos) < deputados:
        for i in partidos:
            #Se não houver partidos com quocientes iguais
            if lista_quocientes[cont] in partidos[i] and ocorrencia_lista(lista_quocientes, lista_quocientes[cont]) == 1:
                lista_partidos.append(i)
                cont += 1
            #Se houver dois ou mais partidos com quocientes iguais
            elif lista_quocientes[cont] in partidos[i] and ocorrencia_lista(lista_quocientes, lista_quocientes[cont]) > 1:
                #Registar que partidos têm quocientes iguais
                for p in partidos:
                    if lista_quocientes[cont] in partidos[p]:
                        iguais.append(p)
                #Comparar votos de partidos com quocientes iguais e adição do partido com menos votos à lista
                dic_iguais = {}
                for l in iguais:
                    dic_iguais[l] = votos[l]

                ind_partido = 0
                for i in dic_iguais:
                    lista_partidos.append(sorted(dic_iguais, key=dic_iguais.get)[ind_partido])
                    ind_partido += 1
                    cont += 1

    while len(lista_partidos) > deputados:
        lista_partidos.pop()

    return lista_partidos

def obtem_partidos(info):
    """Esta função recebe um dicionário e devolve uma lista.

    O dicionário fornecido corresponde à informação sobre as eleições num
    território com vários círculos eleitorais e a lista que é devolvida
    contém, por ordem alfabética, o nome de todos os partidos participantes
    nas eleições.

    :param info: dicionário correspondente à informação sobre as eleições.
    :return: lista com o nome de todos os partidos por ordem alfabética.
    """
    partidos = []

    for r in info:
        for i in info[r]:
            if type(info[r][i]) == dict:
                for p in info[r][i]:
                    if p not in partidos:
                        partidos.append(p)

    return sorted(partidos)

#Função adicional que ordena uma lista por um critério específico
def ordem_lista(x):
    """Esta função recebe uma lista e devolve dois dos seus elementos como
    critério de desempate na ordenação dessa mesma lista.

    :param x: lista a ser ordenada.
    :return: dois elementos da lista por uma ordem específica de ordenamento.
    """
    return x[1], x[2]

def obtem_resultado_eleicoes(info):
    """Esta função recebe um dicionário e devolve uma lista ordenada.

    O dicionário fornecido corresponde à informação sobre as eleições num
    determinado território com vários círculos eleitorais e devolve uma lista
    ordenada cujo comprimento é igual ao número total de partidos participantes
    nas eleições. Cada elemento da lista é um tuplo de tamanho 3 e que contém
    o nome de um partido, o número total de deputados obtidos por esse partido
    e o seu número total de votos. Esta lista está ordenada por ordem descendente
    ao número de deputados obtidos e, em caso de empate, de acordo com o número
    de votos.

    :param info: dicionário correspondente à informação sobre as eleições.
    :return: tuplo correspondente ao resultado das eleições.
    """
    #Validação de Argumentos
    if type(info) != dict or len(info) == 0:
        raise ValueError("obtem_resultado_eleicoes: argumento invalido")
    for c in info:
        votos_circ = 0
        if type(c) != str or len(c) == 0:
            raise ValueError("obtem_resultado_eleicoes: argumento invalido")
        elif type(info[c]) != dict or "deputados" not in info[c] or "votos" not in info[c]:
            raise ValueError("obtem_resultado_eleicoes: argumento invalido")
        elif len(info[c]) != 2 or type(info[c]["deputados"]) != int or type(info[c]["votos"]) != dict:
            raise ValueError("obtem_resultado_eleicoes: argumento invalido")
        elif len(info[c]["votos"]) == 0 or info[c]["deputados"] <= 0:
            raise ValueError("obtem_resultado_eleicoes: argumento invalido")
        for p in info[c]["votos"]:
            if type(info[c]["votos"][p]) != int or info[c]["votos"][p] < 0 or type(p) != str:
                raise ValueError("obtem_resultado_eleicoes: argumento invalido")
            #Número de votos do círculo
            votos_circ += info[c]["votos"][p]
        if votos_circ == 0:
            raise ValueError("obtem_resultado_eleicoes: argumento invalido")

    resultados, lista_deputados = [], []

    #Obter todos os partidos que participaram nas eleições
    partidos = obtem_partidos(info)

    #Calcular quocientes de cada um dos partidos e atribuir mandatos em cada um dos círculos eleitorais
    for r in info:
        deputados, votos = 0, {}

        for i in info[r]:
            if type(info[r][i]) == int:
                deputados = info[r][i]
            elif type(info[r][i]) == dict:
                votos = info[r][i]

        #Lista com todos os deputados
        for d in atribui_mandatos(votos, deputados):
            lista_deputados.append(d)

    #Dicionário ordenado com partidos e número de deputados correspondente
    dic_deputados = {}
    for p in partidos:
        dic_deputados[p] = ocorrencia_lista(lista_deputados, p)
    dic_deputados = ordenar_dic(dic_deputados)

    #Dicionário ordenado com número de votos de cada partido
    dic_votos = {}

    for p in partidos:
        dic_votos[p] = 0

    for r in info:
        for i in info[r]:
            if type(info[r][i]) == dict:
                for p in info[r][i]:
                    dic_votos[p] += info[r][i][p]

    dic_votos = ordenar_dic(dic_votos)

    #Apresentar resultados das eleições no formato pedido
    for p in partidos:
        resultados.append((p,dic_deputados[p], dic_votos[p]))

    resultados.sort(key=ordem_lista, reverse=True)

    return resultados

#Exercício 3
def produto_interno(t1, t2):
    """Esta função recebe dois tuplos com a mesma dimensão e devolve um
    número real.

    Os tuplos fornecidos correspondem a dois vetores e o número real
    devolvido é o resultado do produto interno desses dois vetores.

    :param t1: tuplo correspondente a um vetor.
    :param t2: tuplo correspondente a um outro vetor.
    :return: produto interno entre os dois vetores fornecidos.
    """
    res = 0
    if len(t1) == len(t2):
        for i in range(len(t1)):
            res += t1[i] * t2[i]

    return float(res)

def verifica_convergencia(linhas, const, x, prec):
    """Esta função recebe três tuplos de igual dimensão e um valor real
    positivo e devolve um valor lógico (ou booleano).

    O primeiro tuplo é constituído por um conjunto de tuplos, cada um
    representando uma linha da matriz quadrada A, e os outros dois tuplos
    correspondem, respetivamente, ao vetor de constantes c e à solução atual x.
    O valor real de entrada indica a precisão pretendida para a solução.
    A função devolve True caso o valor absoluto do erro de todas a equações
    seja inferior à precisão fornecida, e False em caso contrário.

    :param linhas: tuplo constituído por tuplos representando linhas da matriz quadrada A.
    :param const: tuplo correspondente ao vetor de constantes c.
    :param x: tuplo correspondente à solução atual x.
    :param prec: valor real correspondente à precisão pretendida para a solução.
    :return: valor lógico correspondente à condição enunciada.
    """
    for i in range(len(linhas)):
        if abs(produto_interno(linhas[i], x) - const[i]) > prec:
            return False
    return True

#Função adicional para trocar linhas de uma matriz e coordenadas de um vetor
def troca_linha(lista, i, j):
    """Esta função troca duas linhas de uma matriz ou duas coordenadas de
    um vetor.

    O primeiro argumento fornecido corresponde a uma lista que representa
    ou uma matriz ou um vetor. Os dois argumentos restantes são dois inteiros
    que correspondem a duas linhas dessa matriz ou vetor. Esta função devolve
    uma lista com o mesmo número de elementos da lista fornecida mas com os
    elementos especificados trocados.

    :param lista: lista cujos elementos serão trocados.
    :param i: inteiro correspondente a uma linha da matriz ou vetor.
    :param j: inteiro correspondente a uma outra linha da matriz ou vetor.
    :return: lista com os elementos especificados trocados.
    """
    lista[j], lista[i] = lista[i], lista[j]
    return lista

#Função adicional que verifica se há zeros na diagonal de uma matriz
def ha_zeros_diagonal(mat):
    """Esta função verifica se há zeros na diagonal principal de uma matriz
    e devolve um valor lógico (ou booleano).

    :param mat: lista cujos elementos correspondem às linhas de uma matriz.
    :return: valor lógico correspondente à condição referida.
    """
    for i in range(len(mat)):
        if mat[i][i] == 0:
            return True
    return False

def retira_zeros_diagonal(mat, const):
    """Esta função recebe dois tuplos e devolve dois tuplos.

    Os tuplos fornecidos correspondem a uma matriz de entrada e a um
    vetor de constantes. Esta função devolve uma nova matriz com as
    mesmas linhas que a de entrada, mas com estas reordenadas de forma
    a não existirem valores 0 na diagonal principal. A função devolve
    ainda o vetor de entrada com a mesma reordenação de linhas aplicada
    à matriz.

    :param mat: tuplo cujos elementos correspondem a linhas de uma matriz.
    :param const: tuplo correspondente a um vetor de constantes.
    :return: tuplos correspondentes à matriz e ao vetor reordenados.
    """
    #Lista cujos elementos são as linhas da matriz
    lista_mat = []
    for l in mat:
        lista_mat.append(l)

    #Lista cujos elementos são as coordenadas do vetor
    lista_const = []
    for c in const:
        lista_const.append(c)

    # Verificar se há zeros na diagonal e, nesse caso, troca de linhas da matriz e do vetor
    while ha_zeros_diagonal(lista_mat):
        encontrar_j = False
        for i in range(len(lista_mat)):
            if lista_mat[i][i] == 0:
                    for j in range(len(lista_mat)):
                        if lista_mat[j][i] != 0 and lista_mat[i][j] != 0:
                            while not encontrar_j:
                                encontrar_j = True
                                lista_mat = troca_linha(lista_mat, i, j)
                                lista_const = troca_linha(lista_const, i, j)
            encontrar_j = False

    return tuple(lista_mat), tuple(lista_const)

def eh_diagonal_dominante(mat):
    """Esta função recebe um tuplo e devolve um valor lógico (ou booleano).

    O tuplo fornecido corresponde a uma matriz quadrada. A função devolve
    True caso a matriz fornecida seja diagonal dominante e False em caso
    contrário.

    :param mat: tuplo correspondente a uma matriz quadrada.
    :return: valor lógico correspondente à condição referida.
    """
    #Cálculo do valor absoluto da diagonal e verificação para cada uma das linhas da matriz
    for i in range(len(mat)):
        soma_diag, soma_linha = abs(mat[i][i]), 0
        for c in range(len(mat[i])):
            if c != i:
                soma_linha += abs(mat[i][c])
        if soma_diag < soma_linha:
            return False
    return True

def resolve_sistema(mat, const, prec):
    """Esta função recebe dois tuplos e um valor real positivo e devolve
    um tuplo.

    Os dois tuplos fornecidos correspondem a uma matriz quadrada e a um
    vetor de constantes, respetivamente. O valor real positivo fornecido
    corresponde à precisão pretendida para a solução. A função devolve
    um tuplo que é a solução do sistema de equações de entrada aplicando
    o método de Jacobi.

    :param mat: tuplo correspondente a uma matriz quadrada.
    :param const: tuplo correspondente a um vetor de constantes.
    :param prec: valor real positivo correspondente à precisão pretendida.
    :return: tuplo correspondente à solução do sistema de equações.
    """
    #Validação de Argumentos
    #Matriz
    if type(mat) != tuple or len(mat) == 0:
        raise ValueError("resolve_sistema: argumentos invalidos")

    for i in mat:
        if type(i) != tuple or len(i) != len(mat):
            raise ValueError("resolve_sistema: argumentos invalidos")

        for j in i:
            if not isinstance(j, (int, float)):
                raise ValueError("resolve_sistema: argumentos invalidos")
    #Constante
    if type(const) != tuple or len(const) == 0 or len(const) != len(mat):
        raise ValueError("resolve_sistema: argumentos invalidos")
    for c in const:
        if not isinstance(c, (int, float)):
            raise ValueError("resolve_sistema: argumentos invalidos")
    #Precisão
    if not isinstance(prec, float) or prec <= 0:
        raise ValueError("resolve_sistema: argumentos invalidos")


    #Eliminação de entradas a zero da diagonal por troca de linhas da matriz
    mat, const = retira_zeros_diagonal(mat, const)

    #Teste se a matriz é diagonal dominante
    if not eh_diagonal_dominante(mat):
        raise ValueError("resolve_sistema: matriz nao diagonal dominante")

    #Cálculo da solução do sistema
    x = ()
    for i in range(len(mat)):
        x += (0,)

    while not verifica_convergencia(mat, const, x, prec):
        xi = ()
        for i in range(len(x)):
            s = x[i] + (const[i] - produto_interno(mat[i], x)) / mat[i][i]
            xi += (s,)
        x = xi

    return x
