import os
import re
import struct
import binascii
import tkinter as tk
import numpy as np
import struct
import threading
from PIL import Image, ImageTk
from tkinter import messagebox, filedialog, ttk
from collections import namedtuple
from tkinter.ttk import Progressbar

# ------------------------
# INICIO DE Theme_Editor
# ------------------------

class ImageProcessorApp(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.root = parent 

        # Configurar el frame para expandirse y centrar su contenido
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.main_frame = tk.Frame(self)
        self.main_frame.grid(row=0, column=0)
        
        # Centrado del contenido dentro del main_frame
        self.main_frame.grid_rowconfigure("all", weight=1)
        self.main_frame.grid_columnconfigure("all", weight=1)

        self.input_folder_path = tk.StringVar()
        self.output_folder_path = tk.StringVar()

        self.progress_bar = Progressbar(self.main_frame, orient="horizontal", length=200, mode="determinate")
        self.progress_bar.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        self.input_folder_button = tk.Button(self.main_frame, text="Input Folder", command=self.select_input_folder)
        self.input_folder_button.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.output_folder_button = tk.Button(self.main_frame, text="Output Folder", command=self.select_output_folder)
        self.output_folder_button.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        self.save_button = tk.Button(self.main_frame, text="Save", command=self.save_changes)
        self.save_button.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        self.original_tk_images = {}
        self.images = []
        self.paginas = []
        self.pagina_actual = 0

        # Ventana flotante para imágenes
        self.image_viewer = tk.Toplevel(self.root)
        self.image_viewer.geometry("800x600")

        self.scrollbar = tk.Scrollbar(self.image_viewer, orient=tk.VERTICAL)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.canvas = tk.Canvas(self.image_viewer, yscrollcommand=self.scrollbar.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.image_viewer.grid_columnconfigure(0, weight=1)
        self.image_viewer.grid_rowconfigure(0, weight=1)

        self.image_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.image_frame, anchor=tk.NW)

        self.scrollbar.config(command=self.canvas.yview)
        self.image_frame.bind("<Configure>", lambda event, canvas=self.canvas: self.on_frame_configure(event, canvas))
        self.image_frame.bind("<MouseWheel>", self.on_mousewheel)

        # Botones "Next" y "Previous"
        self.prev_page_button_popup = tk.Button(self.image_viewer, text="Previous", command=self.prev_page)
        self.prev_page_button_popup.grid(row=1, column=0, pady=5, sticky="w")

        self.next_page_button_popup = tk.Button(self.image_viewer, text="Next", command=self.next_page)
        self.next_page_button_popup.grid(row=1, column=0, pady=5, sticky="e")

        # Diccionario para almacenar las referencias a los tk_image originales
        self.original_tk_images = {}

        # Inicializar la visualización de imágenes
        self.images = []
        self.paginas = []
        self.pagina_actual = 0

        self.bgra_files = [
            "aepic.nec", "appvc.ikb", "awusa.tax", "bttlve.kbp", "certlm.msa", "djctq.rsd", "djoin.nec", "dxdiag.bin",
            "dxkgi.ctp", "ectte.bke", "esent.bvs", "exaxz.hsp", "fvecpl.ai", "gakne.ctp", "gkavc.ers", "htui.kcc",
            "icm32.dll", "igc64.dll", "irmon.tax", "itiss.ers", "ke89a.bvs", "lk7tc.bvs", "msgsm.dll", "mssvp.nec",
            "normidna.bin", "ntdll.bvs", "nvinf.hsp", "okcg2.old", "pcadm.nec", "rmapi.tax", "sensc.bvs", "sfcdr.cpl", "subst.tax",
            "ucby4.aax", "vidca.bvs", "vssvc.nec", "wshrm.nec"            
        ]

    def on_frame_configure(self, event, canvas):
        canvas.config(scrollregion=canvas.bbox("all"))

    def on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * int(event.delta / 120), "units")

    def select_input_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.input_folder_path.set(folder_path)
    
            # Verificar la existencia de Foldername.ini o Foldernamx.ini
            ini_file = os.path.join(folder_path, "Foldername.ini")
            inix_file = os.path.join(folder_path, "Foldernamx.ini")
    
            if os.path.exists(ini_file):
                self.images = [
            {"name": "fixas.ctp", "size": (640, 480)},
            {"name": "urlkp.bvs", "size": (640, 480)},
            {"name": "certlm.msa", "size": (40, 24)},
            {"name": "drivr.ers", "size": (640, 480)},
            {"name": "c1eac.pal", "size": (640, 480)},
            {"name": "djctq.rsd", "size": (40, 24)},
            {"name": "icuin.cpl", "size": (640, 480)},
            {"name": "ihdsf.bke", "size": (640, 480)},
            {"name": "dxdiag.bin", "size": (40, 24)},          
            {"name": "xajkg.hsp", "size": (640, 480)},
            {"name": "fltmc.sta", "size": (640, 480)},
            {"name": "fvecpl.ai", "size": (40, 24)},
            {"name": "qwave.bke", "size": (640, 480)},
            {"name": "cero.phl", "size": (640, 480)},
            {"name": "htui.kcc", "size": (40, 24)},
            {"name": "irftp.ctp", "size": (640, 480)},
            {"name": "efsui.stc", "size": (640, 480)},
            {"name": "icm32.dll", "size": (40, 24)},
            {"name": "hctml.ers", "size": (640, 480)},
            {"name": "apisa.dlk", "size": (640, 480)},
            {"name": "msgsm.dll", "size": (40, 24)},
            {"name": "aepic.nec", "size": (1008, 164)},
            {"name": "appvc.ikb", "size": (150, 214)},
            {"name": "awusa.tax", "size": (1008, 164)},
            {"name": "bisrv.nec", "size": (640, 480)},
            {"name": "bttlve.kbp", "size": (60, 144)},
            {"name": "cketp.bvs", "size": (640, 816)},
            {"name": "d2d1.hgp", "size": (640, 480)},
            {"name": "dism.cef", "size": (640, 480)},
            {"name": "djoin.nec", "size": (1008, 164)},
            {"name": "dpskc.ctp", "size": (640, 320)},
            {"name": "dsuei.cpl", "size": (640, 480)},
            {"name": "dxva2.nec", "size": (640, 480)},
            {"name": "dxkgi.ctp", "size": (1008, 164)},
            {"name": "ectte.bke", "size": (161, 126)},
            {"name": "esent.bvs", "size": (1008, 164)},
            {"name": "exaxz.hsp", "size": (152, 1224)},
            {"name": "gakne.ctp", "size": (576, 256)},
            {"name": "gkavc.ers", "size": (576, 256)},
            {"name": "hlink.bvs", "size": (640, 480)},
            {"name": "igc64.dll", "size": (217, 37)},
            {"name": "irmon.tax", "size": (1008, 164)},
            {"name": "itiss.ers", "size": (1008, 164)},
            {"name": "jccatm.kbp", "size": (640, 480)},
            {"name": "ke89a.bvs", "size": (1008, 164)},
            {"name": "kmbcj.acp", "size": (640, 480)},
            {"name": "lfsvc.dll", "size": (640, 480)},
            {"name": "lk7tc.bvs", "size": (52, 192)},
            {"name": "lkvax.aef", "size": (640, 480)},
            {"name": "mkhbc.rcv", "size": (640, 1440)},
            {"name": "mksh.rcv", "size": (640, 480)},
            {"name": "mssvp.nec", "size": (1008, 164)},
            {"name": "normidna.bin", "size": (40, 24)},
            {"name": "ntdll.bvs", "size": (1008, 164)},
            {"name": "nvinf.hsp", "size": (16, 240)},
            {"name": "okcg2.old", "size": (32, 32)},
            {"name": "pcadm.nec", "size": (1008, 164)},
            {"name": "pwsso.occ", "size": (640, 480)},
            {"name": "qasf.bel", "size": (640, 480)},
            {"name": "rmapi.tax", "size": (640, 480)},
            {"name": "sdclt.occ", "size": (120, 240)},
            {"name": "sensc.bvs", "size": (1008, 164)},
            {"name": "sfcdr.cpl", "size": (576, 1344)},
            {"name": "subst.tax", "size": (1008, 164)},
            {"name": "ucby4.aax", "size": (1008, 164)},
            {"name": "uyhbc.dck", "size": (640, 480)},
            {"name": "vidca.bvs", "size": (1008, 164)},
            {"name": "vssvc.nec", "size": (1008, 164)},
            {"name": "wshrm.nec", "size": (217, 37)},
            {"name": "ztrba.nec", "size": (64, 320)},
        ]
            elif os.path.exists(inix_file):
                self.images = [
            {"name": "m01.gb", "size": (640, 480)},
            {"name": "m01.mm", "size": (640, 480)},
            {"name": "m01.gi", "size": (40, 24)},
            {"name": "m02.gb", "size": (640, 480)},
            {"name": "m02.mm", "size": (640, 480)},
            {"name": "m02.gi", "size": (40, 24)},
            {"name": "m03.gb", "size": (640, 480)},
            {"name": "m03.mm", "size": (640, 480)},
            {"name": "m03.gi", "size": (40, 24)},
            {"name": "m04.gb", "size": (640, 480)},
            {"name": "m04.mm", "size": (640, 480)},
            {"name": "m04.gi", "size": (40, 24)},
            {"name": "m05.gb", "size": (640, 480)},
            {"name": "m05.mm", "size": (640, 480)},
            {"name": "m05.gi", "size": (40, 24)},
            {"name": "m06.gb", "size": (640, 480)},
            {"name": "m06.mm", "size": (640, 480)},
            {"name": "m06.gi", "size": (40, 24)},
            {"name": "m07.gb", "size": (640, 480)},
            {"name": "m07.mm", "size": (640, 480)},
            {"name": "m07.gi", "size": (40, 24)},
            {"name": "m08.gb", "size": (640, 480)},
            {"name": "m08.mm", "size": (640, 480)},
            {"name": "m08.gi", "size": (40, 24)},
            {"name": "m09.gb", "size": (640, 480)},
            {"name": "m09.mm", "size": (640, 480)},
            {"name": "m09.gi", "size": (40, 24)},
            {"name": "m10.gb", "size": (640, 480)},
            {"name": "m10.mm", "size": (640, 480)},
            {"name": "m10.gi", "size": (40, 24)},
            {"name": "m11.gb", "size": (640, 480)},
            {"name": "m11.mm", "size": (640, 480)},
            {"name": "m11.gi", "size": (40, 24)},
            {"name": "m12.gb", "size": (640, 480)},
            {"name": "m12.mm", "size": (640, 480)},
            {"name": "m12.gi", "size": (40, 24)},
            {"name": "sfcdr.cpl", "size": (576, 2184)}, 
            {"name": "aepic.nec", "size": (1008, 164)},
            {"name": "appvc.ikb", "size": (150, 214)},
            {"name": "awusa.tax", "size": (1008, 164)},
            {"name": "bisrv.nec", "size": (640, 480)},
            {"name": "bttlve.kbp", "size": (60, 144)},
            {"name": "cketp.bvs", "size": (640, 816)},
            {"name": "d2d1.hgp", "size": (640, 480)},
            {"name": "dism.cef", "size": (640, 480)},
            {"name": "djoin.nec", "size": (1008, 164)},
            {"name": "dpskc.ctp", "size": (640, 320)},
            {"name": "dsuei.cpl", "size": (640, 480)},    
            {"name": "dxva2.nec", "size": (640, 480)},
            {"name": "dxkgi.ctp", "size": (1008, 164)},
            {"name": "ectte.bke", "size": (161, 126)},
            {"name": "esent.bvs", "size": (1008, 164)},
            {"name": "exaxz.hsp", "size": (152, 1224)},
            {"name": "gakne.ctp", "size": (576, 256)},
            {"name": "gkavc.ers", "size": (576, 256)},
            {"name": "hlink.bvs", "size": (640, 480)},
            {"name": "igc64.dll", "size": (217, 37)},
            {"name": "irmon.tax", "size": (1008, 164)},
            {"name": "itiss.ers", "size": (1008, 164)},
            {"name": "jccatm.kbp", "size": (640, 480)},
            {"name": "ke89a.bvs", "size": (1008, 164)},
            {"name": "kmbcj.acp", "size": (640, 480)},
            {"name": "lfsvc.dll", "size": (640, 480)},
            {"name": "lk7tc.bvs", "size": (52, 192)},
            {"name": "lkvax.aef", "size": (640, 480)},
            {"name": "mkhbc.rcv", "size": (640, 1440)},
            {"name": "mksh.rcv", "size": (640, 480)},
            {"name": "mssvp.nec", "size": (1008, 164)},
            {"name": "normidna.bin", "size": (40, 24)},
            {"name": "ntdll.bvs", "size": (1008, 164)},
            {"name": "nvinf.hsp", "size": (16, 240)},
            {"name": "okcg2.old", "size": (32, 32)},
            {"name": "pcadm.nec", "size": (1008, 164)},
            {"name": "pwsso.occ", "size": (640, 480)},
            {"name": "qasf.bel", "size": (640, 480)},
            {"name": "rmapi.tax", "size": (640, 480)},
            {"name": "sdclt.occ", "size": (120, 240)},
            {"name": "sensc.bvs", "size": (1008, 164)},
            {"name": "subst.tax", "size": (1008, 164)},
            {"name": "ucby4.aax", "size": (1008, 164)},
            {"name": "uyhbc.dck", "size": (640, 480)},
            {"name": "vidca.bvs", "size": (1008, 164)},
            {"name": "vssvc.nec", "size": (1008, 164)},
            {"name": "wshrm.nec", "size": (217, 37)},
            {"name": "ztrba.nec", "size": (64, 320)},
 ]
            else:
                self.images = []
                messagebox.showwarning("Warning", "No valid .ini file found in the selected folder.")
    
            # Llamar a load_images para cargar las imágenes
            self.load_images()
    
            # Dividir las imágenes en páginas
            self.paginas = [self.images[i:i + 1] for i in range(0, len(self.images), 1)]
            self.pagina_actual = 0
            self.update_images()

    def select_output_folder(self):
        folder_path = filedialog.askdirectory()
        self.output_folder_path.set(folder_path)

    def update_images(self):
        if self.main_frame.winfo_exists():
            self.display_images()

        # Cantidad de imágenes por página
        imagenes_por_pagina = 1

        # Dividir las imágenes en páginas
        self.paginas = [self.images[i:i + imagenes_por_pagina] for i in range(0, len(self.images), imagenes_por_pagina)]

        # Página actual (inicialmente la primera)
        self.pagina_actual = 0

        # Inicializar la visualización de imágenes
        self.display_images()


    def load_images(self):
        input_folder = self.input_folder_path.get()

        # Verificar si la carpeta de entrada está seleccionada
        if not input_folder:
            return

        supported_files = [
            "apisa.dlk", "bisrv.nec", "c1eac.pal", "cero.phl", "cketp.bvs", "d2d1.hgp", "dism.cef", "dpskc.ctp",
            "drivr.ers", "dsuei.cpl", "dxva2.nec", "efsui.stc", "fixas.ctp", "fltmc.sta", "hctml.ers", "hlink.bvs",
            "icuin.cpl", "ihdsf.bke", "irftp.ctp", "jccatm.kbp", "kmbcj.acp", "lfsvc.dll", "lkvax.aef", "mkhbc.rcv",
            "mksh.rcv", "pwsso.occ", "qasf.bel", "qwave.bke", "sdclt.occ", "urlkp.bvs", "uyhbc.dck", "xajkg.hsp", 
            "ztrba.nec","m01.gb","m01.mm","m02.gb","m02.mm","m03.gb","m03.mm",
            "m04.gb","m04.mm","m05.gb","m05.mm","m06.gb","m06.mm",
            "m07.gb","m07.mm","m08.gb","m08.mm","m09.gb","m09.mm",
            "m10.gb","m10.mm","m11.gb","m11.mm","m12.gb","m12.mm",
        ]

        bgra_files = [
            "aepic.nec", "appvc.ikb", "awusa.tax", "bttlve.kbp", "certlm.msa", "djctq.rsd", "djoin.nec", "dxdiag.bin",
            "dxkgi.ctp", "ectte.bke", "esent.bvs", "exaxz.hsp", "fvecpl.ai", "gakne.ctp", "gkavc.ers", "htui.kcc",
            "icm32.dll", "igc64.dll", "irmon.tax", "itiss.ers", "ke89a.bvs", "lk7tc.bvs", "msgsm.dll", "mssvp.nec",
            "normidna.bin", "ntdll.bvs", "nvinf.hsp", "okcg2.old", "pcadm.nec", "rmapi.tax", "sensc.bvs", "sfcdr.cpl", "subst.tax",
            "ucby4.aax", "vidca.bvs", "vssvc.nec", "wshrm.nec","m01.gi","m02.gi","m03.gi","m04.gi","m05.gi",
            "m06.gi","m07.gi","m08.gi","m09.gi","m10.gi","m11.gi","m12.gi"
        ]

        for image_data in self.images:
            file_name = image_data["name"]
            size = image_data["size"]

            file_path = f"{input_folder}/{file_name}"

            try:
                # Verificar si el nombre de archivo está en la lista de archivos compatibles
                if file_name in supported_files:
                    # Leer el archivo y convertir los datos BGRA a imagen PIL
                    with open(file_path, 'rb') as file:
                        raw_data = file.read()
                        image = Image.frombytes('RGB', (size[0], size[1]), raw_data, 'raw', 'BGR;16', 0, -1)
                    image = image.transpose(Image.FLIP_TOP_BOTTOM)
                elif file_name in bgra_files:
                    # Leer el archivo y convertir los datos BGRA a imagen PIL
                    with open(file_path, 'rb') as file:
                        raw_data = file.read()
                        image = Image.frombytes('RGBA', (size[0], size[1]), raw_data, 'raw', 'BGRA', 0, -1)
                    image = image.transpose(Image.FLIP_TOP_BOTTOM)
                else:
                    # Si no es un archivo de los seleccionados, cargar la imagen como antes
                    image = Image.open(file_path)

                # Escalar la imagen a miniatura
                image.thumbnail(size)

                # Crear PhotoImage y almacenarlo en el diccionario image_data
                tk_image = ImageTk.PhotoImage(image)
                image_data["tk_image"] = tk_image

                # Almacenar una referencia al tk_image original
                self.original_tk_images[file_name] = tk_image.copy()
            except Exception as e:
                print(f"Could not load image {file_name}: {str(e)}")

    def display_images(self):
        # Establecer el tamaño deseado para la ventana flotante
        self.image_viewer.geometry("1280x600")

        # Limpiar el contenido actual del lienzo
        for widget in self.image_frame.winfo_children():
            widget.destroy()

        # Mostrar imágenes en la cuadrícula en el lienzo existente
        row, col = 0, 0
        for image_data in self.paginas[self.pagina_actual]:
            image_name = image_data["name"]
            tk_image = self.original_tk_images.get(image_name, None)  # Obtener el tk_image original del diccionario

            if tk_image:
                # Si hay un tk_image original, utilizarlo
                image_label = tk.Label(self.image_frame, image=tk_image, text=image_name, compound=tk.TOP)
            else:
                # Si no hay un tk_image original, utilizar el tk_image actualizado o el texto
                tk_image = image_data.get("tk_image")
                if tk_image:
                    image_label = tk.Label(self.image_frame, image=tk_image, text=image_name, compound=tk.TOP)
                else:
                    image_label = tk.Label(self.image_frame, text=image_name)

            image_label.grid(row=row, column=col)

            change_button = tk.Button(self.image_frame, text="Change", command=lambda data=image_data: self.change_image(data))
            change_button.grid(row=row + 1, column=col)

            col += 1
            if col > 5:
                col = 0
                row += 2

        # Ajustar el área de desplazamiento al tamaño del lienzo interior
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        # Añadir el botón de descarga debajo de la imagen actual en la cuadrícula
        for widget in self.image_frame.winfo_children():
            if isinstance(widget, tk.Label) and widget.cget("text") == self.paginas[self.pagina_actual][0]["name"]:
                download_button = tk.Button(self.image_frame, text="Download", command=self.download_image)
                download_button.grid(row=widget.grid_info()["row"] + 2, column=widget.grid_info()["column"])
                break


    def download_image(self):
        output_folder = self.output_folder_path.get()

        # Verificar si se ha seleccionado "Output Folder"
        if not output_folder:
            self.show_error_message("Select the output folder.")
            return

        # Obtener la imagen actual
        current_image_data = self.paginas[self.pagina_actual][0]
        image_name = current_image_data["name"]
        tk_image = current_image_data.get("tk_image")

        # Verificar si la imagen actual tiene una representación en PhotoImage
        if tk_image:
            # Convertir PhotoImage a Image
            image = ImageTk.getimage(tk_image)

            # Guardar la imagen en la carpeta de salida
            try:
                image.save(f"{output_folder}/{image_name}.png", format="PNG")
                self.show_success_message(f"Image '{image_name}' downloaded successfully.")
            except Exception as e:
                self.show_error_message(f"Could not save image {image_name}: {str(e)}")

    def change_image(self, image_data):
        new_image_path = filedialog.askopenfilename()
        if new_image_path:
            new_image = Image.open(new_image_path)
            new_image = new_image.resize(image_data["size"])  # Redimensionar la imagen al tamaño esperado
            tk_new_image = ImageTk.PhotoImage(new_image)
            image_data["tk_image"] = tk_new_image

            # Actualizar el tk_image original en el diccionario
            self.original_tk_images[image_data["name"]] = tk_new_image

            # Buscar la etiqueta de la imagen actual en la cuadrícula en el lienzo
            for widget in self.image_frame.winfo_children():
                if isinstance(widget, tk.Label) and widget.cget("text") == image_data["name"]:
                    # Actualizar la etiqueta de la imagen en el lienzo
                    widget.configure(image=tk_new_image)
                    break

    def save_changes(self):
        output_folder = self.output_folder_path.get()

        # Verificar si se ha seleccionado "Output Folder"
        if not output_folder:
            self.show_error_message("Select the output folder.")
            return

        # Iniciar un hilo para realizar la operación de grabación
        threading.Thread(target=self.save_changes_thread, args=(output_folder,)).start()

    def save_changes_thread(self, output_folder):
        # Lógica para guardar las imágenes en la carpeta de salida
        total_images = len(self.images)
        progress_step = 100 / total_images
        progress = 0

        for index, image_data in enumerate(self.images, start=1):
            image_name = image_data["name"]
            tk_image = image_data.get("tk_image")

            if tk_image:
                # Convertir PhotoImage a Image
                image = ImageTk.getimage(tk_image)

                # Verificar si el archivo actual es uno de los que requiere conversión a RGB565
                if image_name in self.bgra_files:  # Aquí se corrige
                    # Convertir la imagen PIL a datos BGRA
                    raw_data = image.tobytes('raw', 'BGRA')
                else:
                    # Realizar la conversión a RGB565 Little Endian
                    raw_data = self.convert_to_rgb565(image)

                # Guardar la imagen en la carpeta de salida
                try:
                    with open(f"{output_folder}/{image_name}", 'wb') as file:
                        file.write(raw_data)
                except Exception as e:
                    self.show_error_message(f"Could not save image {image_name}: {str(e)}")
                    return
            
            # Actualizar la barra de progreso
            progress += progress_step
            self.update_progress(progress)

        # Mostrar mensaje de éxito
        self.show_success_message("Changes saved successfully.")

    def update_progress(self, value):
        # Actualizar la barra de progreso
        self.progress_bar["value"] = value
        self.main_frame.update_idletasks()

    def convert_to_rgb565(self, image):
        # Obtener los datos de píxeles RGB
        rgb_data = list(image.getdata())

        # Convertir a formato RGB565 Little Endian
        rgb565_data = []
        for pixel in rgb_data:
            r, g, b = pixel[:3]  # Tomar solo los primeros tres valores (R, G, B)
            rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
            rgb565_data.extend(struct.pack('<H', rgb565))

        return bytes(rgb565_data)

    def show_error_message(self, message):
        tk.messagebox.showerror("Error", message)

    def show_success_message(self, message):
        tk.messagebox.showinfo("Success", message)

    def prev_page(self):
        if self.pagina_actual > 0:
            self.pagina_actual -= 1
            self.display_images()

    def next_page(self):
        if self.pagina_actual < len(self.paginas) - 1:
            self.pagina_actual += 1
            self.display_images()

