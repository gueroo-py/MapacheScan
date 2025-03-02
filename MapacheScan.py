import os
import time
import socket
import threading
import subprocess
import random
import requests

# Definir colores ANSI
GREEN = "\033[92m"
CYAN = "\033[96m"
RED = "\033[91m"
RESET = "\033[0m"

# Portada MapacheScan
banner = f"""{GREEN}
MAPACHE SCANNING :)  
Versión: BETA
{RESET}
"""

# Lista de puertos comunes
PUERTOS_COMUNES = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 3389, 5900, 8080]

# Puertos con vulnerabilidades conocidas
PUERTOS_VULNERABLES = {
    21: "FTP inseguro, puede permitir acceso sin cifrado.",
    22: "Si SSH permite autenticación por contraseña, es vulnerable a ataques de fuerza bruta.",
    23: "Telnet transmite datos en texto plano, fácil de interceptar.",
    25: "Puede ser usado para enviar spam si no está configurado correctamente.",
    3306: "Si MySQL está expuesto sin contraseña fuerte, puede ser comprometido.",
    3389: "RDP es objetivo frecuente de ataques de fuerza bruta.",
    5900: "VNC sin autenticación fuerte permite acceso remoto no autorizado."
}

# Función para obtener la IP de una URL
def obtener_ip(url):
    if url.startswith("https://"):
        url = url[8:]
    elif url.startswith("http://"):
        url = url[7:]
    try:
        print(f"{CYAN}Escaneando {url}...{RESET}")
        time.sleep(1)
        ip = socket.gethostbyname(url)
        print(f"{GREEN}✔ La IP de {url} es: {ip}{RESET}")
    except socket.gaierror:
        print(f"{RED}✖ Error: No se pudo obtener la IP de {url}{RESET}")

