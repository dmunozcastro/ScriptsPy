# -*- coding: utf-8 -*-

import os
import xml.etree.ElementTree as ET

"""
# Definir archivos
archivo_a = 'C:/Workspace/01_mede/T_TID.txt'
archivo_b = 'C:/Workspace/01_mede/RIC_SEP_OCT_12_90_rep_III_2ppy.xtf'
archivo_salida = 'C:/Workspace/01_mede/RIC_SEP_OCT_12_90_rep_III_2ppy_mod.xtf'
"""
# Definir archivos
archivo_a = 'C:/Workspace/01_mede/prueba/tids.txt'
archivo_b = 'C:/Workspace/01_mede/prueba/IGAC_25126_mod.xtf'
archivo_salida = 'C:/Workspace/01_mede/prueba/IGAC_25126_mod_del.xtf'


# Definir tags a modificar
tagUE = ".//LADM_COL_V3_1.LADM_Nucleo.col_ueBaunit"
tagUC = ".//Modelo_Aplicacion_LADMCOL_RIC_V0_1.RIC.RIC_UnidadConstruccion"
tagCUC = ".//Modelo_Aplicacion_LADMCOL_RIC_V0_1.RIC.RIC_CaracteristicasUnidadConstruccion"
tagRCUC = ".//ric_caracteristicasunidadconstruccion"
tagRUC = ".//ric_construccion"

# Abrir el archivo de texto con los identificadores
with open(archivo_a, 'r') as f:
    identificadores = f.read().splitlines()

# Abrir el archivo XML original
tree = ET.parse(archivo_b)
root = tree.getroot()

# Buscar y eliminar los elementos coincidentes con base en los identificadores del archivo a
for identificador in identificadores:
    # Buscar y eliminar los elementos coincidentes en terrno y construccion con base en los identificadores del archivo a
    for elem in root.findall(".//*[@TID='" + identificador + "']"):
        elem.clear
        root.remove(elem)
        print(f"Identificador '{identificador}' encontrado en '{elem}' y eliminado.")
    # Buscar y eliminar los elementos coincidentes en uebaunit con base en los identificadores del archivo a
    for elem in root.findall(tagUE):
        for subel in elem.findall(".//*[@REF='" + identificador + "']"):
            elem.clear
            root.remove(elem)
            print(f"Identificador '{identificador}' encontrado en '{elem}' y eliminado.")
    # Buscar y eliminar los elementos coincidentes en unidad de construccion con base en los identificadores del archivo a
    for elem in root.findall(tagUC):
        etid_cuc = None
        #print(f"tid_cuc relacionado = '{tid_cuc}'")
        for subel in elem.findall(".//*[@REF='" + identificador + "']"):
            etid_cuc = elem.find(tagRCUC)
            tid_cuc = etid_cuc.get('REF')
            tid_uc = elem.get('TID')
            elem.clear
            root.remove(elem)
            print(f"Identificador '{tid_uc}', tid_cuc = '{tid_cuc}' y tid_c = '{identificador}' encontrado en '{elem}' y eliminado.")
            # Buscar los elementos coincidentes en unidad de construccion en uebaunit y borrarlos
            for elem in root.findall(tagUE):
                for subel in elem.findall(".//*[@REF='" + tid_uc + "']"):
                    elem.clear
                    root.remove(elem)
                    print(f"Identificador '{tid_uc}' encontrado en '{elem}' y eliminado.")
        # Buscar y eliminar los elementos coincidentes en caracteristicas unidad de construccion con base en los identificadores del archivo a
        if etid_cuc is not None:
            #print(f"tid_cuc relacionado = '{tid_cuc}'")
            etid_uc = None
            for elem in root.findall(".//*[@TID='" + tid_cuc + "']"):
                elem.clear
                root.remove(elem)
                print(f"Identificador '{tid_cuc}' encontrado en '{elem} y eliminado.")
        else:
            pass
    
# escribir los datos actualizados en un nuevo archivo XML
tree.write(archivo_salida, encoding='utf-8', xml_declaration=True)