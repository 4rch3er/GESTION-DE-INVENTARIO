from validaciones import solicitar_texto, solicitar_entero, solicitar_flotante
import sqlite3
import os

# Clase Producto
class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        self._id_producto = id_producto
        self._nombre = nombre
        self._cantidad = cantidad
        self._precio = precio
    
    
    # Getters y setters para encapsulamiento
    def get_id_producto(self):
        return self._id_producto

    def get_nombre(self):
        return self._nombre

    def get_cantidad(self):
        return self._cantidad

    def get_precio(self):
        return self._precio

    def set_precio(self, nuevo_precio):
        if nuevo_precio > 0:
            self._precio = nuevo_precio

        else:
            print("El precio debe ser positivo.")
    
    def __str__(self):
        return f'ID: {self.id_producto}, Nombre: {self.nombre}, Cantidad: {self.cantidad}, Precio: {self.precio}'
    
    # Agregar método común para productos
    def calcular_descuento(self, porsentaje):
        return self.precio - (self.precio * porsentaje / 100)


#Clase derivada de producto
class ProductoCaducable(Producto):
    def __init__(self, id_producto, nombre, cantidad, precio, fecha_expiracion):
        super().__init__(id_producto, nombre, cantidad, precio)
        self.fecha_expiracion = fecha_expiracion

    def __str__(self):
        return f'{super().__str__()}, Fecha de Expiración: {self.fecha_expiracion}'
    
    # Si el producto está cerca de su fecha de expiración, aplicamos un mayor descuento
    def calcular_descuento(self, porsentaje):
        descuento = porsentaje + 10
        return self.precio - (self.precio * descuento / 100)

# Clase Proveedor
class Proveedor:
    def __init__(self, id_proveedor, nombre, telefono, correo):
        self.id_proveedor = id_proveedor
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo 


    def __str__(self):
        return f'ID: {self.id_proveedor}, Nombre: {self.nombre}, Telefono: {self.telefono}, Correo: {self.correo}'

