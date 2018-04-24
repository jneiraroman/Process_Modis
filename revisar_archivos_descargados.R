#[EN] This script was created to check the downloaded files of MODIS products in a 
#folder and then check downloaded files for missing images

#[ES] Este script fue creado para revisar las imangenes descargas de Modis en una 
#carpeta y luego descargar las imagenes faltantes

#[EN] Load libraries
#[ES] Carga librerias
library(dplyr)

#[EN] Set Working directory, set up for test in different computers without change the code
#[ES] Establecer directorio de trabajo, en mas de un pc de trabajo

windir <- 'C:\\MODIS'
lindir <- '/home/casa/'
workdir<- ifelse(dir.exists(file.path('C:\\MODIS')),windir,lindir)

setwd(workdir)

#[EN] create a list of the names of the  files that match with hdf extension on the 
#working directory 
#[ES] Crea una lista de los nombres de los archivos que tienen la extensión HDF y se 
#encuentran en la carpeta de trabajo
files <- list.files(pattern = "hdf$")

#[EN] use the list as datafrme, then split values of the year, day, h and v that are
#[ES] 
test2=data.frame(año =substr(files, 10, 13), dia=substr(files, 14, 16), h= substr(files,19,20),  v=substr(files,22,23))

#[EN] change the julian day value to normal date as string
#[ES] cambia dia juliano por fecha normal como una cadena

fecha <- as.Date( as.integer(trimws(test2$dia)), 
                  origin=as.Date(paste(as.character(trimws(test2$año)),'-01-01',sep='')))


#test=data.frame(año=rep(2001:2004, each=365), dia=rep(001:365, each=8),h=c(11,11,11,12,12,13,13,14),v=c(10,11,12,12,13,13,14,14))

#Create a dataframe whit the expected files in which each columns is a factor, that way it will match with the 
#[EN]  structure of the dataframe test2. To check the struture of the dataframes use:
#
#str(test1) 
# 
#
#test1=data.frame(año=rep(2004:2004, each=365), dia=rep(sprintf('%0.3d', 1:365),each=8),h=c(11,11,11,12,12,13,13,14),v=c(10,11,12,12,13,13,14,14))

test1=data.frame(año=as.factor(rep(2004:2004, each=365)), dia=as.factor(rep(sprintf('%0.3d', 1:365),each=8)),h=as.factor(c(11,11,11,12,12,13,13,14)),v=as.factor(c(10,11,12,12,13,13,14,14)))

#[EN] Use these two lines if you want to check the integrity of the created dataframes
#test
#test2


#[EN] To determinate the left excluding join (compare both dataframes and check if they has the same rows, 
#the rows that there ins't in both tables are save in the "a" object)
a=setdiff(test1,test2)
b=anti_join(test1,test2)

#saving the a object in a csv file

date_info <- with(a, paste(año, dia))
strptime(date_info, "%Y %j")
as.Date(a$dia, origin= "2004-01-01")

strptime(paste(a$año, a$dia), format="%Y %j")


#para descargar los archivos modis 
library(RCurl)
library(rts)



#muestro productos version 6
#modisProducts(version=6)



#[EN]  First, you need to register on https://urs.earthdata.nasa.gov/ and get a username and password
# for the first time, set the authentication info:



setNASAauth(username='jneira',password='Casa3645',update = T)


#lugar donde guardare imagenes, me posiciono antes de la descarga

setwd("C:\\MODIS")



#defino x = producto de la version 6

x='MOD11A1'
i=1


#[EN] loop to download missing images
while(i <= 2) {
  ModisDownload(x=x,h=a[i,3],v=a[i,4],dates='2004.01.31', mosaic = FALSE, proj = FALSE, version = "006")
  i=i+1
}

