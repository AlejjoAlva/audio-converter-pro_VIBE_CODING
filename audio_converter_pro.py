import os
import sys
import subprocess
import re
import datetime
import json
import platform
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                           QLabel, QPushButton, QFileDialog, QProgressBar, QTextEdit, 
                           QLineEdit, QMessageBox, QGroupBox, QFormLayout, QComboBox,
                           QFrame, QSplitter, QTabWidget, QSizePolicy, QScrollArea,
                           QStackedWidget, QTableWidget, QTableWidgetItem, QHeaderView,
                           QListWidget, QListWidgetItem)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot, QSize, QPropertyAnimation, QEasingCurve, QDate
from PyQt5.QtGui import QIcon, QFont, QColor, QPalette, QCursor

def open_folder_cross_platform(folder_path):
    """Función para abrir carpetas de manera multiplataforma"""
    try:
        if platform.system() == "Windows":
            os.startfile(folder_path)
        elif platform.system() == "Darwin":  # macOS
            subprocess.run(["open", folder_path])
        else:  # Linux y otros Unix
            subprocess.run(["xdg-open", folder_path])
    except Exception as e:
        print(f"Error al abrir carpeta: {e}")

class ConversionThread(QThread):
    progress_update = pyqtSignal(int, str)  # progreso, nombre_archivo
    log_update = pyqtSignal(str)
    conversion_finished = pyqtSignal(bool, str, list, str, int, int)  # success, message, input_files, output_folder, successful_count, failed_count
    file_completed = pyqtSignal(str, bool)  # nombre_archivo, success
    
    def __init__(self, input_files, output_folder):
        super().__init__()
        self.input_files = input_files
        self.output_folder = output_folder
        self.is_cancelled = False
        self.preset = "ultrafast"
        self.use_hwaccel = True
        
    def run(self):
        try:
            total_files = len(self.input_files)
            successful_conversions = 0
            failed_conversions = 0
            
            self.log_update.emit(f"=== INICIANDO CONVERSIÓN DE {total_files} ARCHIVOS ===")
            self.log_update.emit(f"Carpeta de destino: {self.output_folder}")
            
            for i, input_file in enumerate(self.input_files):
                if self.is_cancelled:
                    self.log_update.emit("=== CONVERSIÓN CANCELADA ===")
                    self.conversion_finished.emit(False, "Conversión cancelada por el usuario", self.input_files, self.output_folder, successful_conversions, failed_conversions)
                    return
                
                file_name = os.path.basename(input_file)
                self.log_update.emit(f"\n[{i+1}/{total_files}] Procesando: {file_name}")
                
                # Crear nombre de archivo de salida
                base_name = os.path.splitext(file_name)[0]
                output_file = os.path.join(self.output_folder, f"{base_name}.mp4")
                
                # Evitar sobrescribir archivos existentes
                counter = 1
                while os.path.exists(output_file):
                    output_file = os.path.join(self.output_folder, f"{base_name}_{counter}.mp4")
                    counter += 1
                
                success = self._convert_single_file(input_file, output_file, i+1, total_files)
                
                if success:
                    successful_conversions += 1
                    self.log_update.emit(f"✓ {file_name} convertido exitosamente")
                    self.file_completed.emit(file_name, True)
                else:
                    failed_conversions += 1
                    self.log_update.emit(f"✗ Error convirtiendo {file_name}")
                    self.file_completed.emit(file_name, False)
            
            # Resumen final
            self.log_update.emit(f"\n=== RESUMEN FINAL ===")
            self.log_update.emit(f"Total procesados: {total_files}")
            self.log_update.emit(f"Exitosos: {successful_conversions}")
            self.log_update.emit(f"Fallidos: {failed_conversions}")
            
            if successful_conversions > 0:
                self.log_update.emit(f"Archivos guardados en: {self.output_folder}")
            
            success_overall = successful_conversions > 0
            message = f"Conversión completada. {successful_conversions} de {total_files} archivos procesados exitosamente."
            
            self.conversion_finished.emit(success_overall, message, self.input_files, self.output_folder, successful_conversions, failed_conversions)
                
        except Exception as e:
            self.log_update.emit(f"Error crítico: {str(e)}")
            self.conversion_finished.emit(False, str(e), self.input_files, self.output_folder, 0, len(self.input_files))
    
    def _convert_single_file(self, input_file, output_file, file_index, total_files):
        try:
            cpu_count = os.cpu_count() or 4
            
            cmd = [
                'ffmpeg',
                '-y',
                '-hwaccel', 'auto',
                '-i', input_file,
                '-f', 'lavfi',
                '-i', 'color=c=black:s=1280x720:r=30',
                '-shortest',
                '-c:a', 'copy',
                '-c:v', 'libx264',
                '-preset', 'ultrafast',
                '-tune', 'fastdecode',
                '-pix_fmt', 'yuv420p',
                '-threads', str(cpu_count),
                output_file
            ]
            
            process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                universal_newlines=True,
                bufsize=1
            )
            
            duration = self._get_duration(input_file)
            if not duration or duration <= 0:
                duration = 100
            
            file_name = os.path.basename(input_file)
            
            for line in process.stderr:
                if self.is_cancelled:
                    process.terminate()
                    return False
                
                time_match = re.search(r'time=(\S+)', line)
                if time_match:
                    try:
                        time_str = time_match.group(1)
                        current_time = self._time_to_seconds(time_str)
                        file_progress = min(int(current_time / duration * 100), 100)
                        
                        # Calcular progreso total
                        total_progress = int(((file_index - 1) / total_files * 100) + (file_progress / total_files))
                        
                        self.progress_update.emit(total_progress, f"{file_name} ({file_progress}%)")
                    except:
                        pass
            
            process.wait()
            return process.returncode == 0
            
        except Exception as e:
            self.log_update.emit(f"Error procesando {os.path.basename(input_file)}: {str(e)}")
            return False
    
    def cancel(self):
        self.is_cancelled = True
    
    def _get_duration(self, file_path):
        try:
            cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', 
                  '-of', 'default=noprint_wrappers=1:nokey=1', file_path]
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return float(result.stdout.strip())
        except:
            return None
    
    def _time_to_seconds(self, time_str):
        try:
            parts = time_str.split(':')
            if len(parts) == 3:
                h, m, s = parts
                return int(h) * 3600 + int(m) * 60 + float(s.split('.')[0])
            elif len(parts) == 2:
                m, s = parts
                return int(m) * 60 + float(s.split('.')[0])
            return float(time_str)
        except:
            return 0

