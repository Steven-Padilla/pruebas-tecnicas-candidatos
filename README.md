# Configuración del Ambiente de Trabajo

Sigue los pasos a continuación para configurar el ambiente de trabajo correctamente:

## Requisitos Previos

- Asegúrate de tener Python en la versión 3.9.0 instalado en tu sistema. Puedes descargar e instalar Python desde [python.org](https://www.python.org/downloads/).

## Paso 1: Clonar el Repositorio

Clona el repositorio en tu máquina local utilizando el siguiente comando:

```bash
git clone <URL-del-repositorio>
```

## Paso 2: Crear y Activar el Ambiente Virtual

En el directorio del proyecto, crea un ambiente virtual utilizando `venv`:

```bash
python3 -m venv .venv
```

Luego, activa el ambiente virtual:

- En Linux/macOS:

```bash
source .venv/bin/activate
```

- En Windows:

```bash
.venv\Scripts\activate
```

## Paso 3: Instalar las Dependencias

Instala las librerías necesarias utilizando `pip` y el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Paso 4: Crear y Configurar el Archivo `.env`

Copia el contenido del archivo de plantilla `.env_template` proporcionado en el repositorio y pégalo en un nuevo archivo llamado `.env`. Luego, rellena los datos necesarios que se te proporcionaron por privado.

## Paso 5: Configurar la branch desde la que enviaras Cambios

Crea una rama nueva a partir de master para programar y después enviar tus cambios:

```bash
git checkout -b <nombre-de-la-feature>
```

## Paso 7: Enviar Cambios y Crear una Pull Request

Haz tus cambios en el código, commitea y luego envía los cambios a master usando una Pull Request:

```bash
git add .
git commit -m "Descripción de los cambios"
git push origin <nombre-de-la-feature>
```

Luego, desde la página del repositorio en GitHub, puedes crear una Pull Request hacia la rama master, asigna de reviewer al dueño del repositorio y notificale que has hecho una Pull Request.

¡Eso es todo! Ahora tienes el ambiente de trabajo configurado correctamente y has enviado tus cambios para su revisión.

