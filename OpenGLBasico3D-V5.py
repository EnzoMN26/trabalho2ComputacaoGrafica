# ***********************************************************************************
#   OpenGLBasico3D-V5.py
#       Autor: Márcio Sarroglia Pinho
#       pinho@pucrs.br
#   Este programa exibe dois Cubos em OpenGL
#   Para maiores informações, consulte
# 
#   Para construir este programa, foi utilizada a biblioteca PyOpenGL, disponível em
#   http://pyopengl.sourceforge.net/documentation/index.html
#
#   Outro exemplo de código em Python, usando OpenGL3D pode ser obtido em
#   http://openglsamples.sourceforge.net/cube_py.html
#
#   Sugere-se consultar também as páginas listadas
#   a seguir:
#   http://bazaar.launchpad.net/~mcfletch/pyopengl-demo/trunk/view/head:/PyOpenGL-Demo/NeHe/lesson1.py
#   http://pyopengl.sourceforge.net/documentation/manual-3.0/index.html#GLUT
#
#   No caso de usar no MacOS, pode ser necessário alterar o arquivo ctypesloader.py,
#   conforme a descrição que está nestes links:
#   https://stackoverflow.com/questions/63475461/unable-to-import-opengl-gl-in-python-on-macos
#   https://stackoverflow.com/questions/6819661/python-location-on-mac-osx
#   Veja o arquivo Patch.rtf, armazenado na mesma pasta deste fonte.
# 
# ***********************************************************************************
import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Ponto import Ponto
from Linha import Linha
import numpy as np
from PIL import Image
import time
import math

rotaCarro = 0
observador = Ponto(0,2,6)
carro = Ponto(0,-0.75,0)
alvo = Ponto(0,-0.75,-6)
posicoesPredios = [[0,3,4], [0,6,5], [0,7,4], [0,9,5], [0,12,5], [0,13,5], [0,28,4], [0,29,3], [2,1,5], [2,2,5], [2,6,4], [2,8,3], [2,20,3], [2,21,4], [2,27,5], [2,28,3], [3,2,5], [3,3,5], [3,7,4], [3,9,3], [3,11,5], [3,12,5], [3,22,4], [4,2,5], [4,6,4], [4,8,5], [4,10,4], [4,12,3], [4,13,5], [5,3,5], [5,11,5], [5,22,4], [5,28,5], [6,1,3], [6,2,5], [6,10,4], [6,12,3], [6,13,5], [6,20,3], [6,27,3], [7,2,5], [7,3,5], [7,7,4], [7,11,5], [7,12,5], [7,13,4], [7,21,3], [7,22,4], [7,28,5], [7,29,3], [8,1,3], [8,6,4], [8,8,5], [8,12,3], [8,13,5], [8,28,4], [9,3,5], [9,13,4], [9,22,4], [9,28,5], [10,2,5], [10,10,4], [10,12,3], [10,13,5], [10,20,3], [10,21,5], [10,27,3], [10,28,4], [11,2,5], [11,3,5], [11,22,4], [11,28,5], [11,29,3], [12,1,3], [12,2,5], [12,6,4], [12,12,3], [12,13,5], [12,20,3], [12,21,5], [12,28,4], [13,2,5], [13,3,5], [13,7,4], [13,9,3], [13,11,5], [13,29,3], [14,8,5], [14,12,3], [14,20,3], [14,21,5], [14,27,3], [27,21,3],[27,23,5],[27,29,4],[28,28,3],[28,2,5],[19,16,4],[19,20,5],[15,21,3],[17,22,4],[15,22,5],[27,13,4],[19,18,5], [19,2,4],[19,5,3],[19,9,4],[19,12,5],[21,13,3],[21,10,4],[21,6,3],[18,13,5],[21,16,3],[21,21,5],[23,13,4],[25,13,4],[27,16,5]]
posicoesGasolina = [[9,1],[25,1],[0,8],[15,8],[0,29],[25,20],[18,26]]
Texturas = []
Angulo = 0.0
camera = 0
flagAnda = False
contadorCombustivel = 300

