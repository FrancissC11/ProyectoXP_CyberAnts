# Especificación de Pruebas de Aceptación — Colonia CyberAnts

| Atributo | Detalle del Proyecto |
| :--- | :--- |
| **Sistema** | Colonia CyberAnts (Simulación Táctica KGD) |
| **Equipo** | [+] TEAM [2]: Colonia CyberAnts |
| **Metodología** | Extreme Programming (XP) — Pruebas de Cliente (*Customer Tests*) |
| **Stack Tecnológico** | Python 3.12, Flask, SQLite, pytest, Docker |
| **Cliente** | Franciss Cartagena |
| **Estado General** | Validado y aceptado en su totalidad por el cliente |

---

## 1. Matriz de Trazabilidad (Historias de Usuario ↔ Pruebas de Aceptación ↔ Casos de Prueba)

La siguiente matriz vincula las Historias de Usuario del backlog de XP con sus respectivas Pruebas de Aceptación (PA) y los Casos de Prueba técnicos ejecutados y validados:

| ID Prueba Aceptación | Historia de Usuario | Caso(s) de Prueba Vinculado(s) | Estado de Validación |
| :--- | :--- | :--- | :--- |
| **PA-01** | Control de acceso de integrantes del equipo, credenciales autorizadas y bloqueo ante intentos fallidos. | • Auth: Acceso de integrantes, patmic/123 y bloqueo al 3er intento | **Validada por el cliente** |
| **PA-02** | Creación de hormigas en el hormiguero virtual, alimentación y evolución al TIPO_HORMIGA del Grupo 2. | • Ciclo de vida HLarva con Néctar y evolución a HSoldado con Carnívoro<br>• Hormigas: Ciclo HLarva a HSoldado, persistencia SQLite y rutas Flask | **Validada por el cliente** |
| **PA-03** | Evaluación de arsenal mediante autómata finito en AntCiberDron para detonación selectiva según lenguaje L. | • Dron: Validación de Autómata L = { a+, ab*, ab*t+, abcdt+ } y fonética IPA | **Validada por el cliente** |
| **PA-04** | Lectura de Grupo02.csv y visualización de coordenadas ucranianas con animación de carga. | • CSV: Lectura de Grupo02.csv y animación de carga | **Validada por el cliente** |

---

## 2. Especificación Detallada de Pruebas de Aceptación

