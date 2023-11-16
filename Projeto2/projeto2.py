#TAD gerador
#R[xorshiftbits(s=estado)] = {"estado": R[estado], "bits": R[bits]}

#cria_gerador: int x int --> gerador
#cria_copia_gerador: gerador --> gerador
#obtem_estado: gerador --> int
#define_estado: gerador x int --> int
#atualiza_estado: gerador --> int
#eh_gerador: universal --> lógico (booleano)
#geradores_iguais: gerador x gerador --> lógico (booleano)
#gerador_para_str: gerador --> str
#gera_numero_aleatorio: gerador x int --> int
#gera_carater_aleatorio: gerador x str --> str

#Função adicional xorshift
#xorshift: int x int --> int
def xorshift(b, s):
    """Esta função adicional recebe dois inteiros, correspondentes à dimensão do estado
    de um gerador (número de bits) e ao estado atual desse gerador, e realiza uma
    sequência de operações xorshift, devolvendo o novo valor do estado.

    :param b: inteiro positivo correspondente ao número de bits do gerador.
    :param s: inteiro positivo correspondente ao estado atual do gerador.
    :return: inteiro positivo correspondente ao novo valor do estado do gerador.
    """
    if b == 32:
        s ^= (s << 13) & 0xFFFFFFFF
        s ^= (s >> 17) & 0xFFFFFFFF
        s ^= (s << 5) & 0xFFFFFFFF
    elif b == 64:
        s ^= (s << 13) & 0xFFFFFFFFFFFFFFFF
        s ^= (s >> 7) & 0xFFFFFFFFFFFFFFFF
        s ^= (s << 17) & 0xFFFFFFFFFFFFFFFF
    return s

def cria_gerador(b, s):
    """Esta função recebe um inteiro correspondente ao número de bits do gerador
    e um inteiro positivo correspondente ao estado inicial e devolve o gerador
    correspondente, representado internamente por um dicionário.

    :param b: inteiro correspondente ao número de bits do gerador.
    :param s: inteiro positivo correspondente ao estado inicial (seed).
    :return: dicionário correspondente ao gerador.
    """
    #Validação de argumentos
    if b not in (32, 64):
        raise ValueError("cria_gerador: argumentos invalidos")
    elif type(b) != int or type(s) != int or s <= 0:
        raise ValueError("cria_gerador: argumentos invalidos")
    elif s >= 2 ** (b + 1):
        raise ValueError("cria_gerador: argumentos invalidos")
    #Operação xorshift
    xorshift(b, s)
    return {"estado": s, "bits": b}

def cria_copia_gerador(ger):
    """Esta função recebe um gerador como representado na função anterior
    e devolve uma cópia nova do mesmo.

    :param ger: dicionário correspondente ao gerador.
    :return: novo dicionário correspondente à cópia nova do gerador.
    """
    return dict(ger)

def obtem_estado(ger):
    """Esta função recebe um gerador como representado anteriormente e
    devolve o estado atual do mesmo sem o alterar.

    :param ger: dicionário correspondente ao gerador.
    :return: inteiro positivo correspondente ao estado atual do gerador.
    """
    return ger["estado"]

#Função adicional que devolve os bits de um gerador
#obtem_bits: gerador --> int
def obtem_bits(ger):
    """Esta função adicional recebe um gerador como representado anteriormente e
    devolve o número de bits do mesmo sem o alterar.

    :param ger: dicionário correspondente ao gerador.
    :return: inteiro correspondente ao número de bits do gerador.
    """
    return ger["bits"]

def define_estado(ger, est):
    """Esta função recebe um gerador como representado anteriormente e um
    inteiro que irá ser definido como o novo valor do estado do gerador,
    devolvendo esse valor.

    :param ger: dicionário correspondente ao gerador.
    :param est: inteiro que irá ser definido como novo valor do estado do gerador.
    :return: inteiro já definido como novo valor do estado do gerador.
    """
    ger["estado"] = est
    return est

def atualiza_estado(ger):
    """Esta função recebe um gerador como representado anteriormente e atualiza o seu
    estado de acordo com o algoritmo xorshift de geração de números pseudoaleatórios,
    e devolve o novo valor do estado.

    :param ger: dicionário correspondente ao gerador.
    :return: inteiro correspondente ao novo valor do estado do gerador.
    """
    define_estado(ger,xorshift(obtem_bits(ger), obtem_estado(ger)))
    return obtem_estado(ger)

def eh_gerador(arg):
    """Esta função recebe um argumento e devolve True caso este seja
    um TAD gerador e False em caso contrário.

    :param arg: argumento a verificar se é ou não TAD gerador.
    :return: valor lógico correspondente à condição referida.
    """
    return type(arg) == dict and len(arg) == 2 and \
           type(obtem_estado(arg)) == int and type(obtem_bits(arg)) == int and \
           obtem_estado(arg) > 0 and (obtem_bits(arg) in (32, 64))