# **********************************************************************
# LoadTexture
# Retorna o id da textura lida
# **********************************************************************
def LoadTexture(nome) -> int:
    # carrega a imagem
    image = Image.open(nome)
    # print ("X:", image.size[0])
    # print ("Y:", image.size[1])
    # converte para o formato de OpenGL 
    img_data = np.array(list(image.getdata()), np.uint8)
    # Habilita o uso de textura
    glEnable ( GL_TEXTURE_2D )

    #Cria um ID para texura
    texture = glGenTextures(1)
    errorCode =  glGetError()
    if errorCode == GL_INVALID_OPERATION: 
        print ("Erro: glGenTextures chamada entre glBegin/glEnd.")
        return -1

    # Define a forma de armazenamento dos pixels na textura (1= alihamento por byte)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    # Define que tipo de textura ser usada
    # GL_TEXTURE_2D ==> define que ser· usada uma textura 2D (bitmaps)
    # e o nro dela
    glBindTexture(GL_TEXTURE_2D, texture)

    # texture wrapping params
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # texture filtering params
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    errorCode = glGetError()
    if errorCode != GL_NO_ERROR:
        print ("Houve algum erro na criacao da textura.")
        return -1

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.size[0], image.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    # neste ponto, "texture" tem o nro da textura que foi carregada
    errorCode = glGetError()
    if errorCode == GL_INVALID_OPERATION:
        print ("Erro: glTexImage2D chamada entre glBegin/glEnd.")
        return -1

    if errorCode != GL_NO_ERROR:
        print ("Houve algum erro na criacao da textura.")
        return -1
    #image.show()
    return texture

def UseTexture (NroDaTextura: int):
    global Texturas

    if (NroDaTextura>len(Texturas)):
        print ("Numero invalido da textura.")
        glDisable (GL_TEXTURE_2D)
        return
    if (NroDaTextura < 0):
        glDisable (GL_TEXTURE_2D)
    else:
        glEnable (GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, Texturas[NroDaTextura])

# **********************************************************************
#  init()
#  Inicializa os parÃ¢metros globais de OpenGL
#/ **********************************************************************
def init():
    # Define a cor do fundo da tela (BRANCO) 
    glClearColor(0.5, 0.5, 0.5, 1.0)

    glClearDepth(1.0) 
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glEnable (GL_CULL_FACE )
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    nome = "747.tri"

    LeObjeto(nome)
    criaObjeto()

    global Texturas
    Texturas += [LoadTexture('./TexturaAsfalto/CROSS.jpeg')]
    Texturas += [LoadTexture('./TexturaAsfalto/DL.jpeg')]
    Texturas += [LoadTexture('./TexturaAsfalto/DLR.jpeg')]
    Texturas += [LoadTexture('./TexturaAsfalto/DR.jpeg')]
    Texturas += [LoadTexture('./TexturaAsfalto/LR.jpeg')]
    Texturas += [LoadTexture('./TexturaAsfalto/GRASS.jpg')]
    Texturas += [LoadTexture('./TexturaAsfalto/UD.jpeg')]
    Texturas += [LoadTexture('./TexturaAsfalto/UDL.jpeg')]
    Texturas += [LoadTexture('./TexturaAsfalto/UDR.jpeg')]
    Texturas += [LoadTexture('./TexturaAsfalto/UL.jpeg')]
    Texturas += [LoadTexture('./TexturaAsfalto/ULR.jpeg')]
    Texturas += [LoadTexture('./TexturaAsfalto/UR.jpeg')]
    Texturas += [LoadTexture('./TexturaAsfalto/texturaPredio.jpg')]  
    # Texturas += [LoadTexture(Path("TexturaAsfalto/DL.jpg"))] 

   

# **********************************************************************
#  reshape( w: int, h: int )
#  trata o redimensionamento da janela OpenGL
#
# **********************************************************************
def reshape(w: int, h: int):
    global AspectRatio
	# Evita divisÃ£o por zero, no caso de uam janela com largura 0.
    if h == 0:
        h = 1
    # Ajusta a relaÃ§Ã£o entre largura e altura para evitar distorÃ§Ã£o na imagem.
    # Veja funÃ§Ã£o "PosicUser".
    AspectRatio = w / h
	# Reset the coordinate system before modifying
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Seta a viewport para ocupar toda a janela
    glViewport(0, 0, w, h)
    
    PosicUser()
