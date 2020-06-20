class PizzaEntregadaEvent:
   
   def __init__ (self,hora, camioneta, pizza):
       self.camioneta = camioneta
       self.pizza = pizza
       self.hora = hora