### PA-01: Autenticación de Integrantes, Acceso Autorizado y Bloqueo de Seguridad
* **Historia de Usuario Asociada:** Como integrante o administrador de la KGD quiero autenticarme con mis credenciales válidas y contar con protección ante intentos fallidos para garantizar el acceso exclusivo al sistema del Grupo 2.
* **Caso de Prueba Vinculado:** Auth: Acceso de integrantes, patmic/123 y bloqueo al 3er intento
* **Trazabilidad Técnica:** Implementado en AuthService y verificado mediante test_auth.py (Commit #2).

**Escenarios y Criterios de Aceptación:**
* **Escenario 1.1 — Acceso autorizado y despliegue de ficha de equipo:**
  * **Dado que** el usuario se encuentra en la pantalla de inicio de sesión de Colonia CyberAnts,
  * **Cuando** ingresa las credenciales autorizadas (patmic / 123) o las credenciales válidas de cualquiera de los 6 integrantes del Grupo 2,
  * **Entonces** el sistema concede el acceso y renderiza en pantalla el identificador [+] TEAM [2]: Colonia CyberAnts junto con la cédula y el nombre completo del integrante autenticado.
* **Escenario 1.2 — Manejo de entradas vacías y bloqueo al tercer intento fallido:**
  * **Dado que** el sistema recibe un envío con campos vacíos y posteriormente 3 intentos consecutivos con contraseña incorrecta,
  * **Cuando** se intenta iniciar sesión nuevamente incluso con credenciales válidas (patmic / 123),
  * **Entonces** la aplicación no genera excepciones no controladas (*crash*) ante campos vacíos y bloquea el acceso de forma efectiva tras el tercer fallo.

**Resumen de Ejecución Vinculada:**
* **Resultado Esperado:** Acceso permitido a los 6 miembros y a patmic/123 mostrando la ficha del equipo; tolerancia a entradas vacías sin fallos y bloqueo al 3er intento fallido.
* **Resultado Real:** Validado y aprobado por el cliente (Franciss Cartagena); AuthService y test_auth.py operando conforme a lo esperado.

---

### PA-02: Ciclo de Vida, Evolución a HSoldado y Persistencia del Hormiguero Virtual
* **Historia de Usuario Asociada:** *Como Usuario de la KGD quiero crear hormigas en mi hormiguero virtual, alimentarlas y ver cómo se transforman para obtener el TIPO_HORMIGA que corresponde a mi grupo.*
* **Casos de Prueba Vinculados:**
  * Ciclo de vida HLarva con Néctar y evolución a HSoldado con Carnívoro
  * Hormigas: Ciclo HLarva a HSoldado, persistencia SQLite y rutas Flask
* **Trazabilidad Técnica:** Modelo de dominio de hormigas, capa de persistencia en SQLite y controladores web en Flask (Commit #4).

**Escenarios y Criterios de Aceptación:**
* **Escenario 2.1 — Nacimiento y supervivencia inicial en estado larvario:**
  * **Dado que** se crea una nueva hormiga en el Hormiguero Virtual,
  * **Cuando** nace en el sistema y es alimentada con Néctar (ANectar),
  * **Entonces** la entidad se inicializa como HLarva con estado VIVA y conserva tanto su tipo como su estado vital tras consumir Néctar.
* **Escenario 2.2 — Evolución exclusiva a HSoldado (Grupo 2) y control de mortalidad:**
  * **Dado que** existe una HLarva en estado VIVA,
  * **Cuando** se le suministra alimento de tipo Carnívoro (ACarnivoro),
  * **Entonces** evoluciona exclusivamente a HSoldado (tipo correspondiente al Grupo 2) mostrando su id, sexo y estado VIVA; si posteriormente recibe un alimento distinto a Carnívoro (ej. Néctar), pasa a estado MUERTA de forma controlada sin interrumpir la ejecución.
* **Escenario 2.3 — Persistencia en base de datos y disponibilidad web:**
  * **Dado que** se ha modificado el estado de las hormigas en la colonia,
  * **Cuando** se guarda el estado, se recarga la aplicación y se consultan las rutas web en Flask,
  * **Entonces** la información persiste íntegramente en SQLite y todas las vistas HTTP responden con códigos de estado válidos y renderizado correcto.

**Resumen de Ejecución Vinculada:**
* **Resultado Esperado:** Nacimiento como HLarva, supervivencia con ANectar, evolución única a HSoldado con ACarnivoro, muerte controlada ante dieta incompatible, persistencia en SQLite y renderizado correcto en Flask.
* **Resultado Real:** Validado y aprobado por el cliente (Franciss Cartagena); ciclo de vida HLarva/HSoldado, almacenamiento en SQLite y rutas web Flask funcionando correctamente.

---

### PA-03: Validación de Autómata de Detonación (L) y Fonética IPA en AntCiberDron
* **Historia de Usuario Asociada:** *Como Miembro de la KGD quiero que el AntCiberDron valore, con un autómata, si la bomba debe explotar según el tipo de arsenal para destruir exclusivamente el arsenal definido en el lenguaje L.*
* **Caso de Prueba Vinculado:** Dron: Validación de Autómata L = { a+, ab*, ab*t+, abcdt+ } y fonética IPA
* **Trazabilidad Técnica:** Motor de autómata finito y módulo de entrenamiento lingüístico IPA del AntCiberDron.

**Escenarios y Criterios de Aceptación:**
* **Escenario 3.1 — Reconocimiento y detonación ante cadenas válidas del lenguaje L:**
  * **Dado que** el AntCiberDron evalúa un identificador de arsenal mediante el autómata configurado para L = { a+, ab*, ab*t+, abcdt+ },
  * **Cuando** recibe cadenas pertenecientes al lenguaje (como "aa", "abb", "abtt", "abcdttt"),
  * **Entonces** el autómata acepta la cadena y autoriza la detonación de la bomba sobre el objetivo.
* **Escenario 3.2 — Rechazo seguro de cadenas fuera del lenguaje L o vacías:**
  * **Dado que** el AntCiberDron recibe identificadores no reconocidos o entradas vacías (como "", "b", "abcd", "abtc", "xyz"),
  * **Cuando** procesa la cadena a través de las transiciones del autómata,
  * **Entonces** rechaza la entrada sin lanzar excepciones y evita la detonación del explosivo.
* **Escenario 3.3 — Validación de entrenamiento fonético IPA:**
  * **Dado que** se ejecuta el módulo de entrenamiento de idiomas del AntCiberDron,
  * **Cuando** se evalúan las transcripciones bajo el Alfabeto Fonético Internacional (IPA),
  * **Entonces** el sistema valida correctamente las secuencias fonéticas configuradas.

**Resumen de Ejecución Vinculada:**
* **Resultado Esperado:** Aceptación estricta de L = { a+, ab*, ab*t+, abcdt+ }, rechazo seguro de cadenas inválidas/vacías y validación fonética IPA sin errores.
* **Resultado Real:** Validado y aprobado por el cliente (Franciss Cartagena); el autómata discrimina correctamente el lenguaje L, maneja entradas inválidas sin fallos y completa la validación fonética IPA.

---

### PA-04: Ingesta de Coordenadas Ucranianas (Grupo02.csv) y Animación de Carga
* **Historia de Usuario Asociada:** *Como Miembro de la KGD quiero leer Grupo02.csv y ver las coordenadas ucranianas con una animación de carga para conocer geoposición, horarios y tipo de arsenal del ataque.*
* **Caso de Prueba Vinculado:** CSV: Lectura de Grupo02.csv y animación de carga
* **Trazabilidad Técnica:** Módulo de lectura de archivos CSV y vista de monitoreo táctico en Flask.

**Escenarios y Criterios de Aceptación:**
* **Escenario 4.1 — Lectura estructurada de datos tácticos con animación:**
  * **Dado que** el archivo Grupo02.csv se encuentra disponible en el directorio configurado del proyecto con registros válidos,
  * **Cuando** el miembro de la KGD solicita la carga de objetivos ucranianos,
  * **Entonces** el sistema despliega una animación de carga durante el procesamiento y presenta en pantalla la geoposición (coordenadas), los horarios programados y el tipo de arsenal asociado a cada objetivo.
* **Escenario 4.2 — Integración con evaluación del AntCiberDron:**
  * **Dado que** los registros de Grupo02.csv han sido cargados en la interfaz,
  * **Cuando** se inspecciona el tipo de arsenal de cada coordenada,
  * **Entonces** los datos quedan disponibles para su evaluación directa mediante el autómata definido en **PA-03**.

**Resumen de Ejecución Vinculada:**
* **Resultado Esperado:** Visualización fluida de animación de carga seguida de la tabla completa de geoposición, horarios y arsenal extraídos de Grupo02.csv.
* **Resultado Real:** Validado y aprobado por el cliente (Franciss Cartagena); lectura de Grupo02.csv, animación de carga y despliegue de geoposición, horarios y arsenal funcionando correctamente.

---

## 3. Acta de Aceptación del Cliente (Extreme Programming Sign-Off)

Para formalizar el cierre de la iteración bajo la metodología Extreme Programming (XP), se registra la conformidad oficial del cliente (**Franciss Cartagena**) respecto a todas las Pruebas de Aceptación ejecutadas:

| Código PA | Descripción Sintética | Casos de Prueba Vinculados | Estado Técnico | Conformidad Cliente (Franciss Cartagena) |
| :--- | :--- | :--- | :--- | :--- |
| **PA-01** | Control de acceso (patmic/123, 6 integrantes) y bloqueo al 3er intento | Auth: Acceso de integrantes, patmic/123 y bloqueo al 3er intento | Validada | [x] Aceptada |
| **PA-02** | Ciclo HLarva → HSoldado, persistencia SQLite y rutas Flask | Ciclo de vida HLarva con Néctar y evolución a HSoldado con Carnívoro<br>Hormigas: Ciclo HLarva a HSoldado, persistencia SQLite y rutas Flask | Validada | [x] Aceptada |
| **PA-03** | Autómata L = { a+, ab*, ab*t+, abcdt+ } y fonética IPA | Dron: Validación de Autómata L = { a+, ab*, ab*t+, abcdt+ } y fonética IPA | Validada | [x] Aceptada |
| **PA-04** | Lectura de Grupo02.csv, animación de carga y geoposición | CSV: Lectura de Grupo02.csv y animación de carga | Validada | [x] Aceptada |