# **********************************************************************
def DefineLuz():
    # Define cores para um objeto dourado
    LuzAmbiente = [0.4, 0.4, 0.4] 
    LuzDifusa   = [0.7, 0.7, 0.7]
    LuzEspecular = [0.9, 0.9, 0.9]
    PosicaoLuz0  = [2.0, 3.0, 0.0 ]  # PosiÃ§Ã£o da Luz
    Especularidade = [1.0, 1.0, 1.0]

    # ****************  Fonte de Luz 0

    glEnable ( GL_COLOR_MATERIAL )

    #Habilita o uso de iluminaÃ§Ã£o
    glEnable(GL_LIGHTING)

    #Ativa o uso da luz ambiente
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, LuzAmbiente)
    # Define os parametros da luz nÃºmero Zero
    glLightfv(GL_LIGHT0, GL_AMBIENT, LuzAmbiente)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, LuzDifusa  )
    glLightfv(GL_LIGHT0, GL_SPECULAR, LuzEspecular  )
    glLightfv(GL_LIGHT0, GL_POSITION, PosicaoLuz0 )
    glEnable(GL_LIGHT0)

    # Ativa o "Color Tracking"
    glEnable(GL_COLOR_MATERIAL)

    # Define a reflectancia do material
    glMaterialfv(GL_FRONT,GL_SPECULAR, Especularidade)

    # Define a concentraÃ§Ã£oo do brilho.
    # Quanto maior o valor do Segundo parametro, mais
    # concentrado serÃ¡ o brilho. (Valores vÃ¡lidos: de 0 a 128)
    glMateriali(GL_FRONT,GL_SHININESS,51)
    

def leMatriz():
    global matriznp
    matriz = []
    with open('./TexturaAsfalto/Mapa1.txt','r') as data_file:
        next(data_file)
        for line in data_file:
            data = line.split()
            matriz.append(data)
        matriznp = np.array(matriz,dtype='int')

def LeObjeto (nomeFile):
    global triangulos
    triangulos = []
    with open(nomeFile,'r') as tresd:
        for line in tresd:
            data = line.split(' ')
            data = list(filter(('').__ne__, data))
            data = [float(data[0]),float(data[1]),float(data[2]),float(data[3]),float(data[4]),float(data[5]),float(data[6]),float(data[7]),float(data[8])]
            triangulos.append(data) 

def criaObjeto():
    global normais, pontos
    normais = []
    pontos = []
    for t in triangulos:
        vetor1 = [t[3]-t[0],t[4]-t[1],t[5]-t[2]]
        vetor2 = [t[6]-t[0],t[7]-t[1],t[8]-t[2]]
        normais.append(np.cross(vetor1,vetor2))
        pontos.append([t[0]/100,t[1]/100,t[2]/100,t[3]/100,t[4]/100,t[5]/100,t[6]/100,t[7]/100,t[8]/100])

def ExibeObjeto():
    aux = 0
    glBegin( GL_TRIANGLES )
    for p in pontos:
        normal = normais[aux]
        glNormal3f(normal[0],normal[1],normal[2])
        glVertex(p[0],p[1],p[2])
        glVertex(p[3],p[4],p[5])
        glVertex(p[6],p[7],p[8])
        aux+=1
    glEnd()





