# TFG_AsistenteComposicionConIA

## Autores 
- Javier Callejo Herrero
- Miguel González Perez
- Víctor Manuel Extremera Herranz
- Rodrigo Sánchez Torres

## Propuesta
Desarrollo de una aplicación standalone que permita generar música simbólica a partir de IA. El ususario no requiere de conocimientos musicales para producir la pieza.
La aplicación se compone de 3 pasos principales desde el punto de vista del usuario:
- 1: **Generación de melodía simple**: A partir de un botón, una IA (a determinar) genera el tema o motivo principal, de forma **sencilla y simbólica**. También se permite introducir MIDI generado por parte del usuario.
- 2: **Selección de temáticas precargadas**: El usuario podrá elegir, entre unos valores discretos, la temática que quiere aplicar sobre el tema generado en el **paso 1**. Entre estas temáticas se encuentran: desierto, terror, fantasía, subacuático...
- 3: **Acompañamiento y efectos**: El paso 2 genera una serie de acompañamientos y efectos que pueden ser modificados o eliminados por el usuario. Este tercer paso consiste en un modelo aditivo, donde se pueden añadir efectos a los generados por el **paso 2**, pero también se pueden eliminar. De entre estos efectos se pueden encontrar los **filtros paso banda**, **reverberacion**, etc.

## Herramientas
Posibles herramientas que usar para la generación de contenido en nuestra aplicación (por determinar definitivamente).
- Magenta: Generación del **primer paso**
- Cadenas de Markov: Generación del **primer paso**
- Heurística/Algoritmia para generar el **segundo paso** (transformaciones a escalas y selección de filtros).
- IA tradicional para la generación de armónicos
