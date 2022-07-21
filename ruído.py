import math

def trocar(bit):
    if bit == '0': return '1'
    return '0'

def modificar_binario(binario, i):
    binario = list(binario)
    for x in range(8):
        binario[i+x] = trocar(binario[i+x])
    return ''.join(binario)

def remover_bits(binario):
    return binario[:-8]

def adicionar_bits(binario):
    return '1011110000101111' + binario

def main():
    fonte = input('Arquivo fonte: ')
    destino = input('Arquivo destino: ')

    with open(fonte,'rb') as fonte, open(destino,'wb') as destino:
        i = 0
        while True:
            if i ==128:
                i = 0

            leitura = fonte.read(16)

            if leitura == b"":
                break

            if len(leitura)!= 16:
                destino.write(leitura)
                continue

            inteiro = int.from_bytes(leitura,'little')
            binario = bin(inteiro)[2:]
            while len(binario) != len(leitura)*8:
                binario = "0" + binario   
            
            binario = modificar_binario(binario, i)
            novo_inteiro = int(binario,2)

            x = len(binario)/8

            new_codigo = novo_inteiro.to_bytes(math.ceil(x), 'little')
      
            destino.write(new_codigo)
            i+=8
    
    fonte.close()
    destino.close()

if __name__=="__main__":
    main()