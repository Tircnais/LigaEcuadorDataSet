Proyecto MULTIplataforma
======================
### Tema: JUEGO _CAPTAS_.
Versión `0.0.1`

**Contenido**

Aplicativo para brindar otro medio para la capacitación de estudiantes. Preguntas y respuestas empleando el consumo de datos via REST y JSON.

  - [Aspecto Generales](#Aspecto-Generales)
  - [Puesta en marcha](#Puesta-en-marcha)

## Aspecto Generales ##

- Ambiente de desarrollo
   información que se debe tener presente en caso de seguir trabajando sobre el aplicativo.
   - **_Ionic Framework_**
   ```
      Versión:    @ionic/angular 4.0.0
   ```
   - **_Cordova_**
   ```
      Versión:    9.0.0 (cordova-lib@9.0.1)
      Necesario para el cambio de iconos del aplicativo, nombre, versión, entre otras.
   ```
   - **_NodeJS_**
   ```
      Versión:    v10.15.3
   ```
## Puesta en marcha ##
**1. Clonando el repositorio**
```git
   git clone https://github.com/Tircnais/JuegoIONIC.git
```

**2. Descagando modulos**
```ionic
   npm i | npm install
```

Este comando le permite descargar las dependencias de IONIC, puesto que el mismo Framework las ignora al subir al repositorio; le remendamos el mismo.

**3. Ejecutando el proyecto**
```ionic
   ionic serve
```

Ese abre una pestaña en el navegador para visualizar el proyecto, esta visualización es "en vivo", es decir, no requieres recargar la página para visualizar tus cambios.

**4. Modulos requeridos para el funcionamiento**
```ionic
   npm i -g cordova
```


+ **_Cordova_**

Es un modulo necesario para introducir el cambiar el icono de la aplicación, el nombre, version la misma, autor, entre otra información.

Ademas provee de un simulador tanto para Android como IOS los cuales se los puede utilizar con los comandos aqui mostrados.

```ionic
ionic cordova platform add android
ionic cordova run android
```

o
```ionic
ionic cordova platform add ios
ionic cordova run ios
```


**5. Creando contenido**
```ionic
   ionic g page *nombre*
   ionic generate page *nombre*
```
Este le permite crear nuevo contenido a la aplicación, anexando lo de manera correcta.
Revisar la [documentación] respectiva en caso de agregar otro tipo de contenido.

[documentación]: https://ionicframework.com/docs/cli/commands/generate

**6. Creando servicio**
```ionic
   ionic g service **carpetaServicio**/**nombreServicio**
```

Necesario para realizar las solicitudes/recibir las respuesta de la plataforma.

+ Despues importamos la libreria en **_app/app.module.ts:_**
```javascript
import { HttpClientModule } from '@angular/common/http';
```

+ En este mismo archivo lo agregamos en:
```javascript
imports: [
   ...,
   HttpClientModule
   ],
```

+ Nos dirigimos a nuestro servicio (services/apirest.service.ts) creado e importamos la libreria
```javascript
import { HttpClient } from '@angular/common/http';
```

+ Ingresamos la URL de la cual se recibe la respuesta
```javascript
url = 'http://www.ejemplo.com/';
```

+ Se declara un constructor
```javascript
constructor(private http: HttpClient) { }
```

+ Construimos la funcion para leer el JSON
```javascript
getPreguntaServe() {
   return this.http.get(this.urlPreguntas);
}
```

+ Presentamos
Esta parte es en base o lo que se requira de manera que puede consultar la documentación respestiva.


**Modulos utiles para desarrollo**
```ionic
   npm i -D -E @ionic/lab
```

*ionic lab* permite visualizar en tiempo real la compilación tanto de ANDROID como IOS.

**7. Instalando el modulo para guardar el almacenamiento**
```ionic
   ionic cordova plugin add cordova-sqlite-storage
   npm install --save @ionic/storage
```

Su utilidad es guardar la opción de medicna y no tener que volver a marcar dicha opción.

___Crear carpeta pantillas dentro del modulo componente___
===
**Crear modulo componente**
```ionic
   ionic g module components --dry-run
```


**Creación Plantilla Carpeta: Verdadero-Falso**
```ionic
   ionic g component components/unica --spec=false
```

**Creación Plantilla Carpeta: Opción Multiple**
```ionic
   ionic g component components/multiple --spec=false
```

**Creación Plantilla Carpeta: Percepcion**
```ionic
   ionic g component components/percepcion --spec=false
```

