import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from tkinter import Menu
import time

#--------------------------Colores--------------------------
color_boton_ingresar = '#ffde59'
color_entrada_usuario = '#aff5ff'
color_entrada_contrasena = '#aff5ff'
color_fondo_ventana = '#38b6ff'
color_boton_salir = '#ffbd59'

class ventana_login(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bienvenido/a")
        self.resizable(0, 0)
        self.clock_id = None

        #-------------------Imagen fondo ventana-------------------
        self.fondo_ventana = tk.PhotoImage(file='imagen_logueo.png')
        self.fondo1 = tk.Label(self, image=self.fondo_ventana)
        self.fondo1.place(x=0, y=0, relwidth=1, relheight=1)

        #-------------------Tamaño ventana-------------------
        
        ancho_ventana = 500
        alto_ventana = 707
        self.centrar_ventana(ancho_ventana, alto_ventana)

        #-------------------Botones-------------------
        
        self.boton_ingresar = tk.Button(self, text='Ingresar', cursor='hand2', command=self.login,
                                        bg=color_boton_ingresar, width=8, height=1, relief='flat', font=('Open Sans', 16))
        self.boton_ingresar.place(x=280, y=627)

        self.boton_salir = tk.Button(self, text='Salir', cursor='hand2', command=self.destroy,
                                    bg=color_boton_salir, width=8, height=1, relief='flat', font=('Open Sans', 16))
        self.boton_salir.place(x=115, y=627)

        #-------------------Entradas-------------------
        
        self.usuario = tk.StringVar()
        self.contrasena = tk.StringVar()

        self.entrada_usuario = tk.Entry(self, textvariable=self.usuario, width=14, relief='flat',
                                        bg=color_entrada_usuario, font=('Open Sans', 25))
        self.entrada_usuario.place(x=120, y=376)

        self.entrada_contrasena = tk.Entry(self, textvariable=self.contrasena, width=14, relief='flat',
                                          bg=color_entrada_contrasena, font=('Open Sans', 25), show='*')
        self.entrada_contrasena.place(x=120, y=528)
        
        #-------------------Centrar ventana-------------------
    
    def centrar_ventana(self, ancho, alto): 
        pantalla_ancho = self.winfo_screenwidth()
        pantalla_alto = self.winfo_screenheight()
        x = (pantalla_ancho // 2) - (ancho // 2)
        y = (pantalla_alto // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

        #-------------------Reloj-------------------
    
        self.reloj = tk.Label(self, font=('Open Sans', 17), bg='white', fg='black')
        self.reloj.place(x=200, y=17)
        self.actualizar_reloj()

    def actualizar_reloj(self):
        tiempo_actual = time.strftime('%H:%M:%S')
        self.reloj.config(text=tiempo_actual)
        self.clock_id = self.after(1000, self.actualizar_reloj)

        #-------------------Login-------------------
    
    def login(self):
        nombre = self.usuario.get()
        contra = self.contrasena.get()
        if nombre == 'usuario' and contra == 'contraseña':
            messagebox.showinfo(' ', 'Ha ingresado correctamente.')
            self.after_cancel(self.clock_id)  # Cancelar el reloj (importante para no generar error al cerrar el login)
            self.withdraw()
            ventana_programa() 
        else:
            messagebox.showerror('Error', 'Datos incorrectos, intente nuevamente.')



#--------------------------Programa Principal--------------------------

from Productos import productos

class ventana_programa(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ventana Principal")
        self.geometry("800x600")
        self.resizable(0, 0)   
        
        tree_frame = tk.Frame(self)
        tree_frame.pack(pady=20, fill=tk.BOTH, expand=True)

        
        self.product_tree = ttk.Treeview(tree_frame, columns=("Nombre", "Marca", "Código", "Stock", "Precio"), show="headings")
        self.product_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Crear el menú superior
        self.crear_barra()

        # Configurar los encabezados
        self.product_tree.heading("Nombre", text="Nombre del Producto")
        self.product_tree.heading("Marca", text="Marca")
        self.product_tree.heading("Código", text="Código")
        self.product_tree.heading("Stock", text="Stock")
        self.product_tree.heading("Precio", text="Precio")

        # Configurar el tamaño de las columnas
        self.product_tree.column("Nombre", width=150)
        self.product_tree.column("Marca", width=100)
        self.product_tree.column("Código", width=100)
        self.product_tree.column("Stock", width=60)
        self.product_tree.column("Precio", width=80)

        # Crear scrollbar vertical para el Treeview
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.product_tree.yview)
        self.product_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Botones para agregar, modificar y eliminar productos
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        self.boton_agregar = tk.Button(btn_frame, text="Agregar Producto", command=self.agregar_producto)
        self.boton_agregar.grid(row=0, column=0, padx=5)

        self.boton_modificar = tk.Button(btn_frame, text="Modificar Producto", command=self.modificar_producto)
        self.boton_modificar.grid(row=0, column=1, padx=5)

        self.remove_button = tk.Button(btn_frame, text="Quitar Producto", command=self.remove_product)
        self.remove_button.grid(row=0, column=2, padx=5)

        # Inicializar el diccionario de productos
        self.producto = productos

        # Mostrar los productos importados en el Treeview
        self.actualizar_productos()

    def crear_barra(self):
        # Crear la barra de menú
        menubar = Menu(self)

        #Crear el menú de Opciones
        opciones_menu = Menu(menubar, tearoff=0)
        opciones_menu.add_command(label="Acerca de", command=self.acerca_de)
        opciones_menu.add_separator()
        opciones_menu.add_command(label="Salir", command=self.quit)


        # Agregar el menú de Opciones a la barra de menú
        menubar.add_cascade(label="Opciones", menu=opciones_menu)

        # Mostrar la barra de menú
        self.config(menu=menubar)

    def agregar_producto(self):
        # Solicitar información del nuevo producto
        nombre = simpledialog.askstring("Agregar Producto", "Nombre del Producto:", parent=self)
        marca = simpledialog.askstring("Agregar Producto", "Marca:", parent=self)
        codigo = simpledialog.askstring("Agregar Producto", "Código:", parent=self)
        stock = simpledialog.askinteger("Agregar Producto", "Stock:", parent=self)
        precio = simpledialog.askfloat("Agregar Producto", "Precio:", parent=self)

        if nombre and marca and codigo and stock is not None and precio is not None:
            id_producto = len(self.producto) + 1
            self.producto[id_producto] = {"producto": nombre, "marca": marca, "codigo": codigo, "stock": stock, "precio": precio}
            self.actualizar_productos()
        else:
            messagebox.showwarning(" ", "Todos los campos son obligatorios.")

    def modificar_producto(self):
        
        #-------------------Seleccionar producto-------------------
        
        selected_item = self.product_tree.selection()
        if not selected_item:
            messagebox.showwarning(" ", "Por favor, seleccione un producto para modificar.")
            return

        id_producto = int(selected_item[0])

        #-------------------Solicitar nueva informacion-------------------
        
        nombre = simpledialog.askstring("Modificar Producto", "Nombre del Producto:", 
                                        initialvalue=self.producto[id_producto]["producto"], parent=self)
        marca = simpledialog.askstring("Modificar Producto", "Marca:", 
                                        initialvalue=self.producto[id_producto]["marca"], parent=self)
        codigo = simpledialog.askstring("Modificar Producto", "Código:", 
                                        initialvalue=self.producto[id_producto]["codigo"], parent=self)
        stock = simpledialog.askinteger("Modificar Producto", "Stock:", 
                                        initialvalue=self.producto[id_producto]["stock"], parent=self)
        precio = simpledialog.askfloat("Modificar Producto", "Precio:", 
                                        initialvalue=self.producto[id_producto]["precio"], parent=self)

        if nombre and marca and codigo and stock is not None and precio is not None:
            self.producto[id_producto]= {
                "producto": nombre, 
                "marca": marca, 
                "codigo": codigo, 
                "stock": stock, 
                "precio": precio
            }
            self.actualizar_productos()
        else:
            messagebox.showwarning(" ", "Todos los campos son obligatorios.")

    def remove_product(self):
        # Obtener el producto seleccionado
        selected_item = self.product_tree.selection()
        if not selected_item:
            messagebox.showwarning(" ", "Por favor, seleccione un producto para eliminar.")
            return

        id_producto = int(selected_item[0])
        del self.producto[id_producto]
        self.actualizar_productos()

    def actualizar_productos(self):
        # Limpiar el Treeview
        self.product_tree.delete(*self.product_tree.get_children())
        # Insertar producto actualizados
        for id_producto, producto in self.producto.items():
            self.product_tree.insert("", "end", iid=id_producto, values=(
                producto["producto"], producto["marca"], producto["codigo"], producto["stock"], producto["precio"]
            ))

    def acerca_de(self):
        # Mostrar ventana "Acerca de"
        messagebox.showinfo("Acerca de", "Gestor de Productos de Supermercado\nVersión 0.01\nCreado por \nFederico, Vallejos. \nCristian, Caballero. \nManuel, Rodiguez Serrano. \nLuciano, Vazquez")



if __name__ == "__main__":
    app = ventana_login()
    app.mainloop()