# ------------------------
# FIN DE Theme_Editor
# ------------------------

# ------------------------
# INICIO DE ZFBimagesToolSparda
# ------------------------

class ZFBimagesTool(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.master = parent
        self.stop_flag = threading.Event()

        # --- Tamaños de imagen ---
        self.ImageSize = namedtuple('ImageSize', [
            "hyper_width", "hyper_height", 
            "default_width", "default_height", 
            "init_width", "init_height"
        ])
        self.img = self.ImageSize(
            hyper_width="640", hyper_height="480", 
            default_width="144", default_height="208", 
            init_width="144", init_height="208"
        )

        # Centrado en el contenedor
        self.grid(row=0, column=0)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Frame interno centrado
        self.inner_frame = tk.Frame(self)
        self.inner_frame.grid(row=0, column=0)
        self.inner_frame.grid_columnconfigure(0, weight=1)

        # Crear la interfaz dentro del inner_frame
        self.create_widgets()

    def create_widgets(self):
        # Fuentes
        bold_font = ("Helvetica", 10, "bold")
        label_font = ("Helvetica", 10, "normal")

        # Cambiar todos los `self.master` por `self.inner_frame` para centrar
        parent = self.inner_frame

        # Input Folder
        self.create_label_entry(
            row=1, label_text="Input Folder:", var_name="input_folder_var", 
            button_text="Browse", button_command=self.select_input_folder, label_font=label_font, parent=parent
        )

        # Output Folder
        self.create_label_entry(
            row=2, label_text="Output Folder:", var_name="output_folder_var", 
            button_text="Browse", button_command=self.select_output_folder, label_font=label_font, parent=parent
        )

        self.arcade_var = tk.BooleanVar(value=False)
        self.arcade_checkbutton = tk.Checkbutton(
            parent, text="ARCADE", variable=self.arcade_var, command=self.toggle_arcade, font=label_font
        )
        self.arcade_checkbutton.grid(row=3, column=0, columnspan=2, sticky="w", padx=10)

        self.create_core_and_extension(label_font, parent)
        self.create_image_size_widgets(label_font, parent)

        self.create_zfb_button = tk.Button(
            parent, text="Create ZXX Files", command=self.execute_create_zfb, font=("Helvetica", 14)
        )
        self.create_zfb_button.grid(row=7, column=0, columnspan=7, pady=10)

        self.stop_button = tk.Button(
            parent, text="STOP", command=self.stop_processing, font=("Helvetica", 14), fg="red"
        )
        self.stop_button.grid(row=7, column=4, columnspan=2, pady=10)
        self.stop_button["state"] = "disabled"

        self.msg_var = tk.StringVar()
        tk.Label(parent, textvariable=self.msg_var, fg="green", font=label_font).grid(row=8, column=0, columnspan=7, sticky="w", padx=10)

        self.progress = ttk.Progressbar(parent, orient="horizontal", length=400, mode="determinate")
        self.progress.grid(row=9, column=0, columnspan=7, padx=10, pady=5, sticky="ew")

        # Inicialización de valores predeterminados
        c_dir = os.getcwd()
        self.master.bind("<Return>", self.entry_enter_key)
        self.input_folder_var_entry.focus_set()
        self.input_folder_var.set("")
        self.output_folder_var.set("")
        self.img_mode.set("manual") 
        self.imgwidth_var.set(self.img.init_width)
        self.imgheight_var.set(self.img.init_height)
        self.toggle_img_mode()

    def disable_inputs(self):
        # Entradas
        self.input_folder_var_entry.config(state="disabled")
        self.output_folder_var_entry.config(state="disabled")
        self.core_entry.config(state="disabled")
        self.extension_entry.config(state="disabled")
        self.imgwidth_entry.config(state="disabled")
        self.imgheight_entry.config(state="disabled")

        # Botones
        self.input_folder_var_button.config(state="disabled")
        self.output_folder_var_button.config(state="disabled")
        self.arcade_checkbutton.config(state="disabled")
        self.hyperscreen_checkbox.config(state="disabled")

        # Radio buttons
        for child in self.master.grid_slaves():
            if isinstance(child, tk.Radiobutton):
                child.config(state="disabled")

    def enable_inputs(self):
        # Entradas
        self.input_folder_var_entry.config(state="normal")
        self.output_folder_var_entry.config(state="normal")
        self.core_entry.config(state="normal")
        self.extension_entry.config(state="normal")
        self.imgwidth_entry.config(state="normal")
        self.imgheight_entry.config(state="normal")

        # Botones
        self.input_folder_var_button.config(state="normal")
        self.output_folder_var_button.config(state="normal")
        self.arcade_checkbutton.config(state="normal")
        self.hyperscreen_checkbox.config(state="normal")

        # Radio buttons
        for child in self.master.grid_slaves():
            if isinstance(child, tk.Radiobutton):
                child.config(state="normal")

    def stop_processing(self):
        self.stop_flag.set()
        self.msg_var.set("Stopping...")

    def create_label_entry(self, row, label_text, var_name, button_text, button_command, label_font, parent):
        tk.Label(parent, text=label_text, font=label_font).grid(row=row, column=0, sticky="w", padx=10)

        var = tk.StringVar()
        setattr(self, var_name, var)

        entry = tk.Entry(parent, textvariable=var, width=70)
        setattr(self, f"{var_name}_entry", entry)
        entry.grid(row=row, column=1, columnspan=5, sticky="w", padx=5)

        button = tk.Button(parent, text=button_text, command=button_command)
        setattr(self, f"{var_name}_button", button)
        button.grid(row=row, column=6, sticky="w")

    def create_core_and_extension(self, label_font, parent):
        self.core_var = tk.StringVar()
        self.core_label = tk.Label(parent, text="CORE:", font=label_font)
        self.core_label.grid(row=4, column=0, sticky="w", padx=10)
        self.core_entry = tk.Entry(parent, textvariable=self.core_var, width=10)
        self.core_entry.grid(row=4, column=1, sticky="w", padx=6)

        self.extension_frame = tk.Frame(parent, bd=0, relief="flat")
        self.extension_frame.grid(row=4, column=2, columnspan=3, sticky="w")
        self.extension_var = tk.StringVar()
        self.extension_label = tk.Label(self.extension_frame, text="EXTENSION:", font=label_font)
        self.extension_label.grid(row=0, column=0, sticky="w", padx=5)
        self.extension_entry = tk.Entry(self.extension_frame, textvariable=self.extension_var, width=10)
        self.extension_entry.grid(row=0, column=1, columnspan=2, sticky="w", padx=15)

    def create_image_size_widgets(self, label_font, parent):
        self.img_mode = tk.StringVar(value="auto")
        auto_rb = tk.Radiobutton(parent, text="auto", variable=self.img_mode, value="auto", command=self.toggle_img_mode, font=label_font)
        auto_rb.grid(row=5, column=1, sticky="w", padx=5)
        manual_rb = tk.Radiobutton(parent, text="manual", variable=self.img_mode, value="manual", command=self.toggle_img_mode, font=label_font)
        manual_rb.grid(row=5, column=2, sticky="w")

        self.img_size_var = tk.StringVar()
        tk.Label(parent, textvariable=self.img_size_var, fg="green", anchor="w").grid(row=5, column=3, columnspan=3, sticky="ew")

        self.img_mode_frame = tk.Frame(parent)
        self.img_mode_frame.grid(row=6, column=1, columnspan=5, sticky="w", padx=5)

        self.imgwidth_var = tk.StringVar(value=self.img.init_width)
        self.imgheight_var = tk.StringVar(value=self.img.init_height)
        self.img_hyperscreen_var = tk.BooleanVar(value=True)

        tk.Label(parent, text="Image Size:", font=label_font).grid(row=5, column=0, sticky="w", padx=10)
        self.imgwidth_entry = tk.Entry(self.img_mode_frame, textvariable=self.imgwidth_var, width=10, font=label_font)
        self.imgwidth_entry.grid(row=0, column=0, sticky="w", padx=(2, 0))
        self.imgwidth_var.trace_add("write", self.imgsize_input_callback)
        tk.Label(self.img_mode_frame, text="x", font=label_font).grid(row=0, column=1, sticky="w", padx=3)
        self.imgheight_entry = tk.Entry(self.img_mode_frame, textvariable=self.imgheight_var, width=10, font=label_font)
        self.imgheight_entry.grid(row=0, column=2, sticky="w")
        self.imgheight_var.trace_add("write", self.imgsize_input_callback)

        self.hyperscreen_checkbox = tk.Checkbutton(
            self.img_mode_frame, text="HyperScreen", variable=self.img_hyperscreen_var,
            command=self.toggle_hyperscreen, font=label_font
        )
        self.hyperscreen_checkbox.grid(row=0, column=3, sticky="w", padx=15)
        self.toggle_img_mode()

    def entry_enter_key(self, event):
        if event.keysym == "Return":
            focused_widget = self.master.focus_get()
            if focused_widget["state"] == "disabled":
                return
            if focused_widget == self.input_folder_var_entry:
                self.output_folder_var_entry.focus_set()
            if focused_widget == self.output_folder_var_entry:
                self.arcade_checkbutton.focus_set()
            if focused_widget == self.arcade_checkbutton:
                if self.arcade_var.get():
                    self.create_zfb_button.focus_set()
                else:
                    self.core_entry.focus_set()
            if focused_widget == self.core_entry:
                self.extension_entry.focus_set()
            if focused_widget == self.extension_entry:
                self.create_zfb_button.focus_set()
            if focused_widget == self.imgwidth_entry:
                self.imgheight_entry.focus_set()
            if focused_widget == self.imgheight_entry:
                self.create_zfb_button.focus_set()
            if focused_widget == self.create_zfb_button:
                self.execute_create_zfb()
            if focused_widget == self.stop_button:
                self.stop_processing()

    def core_input_callback(self, *args):
        self.extension_var.set(self.core_var.get())

    def imgsize_input_callback(self, *args):
        self.img_hyperscreen_var.set(self.check_image_size())

    def check_image_size(self, img_size=None):
        arg_provided = (img_size is not None)

        width = 0
        height = 0
        if img_size is None:
            try:
                width = int(self.imgwidth_var.get() or 0)
            except ValueError:
                self.imgwidth_var.set("0")
                return False

            try:
                height = int(self.imgheight_var.get() or 0)
            except ValueError:
                self.imgheight_var.set("0")
                return False

            img_size = (width, height)
        else:
            self.imgwidth_var.set(str(img_size[0]))
            self.imgheight_var.set(str(img_size[1]))

        if img_size[0] == int(self.img.default_width) and img_size[1] == int(self.img.default_height):
            mode = 0
        elif img_size[0] >= 360 or img_size[1] >= 360:
            mode = 1
        else:
            mode = 2

        size_txt = "(" + str(img_size[0]) + " x " + str(img_size[1]) + " ["
        if mode == 1:
            size_txt += "HyperScreen"
        elif mode == 2:
            size_txt += "Custom"
        else:
            size_txt += "Default"
        size_txt += "])"

        if arg_provided or self.img_mode.get() != "auto":
            self.img_size_var.set(size_txt)

        return mode == 1

    def toggle_img_mode(self):
        if self.img_mode.get() == "manual":
            self.img_mode_frame.grid()
            self.check_image_size()
        else:
            self.img_mode_frame.grid_remove()
            self.img_size_var.set("")

    def toggle_hyperscreen(self):
        if self.img_hyperscreen_var.get():
            self.imgwidth_var.set(self.img.hyper_width)
            self.imgheight_var.set(self.img.hyper_height)
        else:
            self.imgwidth_var.set(self.img.default_width)
            self.imgheight_var.set(self.img.default_height)
        self.check_image_size()

    def toggle_arcade(self):
        if self.arcade_var.get():
            # Ocultar los campos CORE y EXTENSION
            self.core_entry.grid_remove()
            self.extension_entry.grid_remove()
            self.core_label.grid_remove()
            self.extension_label.grid_remove()
            self.extension_frame.grid_remove()
        else:
            # Mostrar los campos CORE y EXTENSION
            self.core_entry.grid()
            self.extension_entry.grid()
            self.core_label.grid()
            self.extension_label.grid()
            self.extension_frame.grid()


    def execute_create_zfb(self):
        if self.img_mode.get() == "manual":
            try:
                width = int(self.imgwidth_var.get())
                height = int(self.imgheight_var.get())
                if width < int(self.img.default_width) or height < int(self.img.default_height):
                    messagebox.showerror("Image Size Error", "Image size must be at least " + self.img.default_width + " x " + self.img.default_height + ".")
                    return
                if width > int(self.img.hyper_width) or height > int(self.img.hyper_height):
                    messagebox.showerror("Image Size Error", "Image size must be at most " + self.img.hyper_width + " x " + self.img.hyper_height + ".")
                    return
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid numeric values for image size.")
                return

        self.stop_flag.clear()
        thread = threading.Thread(
            target=lambda: self.process_zfb_files(arcade_mode=self.arcade_var.get())
        )
        thread.start()

    def process_zfb_files(self, arcade_mode=False):
        try:
            input_folder = self.input_folder_var.get()
            output_folder = self.output_folder_var.get()
            core = self.core_var.get().lower()
            extension = self.extension_var.get().lower()
    
            core_extension_map = {
                "m2k": "zfb",
                "gba": "zgb", "dblcherrygb": "zgb", "gb": "zgb", "gbb": "zgb",
                "gbgb": "zgb", "gbgc": "zgb", "nes": "zfc", "nesq": "zfc", "snes": "zsf",
                "snes02": "zsf", "sega": "zmd",
                "pcesgx": "zpc", "pce": "zpc",
                "gbav": "zgb", "mgba": "zgb"
            }
    
            if not input_folder or not output_folder or (not arcade_mode and not core):
                messagebox.showwarning('Warning', 'Please fill in all the fields and select input and output folders.')
                return
    
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
    
            self.disable_inputs()
            self.create_zfb_button["state"] = "disabled"
            self.stop_button["state"] = "normal"
    
            files = os.listdir(input_folder)
            total_files = len(files)
            self.progress["maximum"] = total_files
            self.progress["value"] = 0
            self.master.update()
    
            image_files_found = False
    
            for idx, file_name in enumerate(files):
                if self.stop_flag.is_set():
                    self.msg_var.set("Process canceled.")
                    break
    
                file_path = os.path.join(input_folder, file_name)
    
                # Determinar extensión final
                if arcade_mode:
                    final_ext = "zfb"
                else:
                    final_ext = core_extension_map.get(core, "zfb")
    
                zfb_filename = os.path.join(output_folder, os.path.splitext(file_name)[0] + f'.{final_ext}')
    
                try:
                    if file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                        with Image.open(file_path) as img:
                            self.msg_var.set(f"Processing file: {os.path.splitext(file_name)[0]}")
    
                            if self.img_mode.get() == "auto":
                                img_w, img_h = img.size
                                if img_w < int(self.img.default_width) or img_h < int(self.img.default_height):
                                    img_w, img_h = int(self.img.default_width), int(self.img.default_height)
                                elif img_w > int(self.img.hyper_width) or img_h > int(self.img.hyper_height):
                                    img_w, img_h = int(self.img.hyper_width), int(self.img.hyper_height)
    
                                self.img_hyperscreen_var.set(self.check_image_size((img_w, img_h)))
                            else:
                                img_w = int(self.imgwidth_var.get())
                                img_h = int(self.imgheight_var.get())
    
                            img = img.resize((img_w, img_h)).convert("RGB")
    
                            raw_data = []
                            for y in range(img_h):
                                for x in range(img_w):
                                    r, g, b = img.getpixel((x, y))
                                    rgb = ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)
                                    raw_data.append(struct.pack('H', rgb))
    
                            raw_data_bytes = b''.join(raw_data)
    
                        with open(zfb_filename, 'wb') as zfb:
                            zfb.write(raw_data_bytes)
                            zfb.write(b'\x00\x00\x00\x00')
    
                            if arcade_mode:
                                zfb.write(f"{os.path.splitext(file_name)[0]}.zip".encode('utf-8'))
                            else:
                                zfb.write(f"{core};{os.path.splitext(file_name)[0]}.{extension}.gba".encode('utf-8'))
    
                            zfb.write(b'\x00\x00')
    
                        image_files_found = True
    
                    else:
                        with open(zfb_filename, 'wb') as zfb:
                            filler = b'\xFF' if arcade_mode else b'\x00'
                            zfb.write(filler * 0xEA00)
                            zfb.write(b'\x00\x00\x00\x00')
                            if arcade_mode:
                                zfb.write(f"{os.path.splitext(file_name)[0]}.zip".encode('utf-8'))
                            else:
                                zfb.write(f"{core};{os.path.splitext(file_name)[0]}.{extension}.gba".encode('utf-8'))
                            zfb.write(b'\x00\x00')
    
                    self.progress["value"] = idx + 1
                    self.master.update()
    
                except Exception as e:
                    print(f"Error processing {file_name}: {e}")
    
            self.msg_var.set("Process completed." if image_files_found else "No image files found.")
            self.enable_inputs()
            self.create_zfb_button["state"] = "normal"
            self.stop_button["state"] = "disabled"
    
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.enable_inputs()
            self.create_zfb_button["state"] = "normal"
            self.stop_button["state"] = "disabled"

    def select_input_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.input_folder_var.set(folder)

    def select_output_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_folder_var.set(folder)