def geradores_iguais(g1, g2):
    """Esta função recebe dois geradores como representados anteriormente e
    devolve True se estes forem geradores iguais e False em caso contrário.

    :param g1: dicionário correspondente a um dos geradores a verificar.
    :param g2: dicionário correspondente ao outro gerador a verificar.
    :return: valor lógico correspondente à condição referida.
    """
    if eh_gerador(g1) and eh_gerador(g2):
        return obtem_estado(g1) == obtem_estado(g2) and obtem_bits(g1) == obtem_bits(g2)
    return False

def gerador_para_str(ger):
    """Esta função recebe um gerador e devolve uma cadeia de carateres
    correspondente à sua representação externa.

    :param ger: gerador a representar.
    :return: cadeia de carateres correspondente à representação externa do gerador.
    """
    return "xorshift{}(s={})".format(obtem_bits(ger), obtem_estado(ger))

#Função adicional correspondente à operação resto da divisão inteira
#mod: int x int --> int
def mod(s, n):
    """Função adicional que recebe dois inteiros e calcula o resto
    da divisão inteira entre eles.

    :param s: inteiro correspondente ao dividendo.
    :param n: inteiro correspondente ao divisor.
    :return: resto da divisão inteira entre esses dois valores.
    """
    return s % n

def gera_numero_aleatorio(ger, n):
    """Esta função recebe um gerador e um número inteiro n e atualiza o
    estado do gerador, devolvendo um número aleatório no intervalo [1,n]
    obtido a partir do novo estado s do gerador como 1 + mod(s, n), em que
    mod() corresponde à operação do resto da divisão inteira.

    :param ger: gerador a utilizar.
    :param n: inteiro n para a geração do número aleatório do intervalo [1,n].
    :return: inteiro correspondente ao número aleatório do intervalo [1,n] gerado.
    """
    atualiza_estado(ger)
    return 1 + mod(obtem_estado(ger), n)

#Função adicional que devolve uma lista cujos elementos são as letras do alfabeto
#alfabeto: {} --> lista
def alfabeto():
    """Esta função adicionalnão recebe argumentos e devolve uma lista cujos
    elementos são as letras (maiúsculas) do alfabeto.

    :return: lista cujos elementos são as letras (maiúsculas) do alfabeto.
    """
    return list(map(chr, range(65, 91)))

def gera_carater_aleatorio(ger, car):
    """Esta função recebe um gerador e um carater maiúsculo c e atualiza o
    estado do gerador, devolvendo um carater aleatório no intervalo entre
    "A" e c. Este é obtido a partir do novo estado s de g como o carater na
    posição mod(s, l) da cadeia de carateres de tamanho l formada por todos
    os carateres entre "A" e c.

    :param ger: gerador a utiizar.
    :param car: carater maiúsculo c para a geração do carater aleatório entre "A" e c.
    :return: carater aleatório do intervalo entre "A" e c gerado.
    """
    atualiza_estado(ger)
    pos = alfabeto().index(car)
    #Lista equivalente à cadeia de carateres de tamanho l descrita no enunciado
    lista_alfabeto = alfabeto()[:pos + 1]
    return lista_alfabeto[mod(obtem_estado(ger), len(lista_alfabeto))]


#TAD coordenada
#R[A01] = (R[A], R[1])
#(Exemplo das representações utilizando a coordenada correspondente à coluna "A" e linha 1)

#cria_coordenada: str x int --> coordenada
#obtem_coluna: coordenada --> str
#obtem_linha: coordenada --> int
#eh_coordenada: universal --> lógico (booleano)
#coordenadas_iguais: coordenada x coordenada --> lógico (booleano)
#coordenada_para_str: coordenada --> str
#str_para_coordenada: str --> coordenada
#obtem_coordenadas_vizinhas: coordenada --> tuplo
#obtem_coordenada_aleatoria: coordenada x gerador --> coordenada

def cria_coordenada(col, lin):
    """Esta função recebe um carater maiúsculo e um inteiro positivo
    correspondentes a uma coluna e a uma linha, respetivamente, e devolve
    a coordenada correspondente, representada internamente como um tuplo.

    :param col: carater maiúsculo correspondente à coluna.
    :param lin: inteiro positivo correspondente à linha.
    :return: tuplo correspondente à coordenada.
    """
    #Validação de argumentos
    if type(col) != str or len(col) != 1 or col.islower():
        raise ValueError("cria_coordenada: argumentos invalidos")
    elif type(lin) != int or lin <= 0 or lin > 99:
        raise ValueError("cria_coordenada: argumentos invalidos")
    elif col not in alfabeto():
        raise ValueError("cria_coordenada: argumentos invalidos")
    #Coordenada
    return (col, lin)

def obtem_coluna(coor):
    """Esta função recebe uma coordenada como representada na função
    anterior e devolve o carater maiúsculo correspondente à sua coluna.

    :param coor: tuplo correspondente à coordenada.
    :return: carater maiúsculo correspondente à coluna da coordenada.
    """
    return coor[0]

