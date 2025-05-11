Título: YummyChecker - Análisis de Sobras de Comida en Platos

Descripción:
YummyChecker es una aplicación que permite analizar cuánta comida ha dejado un cliente en el plato después de comer, comparando la imagen del plato antes y después. La idea principal es determinar, basándose en el área de la comida restante, cuánto le gustó la comida a un cliente.

La aplicación utiliza técnicas de procesamiento de imágenes, como la conversión a escala de grises, el desenfoque y la segmentación, para calcular el área de la comida que quedó en el plato y compararla con el área de la comida antes de empezar a comer.

Instrucciones de uso:
1. Coloca una imagen del plato antes de que el cliente empiece a comer en la carpeta 'ImgDeReferencia'. Esta carpeta debe contener **exactamente una imagen**.
2. Coloca las imágenes del plato después de que el cliente haya terminado de comer en la carpeta 'ImgParaComparar'. Esta carpeta puede contener una o más imágenes.
3. Asegúrate de que las imágenes estén en formato `.jpg` o `.png`.
4. Ejecuta el programa. El programa analizará cada imagen de comparación, calculará el porcentaje de comida restante y mostrará un análisis de cuánto le gustó la comida al cliente.

Resultados:
- El programa mostrará el porcentaje de comida restante en cada imagen comparada.
- Interpretará el resultado en función de la cantidad de comida que queda (por ejemplo, "Le encantó la comida" o "No le gustó").
- Finalmente, calculará la media del porcentaje de comida restante en todos los platos.

