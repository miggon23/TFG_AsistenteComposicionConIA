import json

class ModeState:

    tematica = 8
    tematica_pistas = [0,1,2,3,4,5,6]
    tematicas_aleatorias = False
    mezclar_tematicas = False
    mezclar_melodias  = True
    semitonos = 3
    reverb = True
    entorno = 0
    lofi = False
    retro = True
    agua = False
    espacial = False
    dream = False
    vintage = False

    # Devuelve una cadena con el formato JSON listo para guardar
    def toJSON(self):
        jsonMap = {
            "tematica": self.tematica,
            "tematica_pistas": self.tematica_pistas,
            "tematicas_aleatorias": self.tematicas_aleatorias,
            "mezclar_tematicas": self.mezclar_tematicas,
            "mezclar_melodias": self.mezclar_melodias,
            "semitonos": self.semitonos,
            "reverb": self.reverb,
            "entorno": self.entorno,
            "lofi": self.lofi,
            "retro": self.retro,
            "agua": self.agua,
            "espacial": self.espacial,
            "dream": self.dream,
            "vintage": self.vintage
        }
   
        return jsonMap

    # Método "estático" de la clase que devuelve una nueva instancia de la clase a partir del JSON
    @classmethod
    def fromJSON(cls, jsonPath):

        with open(jsonPath, "r") as archivo:    
            json_data = json.load(archivo)

        print(json_data)
        # Reconstruye la clase a partir del JSON
        instance = cls()
        for key, value in json_data.items():
            setattr(instance, key, value)
        return instance

        

 