# Clase para gestionar la base de datos
class InventarioDB:
    def __init__(self):
        self.conn = sqlite3.connect('inventario.db')
        self.cursor = self.conn.cursor()
        self.crear_tablas()

    def crear_tablas(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
                                id_producto TEXT PRIMARY KEY,
                                nombre TEXT,
                                cantidad INTEGER,
                                precio REAL,
                                fecha_expiracion TEXT
                              )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS proveedores (
                                id_proveedor TEXT PRIMARY KEY,
                                nombre TEXT,
                                telefono TEXT,
                                correo TEXT
                              )''')
        self.conn.commit()

    # CRUD para productos
    def agregar_producto(self, producto):
        try:
            if isinstance(producto, ProductoCaducable):
                self.cursor.execute(
                    "INSERT INTO productos (id_producto, nombre, cantidad, precio, fecha_expiracion) VALUES (?, ?, ?, ?, ?)",
                    (producto.get_id_producto(), producto.get_nombre(), producto.get_cantidad(), 
                    producto.get_precio(), producto.get_fecha_expiracion()))
            else:
                self.cursor.execute(
                    "INSERT INTO productos (id_producto, nombre, cantidad, precio) VALUES (?, ?, ?, ?)",
                    (producto.get_id_producto(), producto.get_nombre(), producto.get_cantidad(), 
                    producto.get_precio()))
            self.conn.commit()
            print(f"Producto {producto.get_nombre()} agregado al inventario.")
        except sqlite3.IntegrityError:
            print(f"Error: Ya existe un producto con ID {producto.get_id_producto()}.")


    def mostrar_productos(self):
        self.cursor.execute("SELECT * FROM productos")
        productos = self.cursor.fetchall()
        if not productos:
            print("El inventario está vacío.")
        else:
            print("Inventario de productos:")
            for p in productos:
                if p[4]:  # Si el producto tiene fecha de expiración
                    print(f"ID: {p[0]}, Nombre: {p[1]}, Cantidad: {p[2]}, Precio: {p[3]}, Fecha Expiración: {p[4]}")
                else:
                    print(f"ID: {p[0]}, Nombre: {p[1]}, Cantidad: {p[2]}, Precio: {p[3]}")


    def actualizar_producto(self, id_producto, nombre=None, cantidad=None, precio=None, fecha_expiracion=None):
        producto = self.buscar_producto(id_producto)
        if producto:
            if nombre:
                self.cursor.execute("UPDATE productos SET nombre = ? WHERE id_producto = ?", (nombre, id_producto))
            if cantidad:
                self.cursor.execute("UPDATE productos SET cantidad = ? WHERE id_producto = ?", (cantidad, id_producto))
            if precio:
                self.cursor.execute("UPDATE productos SET precio = ? WHERE id_producto = ?", (precio, id_producto))
            if fecha_expiracion:
                self.cursor.execute("UPDATE productos SET fecha_expiracion = ? WHERE id_producto = ?", 
                                    (fecha_expiracion, id_producto))
            self.conn.commit()
            print(f"Producto {id_producto} actualizado.")
        else:
            print(f"Producto con ID {id_producto} no encontrado.")


    def eliminar_producto(self, id_producto):
        if self.buscar_producto(id_producto):
            self.cursor.execute("DELETE FROM productos WHERE id_producto = ?", (id_producto,))
            self.conn.commit()
            print(f"Producto con ID {id_producto} eliminado del inventario.")
        else:
            print(f"Producto con ID {id_producto} no encontrado.")


    def buscar_producto(self, id_producto):
        self.cursor.execute("SELECT * FROM productos WHERE id_producto = ?", (id_producto,))
        return self.cursor.fetchone()

    # CRUD para proveedores
    def agregar_proveedor(self, proveedor):
        try:
            self.cursor.execute("INSERT INTO proveedores (id_proveedor, nombre, telefono, correo) VALUES (?, ?, ?, ?)",
                                (proveedor.id_proveedor, proveedor.nombre, proveedor.telefono, proveedor.correo))
            self.conn.commit()
            print(f"Proveedor {proveedor.nombre} agregado.")
        except sqlite3.IntegrityError:
            print(f"Error: Ya existe un proveedor con ID {proveedor.id_proveedor}.")

    def mostrar_proveedores(self):
        self.cursor.execute("SELECT * FROM proveedores")
        proveedores = self.cursor.fetchall()
        if not proveedores:
            print("No hay proveedores registrados.")
        else:
            print("Lista de proveedores:")
            for p in proveedores:
                print(f"ID: {p[0]}, Nombre: {p[1]}, Telefono: {p[2]}, Correo: {p[3]}")


    def actualizar_proveedor(self, id_proveedor, nombre=None, telefono=None, correo=None):
        proveedor = self.buscar_proveedor(id_proveedor)
        if proveedor:
            if nombre:
                self.cursor.execute("UPDATE proveedores SET nombre = ? WHERE id_proveedor = ?", (nombre, id_proveedor))
            if telefono:
                self.cursor.execute("UPDATE proveedores SET telefono = ? WHERE id_proveedor = ?", (telefono, id_proveedor))
            if correo:
                self.cursor.execute("UPDATE proveedores SET correo = ? WHERE id_proveedor = ?", (correo, id_proveedor))
            self.conn.commit()
            print(f"Proveedor {id_proveedor} actualizado.")
        else:
            print(f"Proveedor con ID {id_proveedor} no encontrado.")

    def eliminar_proveedor(self, id_proveedor):
        if self.buscar_proveedor(id_proveedor):
            self.cursor.execute("DELETE FROM proveedores WHERE id_proveedor = ?", (id_proveedor,))
            self.conn.commit()
            print(f"Proveedor con ID {id_proveedor} eliminado.")
        else:
            print(f"Proveedor con ID {id_proveedor} no encontrado.")

    def buscar_proveedor(self, id_proveedor):
        self.cursor.execute("SELECT * FROM proveedores WHERE id_proveedor = ?", (id_proveedor,))
        return self.cursor.fetchone()

    def cerrar(self):
        self.conn.close()

# Función para limpiar la pantalla
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

# Función para mostrar el menú

def mostrar_menu_principal():
    print("=" * 50)
    print("\n📋 - - - Menú Principal - - - 📋")
    print("1. 🛒 Gestión de Inventario")
    print("2. 🏢 Gestión de Proveedores")
    print("3. 🚪 Salir")
    print("=" * 50)

# Menú para gestión de inventario
def mostrar_menu_inventario():
    print("=" * 50)
    print("\n📦 - - - Gestión de Inventario - - - 📦")
    print("1. ➕  Agregar producto")
    print("2. 📋  Mostrar productos")
    print("3. ✏️   Actualizar producto")
    print("4. ❌  Eliminar producto")
    print("5. 🔙 Volver al menú principal")
    print("=" * 50)

# Menú para gestión de proveedores
def mostrar_menu_proveedores():
    print("=" * 50)
    print("\n🏢 - - - Gestión de Proveedores - - - 🏢")
    print("1. ➕  Agregar proveedor")
    print("2. 📋  Mostrar proveedores")
    print("3. ✏️   Actualizar proveedor")
    print("4. ❌  Eliminar proveedor")
    print("5. 🔙 Volver al menú principal")
    print("=" * 50)

# Función principal para interactuar con el sistema
def main():
    inventario = InventarioDB()

    while True:
        limpiar_pantalla()
        mostrar_menu_principal()

        opcion_principal = input("Elige una opción: ")

        if opcion_principal == '3':  # Opción para salir
            print("Saliendo del sistema...")  
            inventario.cerrar()
            input("Presiona Enter para salir...")  
            break

        elif opcion_principal == '1':  # Menú de gestión de inventario2
            while True:
                limpiar_pantalla()
                mostrar_menu_inventario()
                
                opcion_inventario = input("Elige una opción: ")

                if opcion_inventario == '5':  # Volver al menú principal
                    break

                elif opcion_inventario == '1':  # Agregar producto
                    id_producto = solicitar_texto("ID del producto: ")
                    nombre = solicitar_texto("Nombre del producto: ")
                    cantidad = solicitar_entero("Cantidad: ")
                    precio = solicitar_flotante("Precio: ")
                    producto = Producto(id_producto, nombre, cantidad, precio)
                    inventario.agregar_producto(producto)
                    input("\nPresiona Enter para continuar...")

                elif opcion_inventario == '2':  # Mostrar productos
                    limpiar_pantalla()
                    inventario.mostrar_productos()
                    input("\nPresiona Enter para continuar...")

                elif opcion_inventario == '3':  # Actualizar producto
                    id_producto = solicitar_texto("ID del producto a actualizar: ")
                    nombre = input("Nuevo nombre (deja vacío si no deseas cambiar): ").strip()
                    cantidad = input("Nueva cantidad (deja vacío si no deseas cambiar): ").strip()
                    precio = input("Nuevo precio (deja vacío si no deseas cambiar): ").strip()

                    inventario.actualizar_producto(
                        id_producto,
                        nombre if nombre else None,
                        int(cantidad) if cantidad else None,
                        float(precio) if precio else None
                    )
                    input("\nPresiona Enter para continuar...")

                elif opcion_inventario == '4':  # Eliminar producto
                    id_producto = solicitar_texto("ID del producto a eliminar: ")
                    inventario.eliminar_producto(id_producto)
                    input("\nPresiona Enter para continuar...")

                else:
                    print("Opción no válida, intenta de nuevo.")
                    input("\nPresiona Enter para continuar...")

        elif opcion_principal == '2':  # Menú de gestión de proveedores
            while True:
                limpiar_pantalla()
                mostrar_menu_proveedores()

                opcion_proveedores = input("Elige una opción: ")

                if opcion_proveedores == '5':  # Volver al menú principal
                    break

                elif opcion_proveedores == '1':  # Agregar proveedor
                    id_proveedor = solicitar_texto("ID del proveedor: ")
                    nombre = solicitar_texto("Nombre del proveedor: ")
                    telefono = solicitar_texto("Telefono de proveedor: ")
                    correo = solicitar_texto("Correo de proveedor:")
                    proveedor = Proveedor(id_proveedor, nombre, telefono, correo)
                    inventario.agregar_proveedor(proveedor)
                    input("\nPresiona Enter para continuar...")

                elif opcion_proveedores == '2':  # Mostrar proveedores
                    limpiar_pantalla()
                    inventario.mostrar_proveedores()
                    input("\nPresiona Enter para continuar...")

                elif opcion_proveedores == '3':  # Actualizar proveedor
                    id_proveedor = solicitar_texto("ID del proveedor a actualizar: ")
                    nombre = input("Nuevo nombre (deja vacío si no deseas cambiar): ").strip()
                    telefono = input("Nuevo telefono (deja vacío si no deseas cambiar): ").strip()
                    correo = input("Nuevo correo (deja vacío si no deseas cambiar): ").strip()

                    inventario.actualizar_proveedor(
                        id_proveedor,
                        nombre if nombre else None,
                        telefono if telefono else None,
                        correo if correo else None
                    )
                    input("\nPresiona Enter para continuar...")

                elif opcion_proveedores == '4':  # Eliminar proveedor
                    id_proveedor = solicitar_texto("ID del proveedor a eliminar: ")
                    inventario.eliminar_proveedor(id_proveedor)
                    input("\nPresiona Enter para continuar...")

                else:
                    print("Opción no válida, intenta de nuevo.")
                    input("\nPresiona Enter para continuar...")

        else:
            print("Opción no válida, intenta de nuevo.")
            input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    main()
limpiar_pantalla()  