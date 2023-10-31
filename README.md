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

## Modelo del excel

En la carpeta `ejemplos/` se encuentran algunos modelos para utilizar como plantilla.

Las reglas a seguir son:

- Todos los nombres a continuación **deben respetar la convención planteada**, incluyendo mayúsculas, espacios y tildes.
- Se requieren mínimamente 3 hojas:
	- `Plan23`
	- `Obligatorias`
	- `Electivas`
- Opcionalmente, en caso que la carrera cuente con ellas, se debe crear una hoja extra por cada orientación con el nombre `Orientacion - <nombre>`. Por ejemplo, `Orientacion - Distribuidos`.
- Todas las hojas referentes al plan viejo (`Obligatorias`, `Electivas` y `Orientacion - ...`) utilizan el mismo formato que contiene las siguiente columnas:
	- `Nombre`: Nombre de la materia del plan viejo.
	- `Creditos`: Créditos que aportaba en el plan viejo.
	- `Creditos extra`: Créditos extra a dar de electivas por tener la materia aprobada. Normalmente será 0. Ver como ejemplo `Física II A` del plan de informática.
- En `Plan23` va **una fila por cada equivalencia que tenga una materia del plan nuevo**. El formato con sus columnas es el siguiente:
	- `Nombre`: Nombre de la materia en el plan nuevo.
	- `Equivalencia por materias`: Nombre de la materia del plan viejo que da por aprobada la materia nueva. En el caso de necesitar más de una materia para cumplir la equivalencia se deben anotar todas las necesarias, separadas por `&`.
	- `Diferencia de créditos`: Si una equivalencia requiere cierta materia sumada a algunos créditos, se debe poner la diferencia. Normalmente será 0. Ver como ejemplo `Teoría de Algoritmos` por `Matemática Discreta` del plan de informática.
	- `Equivalencia por creditos`: En caso de haber una equivalencia por cantidad de créditos aprobados del plan viejo, poner aquí esa cantidad.
- En el caso de que una materia del plan nuevo no tenga ninguna equivalencia con el plan viejo, completar solo el nombre.
- En el caso de que una materia del plan nuevo se pueda dar por equivalencia de distintas formas, crear una fila por cada manera. Ver como ejemplo `Teoría de Algoritmos` del plan de informática.