# ------------------------
# FIN DE ZFBimagesToolSparda
# ------------------------

# ------------------------
# INICIO DE FrogtoolGUI
# ------------------------

class Frogtool(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.systems = {
            "FC": ["rdbui.tax", "fhcfg.nec", "nethn.bvs"],
            "SFC": ["urefs.tax", "adsnt.nec", "xvb6c.bvs"],
            "MD": ["scksp.tax", "setxa.nec", "wmiui.bvs"],
            "GB": ["vdsdc.tax", "umboa.nec", "qdvd6.bvs"],
            "GBC": ["pnpui.tax", "wjere.nec", "mgdel.bvs"],
            "GBA": ["vfnet.tax", "htuiw.nec", "sppnp.bvs"],
            "ARCADE": ["mswb7.tax", "msdtc.nec", "mfpmp.bvs"],
            "ALL": []  # Placeholder for "ALL" option
        }
        self.supported_rom_ext = [
            "bkp", "zip", "zfc", "zsf", "zmd", "zgb", "zfb", "smc", "fig", "sfc", "gd3", "gd7", "dx2", "bsx", "swc", "nes",
            "nfc", "fds", "unf", "gba", "agb", "gbz", "gbc", "gb", "sgb", "bin", "md", "smd", "gen", "sms"
        ]
        self.path_entry = None
        self.system_var = None
        self.system_menu = None
        self.init_ui()
        
    def on_drive_selected(self, event):
        self.check_and_find_ini()

    def int_to_4_bytes_reverse(self, src_int):
        hex_string = format(src_int, "x").rjust(8, "0")[0:8]
        return binascii.unhexlify(hex_string)[::-1]

    def find_foldername_ini(self, path):
        ini_path = os.path.join(path, "Resources", "Foldername.ini")
        ini_path_x = os.path.join(path, "Resources", "Foldernamx.ini")
        ini_to_load = None

        if os.path.exists(ini_path):
            ini_to_load = ini_path
        elif os.path.exists(ini_path_x):
            ini_to_load = ini_path_x

        if not ini_to_load:
            messagebox.showerror("Error", "Neither Foldername.ini nor Foldernamx.ini were found.")
            return

        try:
            with open(ini_to_load, "r", encoding="utf-8") as file:
                lines = file.readlines()

            if len(lines) < 3:
                messagebox.showerror("Error", f"Insufficient lines in {ini_to_load}")
                return

            last_number_line = lines[-3].strip().split()[0]
            try:
                num_lines = int(last_number_line) - 1  
            except ValueError:
                messagebox.showerror("Error", f"Invalid number format in antepenultimate line: {last_number_line}")
                return

            if len(lines) < num_lines + 4:  
                messagebox.showerror("Error", f"Not enough lines in {ini_to_load} to process {num_lines}.")
                return

            new_systems = []
            for line in lines[4:4 + num_lines]:
                parts = line.strip().split(" ", 1)
                if len(parts) > 1:
                    new_systems.append(parts[1])
                else:
                    new_systems.append(parts[0])

            self.systems = {}

            if ini_to_load == ini_path_x:
                systems_data = {
                    "FC": ["m01.ta", "m01.ne", "m01.bv"],
                    "SFC": ["m02.ta", "m02.ne", "m02.bv"],
                    "MD": ["m03.ta", "m03.ne", "m03.bv"],
                    "GB": ["m04.ta", "m04.ne", "m04.bv"],
                    "GBC": ["m05.ta", "m05.ne", "m05.bv"],
                    "GBA": ["m06.ta", "m06.ne", "m06.bv"],
                    "ARCADE": ["m07.ta", "m07.ne", "m07.bv"],
                    "SEGA": ["m08.ta", "m08.ne", "m08.bv"],
                    "ATARI_NGP": ["m09.ta", "m09.ne", "m09.bv"],
                    "WONDERSWAN": ["m10.ta", "m10.ne", "m10.bv"],
                    "PCE": ["m11.ta", "m11.ne", "m11.bv"],
                    "MULTICORE": ["m12.ta", "m12.ne", "m12.bv"]
                }
            else:
                systems_data = {
                    "FC": ["rdbui.tax", "fhcfg.nec", "nethn.bvs"],
                    "SFC": ["urefs.tax", "adsnt.nec", "xvb6c.bvs"],
                    "MD": ["scksp.tax", "setxa.nec", "wmiui.bvs"],
                    "GB": ["vdsdc.tax", "umboa.nec", "qdvd6.bvs"],
                    "GBC": ["pnpui.tax", "wjere.nec", "mgdel.bvs"],
                    "GBA": ["vfnet.tax", "htuiw.nec", "sppnp.bvs"],
                    "ARCADE": ["mswb7.tax", "msdtc.nec", "mfpmp.bvs"],
                    "ALL": [] 
                }

            system_keys = list(systems_data.keys())  

            for idx, system_name in enumerate(new_systems):
                if idx < len(system_keys):
                    self.systems[system_name] = systems_data[system_keys[idx]]

            self.systems["ALL"] = []

            menu = self.system_menu["menu"]
            menu.delete(0, "end")
            for key in self.systems.keys():
                menu.add_command(label=key, command=tk._setit(self.system_var, key))

            self.system_var.set("ALL")
            messagebox.showinfo("Success", "Systems updated successfully from Foldername.ini or Foldernamx.ini!")
            print("Updated systems:", self.systems)

        except Exception as e:
            messagebox.showerror("Error", f"Failed to read or process {ini_to_load}: {e}")

    def check_and_find_ini(self):
        path = self.path_entry.get()
        if path:
            self.find_foldername_ini(path)

    def check_file(self, file_entry, supported_exts):
        file_regex = ".+\\.(" + "|".join(supported_exts) + ")$"
        return file_entry.is_file() and re.search(file_regex, file_entry.name.lower())

    def check_rom(self, file_entry):
        return self.check_file(file_entry, self.supported_rom_ext)

    def strip_file_extension(self, name):
        parts = name.split(".")
        parts.pop()
        return ".".join(parts)

    def sort_normal(self, unsorted_list):
        return sorted(unsorted_list)

    def sort_without_file_ext(self, unsorted_list):
        stripped_names = list(map(self.strip_file_extension, unsorted_list))
        sort_map = dict(zip(unsorted_list, stripped_names))
        return sorted(sort_map, key=sort_map.get)

    def process_sys(self, path, system):
        print(f"Processing {system}")

        if not path:
            messagebox.showerror("Error", "No path has been selected.")
            return

        roms_path = os.path.join(path, system)
        if not os.path.isdir(roms_path):
            os.makedirs(os.path.join(roms_path, "save"), exist_ok=True)

        for file_key in range(3):
            index_path = os.path.join(path, "Resources", self.systems[system][file_key])
            self.check_and_generate_file(index_path)

        print(f"Looking for files in {roms_path}")

        files = [file for file in os.scandir(roms_path) if self.check_rom(file)]
        no_files = len(files)

        filenames = [file.name for file in files] if files else []
        stripped_names = [self.strip_file_extension(name) for name in filenames] if files else []

        name_map_files = dict(zip(filenames, filenames))
        name_map_cn = dict(zip(filenames, stripped_names))
        name_map_pinyin = dict(zip(filenames, stripped_names))

        self.write_index_file(name_map_files, self.sort_without_file_ext, os.path.join(path, "Resources", self.systems[system][0]))
        self.write_index_file(name_map_cn, self.sort_normal, os.path.join(path, "Resources", self.systems[system][1]))
        self.write_index_file(name_map_pinyin, self.sort_normal, os.path.join(path, "Resources", self.systems[system][2]))

        print(f"Game list for {system} updated with {no_files} ROMs.\n")

    def check_and_generate_file(self, file_path):
        if not os.path.exists(file_path):
            print(f"{file_path} not found. Creating a blank file.")
            try:
                with open(file_path, 'wb') as file_handle:
                    file_handle.write(b'')
            except (OSError, IOError):
                print(f"! Failed to create file: {file_path}")
                print("  Check the path and Resources directory are writable.")
                raise StopExecution

    def write_index_file(self, name_map, sort_func, index_path):
        sorted_filenames = sorted(name_map.keys())
        names_bytes = b""
        pointers_by_name = {}

        for filename in sorted_filenames:
            display_name = name_map[filename]
            current_pointer = len(names_bytes)
            pointers_by_name[display_name] = current_pointer
            names_bytes += display_name.encode('utf-8') + chr(0).encode('utf-8')

        metadata_bytes = self.int_to_4_bytes_reverse(len(name_map))

        sorted_display_names = sort_func(name_map.values())
        sorted_pointers = map(lambda name: pointers_by_name[name], sorted_display_names)

        for current_pointer in sorted_pointers:
            metadata_bytes += self.int_to_4_bytes_reverse(current_pointer)

        new_index_content = metadata_bytes + names_bytes

        print(f"Overwriting {index_path}")
        try:
            with open(index_path, 'wb') as file_handle:
                file_handle.write(new_index_content)
        except (IOError, OSError):
            print("! Failed overwriting file.")
            print("  Check the path and file are writable, and the file is not open in another program.")
            raise StopExecution

    def select_folder(self):
        folder_selected = filedialog.askdirectory(title="Select Folder")
        if folder_selected:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder_selected)
            self.check_and_find_ini()

    def init_ui(self):
        """Configura los elementos gráficos al iniciar la aplicación."""

        # Construcción del GUI aquí, usando self como contenedor
        self.path_entry = ttk.Entry(self, width=40)
        self.system_var = tk.StringVar(self)
        self.system_var.set("ALL")
        self.system_menu = tk.OptionMenu(self, self.system_var, *self.systems.keys())

        path_label = tk.Label(self, text="SF2000 Location:")
        path_button = ttk.Button(self, text="Browse", command=self.select_folder)
        system_label = tk.Label(self, text="Select System:")
        execute_button = tk.Button(self, text="Update Games List", command=self.execute_conversion)

        # Usa grid (o pack, pero todo consistente)
        path_label.grid(row=0, column=0, pady=5, sticky="w")
        self.path_entry.grid(row=1, column=0, pady=5, sticky="w")
        path_button.grid(row=1, column=1, pady=5, sticky="w")
        system_label.grid(row=2, column=0, pady=5, sticky="w")
        self.system_menu.grid(row=3, column=0, pady=5, sticky="w")
        execute_button.grid(row=4, column=0, pady=10, sticky="w")

    def show_popup(self):
        messagebox.showinfo("Message", "Updated games list!")

    def execute_conversion(self):
        path = self.path_entry.get()

        if not path:
            print("No path has been selected.")
            return

        try:
            system = self.system_var.get()
            if system == "ALL":
                keys_to_process = [key for key in self.systems.keys() if key != "ALL"]
            else:
                keys_to_process = [system]

            for syskey in keys_to_process:
                self.process_sys(path, syskey)

            self.show_popup()

        except StopExecution:
            print("Error updating game list.")

        # Construcción del GUI aquí, usando self como contenedor
        self.path_entry = ttk.Entry(self, width=40)
        self.system_var = tk.StringVar(self)
        self.system_var.set("ALL")
        self.system_menu = tk.OptionMenu(self, self.system_var, *self.systems.keys())

        path_label = tk.Label(self, text="SF2000 Location:")
        path_button = ttk.Button(self, text="Browse", command=self.select_folder)
        system_label = tk.Label(self, text="Select System:")
        execute_button = tk.Button(self, text="Update Games List", command=self.execute_conversion)

        # Usa grid (o pack, pero todo consistente)
        path_label.grid(row=0, column=0, pady=5, sticky="w")
        self.path_entry.grid(row=1, column=0, pady=5, sticky="w")
        path_button.grid(row=1, column=1, pady=5, sticky="w")
        system_label.grid(row=2, column=0, pady=5, sticky="w")
        self.system_menu.grid(row=3, column=0, pady=5, sticky="w")
        execute_button.grid(row=4, column=0, pady=10, sticky="w")

