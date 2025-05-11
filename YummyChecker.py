import os
import cv2
import numpy as np
from dotenv import load_dotenv
import matplotlib.pyplot as plt


def fVisualizarSegmentacion(oImgOriginal, oImgThresh, oImgContornos):
    # Dibujar los contornos sobre la imagen original
    oImgConContornos = oImgOriginal.copy()
    cv2.drawContours(oImgConContornos, oImgContornos, -1, (0, 255, 0), 2)  # Color verde para los contornos
    
    # Mostrar la imagen original, la imagen binaria y la imagen con contornos
    plt.figure(figsize=(10, 5))
    
    plt.subplot(1, 3, 1)
    plt.imshow(cv2.cvtColor(oImgOriginal, cv2.COLOR_BGR2RGB))
    plt.title('Imagen Original')

    plt.subplot(1, 3, 2)
    plt.imshow(oImgThresh, cmap='gray')
    plt.title('Imagen Umbralizada')

    plt.subplot(1, 3, 3)
    plt.imshow(cv2.cvtColor(oImgConContornos, cv2.COLOR_BGR2RGB))
    plt.title('Imagen con Contornos')

    plt.show()



def fPreprocesarImagen(sImagen):
    # Esta función convierte la imagen a escala de grises y la suaviza para reducir el ruido.
    # Cargar la imagen
    oImg = cv2.imread(sImagen)

    # Verificar si la imagen se ha cargado correctamente
    if oImg is None:
        raise FileNotFoundError(f"No se pudo cargar la imagen en la ruta: {sImagen}")
    
    # Convertir a escala de grises
    oImgGray = cv2.cvtColor(oImg, cv2.COLOR_BGR2GRAY)

    # Aplicar desenfoque gaussiano para reducir ruido
    oImgBlurred = cv2.GaussianBlur(oImgGray, (5, 5), 0)
    return oImg, oImgBlurred