def obtem_linha(coor):
    """Esta função recebe uma coordenada como representada anteriormente
    e devolve o inteiro positivo correspondente à sua linha.

    :param coor: tuplo correspondente à coordenada.
    :return: inteiro positivo correspondente à linha da coordenada.
    """
    return coor[1]

def eh_coordenada(arg):
    """Esta função recebe um argumento e devolve True caso este seja
    um TAD coordenada e False em caso contrário.

    :param arg: argumento a verificar se é ou não TAD coordenada.
    :return: valor lógico correspondente à condição referida.
    """
    return type(arg) == tuple and len(arg) == 2 and \
           type(obtem_coluna(arg)) == str and type(obtem_linha(arg)) == int and \
           len(obtem_coluna(arg)) == 1 and 0 < obtem_linha(arg) < 100 and \
           obtem_coluna(arg) in alfabeto()

def coordenadas_iguais(c1, c2):
    """Esta função recebe duas coordenadas como representadas anteriormente e
    devolve True se estas forem coordenadas iguais e False em caso contrário.

    :param c1: tuplo correspondente a uma das coordenadas a verificar.
    :param c2: tuplo correspondente à outra coordenada a verificar.
    :return: valor lógico correspondente à condição referida.
    """
    if eh_coordenada(c1) and eh_coordenada(c2):
        return obtem_coluna(c1) == obtem_coluna(c2) and obtem_linha(c1) == obtem_linha(c2)
    return False

def coordenada_para_str(coor):
    """Esta função recebe uma coordenada e devolve uma cadeia de carateres
    correspondente à sua representação externa.

    :param coor: coordenada a representar.
    :return: cadeia de carateres correspondente à representação externa da coordenada.
    """
    if obtem_linha(coor) < 10:
        return obtem_coluna(coor) + "0" + str(obtem_linha(coor))
    else:
        return obtem_coluna(coor) + str(obtem_linha(coor))

def str_para_coordenada(string):
    """Esta função recebe uma cadeia de carateres correspondente à representação externa
    de uma coordenada e devolve a representação interna dessa mesma coordenada.

    :param string: cadeia de carateres correspondente à representação externa da coordenada.
    :return: representação interna da coordenada.
    """
    col, lin = string[0], int(string[1:])
    if lin < 10:
        lin = int(string[2])
    return cria_coordenada(col, lin)

def obtem_coordenadas_vizinhas(coor):
    """Esta função recebe uma coordenada e devolve um tuplo com as coordenadas
    que lhe são vizinhas, começando pela coordenada na diagonal acima-esquerda
    e seguindo no sentido horário.

    :param coor: coordenada cujas coordenadas vizinhas se quer saber.
    :return: tuplo com as coordenadas vizinhas.
    """
    #Posições relativas das possíveis coordenadas vizinhas (coluna, linha)
    coor_viz = ()
    pos_coor_viz = ((-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0))

    #Verificar se cada uma das coordenadas existe e, nesse caso, adicioná-la a um tuplo
    for p in pos_coor_viz:
        col = alfabeto().index(obtem_coluna(coor)) + p[0]
        lin = obtem_linha(coor) + p[1]
        if 0 <= col < 26 and 0 < lin < 100:
            coor_viz += (cria_coordenada(alfabeto()[col], lin),)

    return coor_viz

def obtem_coordenada_aleatoria(coor, ger):
    """Esta função recebe uma coordenada e um gerador e devolve uma coordenada
    gerada aleatoriamente como descrito anteriormente, em que a coordenada
    fornecida define as maiores colunas e linhas possíveis.

    :param coor: coordenada que define as maiores coluna e linha.
    :param ger: gerador a utilizar.
    :return: coordenada aleatória gerada.
    """
    col = gera_carater_aleatorio(ger, obtem_coluna(coor))
    lin = gera_numero_aleatorio(ger, obtem_linha(coor))
    return cria_coordenada(col, lin)


#TAD parcela
#R[#] = {"estado": "tapada", "minada": False}
#(Exemplo das representações utilizando uma parcela tapada e sem mina)

#cria_parcela: {} --> parcela
#cria_copia_parcela: parcela --> parcela
#limpa_parcela: parcela --> parcela
#marca_parcela: parcela --> parcela
#desmarca_parcela: parcela --> parcela
#esconde_mina: parcela --> parcela
#eh_parcela: universal --> lógico (booleano)
#eh_parcela_tapada: parcela --> lógico (booleano)
#eh_parcela_marcada: parcela --> lógico (booleano)
#eh_parcela_limpa: parcela --> lógico (booleano)
#eh_parcela_minada: parcela --> lógico (booleano)
#parcelas_iguais: parcela x parcela --> lógico (booleano)
#parcela_para_str: parcela --> str
#alterna_bandeira: parcela --> lógico (booleano)

