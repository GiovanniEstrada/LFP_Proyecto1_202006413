import os

archivo = open('text.txt', 'r', encoding="utf-8")
lineas = ''

for i in archivo.readlines():
    lineas += i

print(lineas)


class Analizador:
    def __init__(self, entrada: str):
        self.lineas = entrada  # ENTRADA
        self.index = 0  # POSICION DE CARACTERES EN LA ENTRADA
        self.fila = 1  # FILA ACTUAL
        self.columna = 0  # COLUMNA ACTUAL
        self.guardarFormula = []
        self.ListaErrores = []  # LISTA PARA GUARDAR ERRORES
        self.MaestroFormulas = []
        self.TokenList = []
        self.TokenID = 0
        self.error_type = ""
        self.Formula = ""
        self.TokenActual = ""
        self.DescErr = ""

    def _token(self, token: str, estado_actual: str, estado_sig: str):
        print(f"linea: {self.lineas[self.index]}")
        if self.lineas[self.index] != " ":
            text = self._juntar(self.index, len(token))
            print(f"text: {text}")
            if self._analizar(token, text):
                self.index += len(token) - 1
                self.columna += len(token) - 1
                return estado_sig
            else:
                # GUARDARIA ERROR LEXICO
                return 'ERROR'
        else:
            return estado_actual

    def _juntar(self, _index: int, _count: int):
        try:
            tmp = ''
            for i in range(_index, _index + _count):
                tmp += self.lineas[i]
            return tmp
        except:
            return None

    def _analizar(self, token, texto):
        try:
            count = 0
            tokem_tmp = ""
            for i in texto:
                # CUANDO LA LETRA HAGA MATCH CON EL TOKEN ENTRA
                if str(i) == str(token[count]):
                    tokem_tmp += i
                    count += 1
                else:
                    # print('ERROR1')
                    return False

            print(f'********** ENCONTRE - {tokem_tmp} ***************')
            return True
        except:
            # print('ERROR2')
            return False

    def _analizarCadena(self):
        estado_aux = ""
        tmp = self.index
        cadena = ""
        while self.lineas[tmp] != "":
            if self.lineas[tmp] == '\n':
                return 'ERROR'
            elif estado_aux == '':
                estado_aux = "INICIO"
            elif self.lineas[tmp] == " " or self.lineas[tmp] == "(" or self.lineas[tmp] == ")" or self.lineas[tmp] == ",":
                return [cadena, tmp]
            elif estado_aux == 'INICIO':
                cadena += self.lineas[tmp]
                # print(f'CADENA - {self.lineas[tmp] } ')
            if tmp < len(self.lineas) - 1:
                tmp += 1
            else:
                break

    def _analizarCadenaJSON(self):
        estado_aux = ""
        tmp = self.index
        cadena = ""
        while self.lineas[tmp] != "":
            print(cadena)
            if estado_aux == '':
                estado_aux = "INICIO"
            elif cadena == "$set":
                return [cadena, tmp]
            elif self.lineas[tmp] == '"':
                return [cadena, tmp]
            elif estado_aux == 'INICIO':
                cadena += self.lineas[tmp]
            if tmp < len(self.lineas) - 1:
                tmp += 1
            else:
                break

    def _analizarJSON(self):
        estado_aux = "INICIO"
        estado_tmp = "INICIO"
        cadena = ""
        Json = []
        jsonTmp = []
        while self.lineas[self.index] != "":
            self.columna += 1

            if self.lineas[self.index] == '\n':
                self.fila += 1
                self.columna = 0

            # INICIO -> , S0
            elif estado_aux == 'INICIO':
                estado_aux = self._token(',', 'INICIO', 'S0')
                self.TokenActual = ","
                self.DescErr = "No se encontro el separador de parametros"
                if estado_aux != 'ERROR':
                    self.TokenID += 1
                    self.TokenList.append([self.TokenID, 'Separador', ','])

            # S0 -> " S1
            elif estado_aux == 'S0':
                estado_aux = self._token('“', 'S0', 'S1')
                self.TokenActual = '"'
                self.DescErr = "Error al detectar la cadena"
                if estado_aux != 'ERROR':
                    self.TokenID += 1
                    self.TokenList.append(
                        [self.TokenID, 'Apertura Parametro', '"'])

            # S1 -> { S2
            elif estado_aux == 'S1':
                estado_tmp = 'S1'
                estado_aux = self._token('{', 'S1', 'S2')
                self.TokenActual = "{"
                self.DescErr = "Error al iniciar JSON"
                if estado_tmp != estado_aux:
                    cadena += '"\n {\n'
                    if estado_aux != 'ERROR':
                        self.TokenID += 1
                        self.TokenList.append(
                            [self.TokenID, 'Inicio JSON', '{'])

            # S2 -> " S3
            elif estado_aux == 'S2':
                estado_tmp = 'S2'
                estado_aux = self._token('"', 'S2', 'S3')
                self.TokenActual = '"'
                self.DescErr = "Error al detectar la cadena"
                if estado_tmp != estado_aux:
                    if estado_aux != 'ERROR':
                        self.TokenID += 1
                        self.TokenList.append(
                            [self.TokenID, 'Inicio Cadena', '"'])

            # S3 -> ID S4
            elif estado_aux == 'S3':
                self.index -= 1
                result = self._analizarCadenaJSON()
                self.TokenActual = 'ID'
                self.DescErr = "Error al leer el ID"
                self.index += 1
                estado_aux = self._token(result[0], 'S3', 'S4')
                if estado_tmp != estado_aux:
                    jsonTmp.append(result[0])
                    cadena += '     "'
                    if estado_aux != 'ERROR':
                        self.TokenID += 1
                        self.TokenList.append([self.TokenID, 'ID', result[0]])

            # S4 -> " S5
            elif estado_aux == 'S4':
                estado_tmp == 'S4'
                estado_aux = self._token('"', 'S4', 'S5')
                self.TokenActual = '"'
                self.DescErr = "Error al detectar la cadena"
                if estado_tmp != estado_aux:
                    cadena += f'{result[0]}'
                    if estado_aux != 'ERROR':
                        self.TokenID += 1
                        self.TokenList.append(
                            [self.TokenID, 'Cierre Cadena', '"'])

            # S5 -> : S6
            elif estado_aux == 'S5':
                estado_tmp = 'S5'
                estado_aux = self._token(':', 'S5', 'S6')
                self.TokenActual = ':'
                self.DescErr = "Falta un caracter"
                if estado_tmp != estado_aux:
                    cadena += '"'
                    if estado_aux != 'ERROR':
                        self.TokenID += 1
                        self.TokenList.append(
                            [self.TokenID, 'Asignacion', ':'])

            # S6 -> " S7
            elif estado_aux == 'S6':
                estado_tmp = 'S6'
                estado_aux = self._token('"', 'S6', 'S7')
                self.TokenActual = '"'
                self.DescErr = "Error al detectar la cadena"
                if estado_tmp != estado_aux:
                    cadena += ' :'
                    if estado_aux != 'ERROR':
                        self.TokenID += 1
                        self.TokenList.append(
                            [self.TokenID, 'Inicio Cadena', '"'])

            # S7 -> VAL S8
            elif estado_aux == 'S7':
                estado_tmp = 'S7'
                self.index -= 1
                result = self._analizarCadenaJSON()
                self.index += 1
                self.TokenActual = 'VAL'
                self.DescErr = "Error al detectar la cadena"
                estado_aux = self._token(result[0], 'S7', 'S8')
                if estado_aux != estado_tmp:
                    cadena += ' "'
                    jsonTmp.append(result[0])
                    if estado_aux != 'ERROR':
                        self.TokenID += 1
                        self.TokenList.append(
                            [self.TokenID, 'Valor', result[0]])

            # S8 -> " S9
            elif estado_aux == 'S8':
                estado_tmp = 'S8'
                estado_aux = self._token('"', 'S8', 'S9')
                self.TokenActual = '"'
                self.DescErr = "Error al detectar la cadena"
                if estado_tmp != estado_aux:
                    cadena += f'{result[0]}'
                    if estado_aux != 'ERROR':
                        self.TokenID += 1
                        self.TokenList.append(
                            [self.TokenID, 'Cierre Cadena', '"'])

            # S9 -> , S10 | } S11
            elif estado_aux == 'S9':
                estado_tmp = 'S9'
                estado_aux = self._token('}', 'S9', 'S11')
                self.TokenActual = '}'
                self.DescErr = "Falto cerrar JSON"
                if estado_aux == 'ERROR':
                    estado_aux = self._token(',', 'S9', 'S10')
                    self.TokenActual = ','
                self.DescErr = "Error en separador"
                if estado_tmp != estado_aux:
                    cadena += '"'
                    if estado_aux != 'ERROR':
                        self.TokenID += 1
                        self.TokenList.append(
                            [self.TokenID, 'Separador', ','])
                    else:
                        self.TokenID += 1
                        self.TokenList.append(
                            [self.TokenID, 'Cierre JSON', '}'])

            # S10 -> " S3
            elif estado_aux == 'S10':
                estado_tmp = 'S10'
                estado_aux = self._token('"', 'S2', 'S3')
                self.TokenActual = '"'
                self.DescErr = "Error al detectar la cadena"
                if estado_tmp != estado_aux:
                    cadena += ',\n'
                    if estado_aux != 'ERROR':
                        self.TokenID += 1
                        self.TokenList.append(
                            [self.TokenID, "Inicio Cadena", '"'])

            # S11 -> , S12 | " FIN
            elif estado_aux == 'S11':
                estado_tmp = 'S11'
                estado_aux = self._token('”', 'S11', 'FIN')
                self.TokenActual = '"'
                self.DescErr = "Error al detectar la cadena"
                if estado_aux == 'ERROR':
                    estado_aux = self._token(',', 'S11', 'S12')
                    Json.append(jsonTmp.copy())
                    jsonTmp.clear()
                    if estado_tmp != estado_aux:
                        cadena += '\n }'
                        if estado_aux != 'ERROR':
                            self.TokenID += 1
                            self.TokenList.append(
                                [self.TokenID, 'Separador', ','])
                else:
                    if estado_aux != 'ERROR':
                        cadena += '\n } \n"'
                        self.TokenID += 1
                        self.TokenList.append(
                            [self.TokenID, "Cierre Parametro", '"'])

            # S12 -> { S13
            elif estado_aux == 'S12':
                estado_tmp = 'S12'
                estado_aux = self._token('{', 'S12', 'S13')
                self.TokenActual = '"'
                self.DescErr = "Error al abrir llaves"
                if estado_tmp != estado_aux:
                    cadena += ",\n"
                    if estado_aux != 'ERROR':
                        self.TokenID += 1
                        self.TokenList.append(
                            [self.TokenID, 'Apertura JSON', '{'])

            # S13 -> $set S14
            elif estado_aux == 'S13':
                estado_tmp = 'S13'
                self.index -= 1
                result = self._analizarCadenaJSON()
                self.index += 1
                estado_aux = self._token(result[0], 'S13', 'S14')
                self.TokenActual = '$set'
                self.DescErr = "Error al detectar comando"
                if estado_tmp != estado_aux:
                    jsonTmp.append(result[0])
                    cadena += '\n {\n'
                    if estado_aux != 'ERROR':
                        self.TokenID += 1
                        self.TokenList.append(
                            [self.TokenID, "Indicador", result[0]])

            # S14 -> : S15
            elif estado_aux == 'S14':
                estado_tmp = 'S14'
                estado_aux = self._token(':', 'S14', 'S15')
                self.TokenActual = ':'
                self.DescErr = "Error al ingresar valor"
                if estado_tmp != estado_aux:
                    cadena += "     $set: "
                    if estado_aux != 'ERROR':
                        self.TokenID += 1
                        self.TokenList.append(
                            [self.TokenID, 'Asignacion', ':'])

            # S15 -> { S16
            elif estado_aux == 'S15':
                estado_tmp = 'S15'
                estado_aux = self._token('{', 'S15', 'S16')
                self.TokenActual = '{'
                self.DescErr = "Error al iniciar cadena"
                if estado_tmp != estado_aux:
                    cadena += "{"
                    if estado_aux != 'ERROR':
                        self.TokenID += 1
                        self.TokenList.append(
                            [self.TokenID, 'Apertura JSON', '{'])

            # S16 -> " S17
            elif estado_aux == 'S16':
                estado_tmp = 'S16'
                estado_aux = self._token('"', 'S16', 'S17')
                self.TokenActual = '"'
                self.DescErr = "Error al detectar la cadena"
                if estado_tmp != estado_aux:
                    cadena += '"'
                    if estado_aux != 'ERROR':
                        self.TokenID += 1
                        self.TokenList.append(
                            [self.TokenID, 'Inicio Cadena', '"'])

            # S17 -> ID S18
            elif estado_aux == 'S17':
                estado_tmp = 'S17'
                self.index -= 1
                result = self._analizarCadenaJSON()
                self.index += 1
                estado_aux = self._token(result[0], 'S17', 'S18')
                self.TokenActual = 'ID'
                self.DescErr = "Error al ingresar el ID"
                if estado_tmp != estado_aux:
                    jsonTmp.append(result[0])
                    cadena += f'{result[0]}'
                    if estado_aux != 'ERROR':
                        self.TokenID += 1
                        self.TokenList.append([self.TokenID, 'ID', result[0]])

            elif estado_aux == 'S18':
                estado_tmp = 'S18'
                estado_aux = self._token('"', 'S18', 'S19')
                self.TokenActual = '"'
                self.DescErr = "Error al detectar la cadena"
                if estado_tmp != estado_aux:
                    cadena += '"'
                    if estado_aux != 'ERROR':
                        self.TokenID += 1
                        self.TokenList.append(
                            [self.TokenID, 'Cierre Cadena', '"'])

            elif estado_aux == 'S19':
                estado_tmp = 'S19'
                estado_aux = self._token(':', 'S19', 'S20')
                self.TokenActual = ':'
                self.DescErr = "Error al ingresar valor"
                if estado_tmp != estado_aux:
                    cadena += ' : '
                    if estado_aux != 'ERROR':
                        self.TokenID += 1
                        self.TokenList.append(
                            [self.TokenID, 'Asignacion', ':'])

            # S16 -> " S17
            elif estado_aux == 'S20':
                estado_tmp = 'S20'
                estado_aux = self._token('"', 'S20', 'S21')
                self.TokenActual = '"'
                self.DescErr = "Error al detectar la cadena"
                if estado_tmp != estado_aux:
                    cadena += '"'
                    if estado_aux != 'ERROR':
                        self.TokenID += 1
                        self.TokenList.append(
                            [self.TokenID, 'Inicio Cadena', '"'])

            # S17 -> VAL S18
            elif estado_aux == 'S21':
                estado_tmp = 'S21'
                self.index -= 1
                result = self._analizarCadenaJSON()
                self.index += 1
                estado_aux = self._token(result[0], 'S21', 'S22')
                self.TokenActual = 'Val'
                self.DescErr = "Error al leer valor"
                if estado_tmp != estado_aux:
                    jsonTmp.append(result[0])
                    cadena += f'{result[0]}'
                    if estado_aux != 'ERROR':
                        self.TokenID += 1
                        self.TokenList.append(
                            [self.TokenID, 'Valor', result[0]])

            elif estado_aux == 'S22':
                estado_tmp = 'S22'
                estado_aux = self._token('"', 'S22', 'S23')
                self.TokenActual = '"'
                self.DescErr = "Error al detectar la cadena"
                if estado_tmp != estado_aux:
                    cadena += '"'
                    if estado_aux != 'ERROR':
                        self.TokenID += 1
                        self.TokenList.append(
                            [self.TokenID, 'Cierre Cadena', '"'])

            elif estado_aux == 'S23':
                estado_tmp = 'S23'
                estado_aux = self._token('}', 'S23', 'S24')
                self.TokenActual = '"'
                self.DescErr = "Error al cerrar JSON"
                if estado_tmp != estado_aux:
                    cadena += '}'
                    if estado_aux != 'ERROR':
                        self.TokenID += 1
                        self.TokenList.append(
                            [self.TokenID, 'Cierre JSON', '}'])

            elif estado_aux == 'S24':
                estado_tmp = 'S24'
                estado_aux = self._token('}', 'S24', 'S25')
                self.TokenActual = '"'
                self.DescErr = "Error al cerrar JSON"
                if estado_tmp != estado_aux:
                    cadena += '\n }'
                    if estado_aux != 'ERROR':
                        self.TokenID += 1
                        self.TokenList.append(
                            [self.TokenID, 'Cierre JSON', '}'])

            elif estado_aux == 'S25':
                estado_tmp = 'S25'
                estado_aux = self._token('”', 'S25', 'FIN')
                self.TokenActual = '"'
                self.DescErr = "Error al detectar la cadena"
                if estado_tmp != estado_aux:
                    cadena += '\n"'
                    self.fila += 1
                    if estado_aux != 'ERROR':
                        self.TokenID += 1
                        self.TokenList.append(
                            [self.TokenID, 'Cierre Parametro', '"'])

            if estado_aux == 'ERROR':
                self.ListaErrores.append([
                    "Error en estructura JSON", self.fila, self.columna, self.TokenActual, self.DescErr])
                return 'ERROR'

            if estado_aux == 'FIN':
                Json.append(jsonTmp.copy())
                self.guardarFormula.append(Json)
                self.guardarFormula.append([cadena])
                print(cadena)
                return 'S8'

            # S9  -> } S11
            # S10 -> , S11
            # S11 -> { S12
            # S12 -> $set S13
            # S13 -> : S14
            # S14 -> S1
            # S10 -> " S15

            # INCREMENTAR POSICION
            if self.index < len(self.lineas) - 1:
                self.index += 1
            else:
                break

    def _compile(self):
        estado_actual = 'S0'
        estado_siguiente = 'S0'
        while self.lineas[self.index] != "":
            self.columna += 1

            # print(f"Estado actual: {estado_actual}")
            # print(
            #     f'CARACTER11 - {self.lineas[self.index] } | ESTADO - {estado_actual} | FILA - {self.fila}  | COLUMNA - {self.columna}')
            # print(f"index {self.index}")
            # ************************
            #         ESTADOS
            # ************************
            try:
                while self.lineas[self.index] == "\n":
                    self.index += 1
                    self.fila += 1
                    self.columna = 0
            except:
                print("Fin del recorrido ----------------------")
                break

            if estado_actual == 'AWAIT':
                while self.lineas[self.index] != "\n":
                    self.index += 1
                self.fila += 1
                self.columna = 0
                estado_actual = 'S0'

            elif estado_actual == 'S0':
                _com1 = self._token('---', 'S0', 'COMENTARIO1')
                _com2 = self._token('/*', 'S0', 'COMENTARIO2')
                if _com1 == 'COMENTARIO1':
                    self._comentarioSimple()
                    self.fila += 1
                    if estado_actual != 'ERROR':
                        self.TokenID += 1
                        self.TokenList.append(
                            [self.TokenID, 'Comentario', 'Comentario'])
                elif _com2 == 'COMENTARIO2':
                    self._comentarioVariasLineas()
                    if estado_actual != 'ERROR':
                        self.TokenID += 1
                        self.TokenList.append(
                            [self.TokenID, 'Comentario', 'Comentario'])
                else:
                    funciones = ['CrearBD', 'EliminarBD', 'CrearColeccion', 'EliminarColeccion',
                                 'InsertarUnico', 'ActualizarUnico', 'EliminarUnico', 'BuscarTodo', 'BuscarUnico']
                    estado_siguiente = 'S1'
                    for i in funciones:
                        estado_actual = self._token(i, 'S0', 'S1')
                        self.TokenActual = 'Formula'
                        self.DescErr = "Error, formula no existe"
                        if estado_actual != 'ERROR':
                            self.guardarFormula.append(self.fila)
                            self.guardarFormula.append(i)
                            if estado_actual != 'ERROR':
                                self.TokenID += 1
                                self.TokenList.append(
                                    [self.TokenID, 'Funcion', i])
                            break

            # S1 -> ID S2
            elif estado_actual == 'S1':
                estado_siguiente = 'S2'
                result = self._analizarCadena()
                self.index += 1
                self.guardarFormula.append(result[0])
                estado_actual = self._token(result[0], 'S1', 'S2')
                self.TokenActual = 'ID'
                self.DescErr = "Error al detectar ID"
                if estado_actual != 'ERROR':
                    self.TokenID += 1
                    self.TokenList.append([self.TokenID, 'ID', result[0]])

            elif estado_actual == 'S2':
                estado_siguiente = 'S3'
                estado_actual = self._token('=', 'S2', 'S3')
                self.TokenActual = '='
                self.DescErr = "Error al asignar valor"
                if estado_actual != 'S2':
                    if estado_actual != 'ERROR':
                        self.TokenID += 1
                        self.TokenList.append(
                            [self.TokenID, 'Asignacion', '='])

            elif estado_actual == 'S3':
                estado_siguiente = 'S4'
                self.index += 1
                self.guardarFormula.append('nueva')
                estado_actual = self._token('nueva', 'S3', 'S4')
                self.TokenActual = 'Nuevo'
                self.DescErr = "Error, caracter invalido"
                self.TokenActual = 'Val'
                self.DescErr = "Error, caracter invalido"
                if estado_actual != 'S3':
                    if estado_actual != 'ERROR':
                        self.TokenID += 1
                        self.TokenList.append(
                            [self.TokenID, 'Nuevo', 'nuevo'])

            elif estado_actual == 'S4':
                estado_siguiente = 'S5'
                funciones = ['CrearBD', 'EliminarBD', 'CrearColeccion', 'EliminarColeccion',
                             'InsertarUnico', 'ActualizarUnico', 'EliminarUnico', 'BuscarTodo', 'BuscarUnico']
                for i in funciones:
                    estado_actual = self._token(i, 'S4', 'S5')
                    self.TokenActual = 'Formula'
                    self.DescErr = "Error, formula no existe"
                    if estado_actual != 'ERROR' and estado_actual != 'S4':
                        self.guardarFormula.append(i)
                        if estado_actual != 'ERROR':
                            self.TokenID += 1
                            self.TokenList.append([self.TokenID, 'Funcion', i])
                            self.Formula = i
                        break

            elif estado_actual == 'S5':
                estado_siguiente = 'S6'
                estado_actual = self._token('(', 'S5', 'S6')
                self.TokenActual = '('
                self.DescErr = "Error al iniciar la formula"
                if estado_actual != 'ERROR' and estado_actual != 'S5':
                    self.TokenID += 1
                    self.TokenList.append(
                        [self.TokenID, 'Inicio Parametros', '('])

            elif estado_actual == 'S6':
                estado_actual = self._token(')', 'S6', 'S9')
                self.TokenActual = ')'
                self.DescErr = "Error al cerrar parentesis"
                if estado_actual == 'ERROR':
                    self.TokenActual = 'Param1'
                    self.DescErr = "Error al ingresar el parametro"
                    if self.Formula == "EliminarBD" or self.Formula == "CrearBD":
                        self.error_type = "Param"
                        self.TokenActual = 'Param1'
                        self.DescErr = "Error, formula no tiene parametros"
                    else:
                        estado_siguiente = 'S7'
                        self.index -= 1
                        result = self._analizarCadena()
                        self.index += 1
                        self.guardarFormula.append(result[0])
                        estado_actual = self._token(result[0], 'S6', 'S7')
                        self.TokenList.append(
                            [self.TokenID, 'Param1', result[0]])
                else:
                    if estado_actual != 'ERROR' and estado_actual != 'S6':
                        self.TokenID += 1
                        self.TokenList.append(
                            [self.TokenID, 'Cierre Parametros', ')'])
                    estado_siguiente = 'S9'
                    self.guardarFormula.append("NONE")
                    self.guardarFormula.append("NONE")

            elif estado_actual == 'S7' and self.lineas[self.index] != " ":
                estado_actual = self._token(')', 'S7', 'S9')
                self.TokenActual = ')'
                self.DescErr = "Error al cerrar parentesis"
                if estado_actual == 'ERROR':
                    if self.Formula == "CrearColeccion" or self.Formula == "EliminarColeccion" or self.Formula == "BuscarTodo" or self.Formula == "BuscarUnicio":
                        self.error_type = "Param"
                        self.TokenActual = 'Param2'
                        self.DescErr = "Error, parametros exceden el limite"
                    else:
                        while self.lineas[self.index] == " ":
                            self.index += 1
                            self.columna += 1
                        estado_siguiente = 'S8'
                        result = self._analizarJSON()
                        print(result)
                        estado_actual = result
                        if estado_actual == 'ERROR':
                            break
                else:
                    if estado_actual != 'ERROR':
                        self.TokenID += 1
                        self.TokenList.append(
                            [self.TokenID, 'Cierre Parametros', ')'])
                    estado_siguiente = 'S9'
                    self.guardarFormula.append("NONE")

            elif estado_actual == 'S8':
                estado_siguiente = 'S9'
                estado_actual = self._token(')', 'S8', 'S9')
                self.TokenActual = ')'
                self.DescErr = "Error al cerrar parentesis"
                if estado_actual != 'ERROR':
                    self.TokenID += 1
                    self.TokenList.append(
                        [self.TokenID, 'Cierre Parametros', ')'])

            elif estado_actual == 'S9':
                estado_siguiente = 'S10'
                estado_actual = self._token(';', 'S9', 'S10')
                self.TokenActual = ';'
                self.DescErr = "Error, falta cerrar la linea"
                if estado_actual == 'S10':
                    self.guardarFormula.pop(4)
                    self.MaestroFormulas.append(self.guardarFormula.copy())
                    self.guardarFormula.clear()
                    estado_actual = 'S0'
                    self.columna = 0
                    self.fila += 1
                    self.index += 1
                    if estado_actual != 'ERROR':
                        self.TokenID += 1
                        self.TokenList.append(
                            [self.TokenID, 'Fin de la linea', ';'])

                # ERRORES
            if estado_actual == 'ERROR' and self.lineas[self.index] != "\n":

                self.ListaErrores.append([
                    "Sintax Error", self.fila, self.columna, self.TokenActual, self.DescErr])
                estado_actual = 'AWAIT'

            # if estado_actual == 'ERROR' and self.lineas[self.index] != "\n":
            #     if self.error_type == "Param":
            #         self.error_type = ""
            #         self.ListaErrores.append([
            #             "Sintax Error", self.fila, self.columna - 1, self.TokenActual, self.DescErr])
            #         estado_actual = 'AWAIT'
            #     elif self.lineas[self.index] == " " or self.lineas[self.index] == ")":
            #         self.ListaErrores.append([
            #             "Error en la sintaxis", self.fila, self.columna - 1, self.TokenActual, self.DescErr])
            #         estado_actual = estado_siguiente
            #         estado_actual = 'AWAIT'
            #         self.guardarFormula.clear()
            #     elif self.lineas[self.index] == "\n" and self.columna:
            #         self.ListaErrores.append([
            #             "Error en la sintaxis", self.fila, self.columna - 1, self.TokenActual, self.DescErr])
            #         estado_actual = 'S0'
            #         self.fila += 1

            #         self.columna = 0
            #         self.guardarFormula.clear()

            # INCREMENTAR POSICION
            if self.index < len(self.lineas) - 1:
                self.index += 1
            else:
                break

        self._generarMongoDB()

    def _generarMongoDB(self):

        archivo = open("MongoDB.txt", "w")
        texto = ""
        for i in self.MaestroFormulas:
            if i[1] == 'CrearBD':
                texto += f"use('{i[2]}');\n\n"
                continue
            if i[1] == 'EliminarBD':
                texto += f"{i[2]}.dropDatabase(); \n\n"
                continue
            if i[1] == 'CrearColeccion':
                texto += f"dbo.createCollection({i[4]});\n\n"
                continue
            if i[1] == 'EliminarColeccion':
                texto += f"dbo.{i[4][1:-1]}.drop();\n\n"
                continue
            if i[1] == 'InsertarUnico':
                texto += f"dbo.{i[4][1:-1]}.InsertOne({i[6][0]});\n\n"
                continue
            if i[1] == 'ActualizarUnido':
                texto += f"dbo.{i[4][1:-1]}.InsertOne({i[6][0]});\n\n"
                continue
            if i[1] == 'EliminarUnico':
                texto += f"dbo.{i[4][1:-1]}.InsertOne({i[6][0]});\n\n"
                continue
            if i[1] == 'BuscarTodo':
                texto += f"dbo.{i[4][1:-1]}.Find();\n\n"
                continue
            if i[1] == 'BuscarUnico':
                texto += f"dbo.{i[4][1:-1]}.InsertOne();\n\n"
                continue

        print(texto)
        archivo.write(texto)
        archivo.close()

    def _comentarioSimple(self):
        estado_actual = 'S0'
        while self.lineas[self.index] != "":
            # IDENTIFICAR SALTO DE LINEA
            if self.lineas[self.index] == '\n':
                if self.lineas[self.index + 1] != '\n':
                    return

            # ERRORES
            if estado_actual == 'ERROR':
                return

            # INCREMENTAR POSICION
            if self.index < len(self.lineas) - 1:
                self.index += 1
            else:
                break

    def _comentarioVariasLineas(self):
        # IDENTIFICAR SALTO DE LINEA
        estado_actual = 'S0'
        endC = ""
        while self.lineas[self.index] != "":
            # IDENTIFICAR SALTO DE LINEA
            endC += self.lineas[self.index]
            if self.lineas[self.index] == '\n':
                self.columna = 0
                self.fila += 1

            if endC == "*/":
                break

            # ERRORES
            if estado_actual == 'ERROR':
                return

            # INCREMENTAR POSICION
            if self.index < len(self.lineas) - 1:
                endC = self.lineas[self.index]
                self.index += 1
            else:
                break


a = Analizador(lineas)
a._compile()
print(a.MaestroFormulas)
print(a.ListaErrores)