def fSementarComida(oImgBlurred):
    # Esta función usa el umbral adaptativo para segmentar la comida en la imagen
    _, oImgThresh = cv2.threshold(oImgBlurred, 150, 255, cv2.THRESH_BINARY_INV)
    # Encontrar contornos
    oImgContornos, _ = cv2.findContours(oImgThresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return oImgThresh, oImgContornos



def fCalcularAreaDeLaComida(oImgContornos):
    # Esta función calcula el área de los contornos de la comida que queda en el plato.
    iFoodArea = 0
    for oImgContorno in oImgContornos:
        iFoodArea += cv2.contourArea(oImgContorno)
    return iFoodArea



def fCompararPlatos(sImagenReferencia, lImagenesComparacion):
    # Preprocesar la imagen del plato antes de comer
    oImgReferencia_Original, oImgReferencia_Blurred = fPreprocesarImagen(sImagenReferencia)
    # Segmentar la comida en la imagen "antes"
    oImgReferencia_Thresh, oImgReferencia_Contornos = fSementarComida(oImgReferencia_Blurred)

    # Visualizar la segmentación en la imagen de referencia
    print(f"Visualizando la imagen de Referencia {sImagenReferencia}...")
    fVisualizarSegmentacion(oImgReferencia_Original, oImgReferencia_Thresh, oImgReferencia_Contornos)

    # Calcular el área de la comida en el plato "antes"
    iImgReferencia_FoodArea = fCalcularAreaDeLaComida(oImgReferencia_Contornos)

    # Lista para almacenar los resultados de cada imagen "después"
    lResultadoComida = []

    # Recorrer todas las imágenes de "después"
    for sImagenesComparacion in lImagenesComparacion:
        # Preprocesar la imagen del plato después de comer
        oImgComparacion_Original, oImgComparacion_Blurred = fPreprocesarImagen(sImagenesComparacion)
        # Segmentar la comida en la imagen "después"
        oImgComparacion_Thresh, oImgComparacion_Contornos = fSementarComida(oImgComparacion_Blurred)

        # Visualizar la segmentación en la imagen de comparación
        print(f"Visualizando la imagen de Comparación: {sImagenesComparacion}...")
        fVisualizarSegmentacion(oImgComparacion_Original, oImgComparacion_Thresh, oImgComparacion_Contornos)
        
        # Calcular el área de la comida en el plato "después"
        iImgComparacion_FoodArea = fCalcularAreaDeLaComida(oImgComparacion_Contornos)

        # Calcular la diferencia en el área de comida
        iRatioComidaRestante = (iImgComparacion_FoodArea / iImgReferencia_FoodArea) * 100

        lResultadoComida.append((sImagenesComparacion, iRatioComidaRestante))

    print(f'\n')

    return lResultadoComida



def fAnalizarPlatos(sImagenReferencia, lImagenesComparacion):
    lResultadoComida = fCompararPlatos(sImagenReferencia, lImagenesComparacion)
    
    # Lista para almacenar los valores de iRatioComidaRestante
    lRatioComidaRestante = []

    # Iterar sobre los resultados y mostrar la satisfacción por cada imagen "después"
    for sImagenesComparacion, iRatioComidaRestante in lResultadoComida:
        print(f"Análisis de {sImagenesComparacion}:")

        # Agregar el porcentaje a la lista de ratios
        lRatioComidaRestante.append(iRatioComidaRestante)
        
        # Interpretación del resultado
        if iRatioComidaRestante < 10:
            print(f"Le encantó la comida. Sólo quedó un {iRatioComidaRestante:.2f}% de la comida.")
        elif 10 <= iRatioComidaRestante < 30:
            print(f"Le gustó la comida. Quedó un {iRatioComidaRestante:.2f}% de la comida.")
        elif 30 <= iRatioComidaRestante < 50:
            print(f"Tal vez no le gustó tanto. Quedó un {iRatioComidaRestante:.2f}% de la comida.")
        else:
            print(f"No le gustó la comida. Quedó un {iRatioComidaRestante:.2f}% de la comida.")
        
        print('-' * 50)  # Separador entre cada análisis

    # Calcular la media de los iRatioComidaRestante
    if lRatioComidaRestante:
        lMediaRatioComidaRestante = sum(lRatioComidaRestante) / len(lRatioComidaRestante)
        print(f"Media del porcentaje de comida restante: {lMediaRatioComidaRestante:.2f}%")
    else:
        print("No se pudo calcular la media porque no hay resultados.")



def fObtenerRutaImagenes(sRutaImg):
    # Obtener todas las rutas de los archivos en la carpeta, filtrando solo archivos con extensión .jpg o .png
    sImagen = [os.path.join(sRutaImg, f) for f in os.listdir(sRutaImg) if f.endswith(('.jpg', '.png'))]
    return sImagen



def fYummyChecker():
    # Cargar el archivo .env
    load_dotenv()

    # Obtener la ruta desde el archivo .
    # Ruta de la carpeta "referencia" donde está la imagen del plato antes de comer
    sRUTA_IMG_DE_REFERENCIA = os.getenv('RUTA_IMG_DE_REFERENCIA')
     # Ruta de la carpeta "comparacion" donde están las imágenes después de comer
    sRUTA_IMG_PARA_COMPARAR = os.getenv('RUTA_IMG_PARA_COMPARAR')

    # Obtener la lista de imágenes en la carpeta "referencia"
    lImagenReferencia = fObtenerRutaImagenes(sRUTA_IMG_DE_REFERENCIA)
    # Obtener la lista de imágenes en la carpeta "comparacion"
    lImagenesComparacion = fObtenerRutaImagenes(sRUTA_IMG_PARA_COMPARAR)

    # Verificar que la carpeta "referencia" tenga exactamente una imagen
    if len(lImagenReferencia) != 1:
        print(f"Error: La carpeta 'referencia' debe contener exactamente 1 imagen, pero contiene {len(lImagenReferencia)}.")
        return
    
    # Verificar que la carpeta "comparacion" tenga al menos una imagen
    if len(lImagenesComparacion) == 0:
        print("Error: La carpeta 'comparacion' debe contener al menos 1 imagen.")
        return

    # Si las comprobaciones pasan, obtener la imagen de referencia y las de comparación
    sImagenReferencia = lImagenReferencia[0]  # Sólo hay una imagen de referencia

    # Ejecutar el análisis para todas las imágenes "después"
    fAnalizarPlatos(sImagenReferencia, lImagenesComparacion)


# Llama a esta función para ejecutar el análisis automáticamente
fYummyChecker()