def cria_parcela():
    """Esta função não recebe argumentos e devolve uma parcela tapada sem mina
    escondida, representada internamente por um dicionário.

    :return: dicionário correspondente a uma parcela tapada sem mina escondida.
    """
    return {"estado": "tapada", "minada": False}

def cria_copia_parcela(parc):
    """Esta função recebe uma parcela como representada na função anterior
    e devolve uma cópia nova da mesma.

    :param parc: dicionário correspondente à parcela.
    :return: novo dicionário correspondente à cópia nova da parcela.
    """
    return dict(parc)

def limpa_parcela(parc):
    """Esta função recebe uma parcela como representada anteriormente e
    modifica-a destrutivamente, modificando o seu estado para limpa, e
    devolve a própria parcela.

    :param parc: dicionário correspondente à parcela a modificar.
    :return: dicionário correspondente à parcela já modificada.
    """
    parc["estado"] = "limpa"
    return parc

def marca_parcela(parc):
    """Esta função recebe uma parcela como representada anteriormente e
    modifica-a destrutivamente, modificando o seu estado para marcada
    com bandeira, e devolve a própria parcela.

    :param parc: dicionário correspondente à parcela a modificar.
    :return: dicionário correspondente à parcela já modificada.
    """
    parc["estado"] = "marcada"
    return parc

def desmarca_parcela(parc):
    """Esta função recebe uma parcela como representada anteriormente e
    modifica-a destrutivamente, modificando o seu estado para tapada, e
    devolve a própria parcela.

    :param parc: dicionário correspondente à parcela a modificar.
    :return: dicionário correspondente à parcela já modificada.
    """
    parc["estado"] = "tapada"
    return parc

def esconde_mina(parc):
    """Esta função recebe uma parcela como representada anteriormente e
    modifica-a destrutivamente, escondendo uma mina na parcela, e
    devolve a própria parcela.

    :param parc: dicionário correspondente à parcela a modificar.
    :return: dicionário correspondente à parcela já modificada.
    """
    parc["minada"] = True
    return parc

def eh_parcela(arg):
    """Esta função recebe um argumento e devolve True caso este seja
    um TAD parcela e False em caso contrário.

    :param arg: argumento a verificar se é ou não TAD parcela.
    :return: valor lógico correspondente à condição referida.
    """
    return type(arg) == dict and len(arg) == 2 and \
        "estado" in arg and "minada" in arg and \
        type(arg["estado"]) == str and type(arg["minada"]) == bool

def eh_parcela_tapada(parc):
    """Esta função recebe uma parcela como representada anteriormente e
    devolve True caso esta se encontre tapada e False em caso contrário.

    :param parc: dicionário correspondente à parcela a verificar.
    :return: valor lógico correspondente à condição referida.
    """
    return parc["estado"] == "tapada"

def eh_parcela_marcada(parc):
    """Esta função recebe uma parcela como representada anteriormente e
    devolve True caso esta se encontre marcada com uma bandeira e False
    em caso contrário.

    :param parc: dicionário correspondente à parcela a verificar.
    :return: valor lógico correspondente à condição referida.
    """
    return parc["estado"] == "marcada"

def eh_parcela_limpa(parc):
    """Esta função recebe uma parcela como representada anteriormente e
    devolve True caso esta se encontre limpa e False em caso contrário.

    :param parc: dicionário correspondente à parcela a verificar.
    :return: valor lógico correspondente à condição referida.
    """
    return parc["estado"] == "limpa"

def eh_parcela_minada(parc):
    """Esta função recebe uma parcela como representada anteriormente e
    devolve True caso esta esconda uma mina e False em caso contrário.

    :param parc: dicionário correspondente à parcela a verificar.
    :return: valor lógico correspondente à condição referida.
    """
    return parc["minada"]

def parcelas_iguais(p1, p2):
    """Esta função recebe duas parcelas como representadas anteriormente e
    devolve True se estas forem parcelas iguais e False em caso contrário.

    :param p1: dicionário correspondente a uma das parcelas a verificar.
    :param p2: dicionário correspondente à outra parcela a verificar.
    :return: valor lógico correspondente à condição referida.
    """
    if eh_parcela(p1) and eh_parcela(p2):
        return p1 == p2
    return False

def parcela_para_str(parc):
    """Esta função recebe uma parcela e devolve um carater correspondente
    à sua representação externa.

    :param parc: parcela a representar.
    :return: carater correspondente à representação externa da parcela.
    """
    if eh_parcela_tapada(parc):
        return "#"
    elif eh_parcela_marcada(parc):
        return "@"
    elif eh_parcela_limpa(parc) and not eh_parcela_minada(parc):
        return "?"
    elif eh_parcela_limpa(parc) and eh_parcela_minada(parc):
        return "X"

