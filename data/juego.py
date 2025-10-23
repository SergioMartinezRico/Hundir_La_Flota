import utils as ut
print ("===============================================")
print ("==============  HUNDIR LA FLOTA  ==============")
print ("===============================================")
tipo_juego = input("¿Quiere jugar una partida o una demo? Introduzca Partida o Demo")
jugar = False
while jugar == False:
  if tipo_juego == "Partida":
    ut.jugar_partida()
    jugar = True
  elif tipo_juego == "Demo":
    ut.jugar_demo()
    jugar = True
  else:
    tipo_juego = input ("Entrada erronea. Introduzca Partida o Demo")
    jugar = False
