# 🎵 Audio Converter Pro - Procesamiento Múltiple

**Audio Converter Pro** es una aplicación profesional multiplataforma para la conversión masiva de archivos de audio a formato MP4. Diseñada con una interfaz moderna y minimalista, permite procesar múltiples archivos simultáneamente con seguimiento en tiempo real del progreso.

![Audio Converter Pro Screenshot](screenshot.png)

## ✨ Características Principales

### 🔄 **Procesamiento Múltiple**
- ✅ Selección y conversión de múltiples archivos simultáneamente
- ✅ Progreso individual y total en tiempo real
- ✅ Cola de procesamiento secuencial optimizada
- ✅ Cancelación de conversiones en progreso

### 🎯 **Formatos Soportados**
- **Entrada**: MP3, M4A, WAV, FLAC, OGG, AAC, WMA
- **Salida**: MP4 (video con audio original + fondo negro)
- **Calidad**: Preserva calidad de audio original

### 🖥️ **Interfaz Moderna**
- 🎨 Diseño minimalista con paleta rojo vino tinto, negro y blanco
- 📱 Interfaz responsive que se adapta al tamaño de pantalla
- 🔍 Logs detallados con iconos para mejor legibilidad
- 📊 Barras de progreso con información de estado

### 🛠️ **Funcionalidades Avanzadas**
- 📁 Selección personalizable de carpeta de destino
- 📝 Historial completo de conversiones con estadísticas
- ⚙️ Configuraciones guardadas persistentemente
- 🚫 Prevención de sobrescritura con numeración automática

## 🚀 Instalación

### **Windows**

#### Requisitos Previos
- Python 3.6 o superior
- FFmpeg instalado y en PATH del sistema

#### Instalación Paso a Paso

1. **Clonar o descargar el repositorio:**
```bash
git clone https://github.com/tu-usuario/audio-converter-pro.git
cd audio-converter-pro
```

2. **Crear entorno virtual (recomendado):**
```bash
python -m venv audio_converter_env
audio_converter_env\Scripts\activate
```

3. **Instalar dependencias:**
```bash
pip install --upgrade pip
pip install PyQt5
```

