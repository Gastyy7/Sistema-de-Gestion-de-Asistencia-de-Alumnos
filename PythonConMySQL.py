import tkinter as tk

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import PhotoImage
from Conexion import *

class FormularioAlumnos:

 global base
 base =None
    
 global textBoxId
 textBoxId =None

 global textBoxNombres
 textBoxNombres =None

 global textBoxApellidos
 textBoxApellidos =None

 global textBoxDNI
 textBoxDNI =None

 global textBoxFechaNacimiento
 textBoxFechaNacimiento =None

 global textBoxTelefono
 textBoxTelefono =None

 global textBoxDomicilio
 textBoxDomicilio =None

 global groupBox
 groupBox =None

 global tree
 tree =None
    

def Formulario():

  global base
  global groupBox
  global tree

try:
    # Crear la conexión a la base de datos usando CConexion
    db = CConexion.ConexionBaseDeDatos()
    cursor = db.cursor()

    base = Tk()
    base.geometry("1200x600")
    base.title("Gestión de Cursos y Estudiantes")

    # Cursos y Estudiantes
    groupBoxCursos = LabelFrame(base, text="Cursos y Estudiantes", padx=5, pady=5)
    groupBoxCursos.pack(fill=BOTH, expand=True, padx=15, pady=15)

    # Lista de cursos
    course_frame = Frame(groupBoxCursos)
    course_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

    Label(course_frame, text="Cursos", font=("Arial", 12)).pack(anchor="w", padx=5, pady=5)
    course_list = Listbox(course_frame, height=12)

    # Generar cursos desde 1ro a hasta 6to c
    courses = [f"{grado} {seccion}" for grado in ["1°", "2°", "3°", "4°", "5°", "6°"] for seccion in ["A", "B", "C"]]
    for course in courses:
        course_list.insert(END, course)
    course_list.pack(fill=BOTH, expand=True)

    # Tabla de estudiantes
    student_frame = Frame(groupBoxCursos)
    student_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)
    control_frame = Frame(student_frame)
    control_frame.pack(side=TOP, fill=X, padx=10, pady=5) 

    student_tree = ttk.Treeview(student_frame, columns=("ID", "Fecha", "Nombre", "Apellido", "Presente/Ausente", "Observaciones"), show='headings', height=12)
    student_tree.heading("ID", text="ID")
    student_tree.column("ID", width=50, anchor=CENTER)

    student_tree.heading("Fecha", text="Fecha")
    student_tree.column("Fecha", width=100, anchor=CENTER)

    student_tree.heading("Nombre", text="Nombre")
    student_tree.column("Nombre", width=150, anchor=W)

    student_tree.heading("Apellido", text="Apellido")
    student_tree.column("Apellido", width=150, anchor=W)

    student_tree.heading("Presente/Ausente", text="Asistencia")
    student_tree.column("Presente/Ausente", width=120, anchor=CENTER)

    student_tree.heading("Observaciones", text="Observaciones")
    student_tree.column("Observaciones", width=200, anchor=W)

    student_tree.pack(fill=BOTH, expand=True)

    from tkinter import Menu


    def ordenar_alumnos(criterio):

      if not course_list.curselection():
        messagebox.showwarning("Selección", "Por favor selecciona un curso primero")
        return
    
      selected_course = course_list.get(course_list.curselection())
      table_name = selected_course.lower().replace("°", "").replace(" ", "_")

      try:
 
        query = f"SELECT id, fecha, nombre, apellido, presente_ausente, observaciones FROM `{table_name}` ORDER BY {criterio}"
        cursor.execute(query)
        students = cursor.fetchall()

        for row in student_tree.get_children():
            student_tree.delete(row)

        for student in students:
            estado_presente = "Presente" if student[4] == 1 else "Ausente"
            formatted_student = (student[0], student[1], student[2], student[3], estado_presente, student[5])
            student_tree.insert("", END, values=formatted_student)

      except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudo ordenar a los alumnos: {err}")


    ordenar_menu = Menu(base, tearoff=0)
    ordenar_menu.add_command(label="Ordenar por ID", command=lambda: ordenar_alumnos("id"))
    ordenar_menu.add_command(label="Ordenar por Apellido", command=lambda: ordenar_alumnos("apellido"))


    ordenar_button = Button(control_frame, text="Ordenar Alumnos", command=lambda: ordenar_menu.post(base.winfo_pointerx(), base.winfo_pointery()))
    ordenar_button.pack(side=LEFT, padx=5, pady=5)


    def load_students(event):
      try:
        if not course_list.curselection():
            return 

        selected_course = course_list.get(course_list.curselection()) 

        table_name = selected_course.lower().replace("°", "").replace(" ", "_")  
        print(f"Nombre de la tabla generado: {table_name}") 

        cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
        result = cursor.fetchone()
        if not result:
            raise Exception(f"La tabla '{table_name}' no existe en la base de datos")

        for row in student_tree.get_children():
            student_tree.delete(row)

        query = f"SELECT id, fecha, nombre, apellido, presente_ausente, observaciones FROM `{table_name}`"
        cursor.execute(query)
        students = cursor.fetchall()

        for student in students:
            estado_presente = "Presente" if student[4] == 1 else "Ausente"
            formatted_student = (student[0], student[1], student[2], student[3], estado_presente, student[5])
            student_tree.insert("", END, values=formatted_student)

      except mysql.connector.Error as err:
        print(f"Error MySQL: {err}") 
        messagebox.showerror("Error", f"No se pudo cargar estudiantes: {err}")
      except Exception as e:
        print(f"Error: {e}")  
        messagebox.showerror("Error", f"No se pudo cargar estudiantes: {e}")

    course_list.bind("<<ListboxSelect>>", load_students)


    import re
    from tkinter import messagebox, StringVar, Toplevel, Label, Entry, OptionMenu, Button

    def agregar_alumno():
      add_window = Toplevel(base)
      add_window.title("Agregar Alumno")
      add_window.geometry("400x350")

    # Etiquetas y campos de entrada
      Label(add_window, text="Nombre:", font=("Arial", 12)).grid(row=0, column=0, pady=10, padx=10, sticky="w")
      entry_nombre = Entry(add_window, width=30)
      entry_nombre.grid(row=0, column=1, pady=10, padx=10)
      entry_nombre.insert(0, "Complete el campo (solo letras)")
      entry_nombre.config(fg="grey") 

      Label(add_window, text="Apellido:", font=("Arial", 12)).grid(row=1, column=0, pady=10, padx=10, sticky="w")
      entry_apellido = Entry(add_window, width=30)
      entry_apellido.grid(row=1, column=1, pady=10, padx=10)
      entry_apellido.insert(0, "Complete el campo (solo letras)")  
      entry_apellido.config(fg="grey")  

      Label(add_window, text="Observaciones:", font=("Arial", 12)).grid(row=4, column=0, pady=10, padx=10, sticky="w")
      entry_observaciones = Entry(add_window, width=30)
      entry_observaciones.grid(row=4, column=1, pady=10, padx=10)
      entry_observaciones.insert(0, "Complete el campo (solo letras)") 
      entry_observaciones.config(fg="grey") 

      def borrar_mensaje(entry, placeholder_text):
        if entry.get() == placeholder_text:
            entry.delete(0, "end")
            entry.config(fg="black")

      def restaurar_mensaje(entry, placeholder_text):
        if entry.get() == "":
            entry.insert(0, placeholder_text)
            entry.config(fg="grey")

      entry_nombre.bind("<FocusIn>", lambda event: borrar_mensaje(entry_nombre, "Complete el campo (solo letras)"))
      entry_nombre.bind("<FocusOut>", lambda event: restaurar_mensaje(entry_nombre, "Complete el campo (solo letras)"))

      entry_apellido.bind("<FocusIn>", lambda event: borrar_mensaje(entry_apellido, "Complete el campo (solo letras)"))
      entry_apellido.bind("<FocusOut>", lambda event: restaurar_mensaje(entry_apellido, "Complete el campo (solo letras)"))

      entry_observaciones.bind("<FocusIn>", lambda event: borrar_mensaje(entry_observaciones, "Complete el campo (solo letras)"))
      entry_observaciones.bind("<FocusOut>", lambda event: restaurar_mensaje(entry_observaciones, "Complete el campo (solo letras)"))

      Label(add_window, text="Curso:", font=("Arial", 12)).grid(row=2, column=0, pady=10, padx=10, sticky="w")

    # Generar cursos desde 1ro a hasta 6to c"
      courses = [f"{grado} {seccion}" for grado in ["1°", "2°", "3°", "4°", "5°", "6°"] for seccion in ["A", "B", "C"]]

      selected_course = StringVar()
      selected_course.set(courses[0]) 

      option_course = OptionMenu(add_window, selected_course, *courses)
      option_course.grid(row=2, column=1, pady=10, padx=10)

      Label(add_window, text="Asistencia:", font=("Arial", 12)).grid(row=3, column=0, pady=10, padx=10, sticky="w")
    
      presente_ausente_options = ["Presente", "Ausente"]
      selected_presente = StringVar()
      selected_presente.set(presente_ausente_options[0])  
    
      option_presente = OptionMenu(add_window, selected_presente, *presente_ausente_options)
      option_presente.grid(row=3, column=1, pady=10, padx=10)

      def es_valido(nombre):
        return bool(re.match("^[A-Za-záéíóúÁÉÍÓÚñÑ]+$", nombre))

      def es_valido_observaciones(observaciones):
        return bool(re.match("^[A-Za-z0-9áéíóúÁÉÍÓÚñÑ., ]*$", observaciones))

      def guardar_alumno():
        nombre = entry_nombre.get()
        apellido = entry_apellido.get()
        observaciones = entry_observaciones.get()

        # Validar los campos de nombre y apellido
        if not nombre or not apellido or nombre == "Complete el campo (solo letras)" or apellido == "Complete el campo (solo letras)" or observaciones == "Complete el campo (solo letras)":
            messagebox.showerror("Error", "Debe completar los campos de nombre, apellido y observaciones para continuar.")
            return
        if not es_valido(nombre) or not es_valido(apellido):
            messagebox.showerror("Error", "Los campos de nombre, apellido y obervaciones solo deben contener letras y no deben estar vacíos.")
            return

        # Validar el campo de observaciones
        if not observaciones or observaciones == "Debe completar el campo (sin caracteres especiales)":
            messagebox.showerror("Error", "Debe completar el campo de observaciones.")
            return
        if not es_valido_observaciones(observaciones):
            messagebox.showerror("Error", "El campo de observaciones solo puede contener letras, números, espacios y algunos caracteres especiales como puntos y comas.")
            return

        curso_seleccionado = selected_course.get() 
        table_name = curso_seleccionado.replace(" ", "_").replace("°", "")  

        presente = selected_presente.get()  # Obtener el valor seleccionado del OptionMenu

        # Si la columna presente_ausente es de tipo BOOLEAN, guardamos True o False
        presente_boolean = True if presente == "Presente" else False

        try:
            query = f"INSERT INTO `{table_name}` (fecha, nombre, apellido, presente_ausente, observaciones) VALUES (CURDATE(), %s, %s, %s, %s)"
            cursor.execute(query, (nombre, apellido, presente_boolean, observaciones))
            db.commit()
            messagebox.showinfo("Éxito", "Alumno agregado exitosamente")
            add_window.destroy()
            load_students(None) 
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"No se pudo agregar el alumno: {err}")

      Button(add_window, text="Guardar", command=guardar_alumno, width=15).grid(row=5, column=0, columnspan=2, pady=20)

    import re  

    def modificar_alumno():
      try:
        selected_item = student_tree.selection()[0]
        student_id = student_tree.item(selected_item)["values"][0]
        selected_course = course_list.get(course_list.curselection())
        table_name = selected_course.replace(" ", "_").replace("°", "")


        modify_window = Toplevel(base)
        modify_window.title("Modificar Alumno")
        modify_window.geometry("400x300")

        # Campos de entrada
        Label(modify_window, text="Nombre:", font=("Arial", 12)).grid(row=0, column=0, pady=10, padx=10, sticky="w")
        entry_nombre = Entry(modify_window, width=30)
        entry_nombre.grid(row=0, column=1, pady=10, padx=10)

        Label(modify_window, text="Apellido:", font=("Arial", 12)).grid(row=1, column=0, pady=10, padx=10, sticky="w")
        entry_apellido = Entry(modify_window, width=30)
        entry_apellido.grid(row=1, column=1, pady=10, padx=10)

        Label(modify_window, text="Curso:", font=("Arial", 12)).grid(row=2, column=0, pady=10, padx=10, sticky="w")
        courses = [f"{grado} {seccion}" for grado in ["1°", "2°", "3°", "4°", "5°", "6°"] for seccion in ["A", "B", "C"]]
        selected_course_var = StringVar()
        selected_course_var.set(selected_course)
        option_course = OptionMenu(modify_window, selected_course_var, *courses)
        option_course.grid(row=2, column=1, pady=10, padx=10)

        Label(modify_window, text="Asistencia:", font=("Arial", 12)).grid(row=3, column=0, pady=10, padx=10, sticky="w")
        presente_ausente_options = ["Presente", "Ausente"]
        selected_presente_var = StringVar()
        selected_presente_var.set("Presente")  
        option_presente = OptionMenu(modify_window, selected_presente_var, *presente_ausente_options)
        option_presente.grid(row=3, column=1, pady=10, padx=10)

        Label(modify_window, text="Observaciones:", font=("Arial", 12)).grid(row=4, column=0, pady=10, padx=10, sticky="w")
        entry_observaciones = Entry(modify_window, width=30)
        entry_observaciones.grid(row=4, column=1, pady=10, padx=10)

        query = f"SELECT nombre, apellido, presente_ausente, observaciones FROM `{table_name}` WHERE id = %s"
        cursor.execute(query, (student_id,))
        data = cursor.fetchone()
        entry_nombre.insert(0, data[0])
        entry_apellido.insert(0, data[1])
        selected_presente_var.set("Presente" if data[2] else "Ausente")
        entry_observaciones.insert(0, data[3])

        # Validación de campos
        def es_valido(campo):
            return bool(re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ ]+$", campo.strip()))

        def guardar_modificaciones():
            nuevo_nombre = entry_nombre.get().strip()
            nuevo_apellido = entry_apellido.get().strip()
            nuevo_curso = selected_course_var.get().replace(" ", "_").replace("°", "")
            nuevo_presente = True if selected_presente_var.get() == "Presente" else False
            nuevas_observaciones = entry_observaciones.get().strip()

            # Validaciones
            if not nuevo_nombre:
                messagebox.showerror("Error", "El campo Nombre es obligatorio.")
                return
            if not es_valido(nuevo_nombre):
                messagebox.showerror("Error", "El campo Nombre no debe contener números ni caracteres especiales.")
                return
            if not nuevo_apellido:
                messagebox.showerror("Error", "El campo Apellido es obligatorio.")
                return
            if not es_valido(nuevo_apellido):
                messagebox.showerror("Error", "El campo Apellido no debe contener números ni caracteres especiales.")
                return
            if not nuevas_observaciones:
                messagebox.showerror("Error", "El campo Observaciones es obligatorio.")
                return
            if not es_valido(nuevas_observaciones):
                messagebox.showerror("Error", "El campo Observaciones no debe contener números ni caracteres especiales.")
                return

            try:
                query_update = f"""
                UPDATE `{table_name}` 
                SET nombre = %s, apellido = %s, presente_ausente = %s, observaciones = %s 
                WHERE id = %s
                """
                cursor.execute(query_update, (nuevo_nombre, nuevo_apellido, nuevo_presente, nuevas_observaciones, student_id))

                if nuevo_curso != table_name:
                    query_insert_new_course = f"""
                    INSERT INTO `{nuevo_curso}` (fecha, nombre, apellido, presente_ausente, observaciones)
                    SELECT fecha, %s, %s, %s, %s FROM `{table_name}` WHERE id = %s
                    """
                    cursor.execute(query_insert_new_course, (nuevo_nombre, nuevo_apellido, nuevo_presente, nuevas_observaciones, student_id))

                    query_delete_old_course = f"DELETE FROM `{table_name}` WHERE id = %s"
                    cursor.execute(query_delete_old_course, (student_id,))

                db.commit()
                messagebox.showinfo("Éxito", "Alumno modificado exitosamente")
                modify_window.destroy()
                load_students(None)  
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"No se pudo modificar el alumno: {err}")

        Button(modify_window, text="Guardar Cambios", command=guardar_modificaciones, width=20).grid(row=5, column=0, columnspan=2, pady=20)
      except IndexError:
        messagebox.showwarning("Selección", "Por favor selecciona un alumno para modificar")

    # Función para eliminar alumno
    def eliminar_alumno():
      try:
        selected_item = student_tree.selection()
        if not selected_item:
            messagebox.showwarning("Selección", "Por favor selecciona un alumno para eliminar")
            return

        student_id = student_tree.item(selected_item[0])["values"][0]

        if not course_list.curselection():
            messagebox.showwarning("Selección", "Por favor selecciona un curso primero")
            return

        selected_course = course_list.get(course_list.curselection())
        table_name = selected_course.replace(" ", "_").replace("°", "")

        # Confirmar eliminación
        confirm = messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de que deseas eliminar al alumno con ID {student_id}?")
        if confirm:

            query = f"DELETE FROM `{table_name}` WHERE id = %s"
            cursor.execute(query, (student_id,))
            db.commit()
            
            messagebox.showinfo("Éxito", "Alumno eliminado exitosamente")
            load_students(None) 

      except IndexError:
        messagebox.showwarning("Selección", "Por favor selecciona un alumno para eliminar")
      except mysql.connector.Error as err:
        messagebox.showerror("Error", f"No se pudo eliminar al alumno: {err}")
      except Exception as e:
        messagebox.showerror("Error", f"Ha ocurrido un error inesperado: {e}")


    # Botones 
    button_frame = Frame(base)
    button_frame.pack(fill=X, padx=15, pady=10)

    Button(button_frame, text="Agregar Alumno", command=agregar_alumno, width=20).pack(side=LEFT, padx=5)
    Button(button_frame, text="Modificar", command=modificar_alumno, width=20).pack(side=LEFT, padx=5)
    Button(button_frame, text="Eliminar", command=eliminar_alumno, width=20).pack(side=LEFT, padx=5)

    base.mainloop()
    

except Exception as error:
    print("Error al mostrar interfaz, error: {}".format(error))

Formulario()   
