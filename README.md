# Proyecto_final
Proyecto Final de Programacion Avanzada


PROYECTO: PLANIFY
Materia: Programación Avanzada
------------------------------------------------------------

Este proyecto es una aplicación de escritorio desarrollada en Python utilizando la biblioteca Tkinter. Su propósito principal es permitir a los usuarios llevar un control completo y personalizado de sus ingresos y gastos mensuales.

La aplicación está diseñada con una interfaz gráfica amigable e intuitiva, pensada tanto para usuarios con conocimientos técnicos como para aquellos que no los tienen.

El usuario puede:

-Registrar ingresos y gastos con su respectivo monto, categoría o tipo, y fecha (con un calendario interactivo).
 -Visualizar gráficamente los gastos mensuales por categoría.
 -Generar reportes en formato Excel y PDF con todos los movimientos registrados, incluyendo una gráfica de barras.
 -Predecir su situación financiera basada en balances mensuales.
 -Recibir recomendaciones automáticas si una categoría de gasto excede cierto porcentaje del total.
 -Buscar transacciones por palabra clave o por rango de fechas.
 -Eliminar transacciones seleccionadas para mantener la base de datos limpia y actualizada.
 -Ver todas sus transacciones desde un botón especial si quiere revisar el historial completo.

Toda la información se almacena localmente en un archivo JSON, lo que permite que se guarden los datos.

------------------------------------------------------------
OBJETIVO DEL PROYECTO:
------------------------------------------------------------

Crear una herramienta práctica que permita al usuario:
1. Tener una noción clara de sus hábitos financieros.
2. Identificar patrones de gasto innecesario.
3. Generar reportes útiles para tomar mejores decisiones económicas.
4. Automatizar tareas básicas de control de gastos en una interfaz visual sencilla.

------------------------------------------------------------
TECNOLOGÍAS UTILIZADAS:
------------------------------------------------------------

- Lenguaje: Python 
- Bibliotecas:
    * tkinter
    * tkcalendar
    * pandas
    * matplotlib
    * fpdf
    * xlsxwriter

nota: Para descargar las librerías usa el comando pip install en la terminal del sistema:)

- Manejo de archivos JSON para almacenamiento local

------------------------------------------------------------
ESTRUCTURA DE LOS ARCHIVOS DEL PROYECTO:
------------------------------------------------------------

- main.py: punto de inicio de la aplicación.
- interfaz.py: contiene toda la lógica de la interfaz gráfica y las funciones del sistema.
- modulos.py: define la clase User y las operaciones asociadas a cada usuario.
- usuarios.json: base de datos local donde se guardan ingresos y gastos de cada usuario.
- carpeta dist/: (opcional) contiene el ejecutable si se genera con PyInstaller.
- gráfica_gastos.png: imagen generada automáticamente para el PDF con los datos visuales.

------------------------------------------------------------
MODO DE USO:
------------------------------------------------------------

1. Abrir main.py con Python instalado.
2. Registrar una cuenta o iniciar sesión con un usuario ya existente.
3. Desde el menú principal, navegar por las funciones disponibles:
   - Agregar ingreso o gasto
   - Generar reportes
   - Buscar transacciones
   - Exportar PDF o Excel
   - Eliminar transacciones


