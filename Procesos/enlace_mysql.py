#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
from gi.repository import Gtk
import MySQLdb


class Database:
   def __init__(self,database,usuario=None,password=None):
       self.database_nombre=database

       self.conectada=False
       if usuario is not None:
           self.mysquser=usuario
       else:
           self.mysquser='root' #podemos poner el valor en la clase si va a ser siempre el mismo
       if password is not None:
           self.mysqpasw=password
       else:
           self.mysqpasw='aniremysql' #podemos poner el password por defecto, igual que el usuario
       self.conexion=None

   def conectar(self):
       try:
           self.conexion=MySQLdb.connect(host='localhost',user=self.mysquser,passwd=self.mysqpasw,db=self.database_nombre)
           self.conectada=True
           return self.conexion
       except:
           #error, sacamos dialogo y decimos que hagan configuracion
           md=gtk.MessageDialog(None,gtk.DIALOG_DESTROY_WITH_PARENT,
                       gtk.MESSAGE_ERROR,gtk.BUTTONS_CLOSE,"Error conectando a base de datos\n Compruebe configuracion\n o MySQL")
           md.run()
           md.destroy()
           return False

   def set_dbdatos(self,usuario=None,password=None):

       if usuario is not None:
           self.mysquser=usuario
       if password is not None:
           self.mysqpasw=password




class Tabla:



   def __init__(self,tabla,basedatos):
