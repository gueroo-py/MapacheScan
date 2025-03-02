# MapacheScan 🦝

¡Bienvenido a **MapacheScan**! Esta herramienta en **beta** te permite escanear puertos, verificar vulnerabilidades y obtener información de red, todo con un toque de humor y estilo mapachesco. 🕵️‍♂️✨

---

## ¿Cómo Funciona? ⚙️

MapacheScan utiliza módulos estándar de Python para:
- Resolver la IP de un dominio usando `socket`.
- Escanear puertos comunes o un rango personalizado de puertos mediante *threads*.
- Verificar vulnerabilidades en ciertos puertos basándose en una lista predefinida.
- Obtener información WHOIS de una IP usando `subprocess` y el comando `whois`.
- Consultar el DNS de un dominio y obtener la IP pública con la ayuda del módulo `requests`.
- Crear archivos y limpiar la pantalla para que tu terminal siempre luzca impecable.

Todo ello se ejecuta en una interfaz interactiva en la terminal, donde simplemente escribes comandos y dejas que el mapache haga su magia. 🦝💻

---

## Características ✨

- **Obtención de IPs:** Resuelve y muestra la IP de cualquier dominio. 🌐
- **Escaneo de Puertos:** Escanea puertos comunes o un rango específico. Incluye modo sigiloso con delays aleatorios para no dejar rastro. 🔍
- **Verificación de Vulnerabilidades:** Detecta puertos con vulnerabilidades conocidas (¡ojo, seguridad ante todo!). ⚠️
- **Información WHOIS:** Consulta datos WHOIS de una IP para conocer su historial. 📜
- **Lookup DNS:** Realiza búsquedas de registros DNS de dominios. 🔗
- **Obtención de IP Pública:** Muestra la IP pública de tu máquina. 📡
- **Creación de Archivos:** Permite crear archivos vacíos en cualquier ubicación. 📄
- **Limpieza de Pantalla:** Ordena tu terminal en un abrir y cerrar de ojos. 🧹

---

## Instalación 🔧

### Requisitos

- **Python 3.x**
- Módulos estándar: `os`, `time`, `socket`, `threading`, `subprocess`, `random`
- **Requests:** Si no lo tienes instalado, instálalo con:
  ```bash
  pip install requests
