class Compilador:

    def __init__(self, input):
        self.lineas = input
        self.index = 0
        self.fila = 0
        self.columan = 0
        self.Errores = []

    def _token(self, token, estadoActual, estadoSiguiente):
        if self.lineas[self.index] != " ":
            text = self._juntar(self.index, len(token))
            if self._analizar(token, text):
                self.index += len(token) - 1
                self.columna += len(token) - 1
                return estadoSiguiente
            else:
                return "Fail Error"
        else:
            return estadoActual

    def _juntar(self, index, count):
        try:
            temp = ""
            for i in range(index, index + count):
                temp += self.lineas[i]
            return temp
        except:
            return None

    def _analizar(self, token, text):
        try:
            count = 0
            tmp = ""
            for i in text:
                if str(i) == str(token[count]):
                    temp += i
                    count += 1
                else:
                    return False

            print(temp)
            return True
        except:
            return False

    def _digito(self, estadoSiguiente):
        estadoActual = 'D0'
        numero = ""
        while self.lineas[self.index] != "":

            if self.lineas[self.index] == '\n':
                self.fila += 1
                self.columna = 0

            # PARA SALIRSE
            elif str(self.lineas[self.index]) == '"':
                self.index -= 1
                return [estadoSiguiente, numero]
            elif str(self.lineas[self.index]) == ']':
                self.index -= 1
                return [estadoSiguiente, numero]
            elif str(self.lineas[self.index]) == '}':
                self.index -= 1
                return [estadoSiguiente, numero]

            elif self.lineas[self.index] == '.':
                token = "."
                if estadoActual == 'D2' or estadoActual == 'D0':
                    estadoActual = 'ERROR'
                elif self.lineas[self.index] != ' ':
                    text = self._juntar(self.index, len(token))
                    if self._analizar(token, text):
                        numero += text
                        estadoActual = 'D2'
                        self.index += len(token) - 1
                        self.columna += len(token) - 1
                    else:
                        estadoActual = 'ERROR'

            elif estadoActual == 'D0' or estadoActual == 'D1':
                if self.lineas[self.index] != ' ':
                    estadoActual = 'ERROR'
                    for i in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                        token = i
                        text = self._juntar(self.index, len(token))
                        if self._analizar(token, text):
                            numero += text
                            estadoActual = 'D1'
                            break

            elif estadoActual == 'D2':
                if self.lineas[self.index] != ' ':
                    estadoActual = 'ERROR'
                    for i in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                        text = self._juntar(self.index, len(i))
                        if self._analizar(i, text):
                            numero += text
                            estadoActual = 'D2'
                            break

            if estadoActual == 'ERROR':
                return ['ERROR', -1]

            if self.index < len(self.lineas) - 1:
                self.index += 1
            else:
                break

    def _operaciones(self, estadoSiguiente):
        estadoActual = 'S1'
        hijo_derecho = ""
        hijo_izquierdo = ""
        operador = ""
        while self.lineas[self.index] != "":
            # print(f'CARACTER OP - {self.lineas[self.index] } | ESTADO - {estadoActual} | FILA - {self.fila}  | COLUMNA - {self.columna}')

            # IDENTIFICAR SALTO DE LINEA
            if self.lineas[self.index] == '\n':
                self.fila += 1
                self.columna = 0
                print("here")

            # ************************
            #         ESTADOS
            # ************************

            # S2 -> "Operacion" S3
            elif estadoActual == 'S2':
                estadoActual = self._token('"Operacion"', 'S2', 'S3')

            # S3 -> : S3
            elif estadoActual == 'S2':
                estadoActual = self._token(':', 'S2', 'S3')

            # S3 -> OPERADOR S4
            elif estadoActual == 'S3':
                operadores = ['"Suma"', '"Resta"', '"Multiplicacion"', '"Division"', '"Potencia"',
                              '"Raiz"', '"Inverso"', '"Seno"', '"Coseno"', '"Tangente"', '"Mod"']
                for i in operadores:
                    estadoActual = self._token(i, 'S4', 'S5')
                    if estadoActual != 'ERROR':
                        operador = i
                        break

            # S4 -> "Valor1" S5
            elif estadoActual == 'S4':
                estadoActual = self._token('"Valor1"', 'S4', 'S5')

            # S5 -> : S6
            elif estadoActual == 'S5':
                estadoActual = self._token(':', 'S5', 'S6')

            # S6 -> DIGITO S9
            #    | [ S7
            elif estadoActual == 'S6':
                estadoActual = self._token('[', 'S6', 'S7')
                if estadoActual == 'ERROR':
                    estadoActual = 'S9'
                    a = self._digito('S9')
                    if "ERROR" == a[0]:
                        estadoActual = 'ERROR'
                    elif a[0] == 'S9':
                        hijo_izquierdo = a[1]

            # S7 -> S1 S8
            elif estadoActual == 'S7':
                a = self._operaciones('S8')
                estadoActual = a[0]
                hijo_izquierdo = a[1]

            # S8 -> ] S9
            elif estadoActual == 'S8':
                estadoActual = self._token(']', 'S8', 'S9')

            # S9 -> "Valor2" S10
            elif estadoActual == 'S9':
                if operador == '"Inverso"' or operador == '"Seno"':
                    self.index -= 1
                    # REALIZAR LA OPERACION ARITMETICA Y DEVOLVER UN SOLO VALOR
                    print("\t*****OPERACION ARITMETICA*****")
                    print('\t', operador, '(', hijo_izquierdo, ')')
                    print('\t*******************************\n')
                    op = operador + '('+hijo_izquierdo + ')'
                    return ['S14', op]
                else:
                    estadoActual = self._token('"Valor2"', 'S9', 'S10')

            # S10 -> : S11
            elif estadoActual == 'S10':
                estadoActual = self._token(':', 'S10', 'S11')

            # S11 -> DIGITO S14
            #    | [ S12
            elif estadoActual == 'S11':
                estadoActual = self._token('[', 'S11', 'S12')
                if estadoActual == 'ERROR':
                    estadoActual = 'S14'
                    a = self._digito('S14')
                    if "ERROR" == a[0]:
                        estadoActual = 'ERROR'
                    elif 'S14' == a[0]:
                        hijo_derecho = a[1]
                        # REALIZAR LA OPERACION ARITMETICA Y DEVOLVER UN SOLO VALOR
                        print("\t*****OPERACION ARITMETICA*****")
                        print('\t', hijo_izquierdo, operador, hijo_derecho)
                        print('\t*******************************\n')
                        op = hijo_izquierdo + operador + hijo_derecho
                        return [estadoSiguiente, op]

            # S12 -> S1 S13
            elif estadoActual == 'S12':
                estadoActual = 'S13'
                a = self._operaciones('S13')
                hijo_derecho = a[1]
                if "ERROR" == a[0]:
                    estadoActual = 'ERROR'

            # S13 -> ] S14
            elif estadoActual == 'S13':
                estadoActual = self._token(']', 'S13', 'S14')

                # REALIZAR LA OPERACION ARITMETICA Y DEVOLVER UN SOLO VALOR
                print("\t*****OPERACION ARITMETICA*****")
                print('\t', hijo_izquierdo, operador, hijo_derecho)
                print('\t*******************************\n')
                op = hijo_izquierdo + operador + hijo_derecho
                return [estadoSiguiente, op]

            # ERRORES
            if estadoActual == 'ERROR':
                print("********************************")
                print("\tERROR")
                print("********************************")
                # ERROR
                self.guardarErrores(
                    self.lineas[self.index], self.fila, self.columna)
                return ['ERROR', -1]

            # INCREMENTAR POSICION
            if self.index < len(self.lineas) - 1:
                self.index += 1
            else:
                break

    def _compile(self):
        estadoActual = 'S0'
        while self.lineas[self.index] != "":
            # print(f'CARACTER11 - {self.lineas[self.index] } | ESTADO - {estadoActual} | FILA - {self.fila}  | COLUMNA - {self.columna}')

            # IDENTIFICAR SALTO DE LINEA
            if self.lineas[self.index] == '\n':
                self.fila += 1
                self.columna = 0

            # ************************
            #         ESTADOS
            # ************************

            # S0 -> { S1
            elif estadoActual == 'S0':
                estadoActual = self._token('{', 'S0', 'S1')

            # S1 -> "Operacion" S2
            elif estadoActual == 'S1':
                if self.lineas[self.index] != " ":
                    a = self._operaciones('S14')
                    estadoActual = a[0]
                    print("\t*****RESULTADO*****")
                    print('\t', a[1])
                    print('\t*******************************\n')

            # S14 -> }
            elif estadoActual == 'S14':
                # print("ESTO DE ULTIMO")
                estadoActual = self._token('}', 'S14', 'S15')

            # S15 -> ,
            elif estadoActual == 'S15':
                if self.lineas[self.index] != ' ':
                    estadoActual = self._token(',', 'S16', 'S0')

            elif estadoActual == 'S16':
                break

            # ERRORES
            if estadoActual == 'ERROR':
                # print('\t AQUI OCURRIO UN ERROR')
                estadoActual = 'S0'

            # INCREMENTAR POSICION
            if self.index < len(self.lineas) - 1:
                self.index += 1
            else:
                break

    def guardarErrores(self, token, fila, columna):
        self.Errores.append({"token": token, "fila": fila, "columna": columna})