# ------------------------
# FIN DE FrogtoolGUI
# ------------------------

# ------------------------
# INICIO DE ZFBViewer
# ------------------------

import os
import shutil
import struct
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
import numpy as np

class ZFBViewer(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.folder_path = tk.StringVar()

        self.canvas = tk.Canvas(self, width=640, height=480, bg="gray")
        self.canvas.pack(pady=20)

        self.tree_frame = tk.Frame(self)
        self.tree_frame.pack(fill=tk.BOTH, expand=False, padx=20, pady=10)

        self.tree_scrollbar = tk.Scrollbar(self.tree_frame)
        self.tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=("Name", "Path"),
            show="headings",
            height=5,
            yscrollcommand=self.tree_scrollbar.set
        )
        self.tree.heading("Name", text="Name")
        self.tree.heading("Path", text="Path")
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree_scrollbar.config(command=self.tree.yview)

        self.tree.bind("<Double-1>", self.edit_path)
        self.tree.bind("<<TreeviewSelect>>", self.load_image)

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(pady=20, fill=tk.X)

        self.btn_select_folder = tk.Button(self.button_frame, text="Select Folder", command=self.select_folder)
        self.btn_select_folder.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

        self.btn_download = tk.Button(self.button_frame, text="Download IMG", command=self.download_image)
        self.btn_download.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        self.btn_change = tk.Button(self.button_frame, text="Change IMG", command=self.change_image)
        self.btn_change.grid(row=0, column=2, padx=10, pady=5, sticky="ew")

        self.btn_save = tk.Button(self.button_frame, text="Save", command=self.save_image)
        self.btn_save.grid(row=0, column=3, padx=10, pady=5, sticky="ew")

        self.btn_add_rom = tk.Button(self.button_frame, text="Add ROM", command=self.add_rom)
        self.btn_add_rom.grid(row=0, column=4, padx=10, pady=5, sticky="ew")

        for i in range(5):
            self.button_frame.grid_columnconfigure(i, weight=1)

    def ask_image_size(self, size_options):
        popup = tk.Toplevel()
        popup.title("Select Image Size")
        popup.geometry("250x100")
        popup.resizable(False, False)
    
        tk.Label(popup, text="Image size:").pack(pady=5)
    
        combo = ttk.Combobox(popup, values=size_options, state="readonly")
        combo.pack()
        combo.set(size_options[0])  # Valor por defecto
    
        result = {"value": None}
    
        def confirm():
            result["value"] = combo.get()
            popup.destroy()
    
        tk.Button(popup, text="OK", command=confirm).pack(pady=5)
        popup.grab_set()
        popup.wait_window()
        return result["value"]

    def select_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path.set(folder_selected)
            self.load_files()

    def load_files(self):
        self.tree.delete(*self.tree.get_children())
        folder = self.folder_path.get()
        
        if os.path.isdir(folder):
            # Crear el conjunto de extensiones válidas basadas en los cores
            valid_extensions = {
                "zfc", "zfb", "zsf", "zgb", "zmd", "zpc"
            }
            
            # Filtrar los archivos que tienen una de las extensiones válidas
            files = [f for f in os.listdir(folder) if os.path.splitext(f)[1][1:] in valid_extensions]
            
            # Agregar los archivos válidos al Treeview
            for file in files:
                path = self.extract_path(os.path.join(folder, file))
                self.tree.insert("", tk.END, values=(file, path))

    def extract_path(self, file_path):
        try:
            file_size = os.path.getsize(file_path)
            img_width, img_height = self.detect_image_size(file_size)
            if (img_width, img_height) == (640, 480):
                img_data_size = 0x00096000
            elif (img_width, img_height) == (640, 400):
                img_data_size = 0x0007D000
            elif (img_width, img_height) == (144, 208):
                img_data_size = 0x0000EA00
            else:
                img_data_size = img_width * img_height * 2

            with open(file_path, "rb") as f:
                f.seek(img_data_size)
                extra_data = f.read()
                clean_data = extra_data.strip(b"\x00")
                return clean_data.decode("latin1", errors="ignore") or "Unknown"
        except:
            return "Unknown"

    def update_path(self, item, new_path, entry):
        values = list(self.tree.item(item, "values"))
        encoded_path = b"\x00\x00\x00\x00" + new_path.encode("latin1") + b"\x00\x00"
        values[1] = new_path
        self.tree.item(item, values=values)
        entry.destroy()
        filename = values[0]
        file_path = os.path.join(self.folder_path.get(), filename)
        with open(file_path, "rb") as f:
            data = f.read()
        img_width, img_height = self.detect_image_size(len(data))
        img_data_size = img_width * img_height * 2
        with open(file_path, "wb") as f:
            f.write(data[:img_data_size])
            f.write(encoded_path)

    def edit_path(self, event):
        item = self.tree.selection()[0]
        column = self.tree.identify_column(event.x)
        if column == "#2":
            x, y, width, height = self.tree.bbox(item, column="#2")
            entry = tk.Entry(self.tree)
            entry.place(x=x, y=y, width=width, height=height)
            entry.insert(0, self.tree.item(item, "values")[1])
            entry.focus()
            entry.bind("<Return>", lambda e: self.update_path(item, entry.get(), entry))
            entry.bind("<FocusOut>", lambda e: self.update_path(item, entry.get(), entry))

    def load_image(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        filename = self.tree.item(selected_item[0], "values")[0]
        file_path = os.path.join(self.folder_path.get(), filename)

        try:
            with open(file_path, "rb") as f:
                raw_data = f.read()
                img_width, img_height = self.detect_image_size(len(raw_data))
                pixel_count = img_width * img_height
                pixels = np.frombuffer(raw_data[:pixel_count * 2], dtype=np.uint16)

                r = ((pixels >> 11) & 0x1F) << 3
                g = ((pixels >> 5) & 0x3F) << 2
                b = (pixels & 0x1F) << 3
                rgb = np.dstack((r, g, b)).astype(np.uint8).reshape((img_height, img_width, 3))

                img = Image.fromarray(rgb, "RGB")
                self.current_image = img
                self.tk_image = ImageTk.PhotoImage(img)
                self.canvas.delete("all")
                x_center = self.canvas.winfo_width() // 2
                y_center = self.canvas.winfo_height() // 2
                self.canvas.create_image(x_center, y_center, image=self.tk_image, anchor=tk.CENTER)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading image: {e}")

    def detect_image_size(self, file_size):
        possible_sizes = [(640, 480), (640, 400), (144, 208)]
        for w, h in possible_sizes:
            if file_size >= w * h * 2:
                return w, h
        raise ValueError("Unknown image size")

    def download_image(self):
        if hasattr(self, "current_image"):
            file_path = filedialog.asksaveasfilename(defaultextension=".png")
            if file_path:
                self.current_image.save(file_path)

    def change_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.bmp")])
        if file_path:
            new_img = Image.open(file_path).convert("RGB")
            new_img = new_img.resize(self.current_image.size)
            self.current_image = new_img
            self.tk_image = ImageTk.PhotoImage(new_img)
            self.canvas.delete("all")
            x_center = self.canvas.winfo_width() // 2
            y_center = self.canvas.winfo_height() // 2
            self.canvas.create_image(x_center, y_center, image=self.tk_image, anchor=tk.CENTER)

    def save_image(self):
        if hasattr(self, "current_image"):
            selected_item = self.tree.selection()
            if not selected_item:
                return
            filename = self.tree.item(selected_item[0], "values")[0]
            file_path = os.path.join(self.folder_path.get(), filename)
            with open(file_path, "rb") as f:
                original_data = f.read()
            img_width, img_height = self.current_image.size
            raw_data = bytearray()
            for y in range(img_height):
                for x in range(img_width):
                    r, g, b = self.current_image.getpixel((x, y))
                    rgb565 = ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)
                    raw_data.extend(struct.pack("H", rgb565))
            extra_data = original_data[img_width * img_height * 2:]
            with open(file_path, "wb") as f:
                f.write(raw_data)
                f.write(extra_data)

    def add_rom(self):
        if not self.folder_path.get():
            messagebox.showerror("Error", "First select a folder with the 'Select Folder' button.")
            return
    
        rom_path = filedialog.askopenfilename(title="Select ROM file")
        if not rom_path:
            return
    
        rom_name = os.path.basename(rom_path)
        core = simpledialog.askstring("Core", "Enter the core name:")
        if not core:
            return
    
        # Elegir tamaño de imagen
        size_options = ["640x480", "640x400", "144x208"]
        selected_size = self.ask_image_size(size_options)
        if selected_size is None:
            messagebox.showerror("Error", "No size selected.")
            return
    
        width, height = map(int, selected_size.split("x"))
        img_data_size = width * height * 2
    
        selected_folder = self.folder_path.get()
        base_dir = os.path.abspath(os.path.join(selected_folder, ".."))
        roms_dir = os.path.join(base_dir, "ROMS", core)
        os.makedirs(roms_dir, exist_ok=True)
    
        dest_rom_path = os.path.join(roms_dir, rom_name)
    
        # Mapeo de extensiones válidas por core
        core_extension_map = {
            "m2k": "zfb",
            "gba": "zgb", "dblcherrygb": "zgb", "gb": "zgb", "gbb": "zgb",
            "gbgb": "zgb", "gbgc": "zgb", "nes": "zfc", "nesq": "zfc", "snes": "zsf",
            "snes02": "zsf", "sega": "zmd",
            "pcesgx": "zpc", "pce": "zpc",
            "gbav": "zgb", "mgba": "zgb"
        }
    
        # Determinar la extensión del archivo a crear
        extension = core_extension_map.get(core, "zfb")
    
        # Crear nombre y ruta del archivo de imagen
        zfb_name = os.path.splitext(rom_name)[0] + f".{extension}"
        zfb_path = os.path.join(selected_folder, zfb_name)
    
        try:
            # Verificar si la ROM ya existe con ese nombre exacto
            if os.path.exists(dest_rom_path):
                overwrite = messagebox.askyesno("ROM exists", f"The ROM '{rom_name}' already exists.\nDo you want to overwrite it?")
                if not overwrite:
                    return
            else:
                shutil.copy2(rom_path, dest_rom_path)
    
            # Verificar si la imagen ya existe con ese nombre exacto
            if os.path.exists(zfb_path):
                overwrite_img = messagebox.askyesno("Image exists", f"The image file '{zfb_name}' already exists.\nDo you want to overwrite it?")
                if not overwrite_img:
                    return
    
            # Crear imagen vacía (negro)
            img_data = bytearray([0x00] * img_data_size)
    
            with open(zfb_path, "wb") as f:
                f.write(img_data)
                f.write(b"\x00\x00\x00\x00")
                path_in_bin = f"{core};{rom_name}.gba".encode("latin1")
                f.write(path_in_bin)
                f.write(b"\x00\x00")
    
            self.load_files()
    
            # Mostrar confirmación
            messagebox.showinfo("ROM Added", f"ROM and image saved:\n{zfb_name}")
    
        except Exception as e:
            messagebox.showerror("Error", f"Could not add ROM:\n{e}")


