import math, os
'''
Alunas: Crislanne Letícia Leal de Aviz
        Gabrielli Danker
        Fernanda Ribeiro Martins
        Monique Ellen dos Santos
'''

def bits_hamming(dados, a,b,c,d,e,f,g,h,i,j,k): 
        """
        Esta função recebe uma lista com x inteiros e para calcular a soma dos valores das posições 
        referentes a cada bit de paridade.
        :param dados: lista com x inteiros
        :param a,b,c,d,e,f,g,h,i,j,k: posições
        :return: retorna a lista com os resultados das somas
        """
        paridade_1 = dados[a] + dados[b] + dados[d] + dados[e] + dados[g] + dados[i] + dados[k]  
        paridade_2 = dados[a] + dados[c] + dados[d] + dados[f] + dados[g] + dados[j] + dados[k] 
        paridade_4 = dados[b] + dados[c] + dados[d] + dados[h] + dados[i] + dados[j] + dados[k]
        paridade_8 = dados[e] + dados[f] + dados[g] + dados[h] + dados[i] + dados[j] + dados[k]

        return [paridade_1, paridade_2, paridade_4,paridade_8]

def paridadepar(bit):
    """
    Esta função determina a paridade de um valor inteiro.
    :param bit: inteiro
    :return: retorna 0 se o param for par, 1 se for impar
    """
    
    if bit%2==0:
        return 0
    return 1

def zero_esquerda(leitura, binario):
    """
    Esta função adiciona zeros a esquerda do valor binário caso o tamanho seja
    diferente do tamanho da leitura vezes 8 (bits).
    :param leitura: a leitura do arquivo em bytes (hexadecimal)
    :param binario: inteiro que representa um binário
    :return: retorna o binario com zeros a esquerda
    """       
    while len(binario) != len(leitura)*8:
        binario = "0" + binario       
    return binario

def cria_lista(binario):
    """
    Esta função recebe uma string e tranforma-a em lista.
    :param binario: string
    :return: retorna uma lista
    """     
    l_codigo = []
    for elemento in binario:
        l_codigo.append(int(elemento))
    return l_codigo

def cria_string(codigo):
    """
    Esta função recebe uma lista e tranforma-a em string
    :param codigo: lista
    :return: retorna uma string
    """     
    s_codigo = "" 
    for elemento in codigo:
        s_codigo += str(elemento)
    return s_codigo