def alterna_bandeira(parc):
    """Esta função recebe uma parcela e modifica-a da seguinte forma: desmarca
    se estiver marcada e marca se estiver tapada, devolvendo True. Em qualquer
    outro caso, não modifica a parcela e devolve False.

    :param parc: parcela a modificar destrutivamente.
    :return: valor lógico como descrito acima.
    """
    if eh_parcela_marcada(parc):
        desmarca_parcela(parc)
    elif eh_parcela_tapada(parc):
        marca_parcela(parc)
    else:
        return False
    return True


#TAD campo
#R[cadeia de carateres] = [[{parc}, {parc}, {parc}], [{parc}, {parc}, {parc}]]
#Explicação da representação interna: o campo é representado por uma lista de listas,
#em que cada sublista representa uma linha do campo e é, portanto, constituída pelas
#parcelas (representadas por dicionários) correspondentes às coordenadas dessa linha.
#No exemplo, representei um campo cuja últimas coluna e linha são "C" e 2, respetivamente.

#cria_campo: str x int --> campo
#cria_copia_campo: campo --> campo
#obtem_ultima_coluna: campo --> str
#obtem_ultima_linha: campo --> int
#obtem_parcela: campo x coordenada --> parcela
#obtem_coordenadas: campo x str --> tuplo
#obtem_numero_minas_vizinhas: campo x coordenada --> int
#eh_campo: universal --> lógico (booleano)
#eh_coordenada_do_campo: campo x coordenada --> lógico (booleano)
#campos_iguais: campo x campo --> lógico (booleano)
#campo_para_str: campo --> str
#coloca_minas: campo x coordenada x gerador x int --> campo
#limpa_campo: campo x coordenada --> campo

def cria_campo(col, lin):
    """Esta função recebe uma cadeia de carateres e um inteiro correspondentes às
    últimas coluna e linha de um campo de minas, respetivamente, e devolve o campo
    do tamanho pretendido formado por parcelas tapadas sem minas.

    :param col: cadeia de carateres correspondente à última coluna do campo de minas.
    :param lin: inteiro correspondente à ultima linha do campo de minas.
    :return: lista correspondente ao campo de minas criado.
    """
    #Validação de argumentos
    if type(col) != str or len(col) != 1 or col.islower():
        raise ValueError("cria_campo: argumentos invalidos")
    elif type(lin) != int or lin <= 0 or lin > 99:
        raise ValueError("cria_campo: argumentos invalidos")
    elif col not in alfabeto():
        raise ValueError("cria_campo: argumentos invalidos")
    #Última coordenada do campo e criação do campo
    ult_coor, campo = cria_coordenada(col, lin), []

    for l in range(obtem_linha(ult_coor)):
        linha = []
        for c in range(alfabeto().index(obtem_coluna(ult_coor)) + 1):
            linha.append(cria_parcela())
        campo.append(linha)
    return campo

def cria_copia_campo(campo):
    """Esta função recebe um campo como representado na função anterior
    e devolve uma cópia nova do mesmo.

    :param campo: lista correspondente ao campo de minas.
    :return: nova lista correspondente à cópia nova do campo de minas.
    """
    copia = []
    for l in range(obtem_ultima_linha(campo)):
        linha = []
        for c in range(alfabeto().index(obtem_ultima_coluna(campo)) + 1):
            linha.append(cria_copia_parcela(obtem_parcela(campo, cria_coordenada(alfabeto()[c], l + 1))))
        copia.append(linha)
    return copia

def obtem_ultima_coluna(campo):
    """Esta função recebe um campo como representado anteriormente e devolve
    a cadeia de carateres que corresponde à última coluna do campo de minas.

    :param campo: lista correspondente ao campo de minas.
    :return: cadeia de carateres correspondente à última coluna do campo.
    """
    return alfabeto()[len(campo[0]) - 1]

def obtem_ultima_linha(campo):
    """Esta função recebe um campo como representado anteriormente e devolve
    o valor inteiro que corresponde à última linha do campo de minas.

    :param campo: lista correspondente ao campo de minas.
    :return: inteiro correspondente à última linha do campo.
    """
    return len(campo)

def obtem_parcela(campo, coor):
    """Esta função recebe um campo de minas e uma coordenada como representados
    anteriormente e devolve a parcela do campo que se encontra na respetiva
    coordenada.

    :param campo: lista correspondente ao campo de minas.
    :param coor: tuplo correspondente à coordenada.
    :return: dicionário correspondente à parcela do campo na coordenada dada.
    """
    return campo[obtem_linha(coor) - 1][alfabeto().index(obtem_coluna(coor))]