# los errores en valores de datos en el sql, no da error da warning, lo
# pasamos a error para poder trabajar con try: except:
       import warnings
       warnings.simplefilter("error")

       self.database=basedatos
       self.abierta=False
       self.tabla=tabla
       self.datos_tabla=[]
       self.widgets=[]
       self.descripcion_tabla=[]
       self.nombre_campos=[]
       self.tipo_campos=[]
       self.long_campos=[]
       self.num_campos=0
       self.num_lineas=0
       self.tablas_rel=[]
       self.campos_rel=[]
       self.estado='consultar'
       self.linea_actual=[]
       self.indexado=False
       self.indice=''
       self.abrir()



   def abrir(self):
       #abre la tabla
       res=self.abre_tabla()

       if res:
               self.datos_tabla=self.cursor.fetchall()
               self.num_lineas=len(self.datos_tabla)
               self.linea_actual=self.datos_tabla[0]
               self.linea_pos=0
               #num_campos lleva el numero de campos
               self.num_campos=len(self.cursor.description)
               for i in range(self.num_campos):
                   self.nombre_campos.append(self.cursor.description[i][0])
                   self.tipo_campos.append(self.cursor.description[i][1])
                   self.long_campos.append(self.cursor.description[i][3])

       #cerramos la tabla y la base de datos, y trabajamos con los
       #datos en la variable datos_tabla
       self.cierra_tabla()
       return res


   def abre_tabla(self):

       #conectamos la base de datos
       self.conn=self.database.conectar()
       self.cursor=self.conn.cursor()

       if self.database.conectada: #True si estamos conectados a la base de datos
           try:
               sql='select * from '+self.tabla
               if self.indexado:
                   sql=sql+' order by '+self.indice
               self.cursor.execute(sql)
               self.abierta=True
               result=True
           except:
               #error, sacamos dialogo y decimos que hagan configuracion
               md=gtk.MessageDialog(None,gtk.DIALOG_DESTROY_WITH_PARENT,
                       gtk.MESSAGE_ERROR,gtk.BUTTONS_CLOSE,"Error abriendo tabla\n Compruebe configuracion\n o MySQL")
               md.run()
               md.destroy()
               result=False
       else:
           #la base de datos no esta conectada
               #error, sacamos dialogo y decimos que hagan configuracion
               md=gtk.MessageDialog(None,gtk.DIALOG_DESTROY_WITH_PARENT,
                       gtk.MESSAGE_ERROR,gtk.BUTTONS_CLOSE,"Base de datos no abierta\n Compruebe configuracion\n o MySQL")
               md.run()
               md.destroy()
               result=False
       return result

   def cierra_tabla(self):
       self.cursor.close()
       self.conn.close()

   def set_indice(self,indexado,*indice):
       if indexado:
           self.indexado=True
           self.indice=indice[0]
           self.abrir()
       else:
           self.indexado=False

   def set_tabla(self,tabla):
       self.tabla=tabla
       self.abrir()

   def adelante(self,widget):
           # una fila adelante en la tabla.
           if self.linea_pos<self.num_lineas-1:
               self.linea_pos+=1
               self.linea_actual=self.datos_tabla[self.linea_pos]
               result=True
               if self.linea_pos==self.num_lineas-1:
                   result=False
               self.actualizar()
           else:
               #hemos alcanzado final tabla
               result=False
           return result

   def atras(self,widget):
           #una fila hacia atras, si es la primera, no cambia
           if self.linea_pos>0:
               self.linea_pos-=1
               self.linea_actual=self.datos_tabla[self.linea_pos]
               result=True
               if self.linea_pos==0:
                   result=False
               self.actualizar()
           else:
               #principio de tabla
               result=False
           return result

   def primero(self,widget):
           self.linea_pos=0
           self.linea_actual=self.datos_tabla[self.linea_pos]
           self.actualizar()
           return True

   def ultimo(self,widget):
           self.linea_pos=self.num_lineas-1
           self.linea_actual=self.datos_tabla[self.linea_pos]
           self.actualizar()
           return True

   def aplica_edicion(self):
       #aqui salvamos los datos editados
       #primero seleccionamos la fila de la tabla a cambiar
       #los datos sin editar estan en la variable linea_actual[]
       #hacemos el select con todos los campos, pues no sabemos
       #si hay dos lineas con campos iguales.
       #primero abrimos tabla
       #pero antes guardamos el puntero que llevabamos
       linea_antes=self.linea_pos
       self.abre_tabla()
       datos_antes=''
       for i in range(self.num_campos):
           campo=self.nombre_campos[i]
           dato=str(self.linea_actual[i])
           if dato!='' and dato!='None':
               datos_antes=datos_antes+campo+' = "'+dato+'" AND '
       datos_antes=str(datos_antes[0:len(datos_antes)-4])
       sql='select * from '+self.tabla+' where '+datos_antes
       try:
           self.cursor.execute(sql)
       except:
           #error, el registro a modificar tenia valores inconsistentes
           md=gtk.MessageDialog(None,gtk.DIALOG_DESTROY_WITH_PARENT,
                               gtk.MESSAGE_ERROR,gtk.BUTTONS_CLOSE,"Error en registro\n Debe arreglarlo desde\n Administrador MySQL\n")
           md.run()
           md.destroy()
           return False

       #una vez seleccionada la linea a modificar, comprobamos que es una
       # y solo una.
       if self.cursor.rowcount != 1:
           #error, sacamos dialogo y decimos que comprueben datos
           md=gtk.MessageDialog(None,gtk.DIALOG_DESTROY_WITH_PARENT,
                               gtk.MESSAGE_ERROR,gtk.BUTTONS_CLOSE,"Error al grabar datos\n Mas de un registro cambiado\n ")
           md.run()
           md.destroy()
           return False
       else:
           #correcto, anotamos los nuevos valores
           sql='update '+self.tabla+' set '
           for i in range(self.num_campos):
               campo=self.nombre_campos[i]
               dato=self.widgets[i].get_text()
               if dato!='':
                   if i<self.num_campos-1:
                       sql=sql+campo+' = "'+dato+'" , '
                   else:
                       sql=sql+campo+' = "'+dato+'"'
               else:
                   if i<self.num_campos-1:
                       sql=sql+campo+' = NULL, '
                   else:
                       sql=sql+campo+' = NULL'
           sql=sql+' where '+datos_antes
           try:
               self.cursor.execute(sql)
               #abrir abre la tabla, carga las datos en variables y cierra tabla
               self.abrir()
               #dejamos en pantalla el registro modificado
               self.linea_pos=linea_antes

               #quita el estado de edicion de los widgets
               self.estado_consulta()
               result=True
           except:
               #error, sacamos dialogo y decimos que comprueben datos
               md=gtk.MessageDialog(None,gtk.DIALOG_DESTROY_WITH_PARENT,
                                    gtk.MESSAGE_ERROR,gtk.BUTTONS_CLOSE,"Error al grabar datos\n Compruebe datos \n o Cancele")
               md.run()
               md.destroy()
               result=False

       return result

   def aplica_alta(self):
       #anota nuevo registro en la tabla
       #aqui salvamos los datos anotados
       #primero abrimos tabla

       self.abre_tabla()
       #correcto, anotamos los nuevos valores
       sql='insert into '+self.tabla+' values ( '
       vacio=True
       for i in range(self.num_campos):
           dato=self.widgets[i].get_text()
           if dato != '':
               vacio=False
               if i<self.num_campos-1:
                   sql=sql+'"'+dato+'" , '
               else:
                   sql=sql+'"'+dato+'" )'
           else:
               if i<self.num_campos-1:
                   sql += ' NULL, '
               else:
                   sql += ' NULL )'
       if vacio:
               #error, sacamos dialogo y decimos que comprueben datos
               md=gtk.MessageDialog(None,gtk.DIALOG_DESTROY_WITH_PARENT,
                                    gtk.MESSAGE_ERROR,gtk.BUTTONS_CLOSE,"No se puede guardar un\n Registro vacio\n")
               md.run()
               md.destroy()
               return False
       try:
           self.cursor.execute(sql)
           result=True
           self.abrir()
           self.estado_consulta()
       except:
           #error, sacamos dialogo y decimos que comprueben datos
           md=gtk.MessageDialog(None,gtk.DIALOG_DESTROY_WITH_PARENT,
                   gtk.MESSAGE_ERROR,gtk.BUTTONS_CLOSE,"Error al grabar datos\n Compruebe datos \n o Cancele")
           md.run()
           md.destroy()
           result=False
       return result


   def borrar(self):
       #primero seleccionamos la fila de la tabla a borrar
       #los datos estan en la variable linea_actual[]
       #hacemos el select con todos los campos, pues no sabemos
       #si hay dos lineas con campos iguales.
       #primero abrimos tabla
       #pero antes guardamos el puntero que llevabamos
       linea_antes=self.linea_pos
       self.abre_tabla()
       datos_antes=''
       for i in range(self.num_campos):
           campo=self.nombre_campos[i]
           dato=str(self.linea_actual[i])
           if dato!='' and dato!='None':
               datos_antes=datos_antes+campo+' = "'+dato+'" AND '
       datos_antes=str(datos_antes[0:len(datos_antes)-4])
       sql='select * from '+self.tabla+' where '+datos_antes
       try:
           self.cursor.execute(sql)

       except:
           #error, el registro a modificar tenia valores inconsistentes
           md=gtk.MessageDialog(None,gtk.DIALOG_DESTROY_WITH_PARENT,
                               gtk.MESSAGE_ERROR,gtk.BUTTONS_CLOSE,"Error en registro\n Debe arreglarlo desde\n Administrador MySQL\n")
           md.run()
           md.destroy()
           return False

       #una vez seleccionada la linea a borrar, comprobamos que es una
       # y solo una.
       if self.cursor.rowcount != 1:
           #error, sacamos dialogo y decimos que comprueben datos
           md=gtk.MessageDialog(None,gtk.DIALOG_DESTROY_WITH_PARENT,
                               gtk.MESSAGE_ERROR,gtk.BUTTONS_CLOSE,"Error al borrar registro\n Mas de un registro seleccionado\n ")
           md.run()
           md.destroy()
           return False
       else:
           #correcto, borramos la linea
           sql='delete from '+self.tabla+' where '+datos_antes

           try:
               self.cursor.execute(sql)
               #abrir abre la tabla, carga las datos en variables y cierra tabla
               self.abrir()
               #dejamos en pantalla el registro modificado
               self.linea_pos=linea_antes
               #quita el estado de edicion de los widgets
               self.estado_consulta()
               result=True
           except:
               #error, sacamos dialogo y decimos que comprueben datos
               md=gtk.MessageDialog(None,gtk.DIALOG_DESTROY_WITH_PARENT,
                                    gtk.MESSAGE_ERROR,gtk.BUTTONS_CLOSE,"Error al borrar registro\n Compruebe datos \n o Cancele")
               md.run()
               md.destroy()
               result=False

       return result

   def cancelar(self):
       puntero=self.linea_pos
       self.abrir()
       self.linea_pos=puntero
       self.linea_actual=self.datos_tabla[self.linea_pos]
       self.actualizar()
       self.estado_consulta()
       return

   def buscar(self,campo,valor):
       for n in range(self.num_campos):
           if campo==self.nombre_campos[n]:
               campo_index= n
       encontrado=False
       for n in range(len(self.datos_tabla)):
           if self.datos_tabla[n][campo_index]==valor:
               self.linea_actual=self.datos_tabla[n]
               encontrado=True
               self.actualizar()
               break
       return encontrado

   def actualizar(self):
           #isinstance(obj, int)
           for w in self.widgets:
               w.actualizar_widget()
           self.actualizar_datos_relacionada()
           return True

   def estado_consulta(self):
       #pone los widgets en estado de consulta
       self.estado='consultar'
       for w in self.widgets:
           w.set_editable(False)

   def estado_editar(self):
       #pone los widgets en estado de edicion
       self.estado='editar'
       for w in self.widgets:
           w.set_editable(True)

   def estado_alta(self):
       #pone los widgets en alta, en blanco
       self.estado='alta'
       for w in self.widgets:
           w.set_text('')
           w.set_editable(True)

   def widget_a_tabla(self,widget,campo):
           self.widgets.append(widget)
           result=-1
           for n in range(self.num_campos):
               if campo==self.nombre_campos[n]:
                   result= n

           return result

   def relacionar(self,campoprop,tablarel,camporel):
       #relaciona otra tabla con esta, recibe, campo propio
       #tabla esclava a relacionar, y campo de la tabla a relacionar
       result=-1
       for n in range(self.num_campos):
           if campoprop==self.nombre_campos[n]:
               result= n
               self.tablas_rel.append(tablarel)
               self.campos_rel.append(n)
               #envia a la tabla peticionaria, la identidad de esta tabla
               #y el campo de la peticionaria
               tablarel.relacionada(self,camporel)
       return result

   def relacionada(self,trelacion,camporel):
       self.camporel=camporel
       self.tablarelacion=trelacion

   def actualizar_datos_relacionada(self):
           for t in range(len(self.tablas_rel)):
               dato=self.linea_actual[self.campos_rel[t]]
               tabla=self.tablas_rel[t]
               tabla.actualizar_tabla(dato)
           return True
   def actualizar_tabla(self,dato):
       self.buscar(self.camporel,dato)




