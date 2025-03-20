# Torres de Hanoi - Juego en Pygame

Este es un juego de Torres de Hanoi desarrollado en Python utilizando la biblioteca Pygame. El juego implementa el clásico rompecabezas matemático donde debes mover una pila de discos de una torre a otra, siguiendo reglas específicas.

## Características

- **Múltiples niveles de dificultad**: Elige entre 3, 5 u 8 discos
- **Interfaz gráfica atractiva**: Discos de colores y torres visualmente claras
- **Control mediante ratón**: Interacción intuitiva para seleccionar y colocar discos
- **Contadores**: Seguimiento de movimientos realizados y tiempo transcurrido
- **Información de movimientos mínimos**: Muestra la cantidad mínima de movimientos necesarios
- **Menú de selección**: Interfaz para elegir la dificultad deseada
- **Pantalla de victoria**: Resumen de estadísticas al completar el rompecabezas

## Reglas del juego

1. Solo puedes mover un disco a la vez
2. Un disco solo puede moverse a una torre vacía o encima de un disco más grande
3. No puedes colocar un disco más grande sobre uno más pequeño
4. El objetivo es mover toda la pila de discos de la torre izquierda a la torre derecha

## Controles

- **Clic del ratón**: Seleccionar y colocar discos
- **Tecla R**: Reiniciar el nivel actual
- **Tecla ESC**: Volver al menú principal

## Requisitos

- Python 3.x
- Pygame

## Instalación

1. Asegúrate de tener Python instalado en tu sistema
2. Instala Pygame usando pip:
   ```
   pip install pygame
   ```
3. Descarga el archivo `torres_hanoi.py`
4. Ejecuta el juego:
   ```
   python torres_hanoi.py
   ```

## Estrategia

- Para 3 discos: Se puede resolver en un mínimo de 7 movimientos (2³-1)
- Para 5 discos: Se puede resolver en un mínimo de 31 movimientos (2⁵-1)
- Para 8 discos: Se puede resolver en un mínimo de 255 movimientos (2⁸-1)

La fórmula para calcular el número mínimo de movimientos es 2ⁿ-1, donde n es el número de discos.

## Desarrollo

Este juego fue desarrollado como un proyecto educativo para demostrar:
- Implementación de juegos con Pygame
- Lógica del rompecabezas de Torres de Hanoi
- Manejo de eventos y estado del juego
- Diseño de interfaces gráficas interactivas

## Capturas de pantalla

*(Las capturas de pantalla serían incluidas aquí en un repositorio real)*

## Mejoras futuras

- Añadir efectos de sonido
- Implementar un sistema de guardado de récords
- Añadir animaciones para los movimientos de discos
- Crear un modo de resolución automática
- Añadir más variedad de temas visuales

## Licencia

Este proyecto está disponible como código abierto bajo la licencia MIT.
