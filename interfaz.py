import tkinter as tk
from tkinter import messagebox, Frame, StringVar, OptionMenu
from tkinter import ttk 
from modulos import User
import matplotlib.pyplot as plt
from collections import defaultdict
import json
import os
from datetime import datetime
from tkcalendar import DateEntry
import re
import pandas as pd 
from pandas import ExcelWriter
from fpdf import FPDF
class AnimatedButton(tk.Button):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.default_bg = self["bg"]
        self.default_fg = self["fg"]
        self.default_font = self["font"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self["bg"] = getattr(self, "hover_bg", "#555")
        self["fg"] = "white"
        if isinstance(self.default_font, tuple):
            font_name, font_size, *rest = self.default_font
            self["font"] = (font_name, font_size + 3, *rest)
        else:
            self["font"] = (self.default_font, 15)
        self.config(cursor="hand2")

    def on_leave(self, e):
        self["bg"] = self.default_bg
        self["fg"] = self.default_fg
        self["font"] = self.default_font
        self.config(cursor="")

class Interfaz:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("💰 Aplicación de Monitoreo de Gastos 💰")
        self.ventana.geometry("600x600")
        self.ventana.config(bg="#e0f7fa")
        self.users = {}
        self.current_user = None
        self.cargar_usuarios()
        self.create_login_screen()

    def create_login_screen(self):
        self.clear_screen()
        self.create_header("Iniciar Sesión")
        
        tk.Label(self.ventana, text="Email:", bg="#e0f7fa", fg="#004d40").pack(pady=5)
        self.email_entry = tk.Entry(self.ventana, font=("Arial", 12))
        self.email_entry.pack(pady=5)

        tk.Label(self.ventana, text="Contraseña:", bg="#e0f7fa", fg="#004d40").pack(pady=5)
        self.password_entry = tk.Entry(self.ventana, show="*", font=("Arial", 12))
        self.password_entry.pack(pady=5)

        btn_login = AnimatedButton(self.ventana, text="Iniciar Sesión", command=self.login,
                                   bg="#00796b", fg="white", font=("Arial", 12, "bold"))
        btn_login.hover_bg = "#004d40"
        btn_login.pack(pady=10)

        btn_register = AnimatedButton(self.ventana, text="Registrarse", command=self.create_register_screen,
                                      bg="#009688", fg="white", font=("Arial", 12, "bold"))
        btn_register.hover_bg = "#00675b"
        btn_register.pack(pady=5)

    def create_register_screen(self):
        self.clear_screen()
        self.create_header("Registro")
        
        tk.Label(self.ventana, text="Nombre:", bg="#e0f7fa", fg="#004d40").pack(pady=5)
        self.name_entry = tk.Entry(self.ventana, font=("Arial", 12))
        self.name_entry.pack(pady=5)

        tk.Label(self.ventana, text="Email:", bg="#e0f7fa", fg="#004d40").pack(pady=5)
        self.email_entry = tk.Entry(self.ventana, font=("Arial", 12))
        self.email_entry.pack(pady=5)

        tk.Label(self.ventana, text="Contraseña:", bg="#e0f7fa", fg="#004d40").pack(pady=5)
        self.password_entry = tk.Entry(self.ventana, show="*", font=("Arial", 12))
        self.password_entry.pack(pady=5)

        btn_register = AnimatedButton(self.ventana, text="Registrar", command=self.register,
                                      bg="#00796b", fg="white", font=("Arial", 12, "bold"))
        btn_register.hover_bg = "#004d40"
        btn_register.pack(pady=10)

        btn_back = AnimatedButton(self.ventana, text="Volver", command=self.create_login_screen,
                                  bg="#FF5722", fg="white", font=("Arial", 12, "bold"))
        btn_back.hover_bg = "#e64a19"
        btn_back.pack(pady=5)

    def create_header(self, title):
        header_frame = Frame(self.ventana, bg="#00796b")
        header_frame.pack(fill="x")
        tk.Label(header_frame, text=title, font=("Arial", 20, "bold"), bg="#00796b", fg="white").pack(pady=10)

    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        user = self.users.get(email)

        if user and user.password == password:
            self.current_user = user
            self.create_main_screen()
        else:
            messagebox.showerror("Error", "Email o contraseña incorrectos.")

    def register(self):
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not name or not email or not password:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        if not self.validate_email(email):
            messagebox.showerror("Error", "Email no válido.")
            return

        if email in self.users:
            messagebox.showerror("Error", "El email ya está registrado.")
            return

        self.users[email] = User(name, email, password)
        self.guardar_usuarios()
        messagebox.showinfo("Éxito", "Usuario registrado exitosamente.")
        self.create_login_screen()

    def create_main_screen(self):
        self.clear_screen()
        self.create_header(f"Bienvenido, {self.current_user.name} 🎉")

        opciones = [
            ("Agregar Ingreso", self.create_income_screen, "#4CAF50", "#357a38"),
            ("Agregar Gasto", self.create_expense_screen, "#FF9800", "#c66900"),
            ("Generar Reporte Mensual", self.exportar_reporte_excel, "#2196F3", "#1769aa"),
            ("Visualizar Gastos Mensuales", self.visualize_monthly_expenses, "#FFC107", "#FFA000"),
            ("Buscar Transacciones", self.search_transactions, "#FF5722", "#e64a19"),
            ("Predecir Situación Económica", self.predecir_situacion_financiera, "#9C27B0", "#7B1FA2"),
            ("Ver Recomendaciones", self.generar_recomendaciones_financieras, "#4A148C", "#6A1B9A"),
            ("Exportar Reporte a PDF", self.exportar_reporte_pdf, "#607D8B", "#455A64"),
            ("Cerrar Sesión", self.logout, "#F44336", "#aa2e25"),
            
          
        ]

        for text, command, bg, hover in opciones:
            btn = AnimatedButton(self.ventana, text=text, command=command, bg=bg, fg="black", font=("Arial", 12, "bold"))
            btn.hover_bg = hover
            btn.pack(pady=10)

    def logout(self):
        self.current_user = None
        self.create_login_screen()

    def create_income_screen(self):
        self.clear_screen()
        self.create_header("Agregar Ingreso")

        tk.Label(self.ventana, text="Monto:", bg="#e0f7fa", fg="#004d40").pack(pady=5)
        self.income_amount_entry = tk.Entry(self.ventana, font=("Arial", 12))
        self.income_amount_entry.pack(pady=5)

        tk.Label(self.ventana, text="Tipo de Ingreso:", bg="#e0f7fa", fg="#004d40").pack(pady=5)
        self.income_type_var = StringVar(self.ventana)
        self.income_type_var.set("Fijo")
        OptionMenu(self.ventana, self.income_type_var, "Fijo", "Variable").pack(pady=5)

        tk.Label(self.ventana, text="Fecha:", bg="#e0f7fa", fg="#004d40").pack(pady=5)
        self.income_date_entry = DateEntry(self.ventana, width=12, background='darkblue',
                                        foreground='white', date_pattern='yyyy-mm-dd', font=("Arial", 12))
        self.income_date_entry.pack(pady=5)



        btn_save_income = AnimatedButton(self.ventana, text="Guardar Ingreso", command=self.save_income,
                                        bg="#4CAF50", fg="black", font=("Arial", 12, "bold"))
        btn_save_income.hover_bg = "#357a38"
        btn_save_income.pack(pady=10)

        btn_back = AnimatedButton(self.ventana, text="Volver", command=self.create_main_screen,
                                  bg="#FF5722", fg="black", font=("Arial", 12, "bold"))
        btn_back.hover_bg = "#e64a19"
        btn_back.pack(pady=5)

    def create_expense_screen(self):
        self.clear_screen()
        self.create_header("Agregar Gasto")

        tk.Label(self.ventana, text="Monto:", bg="#e0f7fa", fg="#004d40").pack(pady=5)
        self.expense_amount_entry = tk.Entry(self.ventana, font=("Arial", 12))
        self.expense_amount_entry.pack(pady=5)

        tk.Label(self.ventana, text="Categoría:", bg="#e0f7fa", fg="#004d40").pack(pady=5)
        self.expense_category_var = StringVar(self.ventana)
        self.expense_category_var.set("Alimentación")
        OptionMenu(self.ventana, self.expense_category_var, "Alimentación", "Transporte", "Educación", "Recreación").pack(pady=5)

        tk.Label(self.ventana, text="Fecha:", bg="#e0f7fa", fg="#004d40").pack(pady=5)
        self.expense_date_entry = DateEntry(self.ventana, width=12, background='darkblue',
                                            foreground='white', date_pattern='yyyy-mm-dd', font=("Arial", 12))
        self.expense_date_entry.pack(pady=5)



        btn_save_expense = AnimatedButton(self.ventana, text="Guardar Gasto", command=self.save_expense,
                                         bg="#FF9800", fg="white", font=("Arial", 12, "bold"))
        btn_save_expense.hover_bg = "#c66900"
        btn_save_expense.pack(pady=10)

        btn_back = AnimatedButton(self.ventana, text="Volver", command=self.create_main_screen,
                                  bg="#FF5722", fg="white", font=("Arial", 12, "bold"))
        btn_back.hover_bg = "#e64a19"
        btn_back.pack(pady=5)

    def save_income(self):
        """Guardar ingreso"""
        monto_str = self.income_amount_entry.get()
        if not monto_str.strip():
            messagebox.showerror("Error", "Debe ingresar un monto.")
            return
        try:
            monto = float(monto_str)
            if monto <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "El monto debe ser un número mayor que cero.")
            return

        tipo = self.income_type_var.get()
        fecha = self.income_date_entry.get().strip()

        if not fecha:
            messagebox.showerror("Error", "Debe ingresar una fecha.")
            return
        if not self.validate_date(fecha):
            messagebox.showerror("Error", "La fecha no es válida. Use el formato YYYY-MM-DD.")
            return

        self.current_user.add_income(monto, tipo, fecha)
        self.guardar_usuarios()
        messagebox.showinfo("Éxito", "Ingreso agregado exitosamente.")
        self.create_main_screen()

    def save_expense(self):
        """Guardar gasto con validaciones."""
        monto_str = self.expense_amount_entry.get()
        if not monto_str.strip():
            messagebox.showerror("Error", "Debe ingresar un monto.")
            return
        try:
            monto = float(monto_str)
            if monto <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "El monto debe ser un número mayor que cero.")
            return

        categoria = self.expense_category_var.get()
        fecha = self.expense_date_entry.get().strip()

        if not fecha:
            messagebox.showerror("Error", "Debe ingresar una fecha.")
            return
        if not self.validate_date(fecha):
            messagebox.showerror("Error", "La fecha no es válida. Use el formato YYYY-MM-DD.")
            return

        self.current_user.add_expense(monto, categoria, fecha)
        self.guardar_usuarios()
        messagebox.showinfo("Éxito", "Gasto agregado exitosamente.")
        self.create_main_screen()

   

    def visualize_monthly_expenses(self):
        """Visualizar gastos mensuales mediante gráficas."""
        categorias = defaultdict(float)

        for transaccion in self.current_user.expenses:
            categorias[transaccion.category] += transaccion.amount

        if not categorias:
            messagebox.showinfo("Gráfica de Gastos", "No hay gastos registrados.")
            return

        # Usar pandas para crear un DataFrame
        df = pd.DataFrame(list(categorias.items()), columns=['Categoría', 'Monto'])
        
        plt.figure(figsize=(8, 5))
        plt.bar(df['Categoría'], df['Monto'], color='coral')
        plt.title("Gastos Mensuales por Categoría")
        plt.xlabel("Categoría")
        plt.ylabel("Monto ($)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show(block=False)
    def predecir_situacion_financiera(self):
        if not self.current_user.income and not self.current_user.expenses:
            messagebox.showinfo("Predicción", "No hay datos suficientes para hacer una predicción.")
            return

        ingresos_mensuales = defaultdict(float)
        gastos_mensuales = defaultdict(float)

        for transaccion in self.current_user.income:
            mes = transaccion.date[:7]  # YYYY-MM
            ingresos_mensuales[mes] += transaccion.amount

        for transaccion in self.current_user.expenses:
            mes = transaccion.date[:7]
            gastos_mensuales[mes] += transaccion.amount

        meses = sorted(set(ingresos_mensuales) | set(gastos_mensuales))
        balances = []

        for mes in meses:
            ingreso = ingresos_mensuales.get(mes, 0)
            gasto = gastos_mensuales.get(mes, 0)
            balances.append(ingreso - gasto)

        if not balances:
            messagebox.showinfo("Predicción", "No hay datos suficientes para calcular balances mensuales.")
            return

        balance_promedio = sum(balances) / len(balances)

        if balance_promedio > 0:
            mensaje = f"Tendencia positiva 💚\nSaldo promedio mensual: ${balance_promedio:.2f}"
        elif balance_promedio < 0:
            mensaje = f"Tendencia negativa 🔴\nEstás gastando más de lo que ganas.\nSaldo promedio mensual: ${balance_promedio:.2f}"
        else:
            mensaje = "Tendencia neutra ⚪\nTus ingresos y gastos están completamente equilibrados."

        messagebox.showinfo("Predicción Financiera", mensaje)
    def generar_recomendaciones_financieras(self):
        if not self.current_user.expenses:
            messagebox.showinfo("Recomendaciones", "Aún no hay gastos para analizar.")
            return

        total_gastos = sum(t.amount for t in self.current_user.expenses)
        categorias = defaultdict(float)

        for transaccion in self.current_user.expenses:
            categorias[transaccion.category] += transaccion.amount

        recomendaciones = []

        for categoria, monto in categorias.items():
            porcentaje = (monto / total_gastos) * 100
            if porcentaje >= 40:
                recomendaciones.append(f"⚠️ Gastas mucho en '{categoria}' ({porcentaje:.1f}%). Considera reducirlo.")

        if not recomendaciones:
            mensaje = "✅ Tus gastos están bien distribuidos.\n¡Sigue así!"
        else:
            mensaje = "\n\n".join(recomendaciones)

        messagebox.showinfo("Recomendaciones Financieras", mensaje)
    


    def exportar_reporte_pdf(self):
        if not self.current_user:
            messagebox.showerror("Error", "No hay usuario activo.")
            return

        if not self.current_user.income and not self.current_user.expenses:
            messagebox.showinfo("Exportar PDF", "No hay transacciones para exportar.")
            return

        #imagn de la gráfica
        categorias = defaultdict(float)
        for transaccion in self.current_user.expenses:
            categorias[transaccion.category] += transaccion.amount

        if categorias:
            nombres = list(categorias.keys())
            montos = list(categorias.values())
            plt.figure(figsize=(6, 4))
            plt.bar(nombres, montos, color='teal')
            plt.title("Gastos por categoría")
            plt.xlabel("Categoría")
            plt.ylabel("Monto")
            plt.tight_layout()
            plt.savefig("grafica_gastos.png")
            plt.close()

        # Generar PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "Reporte Financiero", ln=1, align='C')

        total_income, total_expenses, balance = self.current_user.generate_report()
        pdf.set_font("Arial", size=12)
        pdf.ln(10)
        pdf.cell(0, 10, f"Ingresos totales: ${total_income:.2f}", ln=1)
        pdf.cell(0, 10, f"Gastos totales: ${total_expenses:.2f}", ln=1)
        pdf.cell(0, 10, f"Balance: ${balance:.2f}", ln=1)

        pdf.ln(10)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Ingresos:", ln=1)
        pdf.set_font("Arial", size=12)
        for t in self.current_user.income:
            pdf.cell(0, 10, f"- {t.category} | ${t.amount} | {t.date}", ln=1)

        pdf.ln(5)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, "Gastos:", ln=1)
        pdf.set_font("Arial", size=12)
        for t in self.current_user.expenses:
            pdf.cell(0, 10, f"- {t.category} | ${t.amount} | {t.date}", ln=1)

        if categorias:
            pdf.ln(10)
            pdf.image("grafica_gastos.png", x=20, w=170)

        nombre_archivo = f"reporte_{self.current_user.name}.pdf"
        pdf.output(nombre_archivo)

        messagebox.showinfo("Exportar a PDF", f"Reporte exportado como '{nombre_archivo}'")



    def search_transactions(self):
        self.clear_screen()
        self.create_header("Buscar Transacciones por Fecha")

        tk.Label(self.ventana, text="Fecha inicial:", bg="#e0f7fa", fg="#004d40").pack(pady=5)
        self.fecha_inicio_entry = DateEntry(self.ventana, width=12, background='darkblue',
                                            foreground='white', date_pattern='yyyy-mm-dd', font=("Arial", 12))
        self.fecha_inicio_entry.pack(pady=5)

        tk.Label(self.ventana, text="Fecha final:", bg="#e0f7fa", fg="#004d40").pack(pady=5)
        self.fecha_fin_entry = DateEntry(self.ventana, width=12, background='darkblue',
                                        foreground='white', date_pattern='yyyy-mm-dd', font=("Arial", 12))
        self.fecha_fin_entry.pack(pady=5)

        btn_search = AnimatedButton(self.ventana, text="Buscar por fecha", command=self.buscar_transacciones_por_rango,
                                    bg="#2196F3", fg="white", font=("Arial", 12, "bold"))
        btn_search.hover_bg = "#1769aa"
        btn_search.pack(pady=10)
        btn_ver_todas = AnimatedButton(
            self.ventana, 
            text="Ver Todas las Transacciones", 
            command=self.ver_todas_las_transacciones,
            bg="#009688", fg="white", font=("Arial", 12, "bold")
        )
        btn_ver_todas.hover_bg = "#00675b"
        btn_ver_todas.pack(pady=5)


        btn_back = AnimatedButton(self.ventana, text="Volver", command=self.create_main_screen,
                                bg="#FF5722", fg="white", font=("Arial", 12, "bold"))
        btn_back.hover_bg = "#e64a19"
        btn_back.pack(pady=5)

    def buscar_transacciones_por_rango(self):
        fecha_inicio = self.fecha_inicio_entry.get().strip()
        fecha_fin = self.fecha_fin_entry.get().strip()

        try:
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha inválido. Usa YYYY-MM-DD.")
            return

        if fecha_inicio > fecha_fin:
            messagebox.showerror("Error", "La fecha inicial no puede ser posterior a la final.")
            return

        resultados = []

        for t in self.current_user.income:
            fecha_t = datetime.strptime(t.date, "%Y-%m-%d")
            if fecha_inicio <= fecha_t <= fecha_fin:
                resultados.append(("Ingreso", t.category, t.amount, t.date))

        for t in self.current_user.expenses:
            fecha_t = datetime.strptime(t.date, "%Y-%m-%d")
            if fecha_inicio <= fecha_t <= fecha_fin:
                resultados.append(("Gasto", t.category, t.amount, t.date))

        self.mostrar_resultados_en_tabla_con_columnas(resultados)
    def mostrar_resultados_en_tabla_con_columnas(self, resultados):
            ventana = tk.Toplevel(self.ventana)
            ventana.title("Resultados")
            ventana.geometry("800x400")

            columns = ("tipo", "categoría", "monto", "fecha")
            tree = ttk.Treeview(ventana, columns=columns, show="headings")

            for col in columns:
                tree.heading(col, text=col.capitalize())
                tree.column(col, anchor="center")

            for tipo, cat, monto, fecha in resultados:
                tree.insert("", "end", values=(tipo, cat, f"${monto:.2f}", fecha))

            tree.pack(expand=True, fill="both") 
            for col in columns:
                tree.heading(col, text=col.capitalize())
                tree.column(col, anchor="center")

         

            def eliminar_transaccion():
                seleccion = tree.selection()
                if not seleccion:
                    messagebox.showerror("Error", "Selecciona una transacción para eliminar.")
                    return

                tipo, cat, monto_str, fecha = tree.item(seleccion[0])["values"]
                monto = float(monto_str.replace("$", ""))

                if tipo == "Ingreso":
                    self.current_user.income = [t for t in self.current_user.income if not (t.category == cat and t.amount == monto and t.date == fecha)]
                else:
                    self.current_user.expenses = [t for t in self.current_user.expenses if not (t.category == cat and t.amount == monto and t.date == fecha)]

                self.guardar_usuarios()
                tree.delete(seleccion[0])
                messagebox.showinfo("Éxito", "Transacción eliminada correctamente.")

            btn_eliminar = AnimatedButton(ventana, text="Eliminar Seleccionada", command=eliminar_transaccion,
                                        bg="#F44336", fg="white", font=("Arial", 12, "bold"))
            btn_eliminar.hover_bg = "#B71C1C"
            btn_eliminar.pack(pady=10)

            if not resultados:
                messagebox.showinfo("Sin resultados", "No se encontraron transacciones en ese rango.")

            
    


    def buscar_transacciones_por_palabra(self):
        keyword = self.search_entry.get().strip().lower()

        if not keyword:
            messagebox.showerror("Error", "Por favor ingresa una palabra clave para buscar.")
            return

        resultados = []

        for t in self.current_user.income:
            if keyword in t.category.lower() or keyword in t.date.lower() or keyword in str(t.amount):
                resultados.append(f"[Ingreso] {t.category} | ${t.amount} | {t.date}")

        for t in self.current_user.expenses:
            if keyword in t.category.lower() or keyword in t.date.lower() or keyword in str(t.amount):
                resultados.append(f"[Gasto] {t.category} | ${t.amount} | {t.date}")

        self.mostrar_resultados_en_tabla(resultados)

    def mostrar_resultados_en_tabla(self, resultados):
            ventana_resultados = tk.Toplevel(self.ventana)
            ventana_resultados.title("Resultados de búsqueda")
            ventana_resultados.geometry("500x400")
            ventana_resultados.config(bg="#f0f0f0")

            tk.Label(ventana_resultados, text="Resultados encontrados:", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)

            frame = tk.Frame(ventana_resultados)
            frame.pack(expand=True, fill="both", padx=10, pady=10)

            texto = tk.Text(frame, wrap="none", font=("Consolas", 11))
            texto.pack(side="left", expand=True, fill="both")

            scrollbar = tk.Scrollbar(frame, command=texto.yview)
            scrollbar.pack(side="right", fill="y")
            texto.config(yscrollcommand=scrollbar.set)

            if not resultados:
                texto.insert("1.0", "No se encontraron transacciones con ese criterio.")
            else:
                for r in resultados:
                    texto.insert("end", r + "\n")

            texto.config(state="disabled")  

       
    def ver_todas_las_transacciones(self):
        resultados = []

        for t in self.current_user.income:
            resultados.append(("Ingreso", t.category, t.amount, t.date))

        for t in self.current_user.expenses:
            resultados.append(("Gasto", t.category, t.amount, t.date))

        if not resultados:
            messagebox.showinfo("Sin transacciones", "Aún no hay ingresos ni gastos registrados.")
        else:
            self.mostrar_resultados_en_tabla_con_columnas(resultados)

    def predict_financial_situation(self):
        messagebox.showinfo("Predicción Económica", "Predicción de la situación económica en un año.")
    def exportar_reporte_excel(self):
        if not self.current_user:
            messagebox.showerror("Error", "No hay usuario activo.")
            return

        if not self.current_user.income and not self.current_user.expenses:
            messagebox.showinfo("Exportar a Excel", "No hay transacciones para exportar.")
            return

        ingresos_data = [{
            "Tipo": transaccion.category,
            "Monto": transaccion.amount,
            "Fecha": transaccion.date
        } for transaccion in self.current_user.income]

        gastos_data = [{
            "Categoría": transaccion.category,
            "Monto": transaccion.amount,
            "Fecha": transaccion.date
        } for transaccion in self.current_user.expenses]

        df_ingresos = pd.DataFrame(ingresos_data)
        df_gastos = pd.DataFrame(gastos_data)

        nombre_archivo = f"reporte_{self.current_user.name}.xlsx"

        with pd.ExcelWriter(nombre_archivo, engine='xlsxwriter') as writer:
            df_ingresos.to_excel(writer, sheet_name="Ingresos", index=False)
            df_gastos.to_excel(writer, sheet_name="Gastos", index=False)

        messagebox.showinfo("Exportar a Excel", f"Reporte exportado como '{nombre_archivo}' en el mismo directorio.")


    def validate_date(self, date_text):
        try:
            datetime.strptime(date_text, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def validate_email(self, email):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email) is not None

    def clear_screen(self):
        for widget in self.ventana.winfo_children():
            widget.destroy()

    def guardar_usuarios(self):
        data = {}

        for email, user in self.users.items():
            data[email] = {
                "name": user.name,
                "email": user.email,
                "password": user.password,
                "income": [
                    {"amount": t.amount, "type": t.category, "date": t.date}
                    for t in user.income
                ],
                "expenses": [
                    {"amount": t.amount, "category": t.category, "date": t.date}
                    for t in user.expenses
                ]
            }

        with open("usuarios.json", "w") as f:
            json.dump(data, f, indent=4)

    def cargar_usuarios(self):
        if not os.path.exists("usuarios.json"):
            return

        try:
            with open("usuarios.json", "r") as f:
                data = json.load(f)

            for email, u in data.items():
                user = User(u["name"], u["email"], u["password"])
                
                # Aquí corregimos el problema del KeyError
                for inc in u["income"]:
                    tipo = inc.get("type") or inc.get("category") or "Desconocido"
                    user.add_income(inc["amount"], tipo, inc["date"])

                for exp in u["expenses"]:
                    user.add_expense(exp["amount"], exp["category"], exp["date"])

                self.users[email] = user
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Error al cargar los datos de usuarios. El archivo puede estar corrupto.")

    def run(self):
        self.ventana.mainloop()

if __name__ == "__main__":
    app = Interfaz()
    app.run()