class DBLabel(Gtk.Label):
   #un label enlazado a una tabla y un campo de la misma
   def __init__(self,tabla,campo=None,orden=None,titular=False):
       #si no nos dan el campo, y se da el orden del campo,
       #campo=None y orden = n, posicion en la tabla de la columna
       #si titular=True, anteponemos el nombre del campo al label
       Gtk.Label.__init__(self)
       self.tabla=tabla
       self.titular=titular

       if campo is None:
           self.campo=self.tabla.nombre_campos[orden]
       else:
           self.campo=campo

       res=self.campo_index=tabla.widget_a_tabla(self,self.campo)
       if res==-1:
           #error, campo de tabla no encontrado
               md=gtk.MessageDialog(None,gtk.DIALOG_DESTROY_WITH_PARENT,
                                    gtk.MESSAGE_ERROR,gtk.BUTTONS_CLOSE,"Error, campo de tabla \n No existente \n")
               md.run()
               md.destroy()
       self.titulo=self.campo+' : '
       self.show()
       self.actualizar_widget()

   def set_titulo(self,titulo):
       #pone el nombre que deseemos en titulo, en lugar del nombre del campo
       self.titulo=titulo+' : '
       self.titular=True

   def actualizar_widget(self):

       texto=self.tabla.linea_actual[self.campo_index]
       if self.titular:
           texto=self.titulo+str(texto)
       self.set_text(str(texto))

