# excel2json

El script se utiliza para convertir archivos de excel de transición a los JSONs necesarios por la calculadora.

## Requisitos

Se recomienda crear un `virtualenv` para instalar las dependencias necesarias

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
```

Luego se deben instalar las dependencias con `pip install -r requirements.txt`.

## Uso

Para correr el script se debe ejecutar el comando:

```bash
python excel2json.py <archivo_excel> <directorio_salida>
```

Siendo `<archivo_excel>` el archivo a convertir y `<directorio_salida>` la ubicación donde se quieren generar los archivos JSON.

Opcionalmente, se puede incluir un tercer argumento numérico indicando la cantidad de créditos de electivas necesarios en el nuevo plan. Por defecto es 24.