4. **Instalar FFmpeg:**
   - Descargar desde [ffmpeg.org](https://ffmpeg.org/download.html)
   - Extraer y agregar al PATH del sistema
   - Verificar con: `ffmpeg -version`

5. **Ejecutar la aplicación:**
```bash
python audio_converter_pro.py
```

### **Linux Ubuntu/Debian**

#### Instalación Automática

```bash
# 1. Actualizar sistema
sudo apt update

# 2. Instalar dependencias del sistema
sudo apt install python3.12-venv python3-pip ffmpeg

# 3. Clonar repositorio
git clone https://github.com/tu-usuario/audio-converter-pro.git
cd audio-converter-pro

# 4. Crear entorno virtual
python3 -m venv audio_converter_env

# 5. Activar entorno virtual
source audio_converter_env/bin/activate

# 6. Instalar PyQt5
pip install --upgrade pip
pip install PyQt5

# 7. Ejecutar aplicación
python audio_converter_pro.py
```

#### Script de Instalación Rápida

```bash
#!/bin/bash
# Guardar como install.sh y ejecutar: bash install.sh

echo "🎵 Instalando Audio Converter Pro..."
sudo apt update
sudo apt install python3.12-venv python3-pip ffmpeg -y
python3 -m venv audio_converter_env
source audio_converter_env/bin/activate
pip install --upgrade pip PyQt5
echo "✅ Instalación completada!"
echo "💡 Para ejecutar: source audio_converter_env/bin/activate && python audio_converter_pro.py"
```

### **macOS**

```bash
# 1. Instalar Homebrew (si no está instalado)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Instalar dependencias
brew install python3 ffmpeg

# 3. Crear entorno virtual
python3 -m venv audio_converter_env
source audio_converter_env/bin/activate

# 4. Instalar PyQt5
pip install --upgrade pip PyQt5

# 5. Ejecutar aplicación
python audio_converter_pro.py
```

## 📖 Guía de Uso

### **1. Inicio Rápido**

1. **Abrir la aplicación** - Se ejecuta en pantalla completa
2. **Seleccionar archivos** - Clic en "Seleccionar Archivos de Audio"
3. **Elegir destino** - Cambiar carpeta de destino si es necesario
4. **Iniciar conversión** - Clic en "Iniciar Conversión"
5. **Monitorear progreso** - Seguir logs y barra de progreso

### **2. Gestión de Archivos**

- **Agregar archivos**: Botón "Seleccionar Archivos de Audio"
- **Quitar archivo específico**: Seleccionar en lista + "Quitar Seleccionado"
- **Limpiar todo**: Botón "Limpiar Todo"
- **Cambiar destino**: Botón "Cambiar Destino"

### **3. Monitoreo de Conversión**

- **Progreso total**: Barra principal muestra porcentaje global
- **Progreso individual**: Texto de estado muestra archivo actual
- **Logs detallados**: Panel derecho con información completa
- **Cancelación**: Botón "Cancelar Conversión" durante proceso

### **4. Historial y Configuración**

- **Ver historial**: Pestaña "Historial" con estadísticas completas
- **Configurar rutas**: Pestaña "Configuración" para rutas predeterminadas
- **Abrir carpetas**: Botones "Ver Carpeta" en historial

## 🏗️ Estructura del Proyecto

```
audio-converter-pro/
├── audio_converter_pro.py          # Aplicación principal
├── README.md                       # Este archivo
├── LICENSE                         # Licencia MIT
├── requirements.txt                # Dependencias Python
├── install.sh                      # Script instalación Linux
├── audio_converter_env/            # Entorno virtual (creado al instalar)
└── conversion_history.json         # Historial (creado automáticamente)
```

## 🔧 Configuración Avanzada

### **Personalización de Rutas**

La aplicación crea automáticamente las siguientes rutas:

- **Windows**: `C:\Users\[Usuario]\Desktop\blck_mp3_to_mp4\mp4_convert_record`
- **Linux/macOS**: `~/Desktop/blck_mp3_to_mp4/mp4_convert_record`

Puedes cambiar estas rutas desde la pestaña "Configuración".

### **Parámetros de FFmpeg**

La aplicación utiliza configuración optimizada:
- **Preset**: ultrafast (máxima velocidad)
- **Codec video**: libx264
- **Codec audio**: copy (sin recodificación)
- **Aceleración**: hardware automática
- **Threads**: número de núcleos CPU

### **Personalización Visual**

Paleta de colores definida en el código:
- **Primario**: #800020 (Rojo vino tinto)
- **Secundario**: #000000 (Negro)
- **Fondo**: #FFFFFF (Blanco)
- **Acentos**: Grises neutros

## 🐛 Solución de Problemas

### **Error: FFmpeg no encontrado**

```bash
# Linux/macOS
sudo apt install ffmpeg  # Ubuntu/Debian
brew install ffmpeg      # macOS

# Windows
# Descargar desde ffmpeg.org y agregar al PATH
```

### **Error: PyQt5 no se instala**

```bash
# Instalar dependencias del sistema primero
sudo apt install python3-dev python3-distutils build-essential

# Luego instalar PyQt5
pip install PyQt5
```

### **Error: Conflictos con Snap (Linux)**

```bash
# Usar Python del sistema explícitamente
/usr/bin/python3 -m venv audio_converter_env
source audio_converter_env/bin/activate
pip install PyQt5
```

### **Error: Archivos no se convierten**

1. Verificar que FFmpeg está en PATH: `ffmpeg -version`
2. Verificar permisos de escritura en carpeta destino
3. Verificar que archivos de origen no están corruptos
4. Revisar logs detallados en la aplicación

### **Aplicación no abre en pantalla completa**

La aplicación está configurada para abrir maximizada. Si no funciona:
- Verificar resolución de pantalla
- Probar con `window.showMaximized()` en lugar de `window.show()`

## 🔄 Actualizaciones y Mantenimiento

### **Actualizar la aplicación**

```bash
# Activar entorno virtual
source audio_converter_env/bin/activate  # Linux/macOS
# o
audio_converter_env\Scripts\activate     # Windows

# Actualizar dependencias
pip install --upgrade PyQt5

# Actualizar FFmpeg
sudo apt update && sudo apt upgrade ffmpeg  # Linux
brew upgrade ffmpeg                         # macOS
```

### **Backup del historial**

El historial se guarda automáticamente en:
- `[carpeta_salida]/conversion_history.json`

Para hacer backup:
```bash
cp conversion_history.json ~/backup_conversion_history_$(date +%Y%m%d).json
```

## 👨‍💻 Desarrollo

### **Requisitos de Desarrollo**

- Python 3.6+
- PyQt5 5.15+
- FFmpeg
- Git (para control de versiones)

### **Estructura del Código**

- `ConversionThread`: Hilo de conversión con FFmpeg
- `AudioConverterApp`: Clase principal de la aplicación
- `Card`, `PrimaryButton`, etc.: Componentes UI personalizados
- `open_folder_cross_platform()`: Función multiplataforma

### **Contribuir**

1. Fork del repositorio
2. Crear rama feature (`git checkout -b feature/nueva-caracteristica`)
3. Commit cambios (`git commit -am 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Crear Pull Request

## 📋 Dependencias

### **Python**
```txt
PyQt5>=5.15.0
```

### **Sistema**
- FFmpeg (cualquier versión reciente)
- Python 3.6 o superior

### **Instalación de dependencias**
```bash
pip install -r requirements.txt
```

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

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

## 🤝 Soporte

- **Issues**: [GitHub Issues](https://github.com/tu-usuario/audio-converter-pro/issues)
- **Documentación**: Este README y comentarios en el código
- **Email**: audio.team@example.com

## 📊 Estadísticas del Proyecto

- **Líneas de código**: ~1000+
- **Archivos**: 1 archivo principal
- **Plataformas soportadas**: Windows, Linux, macOS
- **Formatos soportados**: 7 de entrada, 1 de salida
- **Idioma**: Python con interfaz en español

---

### 🚀 **¡Comienza a convertir tus archivos de audio ahora!**

```bash
git clone https://github.com/tu-usuario/audio-converter-pro.git
cd audio-converter-pro
source audio_converter_env/bin/activate
python audio_converter_pro.py
```

**Audio Converter Pro v3.0** - *Procesamiento múltiple de audio a video de manera simple y eficiente.*