class DBEntry(gtk.HBox):
   #un label enlazado a una tabla y un campo de la misma
   def __init__(self,tabla,campo=None,orden=None,titular=False):
       #si no nos dan el campo, y se da el orden del campo,
       #campo=None y orden = n, posicion en la tabla de la columna
       #si titular=True, anteponemos el nombre del campo al label
       gtk.HBox.__init__(self)
       self.set_size_request(500,40)
       self.set_homogeneous(False)
       self.entry=gtk.Entry()
       self.entry.set_editable(False)
       self.label=gtk.Label()
       self.pack_start(self.label,False,False,False)
       self.pack_end(self.entry,False,False,False)
       self.entry.show()
       self.label.show()
       self.show()
       self.tabla=tabla
       self.titular=titular
       if campo is None:
           self.campo=self.tabla.nombre_campos[orden]
       else:
           self.campo=campo
       #campo_index lleva el numero de campo en la tabla
       res=self.campo_index=tabla.widget_a_tabla(self,self.campo)
       if res==-1:
           #error, campo de tabla no encontrado
               md=gtk.MessageDialog(None,gtk.DIALOG_DESTROY_WITH_PARENT,
                                    gtk.MESSAGE_ERROR,gtk.BUTTONS_CLOSE,"Error, campo de tabla \n No existente \n")
               md.run()
               md.destroy()

       self.titulo=self.campo+' : '
       #poner anchura adaptada a la del campo
       ancho=tabla.long_campos[self.campo_index]
       self.entry.set_max_length(ancho)
       self.entry.set_width_chars(ancho)
       self.actualizar_widget()

   def set_titulo(self,titulo):
       #pone el nombre que deseemos en titulo, en lugar del nombre del campo
       self.titulo=titulo+' : '
       self.titular=True


   def set_editable(self,estado):
       self.entry.set_editable(estado)

   def get_text(self):
       return self.entry.get_text()

   def set_text(self,texto):
       self.entry.set_text(texto)

   def actualizar_widget(self):

       texto=self.tabla.linea_actual[self.campo_index]
       if self.titular:
               self.label.set_text(self.titulo+' : ')
               self.label.set_alignment(0,0.5)
       self.entry.set_text(str(texto))

