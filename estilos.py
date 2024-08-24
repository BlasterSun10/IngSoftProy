def dicc_colores(color):
    colores= {"negro":(0,0,0),
        "blanco":(255,255,255),
        "verde":(138, 249, 145),
        "azul":(51, 206, 255),
        "rojo":(239,71,71),
        "aqua":(116, 236, 228 ),
        "gris":(170, 180, 179)
        }

    return colores[color]

def drawcol(hoja,color):
    r,g,b = dicc_colores(color)
    hoja.set_draw_color(r,g,b)

def backcol(hoja,color):
    r,g,b = dicc_colores(color)
    hoja.set_fill_color(r,g,b)

def textcol(hoja,color):
    r,g,b = dicc_colores(color)
    hoja.set_text_color(r,g,b)

def text_size(hoja,size):
    hoja.set_font_size(size)