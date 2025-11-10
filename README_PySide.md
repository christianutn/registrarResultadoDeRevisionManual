PySide6 prototype - instrucciones

Este proyecto añade una interfaz prototipo basada en PySide6 en `interfaz_pyside/`.

Requisitos
- Python 3.11 (recomendado) o 3.10/3.12 (versiones < 3.14 compatibles con PySide6 6.9.3)
- virtualenv recomendado

Instalación y ejecución (recomendado)

1) Crear y activar un virtualenv (desde la raíz del repositorio):

```bash
python -m venv .venv_pyside
source .venv_pyside/Scripts/activate
```

2) Instalar dependencias:

```bash
pip install -r requirements.txt
```

3) Ejecutar el prototipo PySide6:

```bash
python interfaz_pyside/main.py
```

Qué hace el prototipo
- Muestra una ventana con una tabla que carga `eventos_sismicos.csv` y columnas: Fecha/Hora, Epicentro, Hipocentro, Magnitud.
- Botones para bloquear, ver detalles, confirmar, rechazar y solicitar revisión a experto. Las acciones por ahora están simuladas (muestran un popup). Más adelante podemos conectar estas acciones al `GestorSismo`.

Notas
- Si tu Python es 3.14, instala Python 3.11 y usa ese intérprete para el virtualenv; PySide6 no tiene ruedas oficiales para 3.14 en muchas versiones.