def codificar(f, d):
    """
    Esta função cria um cabeçalho contendo o tamanho do arquivo, codifica-o pelo hamming e salva no arquivo destino.
    Em seguida faz a leitura de um arquivo fonte em grupos de 11 bytes, converte a leitura para inteiro e depois 
    para binário. 
    É aplicado o código Hamming e cada bit é salvo em uma lista de forma intercalada.
    A lista é convertida em ordem para uma string, inteiro e para bytes. O resultado em bytes é gravado no arquivo 
    destino.
    :param f: arquivo fonte
    :param d: arquivo destino
    :return: retorna ''
    """ 

    def codificar_dados(dados):
        """
        Esta função recebe uma lista com 11 inteiros para codificar e gerar uma lista com 16 inteiros.
        :param dados: lista com 11 bits
        :return: retorna uma lista com 16 inteiros
        """

        paridades = bits_hamming(dados, 0,1,2,3,4,5,6,7,8,9,10)
        posicao = 0
        contador = 0

        for bit in paridades:
            bit = paridadepar(bit)                         
        
            dados.insert(posicao, bit)                          # a variável é inserida na lista com os bits de dados
            posicao = posicao + 2**contador                     # a posição dos bits de redundância aumenta de forma exponencial na base 2
            contador += 1
                                                    
        paridade_0 = 0                                          # determina o bit de paridade do índice 0
        for bit in dados:
            paridade_0 += bit
        paridade_0 = paridadepar(paridade_0)

        dados.insert(0, paridade_0)                          
        
        return dados

    def hamming(dados):
        """
        Esta função recebe uma lista e as separa em grupos com 11 inteiros. 
        Cada grupo é codificado e gera uma lista de 16 inteiros, anexada à lista final. 
        :param dados: lista com bits múltiplos de 11
        :return: retorna uma lista com listas de 16 bits
        """        
        codigo_hamming= []
        
        while len(dados) != 0:            
            proximo_cod = dados[11:]                       
            dados = dados[:11]
 
            while len(dados) % 11 != 0:                       
                dados.insert(0, 0) 
            
            hamming = codificar_dados(dados)                   
            codigo_hamming.append(hamming)                 
            dados = proximo_cod

        return codigo_hamming

    def intercalar(codigo):
        """
        Esta função recebe os dados a serem codificados e aplica a função hamming que retorna uma lista de listas de 16 bits.
        Em seguida embaralha as listas de forma intercalada, gerando uma lista com tamanho divisivel por 16.
        :param codigo: lista de listas com bits codificados com hamming
        :return: retorna uma lista com os códigos alternados
        """   

        cod_hamming = hamming(codigo)
        cod_final =[]
        x = 0
        while x != 16:
            for lista in cod_hamming:
                bit = lista[x]
                cod_final.append(bit)
            x += 1
        return cod_final

    def converter(binario):
        """
        Esta função recebe um valor binário em formato string. 
        Cada bit é anexado em uma lista, que é aplicado o hamming intercalado. A lista 
        é convertida em ordem para string, inteiro e bytes.
        param binario: string 
        return: retorna em bytes codificados
        """
        
        l_codigo = cria_lista(binario)                 
        codigo =  intercalar(l_codigo)                        
        s_codigo = cria_string(codigo)                      
        new_codigo = int(s_codigo, 2)                        
        
        new_codigo = new_codigo.to_bytes((len(s_codigo))//8, 'little')  #divide o tamanho da string por 8 para saber quanto espaço em bytes é necessário armazenar o código
        return(new_codigo)

    with open(f,'rb') as fonte, open(d,'wb') as destino:

        # gerar cabeçalho = tamanho do arquivo original em bits entra no cabeçalho em binario
        # o cabeçalho tem 88 bits que são codificados com hamming e viram no final 16 bytes
        tamanho = os.path.getsize(f)
        cabecalho = bin(tamanho*8)[2:]

        while len(cabecalho) != 88:
            cabecalho = "0" + cabecalho      

        cabecalho_hamming =  converter(cabecalho)
        destino.write(cabecalho_hamming)

        while leitura:= fonte.read(11):    
             
            inteiro = int.from_bytes(leitura, 'little')                          
            binario = bin(inteiro)[2:]                     
            binario = zero_esquerda(leitura, binario)      

            new_codigo = converter(binario)
            destino.write(new_codigo)

    fonte.close()
    destino.close()
    return ''
        
def descodificar(f, d):
    """
    Esta função faz a leitura de um arquivo fonte em grupos de 16 bytes, converte para inteiro e para binário.
    Cada grupo é desintercalado, descodificado e corrigido (se possível) pelo hamming. 
    Caso tenha mais de um erro por quadro hamming ou haja uma divergência de tamanho, é exibido uma mensagem de erro.
    Com a primeira leitura é obtivo o cabeçalho, contendo o tamanho do arquivo. 
    Na última leitura, os zeros que foram adicionados para codificar o arquivo original são removidos.
    Os bits descodificados são convertidos em ordem para string, inteiro e bytes. O resultado em bytes é gravado em destino.
    :param f: arquivo fonte
    :param d: arquivo destino
    :return: retorna ''
    """ 

    def mudar_bit(bit):
        """
        Esta função recebe um parâmetro inteiro que muda de 0 para 1 e vice versa.
        :param bit: inteiro
        :return: retorna 0 se o param for 1, 1 se o param for 0
        """
        if bit == 0:
            return 1
        return 0

    def comparar_paridade(lista_paridade,lista_cod):
        """
        Esta função recebe duas listas com inteiros. Compara os valores da lista_cod
        com os valoes encontrados na lista_paridade, se houver divergências, a posição
        do inteiro com erro entra na lista bits_com_erro, senão entra na lista 
        bits_sem_erro
        :param lista_paridade: lista de inteiros
        :param lista_cod: lista de inteiros
        :return: retorna as listas bits_com_erro e bits_sem_erro
        """
        bits_com_erro= []
        bits_sem_erro= []

        for i, bit_paridade in enumerate(lista_paridade):       
            bit_paridade = (paridadepar(bit_paridade))
             
            if bit_paridade != lista_cod[2**i]:
                bits_com_erro.append(2**i)
            else: 
                bits_sem_erro.append(2**i)
        return bits_com_erro, bits_sem_erro

    def paridade_0(lista_cod):
        """
        Esta função recebe uma lista com inteiros. Soma todos os inteiros da posição 1 em diante e armazena na variável bit_paridade_0. 
        :param lista_cod: lista de inteiros
        :return: retorna a função paridadepar do bit_paridade_0
        """
        bit_paridade_0 = 0
        for bits in lista_cod[1:]:
            bit_paridade_0 += bits

        return(paridadepar(bit_paridade_0))                   

    def desintercalar_hamming(codigo_codificado): 
        """
        Esta função recebe uma lista com inteiros. Separa a lista em listas menores com
        16 itens de forma desintercalada. Armazena essas listas em uma lista final.
        :param codigo_codificado: lista de inteiros que são obtidos da leitura de um 
        arquivo codificado
        :return: retorna uma lista com listas de len() = 16
        """
    
        codigo_separado = []
        lista_codigos_separados = []
        indice = 0
        quantificador = 0

        while codigo_codificado:
            # Determinar a quantidade de hammings que serão necessários para desintercalar
            quantidade_de_hamming = len(codigo_codificado)//16     
            
            if len(lista_codigos_separados) == quantidade_de_hamming:
                break
            elif len(codigo_separado) == 16:
                lista_codigos_separados.append(codigo_separado)
                codigo_separado = []
                quantificador += 1
                indice = 0
            else:        
                # Desintercala o código colocandos os bits de determinadas posições em suas respectivas listas.
                # Caso a quantidade de hammings seja 11, o codigo separado vai receber os itens das posições 0, 11, 22...
                codigo_separado.append(codigo_codificado[(quantidade_de_hamming*indice)+quantificador])
                indice += 1
        return lista_codigos_separados

    def corrigir_erro(bits_com_erro, codigo_separado, bits_sem_erro, bit_paridade_0):
        """
        Esta função compara o bit_paridade_0 com o inteiro da primeira posição da lista codigo_separado e 
        analisa o elementos da lista bits_com_erro e bits_sem_erro para corrigir até um erro por quadro hamming.
        :param bits_com_erro: lista com as posições dos bits com erro
        :param bits_sem_erro: lista com as posições dos bits sem erro
        :param codigo_separado: lista do código com hamming
        :param bit_paridade_0: inteiro (0 ou 1)
        :return: retorna a lista com o código ou retorna um erro
        """
        try:
            
            if bit_paridade_0!=codigo_separado[0] and len(bits_com_erro) != 0:                  # Se há 1 erro, determina qual a posição da lista está errada e a corrige

                # Dicionário com as posições dos bits de paridade
                dicio = {1:{5,9,13,3,7,11,15}, 2:{6,10,14,3,7,11,15}, 4:{5,6,7,12,13,14,15}, 8:{8,9,10,11,12,13,14,15}} 

                if len(bits_com_erro) == 1:
                    codigo_separado[bits_com_erro[0]]= mudar_bit(codigo_separado[bits_com_erro[0]])

                elif len(bits_com_erro)== 2:   
                    x= dicio[bits_com_erro[0]] & dicio[bits_com_erro[1]]- dicio[bits_sem_erro[0]] - dicio[bits_sem_erro[1]]
                 
                    y = list(x)
                  
                    codigo_separado[y[0]]= mudar_bit(codigo_separado[y[0]])
                

                elif len(bits_com_erro)== 3:               
                   
                    x= dicio[bits_com_erro[0]] & dicio[bits_com_erro[1]]& dicio[bits_com_erro[2]] - dicio[bits_sem_erro[0]]
                    y = list(x)
                    
                    codigo_separado[y[0]]= mudar_bit(codigo_separado[y[0]])
           
                elif len(bits_com_erro)== 4:               
                    codigo_separado[15]= mudar_bit(codigo_separado[15])
                return codigo_separado


            elif bit_paridade_0==codigo_separado[0] and len(bits_com_erro) == 0:                # Se não houver erros
                return codigo_separado  
    

            elif bit_paridade_0!=codigo_separado[0] and len(bits_com_erro) == 0:                # Se o erro for no inteiro da posição 0
                codigo_separado[0] = mudar_bit(codigo_separado[0])
                return codigo_separado

    
            elif bit_paridade_0==codigo_separado[0] and len(bits_com_erro) > 0:                 # Se houver dois erros ou mais a função retorna um erro
                return -1   

        except IndexError:
            return -2            

    def tirar_hamming(lista):
        """
        Esta função deleta os itens da lista nas posições 8, 4, 2, 1 e 0
        :param lista: lista com 16 inteiros
        :return: retorna a lista com 11 inteiros
        """
        del lista[8]
        del lista[4]
        del lista[2]
        del lista[1]
        del lista[0]      
        return lista

    def codigo_final(codigo_codificado):
        """
        Esta função gera o código sem hamming para todos os bytes lidos na leitura.
        :param codigo_codificado: lista com inteiros obtida na leitura
        :return: retorna uma lista sem bits de paridade ou um erro
        """
        resultado = []

        lista_codigos = desintercalar_hamming(codigo_codificado) 

        for codigo_separado in lista_codigos:
            paridades =  bits_hamming(codigo_separado, 3,5,6,7,9,10,11,12,13,14,15)
            
            bits_com_erro, bits_sem_erro = comparar_paridade(paridades,codigo_separado)

            bit_paridade_0 = paridade_0(codigo_separado)                

            correcao = corrigir_erro(bits_com_erro, codigo_separado, bits_sem_erro, bit_paridade_0)

            if correcao == -1:
                return -1
            elif correcao == -2:
                return -2       
            resultado+= tirar_hamming(correcao)

        return resultado

    def deletar_zero(codigo): 
        """
        Esta função recebe uma lista e deleta a primira posição, caso seja 0
        :param codigo: lista
        :return: retorna uma lista 
        """         
        while codigo[0] == 0:
            del codigo[0]
        return codigo

    with open(f,'rb') as fonte, open(d,'wb') as destino:

        file_size_descod = os.path.getsize(f)
        i = 1

        # Leitura do arquivo de 16 em 16 bytes(quando houver). Dessa forma são lidos 128 bits, ou seja 8 hammings a cada leitura.
        while leitura:= fonte.read(16):     
                   
            inteiro = int.from_bytes(leitura, 'little')             
            binario = bin(inteiro)[2:]            
            binario = zero_esquerda(leitura, binario)            
            l_codigo = cria_lista(binario)            
            codigo = codigo_final(l_codigo)
        
            #caso tenha erros impossíveis de corrigir
            if codigo == -1 or codigo == -2:
                try:
                    if (math.ceil(file_size_cod/11))*16 != (file_size_descod*8)-128:
                            print("ERRO - DIVERGÊNCIA NO TAMANHO DO ARQUIVO")  
                    else:
                        print("ERRO - MAIS DE UM ERRO, NÃO É POSSÍVEL CORRIGIR")     
                except UnboundLocalError:
                    print("ERRO - MAIS DE UM ERRO, NÃO É POSSÍVEL CORRIGIR")
                break
            
            else:                           
                if i == 1:                                                    # se for a primeira leitura (cabeçalho)                    
                    codigo = (deletar_zero(codigo))
                    s_codigo = cria_string(codigo)
                    file_size_cod = int(s_codigo, 2 )                    
                    padding = (11-(file_size_cod)%11)                         # quantidade de zeros(0) adicionados no último hamming
                   
                    i = 2   
                    continue                
                
                elif i == math.ceil(file_size_descod/16):                     # se for a última leitura, deleta o numero de zeros determinados pelo padding                    
        
                    if file_size_cod % 11 != 0:
                        ultimo_hamming = codigo[-11:]
                        codigo = codigo[:-11]                   
                        for j in range(padding):
                            del ultimo_hamming[0]
                        codigo = codigo + ultimo_hamming
                    
                    if math.ceil((file_size_cod/11))*16 != (file_size_descod*8)-128:    # determina se o arquivo tem o tamanho correto
                        print("ERRO - DIVERGÊNCIA NO TAMANHO DO ARQUIVO")            

                s_codigo = cria_string(codigo)                
                new_codigo = int(s_codigo, 2 ) 

                x = len(s_codigo)/8                                                     # referente a quanto espaço em bytes é necessário armazenar o código
                new_codigo = new_codigo.to_bytes(math.ceil(x), 'little')
                i += 1
        
                destino.write(new_codigo)
        
    fonte.close()
    destino.close()
    return''

def main():
    print(f"--------------  Digite:  --------------")
    print(f"----------  1 - CODIFICAR  ------------")
    print(f"----------  2 - DESCODIFICAR  ---------\n")
    escolha = input("Digite a opção desejada: ")
    print()
    fonte = input('Arquivo fonte: ')
    destino = input('Arquivo destino: ')

    try:
        if escolha == '1':
            codificar(fonte,destino)
        elif escolha == '2':
            descodificar(fonte,destino)
        else:
            print("ERRO - OPÇÃO NÃO EXISTE")

    except FileNotFoundError:
        print("ERRO - ARQUIVO NÃO ENCONTRADO")
    
if __name__ == "__main__":
    main()