def DesenhaPredio(altura: int):
    UseTexture(12)
    glBegin ( GL_QUADS );
    # Front Face
    glNormal3f(0,0,1);
    glTexCoord(1,1)
    glVertex3f(0, 0,  2);
    glTexCoord(0,1)
    glVertex3f( 2, 0,  2);
    glTexCoord(0,0)
    glVertex3f( 2,  altura,  2);
    glTexCoord(1,0)
    glVertex3f(0,  altura,  2);
    # Back Face
    glNormal3f(0,0,-1);
    glTexCoord(0,1)
    glVertex3f(0, 0, 0);
    glTexCoord(0,0)
    glVertex3f(0,  altura, 0);
    glTexCoord(1,0)
    glVertex3f( 2,  altura, 0);
    glTexCoord(1,1)
    glVertex3f( 2, 0, 0);
    # Top Face
    glNormal3f(0,1,0);
    
    glVertex3f(0,  altura, 0);
    glVertex3f(0,  altura,  2);
    glVertex3f( 2,  altura,  2);
    glVertex3f( 2,  altura, 0);
    # Bottom Face
    glNormal3f(0,-1,0);
    glVertex3f(0, 0, 0);
    glVertex3f( 2, 0, 0);
    glVertex3f( 2, 0,  2);
    glVertex3f(0, 0,  2);
    # Right face
    glNormal3f(1,0,0);
    glTexCoord(0,1)
    glVertex3f( 2, 0, 0);
    glTexCoord(0,0)
    glVertex3f( 2,  altura, 0);
    glTexCoord(1,0)
    glVertex3f( 2,  altura,  2);
    glTexCoord(1,1)
    glVertex3f( 2, 0,  2);
    # Left Face
    glNormal3f(-1,0,0);
    glTexCoord(1,1)
    glVertex3f(0, 0, 0);
    glTexCoord(0,1)
    glVertex3f(0, 0,  2);
    glTexCoord(0,0)
    glVertex3f(0,  altura,  2);
    glTexCoord(1,0)
    glVertex3f(0,  altura, 0);
    glEnd();

def DesenhaCarro():

    glBegin ( GL_QUADS );
    glColor3f(0.0,0.0,0.0) # Amarelo
    # Front Face
    glNormal3f(0,0,1);
    glVertex3f(-0.3, -0.2,  0.8);
    glVertex3f( 0.3, -0.2,  0.8);
    glVertex3f( 0.3,  0.2,  0.8);
    glVertex3f(-0.3,  0.2,  0.8);
    # Front Face Teto
    glNormal3f(0,0,1);
    glColor3f(0.5,0.0,0.0) # Vermelho
    glVertex3f(-0.25, -0.2,  0.3);
    glVertex3f( 0.25, -0.2,  0.3);
    glVertex3f( 0.25,  0.3,  0.3);
    glVertex3f(-0.25,  0.3,  0.3);
    
    glColor3f(0.0,0.0,0.0) # Amarelo
    # Back Face
    glNormal3f(0,0,-1);
    glVertex3f(-0.3, -0.2, -0.8);
    glVertex3f(-0.3,  0.2, -0.8);
    glVertex3f( 0.3,  0.2, -0.8);
    glVertex3f( 0.3, -0.2, -0.8);

    # Back Face Teto
    glNormal3f(0,0,-1);
    glColor3f(0.0,0.0,0.5) # Vermelho
    glVertex3f(-0.25, -0.2, -0.3);
    glVertex3f(-0.25,  0.3, -0.3);
    glVertex3f( 0.25,  0.3, -0.3);
    glVertex3f( 0.25, -0.2, -0.3);
    glColor3f(0.0,0.0,0.0) # Amarelo

    #Top Face
    glNormal3f(0,1,0);
    glVertex3f(-0.3,  0.2, -0.8);
    glVertex3f(-0.3,  0.2,  0.8);
    glVertex3f( 0.3,  0.2,  0.8);
    glVertex3f( 0.3,  0.2, -0.8);
    # Top Face Teto
    glColor3f(0.5,0.0,0.0) # Vermelho
    glNormal3f(0,1,0);
    glVertex3f(-0.25,  0.3, -0.3);
    glVertex3f(-0.25,  0.3,  0.3);
    glVertex3f( 0.25,  0.3,  0.3);
    glVertex3f( 0.25,  0.3, -0.3);
    glColor3f(0.0,0.0,0.0) # Amarelo
    #Bottom Face
    glNormal3f(0,-1,0);
    glVertex3f(-0.3, -0.2, -0.8);
    glVertex3f( 0.3, -0.2, -0.8);
    glVertex3f( 0.3, -0.2,  0.8);
    glVertex3f(-0.3, -0.2,  0.8);
    # Right face
    glNormal3f(1,0,0);
    glVertex3f( 0.3, -0.2, -0.8);
    glVertex3f( 0.3,  0.2, -0.8);
    glVertex3f( 0.3,  0.2,  0.8);
    glVertex3f( 0.3, -0.2,  0.8);
    # Right face Teto
    glNormal3f(1,0,0);
    glColor3f(0.5,0.0,0.0) # Vermelho
    glVertex3f( 0.25, -0.2, -0.3);
    glVertex3f( 0.25,  0.3, -0.3);
    glVertex3f( 0.25,  0.3,  0.3);
    glVertex3f( 0.25, -0.2,  0.3);
    
    glColor3f(0.0,0.0,0.0) # Amarelo
    # Left Face
    glNormal3f(-1,0,0);
    glVertex3f(-0.3, -0.2, -0.8);
    glVertex3f(-0.3, -0.2,  0.8);
    glVertex3f(-0.3,  0.2,  0.8);
    glVertex3f(-0.3,  0.2, -0.8);
    
    # Left Face Teto
    glNormal3f(-1,0,0);
    glColor3f(0.5,0.0,0.0) # Vermelho
    glVertex3f(-0.25, -0.2, -0.3);
    glVertex3f(-0.25, -0.2,  0.3);
    glVertex3f(-0.25,  0.3,  0.3);
    glVertex3f(-0.25,  0.3, -0.3);
    glEnd();


