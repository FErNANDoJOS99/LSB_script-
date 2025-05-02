
import sys
from PIL import Image




class LSB:
    def __init__(self, texto,imagen ):
        self.texto = texto
        self.longitud = len(texto)
        # longitud del texto ocupando 2 bytes
        self.binario = format(self.longitud, '016b')
        self.imagen=imagen
        self.lista=[] 
        self.lista_oculta=[]


    # Despues comentar este 
    def mostrar_resultados(self):
        print(f"Texto ingresado: '{self.texto}'")
        print(f"Longitud total (con espacios): {self.longitud}")
        print(f"Longitud en binario (2 bytes): {self.binario}")


    def texto_a_binario(self):
        binarios = [format(ord(c), '08b') for c in self.texto]
        cadena_binaria = ''.join(binarios)
        #print(f"Texto original: {self.texto}")
        #print(f"Cadena binaria: {cadena_binaria}")
        return cadena_binaria


    #Retorna la cadena binaria de la longitud del texto , el texto y el final 
    #del texto
    def cadena_preparada(self,texto1):

        cadena_concatenada = self.binario + texto1 + '00000000'
  
        #print(f"Cadena concatenada con '00000000': {cadena_concatenada}")
        return cadena_concatenada


## Para operar los pixeles
################################################################################################




    # Convierte un binario a entero 
    # Nota el binario es de tipo String
    def binario_a_decimal(self,binario_str):
        return int(binario_str, 2)



    # Convierte un entero a binario
    def entero_a_binario8(self,valor):
        return format(valor, '08b')


    # Cambia el ultimo mas insignificante 
    def cambiar_lsb(self,binario_str, nuevo_bit):
        return binario_str[:-1] + nuevo_bit



    # Genera una lista de todos los pixeles pero en binario
    
    def guardar_pixel_en_binario(self,pixel):
        
        r, g, b = pixel
        bin_r = self.entero_a_binario8(r)
        bin_g = self.entero_a_binario8(g)
        bin_b = self.entero_a_binario8(b)
        self.lista.append((bin_r,bin_g,bin_b))

  
    ## Apartir de una lista de pixeles en binario 
    # Hace la modificación al ultimo bit , lo transforma los bits asu forma norma
    # regresa la lista de bit normales
    def agregar_dato_oculto(self):

        lista_oculta=[]
        # Se hace un iterador sobre la cadena a guardar ya con los datos extras.
        x=self.texto_a_binario()
        #print(x)
        y= self.cadena_preparada(x)
        print("es mi cadena preparada")
        print(y)
        it = iter(y)
        bit_texto = next(it, None)  # None si ya no hay más


        for tupla in self.lista :
            lista_aux=[]

            for segmento in tupla : 
                #que recorra la lista 
                #segmento_viejo=segmento
               
                if bit_texto is not None:           
                    #print("Elemento:", segmento)
                    nuevo_segmento = self.binario_a_decimal( self.cambiar_lsb(segmento,bit_texto))
                    #print(bit_texto)
                    # para avanzar con el iterador
                    lista_aux.append(nuevo_segmento)
                    bit_texto = next(it,None) 
                else :              
                        #print("entro a else") 
                        lista_aux.append(self.binario_a_decimal(segmento))

            tupla_aux=tuple(lista_aux)
            lista_oculta.append(tupla_aux)

        return lista_oculta



    def procesar_imagen_guardar(self):
        imagen = Image.open(self.imagen).convert('RGB')
        pixeles = list(imagen.getdata())

    
        self.lista.clear()
        for p in pixeles :
            self.guardar_pixel_en_binario(p)

        pixeles_transformados=  ( self.agregar_dato_oculto())
      
        
        #print(type(pixeles_transformados))
        #print(pixeles_transformados)

        # Crear nueva imagen con los píxeles modificados
        nueva_imagen = Image.new('RGB', imagen.size)
        nueva_imagen.putdata(pixeles_transformados)
        
        # Guardar o mostrar
        nueva_imagen.show()  # También puedes usar .save('nueva.png')
        nueva_imagen.save("imagen_secreta.png")



    def extraer_mensaje(self): 
        contador=0
        contador2=0
        activate=False
        #Lista que guardara toda la cadena obtenida 
        lista_aux=[]

        for tupla in self.lista :

            for segmento in tupla : 
                contador2=contador2+1
                #print (contador)
                bit_texto = segmento[-1]
                #print(segmento)
                #print(bit_texto)
                #input("dfsdf")
                if (bit_texto == '0'): 
                    #input("Presiona Enter para continuar...")
                    contador = contador +1
                else: 
                    contador=0

                
                lista_aux.append(bit_texto)

                #Se empieza a contar despues de 16 para saltarme los bits de la longitud 
                if (contador2>=16 and contador==8 ):
                    #input("si llego ")
                    return lista_aux


        input("no llego ")
        print(" nunca llego a 8")
        return("111111111111111111111111111111110000000000")



    def binario_a_texto(self, cadena_binaria):
        # Cortar desde el bit 17 (índice 16), y eliminar el último bit
        #recortado = cadena_binaria[16:-1]
        #print(cadena_binaria)
        recortado = cadena_binaria

        # Dividir la cadena en bloques de 8 bits
        caracteres = [recortado[i:i+8] for i in range(0, len(recortado), 8)]

        #
        print("imprimimos ya en 8")
        print(caracteres)
        # Convertir cada bloque de 8 bits a un carácter ASCII
        #input("crush")
        texto = ''.join([chr(int(''.join(b), 2)) for b in caracteres if len(b) == 8])

        return texto


    def procesar_imagen_extraer(self): 
        #imagen = Image.open(self.imagen).convert('RGB')
        imagen = Image.open(self.imagen).convert('RGB')
        pixeles = list(imagen.getdata())
        self.lista.clear()
        for p in pixeles :
            self.guardar_pixel_en_binario(p)
        

        return  self.binario_a_texto (self.extraer_mensaje())


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 programa.py \"<texto>\"")
        sys.exit(1)

    # Une todos los argumentos para permitir frases con espacios
    
    texto_argumento = ' '.join(sys.argv[3:])
    print(texto_argumento)
    analizador = LSB(texto_argumento ,sys.argv[2])
    #analizador.mostrar_resultados()
    #analizador.cadena_final_para_agregar()

    if(sys.argv[1]=="c"):
        analizador.procesar_imagen_guardar()
    elif(sys.argv[1]=="d"):
        print ("El mensaje oculto es : "+ analizador.procesar_imagen_extraer())