# Función para escanear puertos (modo común o rango personalizado)
def escanear_puertos(ip, rango=None, sigiloso=False):
    print(f"{CYAN}Escaneando puertos en {ip}...{RESET}")
    open_ports = []
    
    def scan_port(port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            if sock.connect_ex((ip, port)) == 0:
                # Intentar obtener el servicio solo para puertos comunes
                try:
                    servicio = socket.getservbyport(port, "tcp") if port in PUERTOS_COMUNES else "Desconocido"
                except Exception:
                    servicio = "Desconocido"
                open_ports.append((port, servicio))
            sock.close()
            if sigiloso:
                time.sleep(random.uniform(0.5, 2.0))
        except Exception:
            pass

    threads = []
    # Si se especifica rango, escanear ese rango; sino, los puertos comunes.
    if rango:
        start, end = rango
        ports_to_scan = range(start, end + 1)
    else:
        ports_to_scan = PUERTOS_COMUNES

    for port in ports_to_scan:
        t = threading.Thread(target=scan_port, args=(port,))
        threads.append(t)
        t.start()

    for th in threads:
        th.join()

    if open_ports:
        for port, service in open_ports:
            print(f"{GREEN}✔ Puerto abierto: {port} ({service}){RESET}")
    else:
        print(f"{RED}✖ No se encontraron puertos abiertos en {ip}{RESET}")

# Función para verificar vulnerabilidad de un puerto
def verificar_vulnerabilidad(ip, puerto):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        if sock.connect_ex((ip, puerto)) == 0:
            if puerto in PUERTOS_VULNERABLES:
                print(f"{RED}⚠ El puerto {puerto} en {ip} es potencialmente vulnerable: {PUERTOS_VULNERABLES[puerto]}{RESET}")
            else:
                print(f"{GREEN}✔ El puerto {puerto} en {ip} está abierto pero no es conocido por ser vulnerable.{RESET}")
        else:
            print(f"{RED}✖ El puerto {puerto} en {ip} está cerrado.{RESET}")
        sock.close()
    except Exception as e:
        print(f"{RED}✖ Error al verificar vulnerabilidad en {ip}:{puerto} -> {e}{RESET}")

# Función para obtener información WHOIS de una IP
def obtener_whois(ip):
    try:
        print(f"{CYAN}Obteniendo información WHOIS de {ip}...{RESET}")
        result = subprocess.run(["whois", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            info = result.stdout
            print(f"{GREEN}✔ Información WHOIS:\n{info}{RESET}")
        else:
            print(f"{RED}✖ Error: No se pudo obtener información WHOIS.{RESET}")
    except Exception as e:
        print(f"{RED}✖ Error al ejecutar WHOIS: {e}{RESET}")

# Función para obtener la IP pública de la máquina (mywhois)
def obtener_mi_ip():
    try:
        print(f"{CYAN}Obteniendo la IP pública de tu máquina...{RESET}")
        response = requests.get("https://api.ipify.org?format=json")
        if response.status_code == 200:
            mi_ip = response.json().get("ip")
            print(f"{GREEN}✔ Tu IP pública es: {mi_ip}{RESET}")
        else:
            print(f"{RED}✖ Error: No se pudo obtener la IP pública.{RESET}")
    except requests.RequestException as e:
        print(f"{RED}✖ Error al obtener la IP pública: {e}{RESET}")

# Función para hacer un lookup de DNS
def lookup_dns(dominio):
    try:
        print(f"{CYAN}Buscando registros DNS de {dominio}...{RESET}")
        resultado = socket.gethostbyname_ex(dominio)
        print(f"{GREEN}✔ Registros encontrados: {resultado}{RESET}")
    except socket.gaierror:
        print(f"{RED}✖ Error: No se pudo obtener información de DNS para {dominio}{RESET}")

# Función para crear un archivo en una ubicación específica
def crear_archivo():
    nombre_archivo = input(f"{CYAN}Ingrese el nombre del archivo con extensión (ej: ejemplo.txt): {RESET}").strip()
    directorio = input(f"{CYAN}Ingrese la ruta donde desea crearlo (deje vacío para usar el directorio actual): {RESET}").strip()
    if not directorio:
        directorio = os.getcwd()
    ruta_completa = os.path.join(directorio, nombre_archivo)
    try:
        with open(ruta_completa, "w") as archivo:
            archivo.write("")  # Archivo vacío
        print(f"{GREEN}✔ Archivo creado en: {ruta_completa}{RESET}")
    except Exception as e:
        print(f"{RED}✖ Error al crear el archivo: {e}{RESET}")

# Función para limpiar la pantalla
def limpiar_pantalla():
    os.system("cls" if os.name == "nt" else "clear")

# Función para mostrar ayuda
def mostrar_ayuda():
    ayuda = f"""{CYAN}
Comandos disponibles:
  exit                             - Salir de la herramienta
  help                             - Mostrar esta ayuda
  mapache ip [url]                 - Obtener la IP de un dominio (ej: mapache ip google.com)
  mapache ports [ip] [rango]       - Escanear puertos (usa puertos comunes o rango personalizado ej: mapache ports 192.168.1.1 20-1000)
  mapache ports -s [ip]            - Escaneo de puertos en modo sigiloso (con delays aleatorios)
  mapache port -v [ip] [puerto]      - Verificar vulnerabilidad en un puerto (ej: mapache port -v 192.168.1.1 22)
  mapache whois [ip]               - Obtener información WHOIS de una IP
  mapache mywhois                  - Obtener la IP pública de tu máquina
  mapache dns [dominio]            - Realizar lookup DNS de un dominio (ej: mapache dns google.com)
  mapache -c                       - Crear un archivo vacío en una ubicación específica
  clear                            - Limpiar la pantalla
{RESET}"""
    print(ayuda)

# Función principal
def main():
    limpiar_pantalla()
    print(banner)
    while True:
        comando = input(f"{CYAN}>> {RESET}").strip().lower()
        if comando == "exit":
            break
        elif comando == "help":
            mostrar_ayuda()
        elif comando.startswith("mapache ip "):
            obtener_ip(comando.replace("mapache ip ", "").strip())
        elif comando.startswith("mapache ports -s "):
            ip = comando.replace("mapache ports -s ", "").strip()
            escanear_puertos(ip, sigiloso=True)
        elif comando.startswith("mapache ports "):
            partes = comando.split()
            # Si se pasa rango (ej: mapache ports 192.168.1.1 20-1000)
            if len(partes) == 4 and "-" in partes[3]:
                ip = partes[2]
                try:
                    rango = list(map(int, partes[3].split("-")))
                    escanear_puertos(ip, rango=(rango[0], rango[1]))
                except ValueError:
                    print(f"{RED}✖ Rango no válido. Usa el formato inicio-fin (ej: 20-1000){RESET}")
            elif len(partes) == 3:
                ip = partes[2]
                escanear_puertos(ip)
            else:
                print(f"{RED}✖ Comando incorrecto para escanear puertos.{RESET}")
        elif comando.startswith("mapache port -v "):
            partes = comando.split()
            if len(partes) == 5:
                ip = partes[3]
                try:
                    puerto = int(partes[4])
                    verificar_vulnerabilidad(ip, puerto)
                except ValueError:
                    print(f"{RED}✖ El puerto debe ser un número entero.{RESET}")
            else:
                print(f"{RED}✖ Formato correcto: mapache port -v [ip] [puerto]{RESET}")
        elif comando.startswith("mapache whois "):
            ip = comando.replace("mapache whois ", "").strip()
            obtener_whois(ip)
        elif comando == "mapache mywhois":
            obtener_mi_ip()
        elif comando.startswith("mapache dns "):
            dominio = comando.replace("mapache dns ", "").strip()
            lookup_dns(dominio)
        elif comando == "mapache -c":
            crear_archivo()
        elif comando == "clear":
            limpiar_pantalla()
        else:
            print(f"{RED}Comando no reconocido. Escribe 'help' para ver opciones.{RESET}")

if __name__ == "__main__":
    main()
