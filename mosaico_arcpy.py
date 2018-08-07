# q necesita hacer
# 1 crear mosaico imagenes     SI
# 2 elegir subset imagenes     SI
# 3 cortar por extension       SI
# 4 guardar                    SI

## procesamiento en arcpy
## Diccionarios necesarios para procesamiento
import arcpy  # necesario procesamiento en ARCPY
from arcpy import env  # no recuerdo, pero ejemplos de arcpy siempre lo llaman
from arcpy.sa import *  # diccionario procesamiento
from glob import glob  # necesario para busqueda de HDF
import os, errno  # necesario para el directorio de salida

## comprobacion de que se encuentre disponible el paquete espacial
## de Arcgis para procesar
arcpy.env.overwriteOutput = True  # sobre estricura
# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

## Variables a modificar dentro del script
## LIST: MO11A1 MOD11A2 MOD13Q1 MOD13A2 MOD09A1
imgMOD = 'MOD13Q1'  # imagen a procesar
## SUBSET A OBTENER!! parten en 0, no muy claro como los toma arcgis.
## MOD11A1:
## MOD11A2:
## MOD13Q1: 1 2
## MOD13A2:
## MOD09A1:
imgSET = "1"  # producto a obtener de los dato
entDIR = ('H:\\' + imgMOD)  # ubicacion de las imagenes
salDIR = ('D:\\version00\\' + imgMOD + '.SUBSET-' + str(imgSET).zfill(
    2) + '\\')  # directorio donde se guarda la imagen procesada
tmpDIR = ("D:\\TEMP\\")  # directorio temporal de procesamiento

## Prueba si existe el directorio de salida, sino lo crea.
try:
    os.makedirs(salDIR)
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

clGEO = ('D:\\fanr\\fneira@renare.uchile.cl\\!!entre_drive\\R\\MODIS\\SHP\\clGEO.shp')

agno = range(2000, 2018)  # rango de a?s a procesar
dias = range(1, 366)  # dias a procesar
# dias = range(166,168)

## PATHs de imagenes
# path = ["h11v10","h11v11","h11v12","h12v10","h12v11","h12v12","h12v13","h13v10", "h13v11","h13v12","h13v13","h13v14","h14v10","h14v11","h14v14"]

## COORDENADAS espaciales de salida, en este caso geograficas.
## solo queda chequear si esta correcta completamente, por el tema de las transformaciones
projCOR = "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]"

## Ciclo de procesamiento de las imagenes
for y in agno:
    ## Subciclo de dias de la imagen
    for d in dias:
        ## Listado MODIS, siguiendo patron
        ## MOD11A1.A2001001.h11v10.006.2015111170802.hdf
        HDF = glob(entDIR + '\\' + imgMOD + '.A' + str(y) + str(d).zfill(3) + '.??????.' + '006.' + '*.hdf')

        ## Condicion de procesamiento de datos existentes
        if HDF != []:
            ## Nombre archivo salida
            salMOD = imgMOD + '.' + str(y) + str(d).zfill(3) + '.SUBSET-' + str(imgSET).zfill(2) + '.tif'

            ## F(x) de mosaico arcpy, creo que se puede "abreviar en terminos"
            arcpy.MosaicToNewRaster_management(input_rasters=HDF,  # datos entrada
                                               output_location=tmpDIR,  # directorio salida
                                               raster_dataset_name_with_extension=salMOD,  # nombre salida
                                               coordinate_system_for_the_raster=projCOR,  # coordenadas salida
                                               pixel_type="64_BIT",
                                               # The bit depth, or radiometric resolution of the mosaic dataset A 64-bit data type supporting decimals.
                                               cellsize="",
                                               number_of_bands=imgSET,  # producto a procesar
                                               mosaic_method="BLEND",
                                               # las ?eas superpuestas son una combinaci? de los valores de celda que se superponen; el valor superpuesto depende de un algoritmo que est?basado en la distancia entre las celdas y en el borde dentro del ?ea superpuesta, y que depende de estos dos valores.
                                               mosaic_colormap_mode="MATCH")  # MATCH

            outExtractByMask = ExtractByMask((tmpDIR + salMOD), clGEO)
            outExtractByMask.save(salDIR + salMOD)

            ## Muestra dia procesado
            print(str(y) + '.' + str(d).zfill(3))
        else:
            print('SIN DATO ' + str(y) + '.' + str(d).zfill(3))

##==================================
##Mosaic To New Raster
##Usage: MosaicToNewRaster_management inputs;inputs... output_location raster_dataset_name_with_extension
##                                    {coordinate_system_for_the_raster} 8_BIT_UNSIGNED | 1_BIT | 2_BIT | 4_BIT
##                                    | 8_BIT_SIGNED | 16_BIT_UNSIGNED | 16_BIT_SIGNED | 32_BIT_FLOAT | 32_BIT_UNSIGNED
##                                    | 32_BIT_SIGNED | | 64_BIT {cellsize} number_of_bands {LAST | FIRST | BLEND  | MEAN
##                                    | MINIMUM | MAXIMUM} {FIRST | REJECT | LAST | MATCH}