def obtem_coordenadas(campo, est):
    """Esta função recebe um campo de minas como representado anteriormente e uma
    cadeia de carateres correspondente a uma característica das parcelas e devolve
    o tuplo formado pelas coordenadas, em ordem ascendente da esquerda à direita e
    de cima a baixo, das parcelas com essa característica.

    :param campo: lista correspondente ao campo de minas.
    :param est: cadeia de carateres correspondente a uma característica das parcelas.
    :return: tuplo com as coordenadas do campo cujas parcelas tenham essa característica.
    """
    coor = ()
    for l in range(len(campo)):
        for c in range(len(campo[l])):
            if est == "limpas" and eh_parcela_limpa(campo[l][c]):
                coor += (cria_coordenada(alfabeto()[c], l + 1),)
            elif est == "tapadas" and eh_parcela_tapada(campo[l][c]):
                coor += (cria_coordenada(alfabeto()[c], l + 1),)
            elif est == "marcadas" and eh_parcela_marcada(campo[l][c]):
                coor += (cria_coordenada(alfabeto()[c], l + 1),)
            elif est == "minadas" and eh_parcela_minada(campo[l][c]):
                coor += (cria_coordenada(alfabeto()[c], l + 1),)
    return coor

def obtem_numero_minas_vizinhas(campo, coor):
    """Esta função recebe um campo de minas e uma coordenada como representados anteriormente
    e devolve o número de parcelas vizinhas à parcela fornecida que escondem uma mina.

    :param campo: lista correspondente ao campo de minas.
    :param coor: tuplo correspondente à coordenada.
    :return: inteiro correspondente ao número de minas vizinhas.
    """
    coor_viz, n = obtem_coordenadas_vizinhas(coor), 0
    for c in coor_viz:
        if eh_coordenada_do_campo(campo, c):
            if eh_parcela_minada(obtem_parcela(campo, c)):
                n += 1
    return n

def eh_campo(arg):
    """Esta função recebe um argumento e devolve True caso este seja
    um TAD campo e False em caso contrário.

    :param arg: argumento a verificar se é ou não TAD campo.
    :return: valor lógico correspondente à condição referida.
    """
    if type(arg) != list or len(arg) == 0 or len(arg) != obtem_ultima_linha(arg) or len(arg) > 2574:
        return False
    for l in arg:
        if type(l) != list or len(l) == 0 or len(l) - 1 != alfabeto().index(obtem_ultima_coluna(arg)):
            return False
        for c in l:
            if not eh_parcela(c):
                return False
    return True

def eh_coordenada_do_campo(campo, coor):
    """Esta função recebe um campo de minas e uma coordenada como representados
    anteriormente e devolve True se a coordenada é válida dentro do campo e False
    em caso contrário.

    :param campo: lista correspondente ao campo de minas.
    :param coor: tuplo correspondente à coordenada a verificar.
    :return: valor lógico correspondente à condição referida.
    """
    if alfabeto().index(obtem_coluna(coor)) > alfabeto().index(obtem_ultima_coluna(campo)) \
        or obtem_linha(coor) > obtem_ultima_linha(campo):
        return False
    return True

def campos_iguais(cam1, cam2):
    """Esta função recebe dois campos de minas como representados anteriormente e
    devolve True se estes forem campos iguais e False em caso contrário.

    :param cam1: lista correspondente a um dos campos a verificar.
    :param cam2: lista correspondente ao outro campo a verificar.
    :return: valor lógico correspondente à condição referida.
    """
    #Verifica se ambos os argumentos são campos
    if eh_campo(cam1) and eh_campo(cam2):
        if obtem_ultima_coluna(cam1) != obtem_ultima_coluna(cam2) or \
                obtem_ultima_linha(cam1) != obtem_ultima_linha(cam2):
            return False
        #Verifica se são campos iguais parcela a parcela
        for l in range(obtem_ultima_linha(cam1)):
            for c in range(alfabeto().index(obtem_ultima_coluna(cam1))):
                coor_parc = cria_coordenada(alfabeto()[c], l + 1)
                if eh_coordenada_do_campo(cam2, coor_parc):
                    p1 = obtem_parcela(cam1, coor_parc)
                    p2 = obtem_parcela(cam2, coor_parc)
                    if not parcelas_iguais(p1, p2):
                        return False
                else:
                    return False
    else:
        return False
    return True

def campo_para_str(campo):
    """Esta função recebe um campo de minas e devolve uma cadeia de
    carateres correspondente à sua representação externa.

    :param campo: campo a representar.
    :return: cadeia de carateres correspondente à representação externa do campo.
    """
    res = "   "
    #Colunas do campo
    for c in range(alfabeto().index(obtem_ultima_coluna(campo)) + 1):
        res += alfabeto()[c]
    res += "\n"
    #Delimitação superior do campo
    delim = "  +"
    for c in range(alfabeto().index(obtem_ultima_coluna(campo)) + 1):
        delim += "-"
    delim += "+"
    res += delim + "\n"
    #Linhas do campo
    for l in range(len(campo)):
        #Número da linha
        linha = ""
        if l + 1 < 10:
            num = "0" + str(l + 1) + "|"
        else:
            num = str(l + 1) + "|"
        linha += num
        #Parcelas da linha
        for c in range(len(campo[l])):
            coor_parc = cria_coordenada(alfabeto()[c], l + 1)
            if eh_parcela_limpa(campo[l][c]) and not eh_parcela_minada(campo[l][c]):
                if obtem_numero_minas_vizinhas(campo, coor_parc) == 0:
                    linha += " "
                else:
                    linha += str(obtem_numero_minas_vizinhas(campo, coor_parc))
            else:
                linha += parcela_para_str(campo[l][c])
        #Adição da linha à cadeia de carateres
        res += linha + "|\n"
    #Delimitação inferior do campo
    res += delim

    return res

