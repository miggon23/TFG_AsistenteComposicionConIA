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

    background_underwater_id = None
    background_retro_id = None
    background_spacial_id = None
    background_dream_id = None
    background_vintage_id = None
    background_lofi_id = None

    def __init__(self, canvas):
        self.canvas = canvas
        self.img_map = {
            "lightOff":   load_image("apagado"),
            "lightUp":    load_image("encendido"),

            "dream":      load_image("overlay_dream"),
            "lofi":       load_image("overlay_lofi"),
            "espacial":   load_image("overlay_espacial"),
            "vintage":    load_image("overlay_vintage"),

            "c_modern":    load_image("caracter_moderno"),
            "c_modern_r":    load_image("caracter_moderno_r"),
            "c_vintage":    load_image("caracter_vintage"),
            "c_vintage_r":    load_image("caracter_vintage_r"),
            "c_espacial":    load_image("caracter_espacial"),
            "c_espacial_r":    load_image("caracter_espacial_r"),
            "c_modern_1":    load_image("1caracter_moderno"),
            "c_modern_r_1":    load_image("1caracter_moderno_r"),
            "c_vintage_1":    load_image("1caracter_vintage"),
            "c_vintage_r_1":    load_image("1caracter_vintage_r"),
            "c_espacial_1":    load_image("1caracter_espacial"),
            "c_espacial_r_1":    load_image("1caracter_espacial_r"),
        }
        self.load_tematic_backgrounds()
        print(self.img_map)

    def load_tematic_backgrounds(self):
        i = 0
        for theme in TematicEnum:
            clave = theme.value
            route = "t" + str(i) +"_0"
            valor = load_image(route)
            self.img_map[clave] = valor

            clave = theme.value + "_r"
            route = "t" + str(i) +"_1"
            valor = load_image(route)
            self.img_map[clave] = valor

            clave = theme.value + "_a"
            route = "t" + str(i) +"_2"
            valor = load_image(route)
            self.img_map[clave] = valor

            clave = theme.value + "_a_r"
            route = "t" + str(i) +"_3"
            valor = load_image(route)
            self.img_map[clave] = valor

            clave = theme.value + "_color"
            route = "color_" + str(i)
            valor = load_image(route)
            self.img_map[clave] = valor

            i += 1

    def configure_background(self, theme, dream, lofi, vintage, spacial, underwater, retro, lighted = True): # Completar con el resto de checkboxes

        if(not lighted):
            self.background_img_pil = self.img_map["lightOff"]
        else:
            if(retro and underwater):
                self.background_img_pil = self.img_map[theme + "_a_r"]
            elif(retro):
                self.background_img_pil = self.img_map[theme + "_r"]
            elif(underwater):
                self.background_img_pil = self.img_map[theme + "_a"]
            else:
                self.background_img_pil = self.img_map[theme]
                

        self.background_img = ImageTk.PhotoImage(self.background_img_pil)
        self.background_img_id = self.canvas.create_image(0, 0, anchor="nw", image=self.background_img)


        # ------ CARACTER ------
        caracter = "c_"
        if(spacial):
            caracter = caracter + "espacial"
        elif(lofi or vintage):
            caracter = caracter + "vintage"
        else:
            caracter = caracter + "modern"

        if(retro):
            caracter = caracter + "_r"
            
        if(theme == "Piano" or theme == "Tenebroso"):
            caracter = caracter + "_1"

        self.background_caracter_pil = self.img_map[caracter]
        self.background_caracter = ImageTk.PhotoImage(self.background_caracter_pil)
        self.background_caracter_id = self.canvas.create_image(0, 0, anchor="nw", image=self.background_caracter)

        if(theme == "Agua" and underwater):
            self.canvas.delete(self.background_caracter_id)
            self.background_caracter_id = None


        # ------ LOFI ------
        if(lofi):
            self.background_lofi_pil = self.img_map["lofi"]
            self.background_lofi = ImageTk.PhotoImage(self.background_lofi_pil)
            self.background_lofi_id = self.canvas.create_image(0, 0, anchor="nw", image=self.background_lofi)
        elif (self.background_lofi_id != None):
            self.canvas.delete(self.background_lofi_id)
            self.background_lofi_id = None

        # ------ VINTAGE ------
        if(vintage):
            self.background_vintage_pil = self.img_map["vintage"]
            self.background_vintage = ImageTk.PhotoImage(self.background_vintage_pil)
            self.background_vintage_id = self.canvas.create_image(0, 0, anchor="nw", image=self.background_vintage)
        elif (self.background_vintage_id != None):
            self.canvas.delete(self.background_vintage_id)
            self.background_vintage_id = None

        # ------ DREAM ------
        if (dream):
            self.background_dream_pil = self.img_map["dream"]
            self.background_dream = ImageTk.PhotoImage(self.background_dream_pil)
            self.background_dream_id = self.canvas.create_image(0, 0, anchor="nw", image=self.background_dream)
        elif (self.background_dream_id != None):
            self.canvas.delete(self.background_dream_id)
            self.background_dream_id = None

        # ------ SPACIAL ------
        if(spacial):
            self.background_spacial_pil = self.img_map["espacial"]
            self.background_spacial = ImageTk.PhotoImage(self.background_spacial_pil)
            self.background_spacial_id = self.canvas.create_image(0, 0, anchor="nw", image=self.background_spacial)
        elif (self.background_spacial_id != None):
            self.canvas.delete(self.background_spacial_id)
            self.background_spacial_id = None

        # ------ TEMATICAS ------
        self.background_color_pil = self.img_map[theme+"_color"]
        self.background_color = ImageTk.PhotoImage(self.background_color_pil)
        self.background_color_id = self.canvas.create_image(0, 0, anchor="nw", image=self.background_color)



    def resize_image(self, tab):
        if(self.background_img_pil == None):
            return
  
        #Redimensionar la imagen original cuando cambia el tamaño de la ventana
        new_width = (int) (tab.winfo_width() * 0.965)
        new_height = (int) (tab.winfo_height() * 0.935)



        # ------ TEMATICA ------
        resized_image_pil = self.background_img_pil.resize((new_width, new_height), Image.LANCZOS)
        self.background_img = ImageTk.PhotoImage(resized_image_pil)
        self.canvas.itemconfig(self.background_img_id, image=self.background_img)

        # ------ CARACTER ------
        resized_image_caracter_pil = self.background_caracter_pil.resize((new_width, new_height), Image.LANCZOS)
        self.background_caracter = ImageTk.PhotoImage(resized_image_caracter_pil)
        self.canvas.itemconfig(self.background_caracter_id, image=self.background_caracter)

        # ------ LOFI ------
        if(self.background_lofi_id != None):
            resized_image_lofi_pil = self.background_lofi_pil.resize((new_width, new_height), Image.LANCZOS)
            self.background_lofi = ImageTk.PhotoImage(resized_image_lofi_pil)
            self.canvas.itemconfig(self.background_lofi_id, image=self.background_lofi)

        # ------ VINTAGE -----
        if(self.background_vintage_id != None):
            resized_image_vintage_pil = self.background_vintage_pil.resize((new_width, new_height), Image.LANCZOS)
            self.background_vintage = ImageTk.PhotoImage(resized_image_vintage_pil)
            self.canvas.itemconfig(self.background_vintage_id, image=self.background_vintage)

        # ------ DREAM -----
        if(self.background_dream_id != None):
            resized_image_dream_pil = self.background_dream_pil.resize((new_width, new_height), Image.LANCZOS)
            self.background_dream = ImageTk.PhotoImage(resized_image_dream_pil)
            self.canvas.itemconfig(self.background_dream_id, image=self.background_dream)

        # ------ SPACIAL ------
        if(self.background_spacial_id != None):
            resized_image_spacial_pil = self.background_spacial_pil.resize((new_width, new_height), Image.LANCZOS)
            self.background_spacial = ImageTk.PhotoImage(resized_image_spacial_pil)
            self.canvas.itemconfig(self.background_spacial_id, image=self.background_spacial)

        # ------ TEMATICAS ------
        resized_image_color_pil = self.background_color_pil.resize((new_width, new_height), Image.LANCZOS)
        self.background_color = ImageTk.PhotoImage(resized_image_color_pil)
        self.canvas.itemconfig(self.background_color_id, image=self.background_color)
        