# **********************************************************************
# DesenhaCubos()
# Desenha o cenario
#
# **********************************************************************
def DesenhaCubo():
    glutSolidCube(1)
    
def PosicUser():
    global observador, alvo, carro, camera
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Seta a viewport para ocupar toda a janela
    # glViewport(0, 0, 500, 500)
    #print ("AspectRatio", AspectRatio)
    
    if camera == 0:
        gluPerspective(60,AspectRatio,0.01,100) # Projecao perspectiva
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(observador.x, observador.y, observador.z, alvo.x, alvo.y, alvo.z, 0,1.0,0)
    elif camera == 1:
        gluPerspective(60,AspectRatio,0.01,100) # Projecao perspectiva
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        vetor_aux = alvo.__sub__(carro)
        vetor_aux = vetor_aux.__mul__(0.01)
        
        gluLookAt((carro.__add__(vetor_aux)).x, (carro.__add__(vetor_aux)).y, (carro.__add__(vetor_aux)).z, alvo.x, alvo.y, alvo.z, 0,1.0,0)
    else:
        gluPerspective(90,AspectRatio,0.01,200) # Projecao perspectiva
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0, 45, 0, -0.01, 0, 0, 0,1.0,0)
        
        

# **********************************************************************
# void DesenhaLadrilho(int corBorda, int corDentro)
# Desenha uma cÃ©lula do piso.
# O ladrilho tem largula 1, centro no (0,0,0) e estÃ¡ sobre o plano XZ
# **********************************************************************
def DesenhaLadrilho():
    glColor3f(1,1,1) # desenha QUAD preenchido
    glBegin ( GL_QUADS )
    glNormal3f(0,1,0)
    glTexCoord(0,0)
    glVertex3f(0,  0.0, 0)
    glTexCoord(0,1)
    glVertex3f(0,  0.0,  3)
    glTexCoord(1,1)
    glVertex3f( 3,  0.0,  3)
    glTexCoord(1,0)
    glVertex3f( 3,  0.0, 0)
    glEnd()
    
    glColor3f(1,1,1) # desenha a borda da QUAD 
    glBegin ( GL_LINE_STRIP )
    glNormal3f(0,1,0)
    glVertex3f(0,  0.0, 0)
    glVertex3f(0,  0.0,  3)
    glVertex3f( 3,  0.0,  3)
    glVertex3f( 3,  0.0, 0)
    glEnd()
    
# **********************************************************************
def DesenhaPiso():
    glPushMatrix()
    glTranslated(-45,-1,-45)
    aux = 0
    for x in matriznp:
        glPushMatrix()
        aux2 = 0
        for y in x:
            if y==0:
                for p in posicoesPredios:
                    if p[0] == aux and p[1] == aux2:
                        DesenhaPredio(p[2])
                UseTexture(5)
            else:
                for p in posicoesGasolina:
                    if p[1] == aux and p[0] == aux2:
                        glColor3f(0.5,0.0,0.0) # Vermelho
                        glPushMatrix()
                        glTranslatef(1,1,1)
                        glRotatef(Angulo,0,1,0)
                        DesenhaCubo()
                        glPopMatrix()
                UseTexture(y-1)
            DesenhaLadrilho()
            glTranslated(3, 0, 0)
            aux2 += 1
        glPopMatrix()
        glTranslated(0, 0, 3)
        aux += 1
    glPopMatrix()       
    
