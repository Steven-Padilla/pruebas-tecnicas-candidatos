# Configuración del Ambiente de Trabajo

Sigue los pasos a continuación para configurar el ambiente de trabajo correctamente:

## Requisitos Previos

- Asegúrate de tener Python en la versión 3.9.0 instalado en tu sistema. Puedes descargar e instalar Python desde [python.org](https://www.python.org/downloads/).

## Paso 1: Realizar un Fork del Repositorio

Haz un fork del repositorio original a tu propia cuenta de GitHub haciendo clic en el botón "Fork" en la esquina superior derecha de la página del repositorio en GitHub.

## Paso 2: Clonar tu Repositorio Forked

Clona tu repositorio forked en tu máquina local utilizando el siguiente comando:

```bash
git clone <URL-de-tu-repositorio-forked>
```

## Paso 3: Crear y Activar el Ambiente Virtual

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

## Paso 4: Instalar las Dependencias

Instala las librerías necesarias utilizando `pip` y el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Paso 5: Crear y Configurar el Archivo `.env`

Copia el contenido del archivo de plantilla `.env_template` proporcionado en el repositorio y pégalo en un nuevo archivo llamado `.env`. Luego, rellena los datos necesarios que se te proporcionaron por privado.

## Paso 6: Configurar el Remoto para Enviar Cambios

Configura el remoto para enviar los cambios a tu repositorio forked:

```bash
git remote add origin <URL-de-tu-repositorio-forked>
```

## Paso 7: Enviar Cambios y Crear una Pull Request

Haz tus cambios en el código, commitea y luego envía los cambios a tu repositorio forked:

```bash
git add .
git commit -m "Descripción de los cambios"
git push origin main
```

Luego, desde la página de tu repositorio forked en GitHub, puedes crear una Pull Request hacia el repositorio original.

## Paso 8: Enviar una Invitación al Repositorio Original

Después de enviar la Pull Request al repositorio original, envía una invitación a los colaboradores necesarios desde la configuración de colaboradores del repositorio original en GitHub.

¡Eso es todo! Ahora tienes el ambiente de trabajo configurado correctamente y has enviado tus cambios para su revisión.