# ------------------------
# FIN DE ZFBViewer
# ------------------------

# ------------------------
# INICIO DE Menu_Image_Generator
# ------------------------

class MenuImageGenerator(tk.Frame):

    def __init__(self, root):
        super().__init__(root)
        self.img_width = 576
        self.img_height = 168

        self.preview_width = self.img_width // 3
        self.preview_height = self.img_height // 3

        self.export_path = ""
        self.images = []
        self.previews = []
        self.image_buttons = []

        self.preview_window = MenuImagePreview(self)

        self.initialize_images()

        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.selected_option = tk.IntVar(value=8)
        tk.Label(self.button_frame, text="Number of images:").grid(row=0, column=0, padx=5, pady=5, sticky="e")

        self.option_menu = tk.OptionMenu(self.button_frame, self.selected_option, *range(1, 14), command=lambda _: self.update_previews())
        self.option_menu.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        for i in range(13):
            btn = tk.Button(self.button_frame, text=f"Image {i+1}", command=lambda i=i: self.load_image(i))
            self.image_buttons.append(btn)
            if i < 8:  # Show the first 8 buttons initially
                btn.grid(row=i + 1, column=0, columnspan=2, pady=2)

        self.destination_label = tk.Label(self.button_frame, text="Destination: Not selected", anchor="w")
        self.destination_label.grid(row=14, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        tk.Button(self.button_frame, text="Select destination", command=self.select_destination).grid(row=15, column=0, columnspan=2, pady=5)

        tk.Button(self.button_frame, text="Export", command=self.export_images, bg="green", fg="white").grid(row=16, column=0, columnspan=2, pady=10)

        self.update_previews()

    def create_transparent_image(self):
        """Creates a transparent image."""
        return Image.new("RGBA", (self.img_width, self.img_height), (0, 0, 0, 0))

    def update_previews(self):
        """Updates preview images and buttons."""
        total_images = self.selected_option.get()  # Number of selected images
        for i in range(13):
            preview_img = self.images[i].resize((self.preview_width, self.preview_height), Image.Resampling.LANCZOS)
            preview_photo = ImageTk.PhotoImage(preview_img)
            self.previews[i].config(image=preview_photo)
            self.previews[i].image = preview_photo
            self.previews[i].pack_forget() if i >= total_images else self.previews[i].pack(pady=2)
            if i < total_images:
                self.image_buttons[i].grid(row=i + 1, column=0, columnspan=2, pady=2)
            else:
                self.image_buttons[i].grid_forget()

    def initialize_images(self):
        """Initializes images with default transparency."""
        self.images = [self.create_transparent_image() for _ in range(13)]
        self.previews = []
        for i in range(13):
            self.preview_img = self.images[i].resize((self.preview_width, self.preview_height), Image.Resampling.LANCZOS)
            self.preview_photo = ImageTk.PhotoImage(self.preview_img)
            self.preview_label = tk.Label(self.preview_window.preview_frame, image=self.preview_photo)
            self.preview_label.image = self.preview_photo
            self.preview_label.pack(pady=2)
            self.previews.append(self.preview_label)

    def load_image(self, index):
        """Loads an image at the specified position."""
        filepath = filedialog.askopenfilename()
        if not filepath:
            return

        try:
            img = Image.open(filepath).convert("RGBA")
            img = img.resize((self.img_width, self.img_height), Image.Resampling.LANCZOS)
            self.images[index] = img
            self.update_previews()
        except Exception as e:
            messagebox.showerror("Error", f"The image could not be loaded: {e}")

    def select_destination(self):
        """Selects the export destination folder."""
        global export_path
        export_path = filedialog.askdirectory()
        if export_path:
            self.destination_label.config(text=f"Destination: {export_path}")

    def export_images(self):
        """Exports the combined images."""
        if not export_path:
            messagebox.showerror("Error", "Please select a destination.")
            return

        total_images = self.selected_option.get()
        canvas_height = total_images * self.img_height

        composite = Image.new("RGBA", (self.img_width, canvas_height), (0, 0, 0, 0))

        for i in range(total_images):
            if self.images[i]:
                composite.paste(self.images[i], (0, i * self.img_height))

        output_file = f"{export_path}/sfcdr.cpl.png"
        try:
            composite.save(output_file)
            messagebox.showinfo("Success", f"Image exported to {output_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not export image: {e}")

class MenuImagePreview(tk.Toplevel):

    def __init__(self, root):
        super().__init__(root)

        self.title("Preview")
        self.geometry(f"{self.master.preview_width+40}x{self.master.preview_height*8+40}")

        self.preview_canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.preview_canvas.yview)
        self.preview_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.preview_canvas.pack(side="left", fill="both", expand=True)

        self.preview_frame = tk.Frame(self.preview_canvas)
        self.preview_canvas.create_window((0, 0), window=self.preview_frame, anchor="nw")
        self.preview_frame.bind("<Configure>", self.configure_scroll)

    def configure_scroll(self, event):
        self.preview_canvas.configure(scrollregion=self.preview_canvas.bbox("all"))

