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
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Ponto import Ponto
from Linha import Linha
#from PIL import Image
import time
import math

rotaCarro = 0
observador = Ponto(0,2,6)
carro = Ponto(0,-0.75,0)
alvo = Ponto(0,-0.75,-6)

Angulo = 0.0
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

    #image = Image.open("Tex.png")
    #print ("X:", image.size[0])
    #print ("Y:", image.size[1])
    #image.show()
    
   

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
    


    
    
def DesenhaRetangulo(altura: int):

    glBegin ( GL_QUADS );
    # Front Face
    glNormal3f(0,0,1);
    glVertex3f(-1, -1,  1);
    glVertex3f( 1, -1,  1);
    glVertex3f( 1,  altura,  1);
    glVertex3f(-1,  altura,  1);
    # Back Face
    glNormal3f(0,0,-1);
    glVertex3f(-1, -1, -1);
    glVertex3f(-1,  altura, -1);
    glVertex3f( 1,  altura, -1);
    glVertex3f( 1, -1, -1);
    # Top Face
    glNormal3f(0,1,0);
    glVertex3f(-1,  altura, -1);
    glVertex3f(-1,  altura,  1);
    glVertex3f( 1,  altura,  1);
    glVertex3f( 1,  altura, -1);
    # Bottom Face
    glNormal3f(0,-1,0);
    glVertex3f(-1, -1, -1);
    glVertex3f( 1, -1, -1);
    glVertex3f( 1, -1,  1);
    glVertex3f(-1, -1,  1);
    # Right face
    glNormal3f(1,0,0);
    glVertex3f( 1, -1, -1);
    glVertex3f( 1,  altura, -1);
    glVertex3f( 1,  altura,  1);
    glVertex3f( 1, -1,  1);
    # Left Face
    glNormal3f(-1,0,0);
    glVertex3f(-1, -1, -1);
    glVertex3f(-1, -1,  1);
    glVertex3f(-1,  altura,  1);
    glVertex3f(-1,  altura, -1);
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
    global observador, alvo, carro
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Seta a viewport para ocupar toda a janela
    # glViewport(0, 0, 500, 500)
    #print ("AspectRatio", AspectRatio)
    
    gluPerspective(60,AspectRatio,0.01,50) # Projecao perspectiva
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(observador.x, observador.y, observador.z, alvo.x, alvo.y, alvo.z, 0,1.0,0)

# **********************************************************************
# void DesenhaLadrilho(int corBorda, int corDentro)
# Desenha uma cÃ©lula do piso.
# O ladrilho tem largula 1, centro no (0,0,0) e estÃ¡ sobre o plano XZ
# **********************************************************************
def DesenhaLadrilho():
    glColor3f(0,0,1) # desenha QUAD preenchido
    glBegin ( GL_QUADS )
    glNormal3f(0,1,0)
    glVertex3f(-0.5,  0.0, -0.5)
    glVertex3f(-0.5,  0.0,  0.5)
    glVertex3f( 0.5,  0.0,  0.5)
    glVertex3f( 0.5,  0.0, -0.5)
    glEnd()
    
    glColor3f(1,1,1) # desenha a borda da QUAD 
    glBegin ( GL_LINE_STRIP )
    glNormal3f(0,1,0)
    glVertex3f(-0.5,  0.0, -0.5)
    glVertex3f(-0.5,  0.0,  0.5)
    glVertex3f( 0.5,  0.0,  0.5)
    glVertex3f( 0.5,  0.0, -0.5)
    glEnd()
    
# **********************************************************************
def DesenhaPiso():
    glPushMatrix()
    glTranslated(-20,-1,-10)
    for x in range(-20, 20):
        glPushMatrix()
        for z in range(-20, 20):
            DesenhaLadrilho()
            glTranslated(0, 0, 1)
        glPopMatrix()
        glTranslated(1, 0, 0)
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
    global carro, alvo, observador
    
    vetor_aux = alvo.__sub__(carro)
    vetor_aux = vetor_aux.__mul__(0.5)
    carro = carro.__add__(vetor_aux)
    alvo = alvo.__add__(vetor_aux)
    vetor_aux2 = alvo.__sub__(carro)
    observador = carro.__sub__(vetor_aux2)
    observador.y = 2
    

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
    glColor3f(0.5,0.0,0.0) # Vermelho
    glPushMatrix()
    glTranslatef(-2,0,0)
    glRotatef(Angulo,0,1,0)
    #DesenhaRetangulo(3)
    glPopMatrix()
    
    glColor3f(0.5,0.5,0.0) # Amarelo
    glPushMatrix()
    glTranslatef(2,0,0)
    glRotatef(-Angulo,0,1,0)
    #DesenhaCubo()
    glPopMatrix()

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
    global image
    #print (args)
    # If escape is pressed, kill everything.

    if args[0] == ESCAPE:   # Termina o programa qdo
        os._exit(0)         # a tecla ESC for pressionada

    if args[0] == b' ':
        init()

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
        andaCarro()
    if a_keys == GLUT_KEY_DOWN:       # Se pressionar DOWN
        pass
    if a_keys == GLUT_KEY_LEFT:       # Se pressionar LEFT
        rotaAlvo(10)
        rotaCarro += -10
    if a_keys == GLUT_KEY_RIGHT:      # Se pressionar RIGHT
        rotaAlvo(-10)
        rotaCarro += 10
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