class Navegador(gtk.HButtonBox):
   def __init__(self,tabla,main=None):
       #conjunto de botones para navegar y actuar sobre la tabla
       gtk.HButtonBox.__init__(self)
       self.main=main
       self.tabla=tabla
       self.estado='consultar'
       self.set_homogeneous(False)
       # METEMOS LOS BOTONES
       self.principio=gtk.Button('<<')
       self.add(self.principio)
       self.principio.connect_object("clicked", self.movimiento, self.principio)
       self.atras=gtk.Button('<')
       self.add(self.atras)
       self.atras.connect_object("clicked", self.movimiento, self.atras)
       self.delante=gtk.Button('>')
       self.add(self.delante)
       self.delante.connect_object("clicked", self.movimiento, self.delante)
       self.fin=gtk.Button('>>')
       self.add(self.fin)
       self.fin.connect_object("clicked", self.movimiento, self.fin)
       self.editar=gtk.Button('Editar')
       self.add(self.editar)
       self.editar.connect_object("clicked", self.control, self.editar)
       self.borrar=gtk.Button('Borrar')
       self.add(self.borrar)
       self.borrar.connect_object("clicked", self.control, self.borrar)
       self.alta=gtk.Button('Alta')
       self.add(self.alta)
       self.alta.connect_object("clicked", self.control, self.alta)
       self.aplicar=gtk.Button('Aplicar')
       self.add(self.aplicar)
       self.aplicar.connect_object("clicked", self.control, self.aplicar)
       self.cancelar=gtk.Button('Cancelar')
       self.add(self.cancelar)
       self.cancelar.connect_object("clicked", self.control, self.cancelar)
       if main is not None:
       #crea un toolbar en la ventana que contiene al navegador,
       #donde representamos el numero de registro visualizado.
           self.lestado=gtk.Label('inicio')
           labelitem=gtk.ToolItem()
           labelitem.add(self.lestado)
           self.toolb=gtk.Toolbar()
           self.toolb.insert(labelitem,0)
           main.vbox.pack_start(self.toolb,False,True)
           self.lestado.show()
           labelitem.show()
           self.toolb.show()

       self.atras.show()
       self.delante.show()
       self.principio.show()
       self.fin.show()
       self.editar.show()
       self.borrar.show()
       self.alta.show()
       self.show()
       self.actualizar_widget()

   def actualizar_widget(self):
       if self.tabla.linea_pos==0:
           #primera linea
           inicio=True
           fin=False
       elif self.tabla.linea_pos==len(self.tabla.datos_tabla)-1:
           #ultima linea
           fin=True
           inicio=False
       else:
           inicio=False
           fin=False
       if self.tabla.num_lineas==1:
           #solo hay un registro, ni palante ni patras
           inicio=True
           fin=True
       # oculta los botones que no estan operativos
       if self.estado != 'consultar':
           self.delante.hide()
           self.fin.hide()
           self.atras.hide()
           self.principio.hide()
           self.editar.hide()
           self.alta.hide()
           self.borrar.hide()
           self.aplicar.show()
           self.cancelar.show()
           self.cancelar.grab_focus()
           if self.main is not None:
               self.lestado.set_text('Record : '+str(self.tabla.linea_pos)+' estado : '+self.estado)
       else:
           self.delante.show()
           self.fin.show()
           self.atras.show()
           self.principio.show()
           self.editar.show()
           self.alta.show()
           self.borrar.show()
           self.aplicar.hide()
           self.cancelar.hide()

           if self.main is not None:
               self.lestado.set_text('Record : '+str(self.tabla.linea_pos))
           if inicio:
               self.atras.hide()
               self.principio.hide()
               # y anota en el label el numero de record mostrado
               if self.main is not None:
                   self.lestado.set_text('Record : '+str(self.tabla.linea_pos)+' Principio de fichero')
           if fin:
               self.delante.hide()
               self.fin.hide()
               if self.main is not None:
                   self.lestado.set_text('Record : '+str(self.tabla.linea_pos)+' Fin de fichero')

   def movimiento(self,widget):
       if widget==self.delante:
           self.tabla.adelante(widget)
       elif widget==self.atras:
           self.tabla.atras(widget)
       elif widget==self.principio:
           self.tabla.primero(widget)
       elif widget==self.fin:
           self.tabla.ultimo(widget)
       self.actualizar_widget()


   def control(self,widget):
       res=True
       if widget==self.editar:
           self.estado='editar'
           self.tabla.estado_editar()
       elif widget==self.alta:
           self.estado='alta'
           self.tabla.estado_alta()
       elif widget==self.borrar:
           self.tabla.estado='borrar'
           self.estado='borrar'
       elif widget==self.aplicar:
           if self.estado=='editar':
               #actualiza los datos en la tabla
               res=self.tabla.aplica_edicion()
               if res:
                   self.estado='consultar'
           elif self.estado=='alta':
               res=self.tabla.aplica_alta()
               if res:
                   self.estado='consultar'
           else:
               self.tabla.borrar()
               self.estado='consultar'

       elif widget==self.cancelar:
           self.tabla.cancelar()
           self.estado='consultar'
       if res:
           self.actualizar_widget()