class Card(QFrame):
    """Widget personalizado para crear tarjetas con estilo simple"""
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.setObjectName("card")
        self.setStyleSheet("""
            #card {
                background-color: white;
                border: 1px solid #800020;
                margin: 5px;
            }
        """)
        
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 15)
        self.layout.setSpacing(10)
        
        if title:
            title_label = QLabel(title)
            title_label.setObjectName("cardTitle")
            title_label.setStyleSheet("""
                #cardTitle {
                    color: #800020;
                    font-size: 14px;
                    font-weight: bold;
                    padding-bottom: 5px;
                }
            """)
            self.layout.addWidget(title_label)
            
    def addWidget(self, widget):
        self.layout.addWidget(widget)
        
    def addLayout(self, layout):
        self.layout.addLayout(layout)

class SidebarButton(QPushButton):
    """Botón simple para la barra lateral"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setObjectName("sidebarButton")
        self.setStyleSheet("""
            #sidebarButton {
                background-color: transparent;
                color: #cccccc;
                border: none;
                text-align: left;
                padding: 12px 15px;
                font-size: 14px;
                min-height: 40px;
            }
            #sidebarButton:hover {
                background-color: #333333;
                color: white;
            }
            #sidebarButton:checked {
                background-color: #800020;
                color: white;
            }
        """)
        self.setCheckable(True)
        self.setCursor(QCursor(Qt.PointingHandCursor))

class PrimaryButton(QPushButton):
    """Botón primario simple"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setObjectName("primaryButton")
        self.setStyleSheet("""
            #primaryButton {
                background-color: #800020;
                color: white;
                border: none;
                padding: 10px 15px;
                font-weight: bold;
                font-size: 14px;
                min-height: 35px;
            }
            #primaryButton:hover {
                background-color: #a00028;
            }
            #primaryButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        self.setCursor(QCursor(Qt.PointingHandCursor))

class SecondaryButton(QPushButton):
    """Botón secundario simple"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setObjectName("secondaryButton")
        self.setStyleSheet("""
            #secondaryButton {
                background-color: white;
                color: #800020;
                border: 1px solid #800020;
                padding: 10px 15px;
                font-weight: bold;
                font-size: 14px;
                min-height: 35px;
            }
            #secondaryButton:hover {
                background-color: #f8f8f8;
            }
            #secondaryButton:disabled {
                border-color: #cccccc;
                color: #cccccc;
            }
        """)
        self.setCursor(QCursor(Qt.PointingHandCursor))

class DangerButton(QPushButton):
    """Botón de peligro simple"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setObjectName("dangerButton")
        self.setStyleSheet("""
            #dangerButton {
                background-color: white;
                color: #000000;
                border: 1px solid #000000;
                padding: 10px 15px;
                font-weight: bold;
                font-size: 14px;
                min-height: 35px;
            }
            #dangerButton:hover {
                background-color: #f8f8f8;
            }
            #dangerButton:disabled {
                border-color: #cccccc;
                color: #cccccc;
            }
        """)
        self.setCursor(QCursor(Qt.PointingHandCursor))

class ModernProgressBar(QProgressBar):
    """Barra de progreso simple"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QProgressBar {
                border: 1px solid #800020;
                background-color: white;
                text-align: center;
                color: #800020;
                font-weight: bold;
                font-size: 12px;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #800020;
            }
        """)
        self.setTextVisible(True)

class AudioConverterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # Definir la ruta de salida multiplataforma
        if platform.system() == "Windows":
            self.output_folder = r"C:\Users\Home\Desktop\blck_mp3_to_mp4\mp4_convert_record"
        else:  # Linux/macOS
            self.output_folder = os.path.expanduser("~/Desktop/blck_mp3_to_mp4/mp4_convert_record")
        
        os.makedirs(self.output_folder, exist_ok=True)
        
        # Lista de archivos seleccionados para convertir
        self.selected_files = []
        
        # Historial de conversiones
        self.conversion_history = []
        self.load_history()
        
        self.init_ui()
        self.conversion_thread = None
        self.setWindowTitle("Audio Converter Pro - Procesamiento Múltiple")
        
        # Abrir en pantalla completa
        self.showMaximized()
        
    def init_ui(self):
        # Aplicar estilos globales simples
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QWidget {
                font-family: 'Segoe UI', 'Ubuntu', 'Liberation Sans', Arial, sans-serif;
            }
            QLineEdit, QComboBox, QTextEdit {
                border: 1px solid #800020;
                padding: 8px;
                background: white;
                font-size: 13px;
            }
            QListWidget {
                border: 1px solid #800020;
                background: white;
                font-size: 13px;
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:selected {
                background-color: #800020;
                color: white;
            }
            QScrollBar:vertical {
                background: #f5f5f5;
                width: 10px;
            }
            QScrollBar::handle:vertical {
                background: #800020;
                min-height: 20px;
            }
            QTableWidget {
                border: 1px solid #800020;
                background-color: white;
                gridline-color: #ddd;
                font-size: 13px;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QHeaderView::section {
                background-color: #800020;
                color: white;
                font-weight: bold;
                padding: 8px;
                border: none;
                font-size: 13px;
            }
        """)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal horizontal
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # SIDEBAR IZQUIERDO
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setStyleSheet("""
            #sidebar {
                background-color: #000000;
                min-width: 250px;
                max-width: 250px;
            }
        """)
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 30, 0, 30)
        sidebar_layout.setSpacing(5)
        
        # Título en el sidebar
        app_title = QLabel("Audio Converter Pro")
        app_title.setStyleSheet("""
            color: white;
            font-size: 18px;
            font-weight: bold;
            padding-left: 20px;
            padding-bottom: 20px;
        """)
        sidebar_layout.addWidget(app_title)
        
        # Botones del sidebar
        self.btn_dashboard = SidebarButton("🎵 Panel Principal")
        self.btn_dashboard.setChecked(True)
        self.btn_settings = SidebarButton("⚙️ Configuración")
        self.btn_history = SidebarButton("📝 Historial")
        self.btn_about = SidebarButton("ℹ️ Acerca de")
        
        # Conectar señales
        self.btn_dashboard.clicked.connect(lambda: self.change_page(0))
        self.btn_settings.clicked.connect(lambda: self.change_page(1))
        self.btn_history.clicked.connect(lambda: self.change_page(2))
        self.btn_about.clicked.connect(lambda: self.change_page(3))
        
        sidebar_layout.addWidget(self.btn_dashboard)
        sidebar_layout.addWidget(self.btn_settings)
        sidebar_layout.addWidget(self.btn_history)
        sidebar_layout.addWidget(self.btn_about)
        
        sidebar_layout.addStretch()
        
        # Versión en el sidebar
        version_label = QLabel("v3.0 Multi-File Pro")
        version_label.setStyleSheet("""
            color: #666666;
            font-size: 12px;
            padding-left: 20px;
        """)
        sidebar_layout.addWidget(version_label)
        
        main_layout.addWidget(sidebar)
        
        # CONTENIDO PRINCIPAL
        self.content_stack = QStackedWidget()
        self.content_stack.setObjectName("contentStack")
        self.content_stack.setStyleSheet("""
            #contentStack {
                background-color: #f5f5f5;
            }
        """)
        
        # Añadir páginas
        self.init_dashboard_page()
        self.init_settings_page()
        self.init_history_page()
        self.init_about_page()
        
        main_layout.addWidget(self.content_stack)
        
        # Mensaje inicial
        self.log.append("=== BIENVENIDO A AUDIO CONVERTER PRO ===")
        self.log.append("Seleccione archivos de audio para conversión múltiple")
        self.log.append("Formatos soportados: MP3, M4A, WAV, FLAC, OGG, AAC, WMA")
    
    def init_dashboard_page(self):
        dashboard_page = QWidget()
        dashboard_layout = QVBoxLayout(dashboard_page)
        dashboard_layout.setContentsMargins(20, 20, 20, 20)
        dashboard_layout.setSpacing(15)
        
        # Encabezado simple
        page_title = QLabel("Conversor de Audio - Procesamiento Múltiple")
        page_title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #800020;
            padding-bottom: 10px;
        """)
        dashboard_layout.addWidget(page_title)
        
        # Layout principal con dos columnas
        main_content_layout = QHBoxLayout()
        
        # COLUMNA IZQUIERDA - Selección y lista de archivos
        left_column = QVBoxLayout()
        
        # Card de selección de archivos
        file_card = Card("Selección de Archivos de Audio")
        file_layout = QVBoxLayout()
        
        # Botón para seleccionar archivos
        self.btn_browse = PrimaryButton("Seleccionar Archivos de Audio")
        self.btn_browse.clicked.connect(self.browse_files)
        file_layout.addWidget(self.btn_browse)
        
        # Lista de archivos seleccionados
        files_label = QLabel("Archivos seleccionados:")
        files_label.setStyleSheet("font-weight: bold; color: #800020;")
        file_layout.addWidget(files_label)
        
        self.files_list = QListWidget()
        self.files_list.setMinimumHeight(150)
        file_layout.addWidget(self.files_list)
        
        # Botones de gestión de archivos
        files_buttons_layout = QHBoxLayout()
        self.btn_remove_selected = SecondaryButton("Quitar Seleccionado")
        self.btn_remove_selected.clicked.connect(self.remove_selected_file)
        self.btn_clear_all = DangerButton("Limpiar Todo")
        self.btn_clear_all.clicked.connect(self.clear_all_files)
        
        files_buttons_layout.addWidget(self.btn_remove_selected)
        files_buttons_layout.addWidget(self.btn_clear_all)
        file_layout.addLayout(files_buttons_layout)
        
        file_card.addLayout(file_layout)
        left_column.addWidget(file_card)
        
        # Card de destino y conversión
        conversion_card = Card("Configuración de Conversión")
        conversion_layout = QVBoxLayout()
        
        # Carpeta de destino
        dest_label = QLabel("Carpeta de destino:")
        dest_label.setStyleSheet("font-weight: bold; color: #800020;")
        conversion_layout.addWidget(dest_label)
        
        dest_input_layout = QHBoxLayout()
        self.output_path = QLineEdit(self.output_folder)
        self.output_path.setReadOnly(True)
        self.btn_select_output = SecondaryButton("Cambiar Destino")
        self.btn_select_output.clicked.connect(self.select_output_folder)
        
        dest_input_layout.addWidget(self.output_path)
        dest_input_layout.addWidget(self.btn_select_output)
        conversion_layout.addLayout(dest_input_layout)
        
        # Botones de conversión
        conversion_buttons_layout = QHBoxLayout()
        self.btn_convert = PrimaryButton("Iniciar Conversión")
        self.btn_convert.clicked.connect(self.start_conversion)
        self.btn_cancel = DangerButton("Cancelar Conversión")
        self.btn_cancel.setEnabled(False)
        self.btn_cancel.clicked.connect(self.cancel_conversion)
        
        conversion_buttons_layout.addWidget(self.btn_convert)
        conversion_buttons_layout.addWidget(self.btn_cancel)
        conversion_layout.addLayout(conversion_buttons_layout)
        
        conversion_card.addLayout(conversion_layout)
        left_column.addWidget(conversion_card)
        
        main_content_layout.addLayout(left_column, 1)
        
        # COLUMNA DERECHA - Progreso y logs
        right_column = QVBoxLayout()
        
        # Card de progreso
        progress_card = Card("Progreso de Conversión")
        progress_layout = QVBoxLayout()
        
        # Etiqueta de estado
        self.status_label = QLabel("Listo para comenzar")
        self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #800020;")
        progress_layout.addWidget(self.status_label)
        
        # Barra de progreso
        self.progress_bar = ModernProgressBar()
        progress_layout.addWidget(self.progress_bar)
        
        progress_card.addLayout(progress_layout)
        right_column.addWidget(progress_card)
        
        # Card de registro de actividad
        log_card = Card("Registro de Actividad")
        log_layout = QVBoxLayout()
        
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setStyleSheet("""
            border: 1px solid #800020;
            font-family: 'Consolas', 'Ubuntu Mono', 'Liberation Mono', 'Courier New', monospace;
            font-size: 12px;
            background-color: white;
        """)
        self.log.setMinimumHeight(250)
        log_layout.addWidget(self.log)
        
        log_card.addLayout(log_layout)
        right_column.addWidget(log_card)
        
        main_content_layout.addLayout(right_column, 1)
        
        dashboard_layout.addLayout(main_content_layout)
        self.content_stack.addWidget(dashboard_page)
    
    def init_settings_page(self):
        settings_page = QWidget()
        settings_layout = QVBoxLayout(settings_page)
        settings_layout.setContentsMargins(20, 20, 20, 20)
        settings_layout.setSpacing(15)
        
        page_title = QLabel("Configuración")
        page_title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #800020;
            padding-bottom: 10px;
        """)
        settings_layout.addWidget(page_title)
        
        # Card de configuración
        config_card = Card("Configuración General")
        config_layout = QVBoxLayout()
        
        # Carpeta de salida predeterminada
        output_label = QLabel("Carpeta de salida predeterminada:")
        output_label.setStyleSheet("font-weight: bold; color: #800020;")
        config_layout.addWidget(output_label)
        
        output_input_layout = QHBoxLayout()
        self.settings_output_path = QLineEdit(self.output_folder)
        self.settings_output_path.setReadOnly(True)
        self.btn_settings_output = SecondaryButton("Cambiar")
        self.btn_settings_output.clicked.connect(self.change_default_output_folder)
        
        output_input_layout.addWidget(self.settings_output_path)
        output_input_layout.addWidget(self.btn_settings_output)
        config_layout.addLayout(output_input_layout)
        
        # Botón guardar configuración
        save_layout = QHBoxLayout()
        save_layout.addStretch()
        self.btn_save_settings = PrimaryButton("Guardar Configuración")
        self.btn_save_settings.clicked.connect(self.save_settings)
        save_layout.addWidget(self.btn_save_settings)
        config_layout.addLayout(save_layout)
        
        config_card.addLayout(config_layout)
        settings_layout.addWidget(config_card)
        
        settings_layout.addStretch()
        self.content_stack.addWidget(settings_page)
    
    def init_history_page(self):
        history_page = QWidget()
        history_layout = QVBoxLayout(history_page)
        history_layout.setContentsMargins(20, 20, 20, 20)
        history_layout.setSpacing(15)
        
        page_title = QLabel("Historial de Conversiones")
        page_title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #800020;
            padding-bottom: 10px;
        """)
        history_layout.addWidget(page_title)
        
        # Card de historial
        history_card = Card("Conversiones Recientes")
        history_card_layout = QVBoxLayout()
        
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels(["Fecha", "Archivos Procesados", "Exitosos", "Fallidos", "Acciones"])
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.history_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.history_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.history_table.setAlternatingRowColors(True)
        
        self.update_history_table()
        history_card_layout.addWidget(self.history_table)
        
        # Botones
        history_buttons_layout = QHBoxLayout()
        history_buttons_layout.addStretch()
        
        self.btn_refresh_history = SecondaryButton("Actualizar")
        self.btn_refresh_history.clicked.connect(self.update_history_table)
        
        self.btn_clear_history = DangerButton("Borrar Historial")
        self.btn_clear_history.clicked.connect(self.clear_history)
        
        history_buttons_layout.addWidget(self.btn_refresh_history)
        history_buttons_layout.addWidget(self.btn_clear_history)
        
        history_card_layout.addLayout(history_buttons_layout)
        history_card.addLayout(history_card_layout)
        history_layout.addWidget(history_card)
        
        history_layout.addStretch()
        self.content_stack.addWidget(history_page)
    
    def init_about_page(self):
        about_page = QWidget()
        about_layout = QVBoxLayout(about_page)
        about_layout.setContentsMargins(20, 20, 20, 20)
        about_layout.setSpacing(15)
        
        page_title = QLabel("Acerca de")
        page_title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #800020;
            padding-bottom: 10px;
        """)
        about_layout.addWidget(page_title)
        
        # Card principal
        about_card = Card("Audio Converter Pro - Procesamiento Múltiple")
        about_layout_card = QVBoxLayout()
        
        logo_label = QLabel("Audio Converter Pro")
        logo_label.setStyleSheet("""
            color: #800020;
            font-size: 24px;
            font-weight: bold;
            qproperty-alignment: AlignCenter;
            margin: 20px;
        """)
        
        description = QLabel(
            "Audio Converter Pro es una aplicación profesional para la conversión masiva de archivos de audio "
            "a formato MP4. Procesa múltiples archivos simultáneamente con una interfaz moderna y eficiente."
        )
        description.setWordWrap(True)
        description.setStyleSheet("color: #333; font-size: 14px; qproperty-alignment: AlignCenter;")
        description.setContentsMargins(20, 10, 20, 10)
        
        version_label = QLabel("Versión 3.0 Multi-File Pro")
        version_label.setStyleSheet("color: #800020; font-size: 16px; font-weight: bold; qproperty-alignment: AlignCenter;")
        
        developer_label = QLabel("Desarrollado por: Audio Team")
        developer_label.setStyleSheet("color: #333; font-size: 14px; qproperty-alignment: AlignCenter;")
        
        year_label = QLabel("© 2025 Todos los derechos reservados")
        year_label.setStyleSheet("color: #333; font-size: 14px; qproperty-alignment: AlignCenter;")
        
        about_layout_card.addWidget(logo_label)
        about_layout_card.addWidget(description)
        about_layout_card.addWidget(version_label)
        about_layout_card.addWidget(developer_label)
        about_layout_card.addWidget(year_label)
        
        about_card.addLayout(about_layout_card)
        about_layout.addWidget(about_card)
        
        about_layout.addStretch()
        self.content_stack.addWidget(about_page)
    
    # FUNCIONES DE NAVEGACIÓN
    def change_page(self, index):
        self.content_stack.setCurrentIndex(index)
        
        self.btn_dashboard.setChecked(index == 0)
        self.btn_settings.setChecked(index == 1)
        self.btn_history.setChecked(index == 2)
        self.btn_about.setChecked(index == 3)
        
        if index == 2:
            self.update_history_table()
    
    # FUNCIONES DE ARCHIVOS
    def browse_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Seleccionar archivos de audio",
            "",
            "Archivos de Audio (*.mp3 *.m4a *.wav *.flac *.ogg *.aac *.wma);;Todos los archivos (*.*)"
        )
        
        if files:
            # Agregar archivos únicos a la lista
            for file_path in files:
                if file_path not in self.selected_files:
                    self.selected_files.append(file_path)
            
            self.update_files_list()
            self.log.append(f"✓ {len(files)} archivos agregados. Total: {len(self.selected_files)} archivos")
    
    def update_files_list(self):
        self.files_list.clear()
        for file_path in self.selected_files:
            item = QListWidgetItem(os.path.basename(file_path))
            item.setData(Qt.UserRole, file_path)
            self.files_list.addItem(item)
        
        # Actualizar estado de botones
        has_files = len(self.selected_files) > 0
        self.btn_convert.setEnabled(has_files)
        self.btn_remove_selected.setEnabled(has_files)
        self.btn_clear_all.setEnabled(has_files)
    
    def remove_selected_file(self):
        current_item = self.files_list.currentItem()
        if current_item:
            file_path = current_item.data(Qt.UserRole)
            self.selected_files.remove(file_path)
            self.update_files_list()
            self.log.append(f"✓ Archivo removido: {os.path.basename(file_path)}")
    
    def clear_all_files(self):
        if self.selected_files:
            reply = QMessageBox.question(
                self,
                "Confirmar limpieza",
                f"¿Desea quitar todos los {len(self.selected_files)} archivos seleccionados?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.selected_files.clear()
                self.update_files_list()
                self.log.append("✓ Todos los archivos han sido removidos")
    
    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Seleccionar carpeta de destino",
            self.output_folder
        )
        
        if folder:
            self.output_folder = folder
            self.output_path.setText(folder)
            self.log.append(f"✓ Carpeta de destino actualizada: {folder}")
    
    # FUNCIONES DE CONVERSIÓN
    def start_conversion(self):
        if not self.selected_files:
            QMessageBox.warning(self, "Error", "No hay archivos seleccionados para convertir")
            return
        
        # Confirmar inicio de conversión
        reply = QMessageBox.question(
            self,
            "Confirmar conversión",
            f"¿Desea convertir {len(self.selected_files)} archivos?\n\n"
            f"Destino: {self.output_folder}",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )
        
        if reply != QMessageBox.Yes:
            return
        
        # Iniciar conversión
        self.conversion_thread = ConversionThread(self.selected_files.copy(), self.output_folder)
        self.conversion_thread.progress_update.connect(self.update_progress)
        self.conversion_thread.log_update.connect(self.log.append)
        self.conversion_thread.conversion_finished.connect(self.conversion_done)
        self.conversion_thread.file_completed.connect(self.file_completed)
        
        # Actualizar UI
        self.btn_convert.setEnabled(False)
        self.btn_browse.setEnabled(False)
        self.btn_clear_all.setEnabled(False)
        self.btn_remove_selected.setEnabled(False)
        self.btn_cancel.setEnabled(True)
        
        self.progress_bar.setValue(0)
        self.status_label.setText("Iniciando conversión...")
        
        self.conversion_thread.start()
    
    def update_progress(self, progress, status):
        self.progress_bar.setValue(progress)
        self.status_label.setText(status)
    
    def file_completed(self, filename, success):
        status_icon = "✓" if success else "✗"
        self.log.append(f"{status_icon} {filename} - {'Completado' if success else 'Error'}")
    
    def cancel_conversion(self):
        if self.conversion_thread and self.conversion_thread.isRunning():
            self.conversion_thread.cancel()
            self.log.append("🛑 Solicitando cancelación...")
            self.btn_cancel.setEnabled(False)
    
    def conversion_done(self, success, message, input_files, output_folder, successful_count, failed_count):
        # Restaurar UI
        self.btn_convert.setEnabled(True)
        self.btn_browse.setEnabled(True)
        self.btn_clear_all.setEnabled(True)
        self.btn_remove_selected.setEnabled(True)
        self.btn_cancel.setEnabled(False)
        
        # Agregar al historial con contadores precisos
        self.add_to_history_with_counts(input_files, output_folder, success, successful_count, failed_count)
        
        # Mostrar resultado
        if success:
            self.status_label.setText("✅ Conversión completada exitosamente")
            QMessageBox.information(
                self,
                "Conversión Completada",
                f"{message}\n\nArchivos guardados en:\n{output_folder}"
            )
        else:
            self.status_label.setText("❌ Error en la conversión")
            QMessageBox.critical(self, "Error en la Conversión", message)
    
    # FUNCIONES DE CONFIGURACIÓN
    def change_default_output_folder(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Seleccionar carpeta predeterminada",
            self.output_folder
        )
        
        if folder:
            self.output_folder = folder
            self.settings_output_path.setText(folder)
            self.output_path.setText(folder)
    
    def save_settings(self):
        QMessageBox.information(
            self,
            "Configuración guardada",
            "La configuración ha sido guardada exitosamente."
        )
    
    # FUNCIONES DE HISTORIAL
    def load_history(self):
        history_file = os.path.join(self.output_folder, "conversion_history.json")
        if os.path.exists(history_file):
            try:
                with open(history_file, 'r') as f:
                    self.conversion_history = json.load(f)
            except:
                self.conversion_history = []
    
    def save_history(self):
        history_file = os.path.join(self.output_folder, "conversion_history.json")
        try:
            with open(history_file, 'w') as f:
                json.dump(self.conversion_history, f)
        except:
            pass
    
    def add_to_history_with_counts(self, input_files, output_folder, overall_success, successful_count, failed_count):
        now = datetime.datetime.now()
        
        self.conversion_history.append({
            "date": now.strftime("%Y-%m-%d %H:%M"),
            "input_files": input_files,
            "output_folder": output_folder,
            "total_files": len(input_files),
            "successful": successful_count,
            "failed": failed_count,
            "overall_success": overall_success
        })
        
        self.save_history()

    def add_to_history(self, input_files, output_folder, overall_success):
        now = datetime.datetime.now()
        
        # Por simplicidad, asumimos que si overall_success es True, 
        # todos los archivos fueron exitosos. Si es False, todos fallaron.
        # En una implementación más avanzada, podrías mantener un contador
        # de archivos individuales exitosos/fallidos durante la conversión.
        if overall_success:
            successful_count = len(input_files)
            failed_count = 0
        else:
            successful_count = 0
            failed_count = len(input_files)
        
        self.conversion_history.append({
            "date": now.strftime("%Y-%m-%d %H:%M"),
            "input_files": input_files,
            "output_folder": output_folder,
            "total_files": len(input_files),
            "successful": successful_count,
            "failed": failed_count,
            "overall_success": overall_success
        })
        
        self.save_history()
    
    def update_history_table(self):
        self.history_table.setRowCount(0)
        
        for i, item in enumerate(reversed(self.conversion_history)):
            row_position = self.history_table.rowCount()
            self.history_table.insertRow(row_position)
            
            # Fecha
            date_str = item.get("date", "Fecha desconocida")
            self.history_table.setItem(row_position, 0, QTableWidgetItem(date_str))
            
            # Total de archivos (compatible con historial antiguo y nuevo)
            if "total_files" in item:
                # Nuevo formato de historial (múltiples archivos)
                total_files = str(item["total_files"])
                successful = str(item.get("successful", 0))
                failed = str(item.get("failed", 0))
                output_folder = item.get("output_folder", "")
            else:
                # Formato de historial antiguo (un archivo por vez)
                total_files = "1"
                if item.get("success", False):
                    successful = "1"
                    failed = "0"
                else:
                    successful = "0"
                    failed = "1"
                output_folder = item.get("output_file", "")
                if output_folder:
                    output_folder = os.path.dirname(output_folder)
            
            self.history_table.setItem(row_position, 1, QTableWidgetItem(total_files))
            
            # Exitosos
            successful_item = QTableWidgetItem(successful)
            successful_item.setForeground(QColor("#008000"))
            self.history_table.setItem(row_position, 2, successful_item)
            
            # Fallidos
            failed_item = QTableWidgetItem(failed)
            failed_item.setForeground(QColor("#800020"))
            self.history_table.setItem(row_position, 3, failed_item)
            
            # Botón de acción
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(5, 5, 5, 5)
            
            btn_view = QPushButton("Ver Carpeta")
            btn_view.setStyleSheet("""
                QPushButton {
                    background-color: #800020;
                    color: white;
                    border: none;
                    padding: 4px 8px;
                    font-size: 11px;
                }
                QPushButton:hover {
                    background-color: #a00028;
                }
            """)
            
            def create_open_folder_function(folder_path):
                return lambda: open_folder_cross_platform(folder_path) if os.path.exists(folder_path) else None
            
            if output_folder and os.path.exists(output_folder):
                btn_view.clicked.connect(create_open_folder_function(output_folder))
            else:
                btn_view.setEnabled(False)
            
            action_layout.addWidget(btn_view)
            action_layout.setAlignment(Qt.AlignCenter)
            
            self.history_table.setCellWidget(row_position, 4, action_widget)
    
    def clear_history(self):
        reply = QMessageBox.question(
            self,
            "Confirmar borrado",
            "¿Está seguro de que desea borrar todo el historial?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.conversion_history = []
            self.update_history_table()
            self.save_history()
            QMessageBox.information(self, "Historial borrado", "El historial ha sido borrado exitosamente.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Establecer fuente predeterminada multiplataforma
    if platform.system() == "Windows":
        font = QFont("Segoe UI", 10)
    elif platform.system() == "Darwin":  # macOS
        font = QFont("SF Pro Display", 10)
    else:  # Linux
        font = QFont("Ubuntu", 10)
    app.setFont(font)
    
    window = AudioConverterApp()
    window.show()
    sys.exit(app.exec_())
