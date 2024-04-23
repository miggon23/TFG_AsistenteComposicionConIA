from PIL import Image, ImageTk
from App.AppEnums.tematicEnum import TematicEnum

def load_image(image):
    # Cargar la imagen original
    background_image_pil = Image.open("App/Images/Backgrounds/"+ image +".png")
    
    # Crear una instancia de ImageTk para la imagen original    
    #return ImageTk.PhotoImage(background_image_pil)
    return background_image_pil

class BackgroundSystem:
    backgroundPath = ""

    def __init__(self):
        self.img_map = {
            "dream": load_image("dream"),
            "lofi": load_image("lofi"),
            "espacial": load_image("espacial"),
            "vintage": load_image("vintage"),
            #completear con los checkboxes restantes
        }
        self.load_tematic_backgrounds()
        print(self.img_map)

    def load_tematic_backgrounds(self):
        i = 0
        for theme in TematicEnum:
            clave = theme.value
            route = "t" + str(i)
            valor = load_image(route)
            self.img_map[clave] = valor

            i += 1

    def configure_background(self, theme, dream, lofi, vintage, spacial): # Completar con el resto de checkboxes
        themeImg = self.img_map[theme]
        dreamImg = None
        vintageImg = None
        spacialImg = None
        lofiImg = None

        if (dream):
            dreamImg = self.img_map["dream"]

        if(vintage):
            vintageImg = self.img_map["vintage"]

        if(spacial):
            spacialImg = self.img_map["espacial"]

        if(lofi):
            lofiImg = self.img_map["lofi"]

        return themeImg, dreamImg, vintageImg, spacialImg, lofiImg
        