# ------------------------
# FIN DE Menu_Image_Generator
# ------------------------



class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SPARDA APPS")
        self.geometry("900x750")

        # Frame lateral con botones
        self.sidebar = tk.Frame(self, width=200, bg='white')
        self.sidebar.pack(side="left", fill="y")

        # Frame principal para cargar las apps
        self.main_area = tk.Frame(self)
        self.main_area.pack(side="right", fill="both", expand=True)

        # Establecer configuración de rejilla para centrar contenido
        self.main_area.grid_rowconfigure(0, weight=1)
        self.main_area.grid_columnconfigure(0, weight=1)

        # Diccionario de apps
        self.apps = {
            "Create ZXX": ZFBimagesTool,
            "ZXX Viewer": ZFBViewer,
            "Frogtool GUI": Frogtool,
            "Theme Editor": ImageProcessorApp,
            "Menu Image Generator": MenuImageGenerator,
#            "App 6": App6
        }

        # Botones
        for name in self.apps:
            b = tk.Button(self.sidebar, text=name, command=lambda n=name: self.show_app(n))
            b.pack(fill='x', padx=10, pady=5)

        self.current_app = None

    def show_app(self, app_name):
        # Elimina completamente todo del main_area
        for widget in self.main_area.winfo_children():
            widget.destroy()
        self.current_app = None

        # Carga y muestra la nueva app
        app_class = self.apps[app_name]
        self.current_app = app_class(self.main_area)
        self.current_app.grid(row=0, column=0)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
