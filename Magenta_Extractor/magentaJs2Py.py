import js2py

def generate_melody():
    # Lee el contenido del archivo JavaScript
    with open('D:/Universidad/TFG_AsistenteComposicionConIA/Magenta_Extractor/magentaTests.js', 'r') as file:
        js_code = file.read()
    
    # Ejecuta el código JavaScript en un entorno de js2py
    context = js2py.EvalJs()
    context.execute(js_code)
    
    # Obtén la secuencia de notas generada
    melody_sequence = context.generate()

    return melody_sequence

# Llama a la función para generar la melodía y obtén la secuencia de notas
melody_sequence = generate_melody()

# Usa la secuencia de notas como desees
print(melody_sequence)
