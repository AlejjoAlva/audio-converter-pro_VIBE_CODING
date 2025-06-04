# 🎵 Audio Converter Pro - Procesamiento Múltiple

**Una aplicación profesional para la conversión masiva de archivos de audio a formato MP4 con interfaz gráfica moderna.**

![Version](https://img.shields.io/badge/version-3.0-blue)
![Python](https://img.shields.io/badge/python-3.6+-green)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey)
![License](https://img.shields.io/badge/license-MIT-orange)

## 📋 Descripción

Audio Converter Pro es una aplicación de escritorio desarrollada en Python con PyQt5 que permite convertir múltiples archivos de audio simultáneamente a formato MP4. Diseñada con una interfaz minimalista en colores rojo vino tinto, negro y blanco, ofrece una experiencia de usuario intuitiva y profesional.

### ✨ Características Principales

- 🎵 **Conversión múltiple**: Procesa varios archivos de audio simultáneamente
- 🔄 **Formatos soportados**: MP3, M4A, WAV, FLAC, OGG, AAC, WMA
- 📊 **Progreso en tiempo real**: Seguimiento detallado del proceso de conversión
- 📁 **Gestión de destinos**: Selección flexible de carpetas de salida
- 📝 **Historial completo**: Registro de todas las conversiones realizadas
- ⚙️ **Configuración personalizable**: Ajustes de rutas y preferencias
- 🖥️ **Interfaz moderna**: Diseño limpio y profesional
- 🔧 **Multiplataforma**: Compatible con Linux, Windows y macOS

## 🖥️ Requisitos del Sistema

### Requisitos Mínimos
- **Python**: 3.6 o superior
- **RAM**: 4GB
- **Espacio en disco**: 500MB libres
- **FFmpeg**: Instalado y disponible en PATH

### Sistemas Operativos Soportados
- ✅ **Linux Ubuntu 20.04+** (Probado y verificado)
- ✅ **Windows 10/11**
- ✅ **macOS 10.14+**

## 🛠️ Instalación

### Para Linux Ubuntu (Probado en Ubuntu 22.04)

#### Opción 1: Instalación con Entorno Virtual (Recomendada)

```bash
# 1. Actualizar el sistema
sudo apt update

# 2. Instalar dependencias del sistema
sudo apt install python3.12-venv python3-pip python3-dev ffmpeg

# 3. Clonar o descargar el proyecto
git clone https://github.com/tuusuario/audio-converter-pro.git
cd audio-converter-pro

# 4. Crear entorno virtual
python3 -m venv audio_converter_env

# 5. Activar entorno virtual
source audio_converter_env/bin/activate

# 6. Instalar PyQt5
pip install --upgrade pip
pip install PyQt5

# 7. Ejecutar la aplicación
python audio_converter_pro.py
```

#### Opción 2: Instalación Global

```bash
# 1. Instalar dependencias
sudo apt update
sudo apt install python3-pyqt5 python3-pyqt5.qtwidgets ffmpeg

# 2. Ejecutar directamente
python3 audio_converter_pro.py
```

### Para Windows

```bash
# 1. Instalar Python 3.6+ desde python.org
# 2. Instalar FFmpeg desde ffmpeg.org y agregarlo al PATH
# 3. Instalar PyQt5
pip install PyQt5

# 4. Ejecutar la aplicación
python audio_converter_pro.py
```

### Para macOS

```bash
# 1. Instalar Homebrew (si no está instalado)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Instalar dependencias
brew install python3 ffmpeg

# 3. Instalar PyQt5
pip3 install PyQt5

# 4. Ejecutar la aplicación
python3 audio_converter_pro.py
```

## 🚀 Uso de la Aplicación

### Inicio Rápido

1. **Abrir la aplicación**:
   ```bash
   # Si usas entorno virtual
   source audio_converter_env/bin/activate
   python audio_converter_pro.py
   ```

2. **Seleccionar archivos**:
   - Haz clic en "Seleccionar Archivos de Audio"
   - Selecciona uno o múltiples archivos de audio
   - Los archivos aparecerán en la lista

3. **Configurar destino**:
   - Verifica o cambia la carpeta de destino
   - Por defecto: `~/Desktop/blck_mp3_to_mp4/mp4_convert_record`

4. **Iniciar conversión**:
   - Haz clic en "Iniciar Conversión"
   - Observa el progreso en tiempo real
   - Los logs mostrarán el estado de cada archivo

### Funciones Avanzadas

#### Panel Principal
- **Gestión de archivos**: Agregar, quitar individual o limpiar todos
- **Progreso detallado**: Barra de progreso total y estado por archivo
- **Logs en tiempo real**: Información detallada del proceso

#### Configuración
- **Ruta predeterminada**: Cambiar carpeta de salida por defecto
- **Guardar preferencias**: Mantener configuración entre sesiones

#### Historial
- **Registro completo**: Ver todas las conversiones realizadas
- **Estadísticas**: Archivos procesados, exitosos y fallidos
- **Acceso rápido**: Abrir carpetas de destino directamente

## 📁 Estructura del Proyecto

```
audio-converter-pro/
├── audio_converter_pro.py          # Archivo principal de la aplicación
├── README.md                       # Este archivo
├── LICENSE                         # Licencia MIT
├── requirements.txt                # Dependencias de Python
├── audio_converter_env/            # Entorno virtual (si se usa)
└── docs/                          # Documentación adicional
    ├── screenshots/               # Capturas de pantalla
    └── manual.md                  # Manual de usuario detallado
```

## 🎨 Interfaz de Usuario

### Diseño Visual
- **Colores principales**: Rojo vino tinto (#800020), Negro (#000000), Blanco (#FFFFFF)
- **Estilo**: Minimalista y moderno
- **Layout**: Sidebar de navegación + área de contenido principal
- **Responsive**: Se adapta al tamaño de la ventana (abre maximizada)

### Secciones
1. **🎵 Panel Principal**: Conversión de archivos
2. **⚙️ Configuración**: Ajustes de la aplicación
3. **📝 Historial**: Registro de conversiones
4. **ℹ️ Acerca de**: Información de la aplicación

## 🔧 Solución de Problemas

### Error: `QSocketNotifier: Can only be used with threads started with QThread`

**Solución**:
```bash
# Usar entorno virtual limpio
python3 -m venv fresh_env
source fresh_env/bin/activate
pip install PyQt5
```

### Error: `symbol lookup error: libpthread.so.0`

**Solución**:
```bash
# Evitar conflictos con snap
/usr/bin/python3 audio_converter_pro.py
```

### Error: `ensurepip is not available`

**Solución**:
```bash
sudo apt install python3.12-venv python3-distutils
```

### FFmpeg no encontrado

**Solución Linux**:
```bash
sudo apt install ffmpeg
```

**Solución Windows**:
1. Descargar FFmpeg desde https://ffmpeg.org/download.html
2. Extraer y agregar al PATH del sistema
3. Reiniciar la terminal

### PyQt5 no se instala

**Alternativa con PySide2**:
```bash
pip install PySide2
# Cambiar las importaciones en el código de PyQt5 a PySide2
```

## 📊 Rendimiento

### Tiempos de Conversión Típicos
- **Archivo MP3 (4MB)**: ~15-30 segundos
- **Archivo FLAC (40MB)**: ~60-120 segundos
- **Múltiples archivos**: Procesamiento secuencial optimizado

### Uso de Recursos
- **CPU**: Utiliza todos los núcleos disponibles
- **RAM**: ~100-200MB durante la conversión
- **Disco**: Espacio temporal mínimo requerido

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

```
MIT License

Copyright (c) 2025 Audio Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 👥 Créditos

- **Desarrollado por**: Audio Team
- **Versión**: 3.0 Multi-File Pro
- **Año**: 2025
- **Tecnologías**: Python, PyQt5, FFmpeg
- **Probado en**: Ubuntu 22.04, Windows 11

## 📞 Soporte

- **Issues**: [GitHub Issues](https://github.com/tuusuario/audio-converter-pro/issues)
- **Documentación**: [Wiki del proyecto](https://github.com/tuusuario/audio-converter-pro/wiki)
- **Email**: audioconverter.support@example.com

## 🔄 Historial de Versiones

### v3.0 Multi-File Pro (2025-01-XX)
- ✅ Procesamiento múltiple de archivos
- ✅ Interfaz rediseñada minimalista
- ✅ Compatibilidad multiplataforma (Linux/Windows/macOS)
- ✅ Historial de conversiones mejorado
- ✅ Gestión avanzada de archivos

### v2.0 Pro (2024-XX-XX)
- ✅ Interfaz moderna con PyQt5
- ✅ Configuraciones personalizables
- ✅ Historial básico

### v1.0 (2024-XX-XX)
- ✅ Conversión básica de audio a MP4
- ✅ Interfaz simple

---

**⭐ Si te gusta este proyecto, ¡no olvides darle una estrella en GitHub!**

**🔔 ¿Encontraste un bug? [Reporta un issue](https://github.com/tuusuario/audio-converter-pro/issues/new)**