def coloca_minas(campo, coor, ger, n):
    """Esta função recebe um campo de minas, uma coordenada, um gerador e um
    inteiro positivo n, e gera n coordenadas com o objetivo de esconder uma
    mina em cada uma das suas parcelas, devolvendo, no final deste processo,
    o campo de minas modificado destrutivamente.

    :param campo: campo de minas a modificar destrutivamente.
    :param coor: coordenada a utilizar.
    :param ger: gerador a utilizar.
    :param n: inteiro correspondente ao número de minas.
    :return: campo de minas modificado destrutivamente.
    """
    #Coordenadas a evitar
    coor_a_evitar = (coor,) + obtem_coordenadas_vizinhas(coor)
    #Gerar n coordenadas
    n_coor, ult_coor_campo = (), cria_coordenada(obtem_ultima_coluna(campo), obtem_ultima_linha(campo))
    while len(n_coor) < n:
        coor_a_adic = obtem_coordenada_aleatoria(ult_coor_campo, ger)
        if coor_a_adic not in coor_a_evitar:
            n_coor += (coor_a_adic,)
            coor_a_evitar += (coor_a_adic,)
    #Esconder n minas nas coordenadas geradas
    for c in n_coor:
        esconde_mina(obtem_parcela(campo, c))
    return campo

def limpa_campo(campo, coor):
    """Esta função recebe um campo de minas e uma coordenada e modifica
    destrutivamente o campo limpando a parcela na coordenada fornecida.
    Caso não haja nenhuma mina vizinha escondida, limpa também todas as
    parcelas vizinhas tapadas. Caso a parcela da coordenada fornecida já
    se encontre limpa, a operação não tem efeito. No final deste processo,
    é devolvido o campo modificado destrutivamente.

    :param campo: campo de minas a modificar destrutivamente.
    :param coor: coordenada a limpar.
    :return: campo de minas modificado destrutivamente.
    """
    #Caso a parcela da coordenada fornecida já se encontre limpa
    if eh_parcela_limpa(obtem_parcela(campo, coor)):
        return campo
    limpa_parcela(obtem_parcela(campo, coor))
    #Verifica se há minas vizinhas escondidas e, caso tal não se verifique,
    #adiciona as coordenadas vizinhas a uma fila de limpeza
    fila = []
    if not eh_parcela_minada(obtem_parcela(campo, coor)):
        if obtem_numero_minas_vizinhas(campo, coor) == 0:
            for c in obtem_coordenadas_vizinhas(coor):
                if eh_coordenada_do_campo(campo, c):
                    if not eh_parcela_limpa(obtem_parcela(campo, c)):
                        fila.append(c)
    #Função auxiliar para limpar o campo até a fila se encontrar vazia
    def limpa_campo_aux(campo, fila):
        if fila == []:
            return campo
        else:
            #Caso a parcela não se encontre limpa nem marcada, limpa-a
            if not eh_parcela_limpa(obtem_parcela(campo, fila[0])):
                if not eh_parcela_marcada(obtem_parcela(campo, fila[0])):
                    limpa_parcela(obtem_parcela(campo, fila[0]))
                    #Verifica se é preciso adicionar mais coordenadas à fila
                    if obtem_numero_minas_vizinhas(campo, fila[0]) == 0:
                        for c in obtem_coordenadas_vizinhas(fila[0]):
                            if eh_coordenada_do_campo(campo, c):
                                if not eh_parcela_limpa(obtem_parcela(campo, c)) and \
                                        not eh_parcela_minada(obtem_parcela(campo, c)):
                                    fila.append(c)
                limpa_campo_aux(campo, fila[1:])
            else:
                limpa_campo_aux(campo, fila[1:])
    limpa_campo_aux(campo, fila)
    return campo


#Funções adicionais

#jogo_ganho: campo --> lógico (booleano)
#turno_jogador: campo --> lógico (booleano)
#minas: str x int x int x int x int --> lógico (booleano)

def jogo_ganho(campo):
    """Esta função recebe um campo de minas e devolve True se todas as
    parcelas sem minas se encontram limpas ou False em caso contrário.

    :param campo: campo de minas a ser verificado.
    :return: valor lógico correspondente à condição referida.
    """
    tap_e_marc = obtem_coordenadas(campo, "tapadas") + obtem_coordenadas(campo, "marcadas")
    for c in tap_e_marc:
        if not eh_parcela_minada(obtem_parcela(campo, c)):
            return False
    return True

