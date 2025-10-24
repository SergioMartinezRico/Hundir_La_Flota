import utils as ut
print ("\n🚢🌊⚓️==================================================⚓️🌊🚢")
print ("==================    HUNDIR LA FLOTA    ==================")
print ("==================  ¡A LA BATALLA NAVAL! ⚔️  ==================")
print ("🚢🌊⚓️==================================================⚓️🌊🚢\n")

tipo_juego = input("¿Quiere jugar una partida o una demo? Introduzca Partida o Demo:  ")
jugar = False
while jugar == False:
  if tipo_juego.lower() == "partida":
    ut.jugar_partida()
    jugar = True
  elif tipo_juego.lower() == "demo":
    ut.jugar_demo()
    jugar = True
  else:
    tipo_juego = input ("Entrada erronea. Introduzca Partida o Demo:  ")
    jugar = False