def rotateVertex(origin, point, angle):

    ox = origin.x
    oz = origin.z
    px = point.x
    pz = point.z

    angulo = math.radians(angle)

    qx = ox + math.cos(angulo) * (px - ox) - math.sin(angulo) * (pz - oz)
    qz = oz + math.sin(angulo) * (px - ox) + math.cos(angulo) * (pz - oz)
    
    point.x = qx
    point.z = qz
    

def rotaAlvo(angulo):
    global carro, alvo
    rotateVertex(carro, alvo, angulo)
    rotaObs()


def rotaObs():
    global observador, carro, alvo
    vetor_aux = alvo.__sub__(carro)
    observador = carro.__sub__(vetor_aux)
    observador.y = 2
    
def andaCarro():
    global carro, alvo, observador, matriznp, contadorCombustivel
    
    vetor_aux = (alvo.__sub__(carro)).__mul__(0.2)
    
    auxX = math.floor(((carro.__add__(vetor_aux)).x)/3)
    auxZ = math.floor(((carro.__add__(vetor_aux)).z)/3)
    i = 0

    xMatriz = auxX + 15
    zMatriz = auxZ + 15
    
    if zMatriz > 29 or xMatriz > 29 or zMatriz < 0 or xMatriz < 0:
        return
    elif matriznp[zMatriz][xMatriz] == 0:
        return
    for p in posicoesGasolina:
        if p[0] == xMatriz and p[1] == zMatriz:
            posicoesGasolina.pop(i)
            contadorCombustivel+=175
        i+=1
    if contadorCombustivel<=0:
        return
    
    vetor_aux = alvo.__sub__(carro)
    vetor_aux = vetor_aux.__mul__(0.05)
    carro = carro.__add__(vetor_aux)
    alvo = alvo.__add__(vetor_aux)
    vetor_aux2 = alvo.__sub__(carro)
    observador = carro.__sub__(vetor_aux2)
    observador.y = 2
    contadorCombustivel-=1
    print(contadorCombustivel)
    
leMatriz()
# **********************************************************************
# display()
# Funcao que exibe os desenhos na tela
#
# **********************************************************************
def display():
    global carro, observador, alvo, Angulo, rotaCarro
    # Limpa a tela com  a cor de fundo
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    DefineLuz()
    PosicUser()

    glMatrixMode(GL_MODELVIEW)
    
    glPushMatrix()
    glTranslatef(carro.x,carro.y,carro.z)
    glRotatef(rotaCarro,0,1,0)
    DesenhaCarro()
    glPopMatrix()
    
     
    DesenhaPiso()

    UseTexture(-1)
    
    if flagAnda:
        andaCarro()
    
    glPushMatrix()
    glTranslatef ( -1, 5, -8 )
    glRotatef(0,0,0,1)
    glColor3f(1,0,0)
    ExibeObjeto()
    glPopMatrix()

    glPushMatrix()
    glTranslatef ( -10, 5, -5 )
    glRotatef(0,0,0,1)
    glColor3f(1,0,0)
    ExibeObjeto()
    glPopMatrix()

    glPushMatrix()
    glTranslatef ( 15, 5, 6 )
    glRotatef(0,0,0,1)
    glColor3f(1,0,0)
    ExibeObjeto()
    glPopMatrix()

    glPushMatrix()
    glTranslatef ( -10, 5, 8 )
    glRotatef(0,0,0,1)
    glColor3f(1,0,0)
    ExibeObjeto()
    glPopMatrix()

    #glColor3f(0.5,0.0,0.0) # Vermelho
    # glPushMatrix()
    # glTranslatef(0,1,0)
    # glRotatef(Angulo,0,1,0)
    # DesenhaRetangulo(3)
    # glPopMatrix()
    
    # glColor3f(0.5,0.5,0.0) # Amarelo
    # glPushMatrix()
    # glTranslatef(2,0,0)
    # glRotatef(-Angulo,0,1,0)
    # #DesenhaCubo()
    # glPopMatrix()

    Angulo = Angulo + 1

    glutSwapBuffers()


