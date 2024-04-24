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
            "lightOff":   load_image("DarkRiders"),
            "lightUp":    load_image("filterBlue"),
            "dream":      load_image("dream"),
            "lofi":       load_image("lofi"),
            "espacial":   load_image("espacial"),
            "vintage":    load_image("vintage"),
            "underwater": load_image("dream"), # cambiar a underwater cuando esté 
            "retro":      load_image("dream")  # cambiar retro cuando esté
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

    def configure_background(self, theme, dream, lofi, vintage, spacial, underwater, retro, lighted = True): # Completar con el resto de checkboxes

        if(lighted):
            self.background_img_pil = self.img_map["lightUp"]
        else:
            self.background_img_pil = self.img_map["lightOff"]

        self.background_img = ImageTk.PhotoImage(self.background_img_pil)
        self.background_img_id = self.canvas.create_image(0, 0, anchor="nw", image=self.background_img)

        self.background_theme_pil = self.img_map[theme]
        self.background_theme = ImageTk.PhotoImage(self.background_theme_pil)
        self.background_theme_id = self.canvas.create_image(0, 0, anchor="nw", image=self.background_theme)   

        # ------ UNDERWATER ------
        if(underwater):
            self.background_underwater_pil = self.img_map["retro"]
            self.background_underwater = ImageTk.PhotoImage(self.background_underwater_pil)
            self.background_underwater_id = self.canvas.create_image(0, 0, anchor="nw", image=self.background_underwater)
        elif (self.background_underwater_id != None):
            self.canvas.delete(self.background_underwater_id)
            self.background_underwater_id = None

        # ------ RETRO ------
        if(retro):
            self.background_retro_pil = self.img_map["retro"]
            self.background_retro = ImageTk.PhotoImage(self.background_retro_pil)
            self.background_retro_id = self.canvas.create_image(0, 0, anchor="nw", image=self.background_retro)
        elif (self.background_retro_id != None):
            self.canvas.delete(self.background_retro_id)
            self.background_retro_id = None

        # ------ DREAM ------
        if (dream):
            self.background_dream_pil = self.img_map["dream"]
            self.background_dream = ImageTk.PhotoImage(self.background_dream_pil)
            self.background_dream_id = self.canvas.create_image(0, 0, anchor="nw", image=self.background_dream)
        elif (self.background_dream_id != None):
            self.canvas.delete(self.background_dream_id)
            self.background_dream_id = None

        # ------ VINTAGE ------
        if(vintage):
            self.background_vintage_pil = self.img_map["vintage"]
            self.background_vintage = ImageTk.PhotoImage(self.background_vintage_pil)
            self.background_vintage_id = self.canvas.create_image(0, 0, anchor="nw", image=self.background_vintage)
        elif (self.background_vintage_id != None):
            self.canvas.delete(self.background_vintage_id)
            self.background_vintage_id = None

        # ------ SPACIAL ------
        if(spacial):
            self.background_spacial_pil = self.img_map["vintage"]
            self.background_spacial = ImageTk.PhotoImage(self.background_spacial_pil)
            self.background_spacial_id = self.canvas.create_image(0, 0, anchor="nw", image=self.background_spacial)
        elif (self.background_spacial_id != None):
            self.canvas.delete(self.background_spacial_id)
            self.background_spacial_id = None

        # ------ LOFI ------
        if(lofi):
            self.background_lofi_pil = self.img_map["lofi"]
            self.background_lofi = ImageTk.PhotoImage(self.background_lofi_pil)
            self.background_lofi_id = self.canvas.create_image(0, 0, anchor="nw", image=self.background_lofi)
        elif (self.background_lofi_id != None):
            self.canvas.delete(self.background_lofi_id)
            self.background_lofi_id = None


    def resize_image(self, tab):
        if(self.background_theme_pil == None):
            return
  
        #Redimensionar la imagen original cuando cambia el tamaño de la ventana
        new_width = tab.winfo_width()
        new_height = tab.winfo_height()

        resized_image_pil = self.background_img_pil.resize((new_width, new_height), Image.LANCZOS)
        self.background_img = ImageTk.PhotoImage(resized_image_pil)
        self.canvas.itemconfig(self.background_img_id, image=self.background_img)

        resized_theme_pil = self.background_theme_pil.resize((new_width, new_height), Image.LANCZOS)
        self.background_theme = ImageTk.PhotoImage(resized_theme_pil)
        self.canvas.itemconfig(self.background_theme_id, image=self.background_theme)

        # ------ UNDERWATER ------
        if(self.background_underwater_id != None):
            resized_image_water_pil = self.background_underwater_pil.resize((new_width, new_height), Image.LANCZOS)
            self.background_underwater = ImageTk.PhotoImage(resized_image_water_pil)
            self.canvas.itemconfig(self.background_underwater_id, image=self.background_underwater)

        # ------ RETRO ------
        if(self.background_retro_id != None):
            resized_image_retro_pil = self.background_retro_pil.resize((new_width, new_height), Image.LANCZOS)
            self.background_retro = ImageTk.PhotoImage(resized_image_retro_pil)
            self.canvas.itemconfig(self.background_retro_id, image=self.background_retro)

        # ------ DREAM -----
        if(self.background_dream_id != None):
            resized_image_dream_pil = self.background_dream_pil.resize((new_width, new_height), Image.LANCZOS)
            self.background_dream = ImageTk.PhotoImage(resized_image_dream_pil)
            self.canvas.itemconfig(self.background_dream_id, image=self.background_dream)

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

        # ------ SPACIAL ------
        if(self.background_spacial_id != None):
            resized_image_spacial_pil = self.background_spacial_pil.resize((new_width, new_height), Image.LANCZOS)
            self.background_spacial = ImageTk.PhotoImage(resized_image_spacial_pil)
            self.canvas.itemconfig(self.background_spacial_id, image=self.background_spacial)

        
        