def turno_jogador(campo):
    """Esta função recebe um campo de minas e oferece ao jogador a opção
    de escolher uma ação ([L]impar ou [M]arcar) e uma coordenada, modificando
    destrutivamente o campo de acordo com a ação escolhida, e devolvendo
    False caso o jogador tenha limpo uma parcela que continha mina, ou
    True em caso contrário.

    :param campo: campo de minas a ser modificado destrutivamente.
    :return: valor lógico correspondente à ação realizada, como descrito.
    """
    #Ação do jogador
    acao = input("Escolha uma ação, [L]impar ou [M]arcar:")
    while acao not in ("L", "M"):
        acao = input("Escolha uma ação, [L]impar ou [M]arcar:")
    #Coordenada escolhida para a respetiva ação
    coor = input("Escolha uma coordenada:")
    while len(coor) != 3 or len(coor[1:]) != 2 or coor[0] not in alfabeto() or coor[0].islower() \
             or coor[1] in alfabeto() or coor[2] in alfabeto() or int(coor[1:]) <= 0 or \
            int(coor[1:]) > 99 or not eh_coordenada_do_campo(campo, str_para_coordenada(coor)):
        coor = input("Escolha uma coordenada:")
    #Modifica o campo de acordo com a ação escolhida
    if acao == "L":
        limpa_campo(campo, str_para_coordenada(coor))
        if eh_parcela_minada(obtem_parcela(campo, str_para_coordenada(coor))):
            return False
        return True
    elif acao == "M":
        return alterna_bandeira(obtem_parcela(campo, str_para_coordenada(coor)))

def minas(col, lin, n, bits, estado):
    """Esta função recebe uma cadeia de carateres e 4 valores inteiros
    correspondentes, respetivamente, a: última coluna, última linha,
    número de parcelas com mina, dimensão do gerador de números e
    estado inicial do mesmo. Esta é a função principal que permite
    jogar ao jogo das minas e devolve True se o jogador conseguir
    ganhar o jogo, ou False em caso contrário.

    :param col: cadeia de carateres correspondente à última coluna.
    :param lin: inteiro correspondente à última linha.
    :param n: inteiro correspondente ao número de parcelas com mina.
    :param bits: inteiro correspondente à dimensão do gerador de números.
    :param estado: inteiro correspondente ao estado inicial do gerador.
    :return: valor lógico como descrito acima.
    """
    #Validação de argumentos
    if type(col) != str or len(col) != 1 or col.islower():
        raise ValueError("minas: argumentos invalidos")
    elif type(lin) != int or lin <= 0 or lin > 99:
        raise ValueError("minas: argumentos invalidos")
    elif type(n) != int or n <= 0:
        raise ValueError("minas: argumentos invalidos")
    elif type(bits) != int or bits not in (32, 64):
        raise ValueError("minas: argumentos invalidos")
    elif type(estado)!= int or estado <= 0 or estado >= 2 ** (bits+1) :
        raise ValueError("minas: argumentos invalidos")
    num_parc = 0
    for c in obtem_coordenadas(cria_campo(col, lin), "tapadas"):
        num_parc += 1
    if n > num_parc:
        raise ValueError("minas: argumentos invalidos")
    elif num_parc in (1, 2, 4):
        raise ValueError("minas: argumentos invalidos")
    #Cria o campo e o gerador
    campo = cria_campo(col, lin)
    ger = cria_gerador(bits, estado)
    #Atualiza o campo conforme as jogadas
    contador = 0
    while not jogo_ganho(campo):
        #Caso haja parcelas minadas e limpas, termina o ciclo e o jogador perde o jogo
        for c in obtem_coordenadas(campo, "minadas"):
            if c in obtem_coordenadas(campo, "limpas"):
                print("   [Bandeiras {}/{}]".format(len(obtem_coordenadas(campo, "marcadas")), n))
                print(campo_para_str(campo))
                print("BOOOOOOOM!!!")
                return False
        print("   [Bandeiras {}/{}]".format(len(obtem_coordenadas(campo, "marcadas")), n))
        print(campo_para_str(campo))
        #Primeira jogada a ser realizada
        if contador == 0:
            prim_coor = input("Escolha uma coordenada:")
            while len(prim_coor) != 3 or len(prim_coor[1:]) != 2 or \
                    not eh_coordenada_do_campo(campo, str_para_coordenada(prim_coor)):
                prim_coor = input("Escolha uma coordenada:")
            coloca_minas(campo, str_para_coordenada(prim_coor), ger, n)
            limpa_campo(campo, str_para_coordenada(prim_coor))
            print("   [Bandeiras {}/{}]".format(len(obtem_coordenadas(campo, "marcadas")), n))
            print(campo_para_str(campo))
            contador += 1
        #Todas as outras jogadas
        turno_jogador(campo)
    #Vitória do jogador
    print("   [Bandeiras {}/{}]".format(len(obtem_coordenadas(campo, "marcadas")), n))
    print(campo_para_str(campo))
    print("VITORIA!!!")
    return True