# **********************************************************************
# animate()
# Funcao chama enquanto o programa esta ocioso
# Calcula o FPS e numero de interseccao detectadas, junto com outras informacoes
#
# **********************************************************************
# Variaveis Globais
nFrames, TempoTotal, AccumDeltaT = 0, 0, 0
oldTime = time.time()

def animate():
    global nFrames, TempoTotal, AccumDeltaT, oldTime

    nowTime = time.time()
    dt = nowTime - oldTime
    oldTime = nowTime

    AccumDeltaT += dt
    TempoTotal += dt
    nFrames += 1
    
    if AccumDeltaT > 1.0/30:  # fixa a atualizaÃ§Ã£o da tela em 30
        AccumDeltaT = 0
        glutPostRedisplay()

    

# **********************************************************************
#  keyboard ( key: int, x: int, y: int )
#
# **********************************************************************
ESCAPE = b'\x1b'
def keyboard(*args):
    global image, camera, flagAnda
    #print (args)
    # If escape is pressed, kill everything.
    
    if args[0] == ESCAPE:   # Termina o programa qdo
        os._exit(0)     
        # a tecla ESC for pressionada
    if args[0] == b'k' or args[0] == b'K':   # Termina o programa qdo
        #os._exit(0)         # a tecla ESC for pressionada
        if camera == 0:
            camera = 1
        elif camera == 1:
            camera = 2
        else:
            camera = 0
            
    if args[0] == b' ':
        flagAnda = not(flagAnda)

    if args[0] == b'i':
        image.show()
        print("OLA")
    
    # ForÃ§a o redesenho da tela
    glutPostRedisplay()

# **********************************************************************
#  arrow_keys ( a_keys: int, x: int, y: int )   
# **********************************************************************

def arrow_keys(a_keys: int, x: int, y: int):
    global rotaCarro

    if a_keys == GLUT_KEY_UP:         # Se pressionar UP
        pass
    if a_keys == GLUT_KEY_DOWN:       # Se pressionar DOWN
        pass
    if a_keys == GLUT_KEY_LEFT:       # Se pressionar LEFT
        rotaAlvo(-15)
        rotaCarro += 15
    if a_keys == GLUT_KEY_RIGHT:      # Se pressionar RIGHT
        rotaAlvo(15)
        rotaCarro += -15
    glutPostRedisplay()



def mouse(button: int, state: int, x: int, y: int):
    glutPostRedisplay()

def mouseMove(x: int, y: int):
    glutPostRedisplay()

# ***********************************************************************************
# Programa Principal
# ***********************************************************************************

glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA|GLUT_DEPTH | GLUT_RGB)
glutInitWindowPosition(0, 0)

# Define o tamanho inicial da janela grafica do programa
glutInitWindowSize(650, 500)
# Cria a janela na tela, definindo o nome da
# que aparecera na barra de tÃ­tulo da janela.
glutInitWindowPosition(100, 100)
wind = glutCreateWindow("OpenGL 3D")

# executa algumas inicializaÃ§Ãµes
init ()

# Define que o tratador de evento para
# o redesenho da tela. A funcao "display"
# serÃ¡ chamada automaticamente quando
# for necessÃ¡rio redesenhar a janela
glutDisplayFunc(display)
glutIdleFunc (animate)

# o redimensionamento da janela. A funcao "reshape"
# Define que o tratador de evento para
# serÃ¡ chamada automaticamente quando
# o usuÃ¡rio alterar o tamanho da janela
glutReshapeFunc(reshape)

# Define que o tratador de evento para
# as teclas. A funcao "keyboard"
# serÃ¡ chamada automaticamente sempre
# o usuÃ¡rio pressionar uma tecla comum
glutKeyboardFunc(keyboard)
    
# Define que o tratador de evento para
# as teclas especiais(F1, F2,... ALT-A,
# ALT-B, Teclas de Seta, ...).
# A funcao "arrow_keys" serÃ¡ chamada
# automaticamente sempre o usuÃ¡rio
# pressionar uma tecla especial
glutSpecialFunc(arrow_keys)

#glutMouseFunc(mouse)
#glutMotionFunc(mouseMove)


try:
    # inicia o tratamento dos eventos
    glutMainLoop()
except SystemExit:
    pass
