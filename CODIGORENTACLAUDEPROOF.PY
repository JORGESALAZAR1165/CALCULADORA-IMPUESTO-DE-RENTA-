import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Tuple

class CalculadoraRentaColombia:
    """
    Calculadora de Impuesto de Renta para Personas Naturales
    Residentes Fiscales en Colombia - Año Gravable 2024
    Basada en el Estatuto Tributario y Ley 2277 de 2022
    """
    
    UVT_2024 = 47065
    
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("CALCULADORA IMPUESTO DE RENTA AÑO GRAVABLE 2024")
        self.ventana.geometry("1200x800")
        self.ventana.configure(bg="#E3F2FD")
        
        self.datos = {}
        self.crear_interfaz()
    
    def crear_interfaz(self):
        """Crea la interfaz gráfica de usuario"""
        
        # Frame principal con scroll
        main_frame = tk.Frame(self.ventana, bg="#E3F2FD")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas para scroll
        canvas = tk.Canvas(main_frame, bg="#E3F2FD", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#E3F2FD")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Título
        titulo_frame = tk.Frame(scrollable_frame, bg="#1565C0", pady=20)
        titulo_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Label(
            titulo_frame,
            text="CALCULADORA IMPUESTO DE RENTA AÑO GRAVABLE 2024",
            font=("Arial", 18, "bold"),
            bg="#1565C0",
            fg="white"
        ).pack()
        
        tk.Label(
            titulo_frame,
            text="Personas Naturales Residentes - Colombia",
            font=("Arial", 12),
            bg="#1565C0",
            fg="#BBDEFB"
        ).pack()
        
        # Frame de entrada de datos
        datos_frame = tk.Frame(scrollable_frame, bg="#E3F2FD")
        datos_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=10)
        
        # Definir campos de entrada
        campos = [
            ("Salarios", "salarios"),
            ("Cesantías pagadas o consignadas al fondo", "cesantias"),
            ("Prestaciones sociales", "prestaciones"),
            ("Otros pagos laborales", "otros_pagos"),
            ("INCR Salud", "incr_salud"),
            ("INCR Pensiones", "incr_pensiones"),
            ("Número de dependientes (máx. 4)", "num_dependientes"),
            ("Deducción intereses vivienda", "intereses_vivienda"),
            ("Deducción medicina prepagada", "medicina_prepagada"),
            ("Renta exenta pensión voluntaria", "pension_voluntaria"),
            ("Renta exenta AFC", "renta_exenta_afc"),
            ("Valor compras con factura electrónica", "compras_factura"),
            ("GMF", "gmf"),
            ("Ingreso mensual promedio últimos 6 meses", "ingreso_mensual_promedio"),
            ("Impuesto neto de renta año anterior", "impuesto_neto_anterior"),
            ("Saldo a favor año anterior sin solicitud", "saldo_favor_anterior"),
            ("Retenciones que le practicaron", "retenciones_anterior"),
            ("Anticipo del año anterior", "anticipo_anterior")
        ]
        
        # Crear campos en grid
        row = 0
        col = 0
        self.entries = {}
        
        for etiqueta, nombre in campos:
            frame_campo = tk.Frame(datos_frame, bg="white", relief=tk.RAISED, borderwidth=1)
            frame_campo.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
            
            tk.Label(
                frame_campo,
                text=etiqueta,
                font=("Arial", 9, "bold"),
                bg="white",
                fg="#0D47A1",
                anchor="w"
            ).pack(fill=tk.X, padx=5, pady=(5, 2))
            
            entry = tk.Entry(frame_campo, font=("Arial", 10), relief=tk.SOLID, borderwidth=1)
            entry.insert(0, "0")
            entry.pack(fill=tk.X, padx=5, pady=(0, 5))
            self.entries[nombre] = entry
            
            col += 1
            if col > 2:
                col = 0
                row += 1
        
        # Campo especial para años declarando
        frame_anios = tk.Frame(datos_frame, bg="white", relief=tk.RAISED, borderwidth=1)
        frame_anios.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
        
        tk.Label(
            frame_anios,
            text="Número de años que lleva declarando",
            font=("Arial", 9, "bold"),
            bg="white",
            fg="#0D47A1",
            anchor="w"
        ).pack(fill=tk.X, padx=5, pady=(5, 2))
        
        self.anios_var = tk.StringVar(value="1")
        combo_anios = ttk.Combobox(
            frame_anios,
            textvariable=self.anios_var,
            values=["1", "2", "3"],
            state="readonly",
            font=("Arial", 10)
        )
        combo_anios.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        # Configurar expansión de columnas
        for i in range(3):
            datos_frame.columnconfigure(i, weight=1)
        
        # Botón calcular
        btn_calcular = tk.Button(
            scrollable_frame,
            text="CALCULAR IMPUESTO",
            font=("Arial", 14, "bold"),
            bg="#1565C0",
            fg="white",
            relief=tk.RAISED,
            borderwidth=3,
            command=self.calcular,
            cursor="hand2",
            pady=10
        )
        btn_calcular.pack(pady=20, padx=100, fill=tk.X)
        
        # Frame de resultados
        self.resultados_frame = tk.Frame(scrollable_frame, bg="#E3F2FD")
        self.resultados_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=10)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind del scroll con rueda del mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    def obtener_datos(self) -> Dict:
        """Obtiene los datos ingresados por el usuario"""
        datos = {}
        try:
            for nombre, entry in self.entries.items():
                valor = entry.get().replace(",", "").replace("$", "").replace(".", "").strip()
                datos[nombre] = float(valor) if valor else 0.0
            
            datos["anios_declarando"] = int(self.anios_var.get())
            return datos
        except ValueError as e:
            messagebox.showerror("Error", f"Por favor ingrese valores numéricos válidos\n{str(e)}")
            return None
    
    def calcular_cesantias_exentas(self, cesantias: float, ingreso_mensual_promedio: float) -> float:
        """Calcula las cesantías exentas según Art. 206 numeral 4"""
        if ingreso_mensual_promedio == 0:
            return cesantias
        
        salarios_minimos_mensuales = ingreso_mensual_promedio / 1300000
        
        if salarios_minimos_mensuales <= 10:
            return cesantias
        elif salarios_minimos_mensuales <= 17:
            return cesantias * 0.90
        elif salarios_minimos_mensuales <= 18:
            return cesantias * 0.80
        elif salarios_minimos_mensuales <= 19:
            return cesantias * 0.60
        elif salarios_minimos_mensuales <= 20:
            return cesantias * 0.40
        else:
            return cesantias * 0.20
    
    def aplicar_tabla_articulo_241(self, base_gravable: float) -> float:
        """Aplica la tabla del Artículo 241 del Estatuto Tributario"""
        base_uvt = base_gravable / self.UVT_2024
        
        if base_uvt <= 1090:
            return 0
        elif base_uvt <= 1700:
            return ((base_uvt - 1090) * 0.19) * self.UVT_2024
        elif base_uvt <= 4100:
            return (((base_uvt - 1700) * 0.28) + 116) * self.UVT_2024
        elif base_uvt <= 8670:
            return (((base_uvt - 4100) * 0.33) + 788) * self.UVT_2024
        elif base_uvt <= 18970:
            return (((base_uvt - 8670) * 0.35) + 2296) * self.UVT_2024
        elif base_uvt <= 31000:
            return (((base_uvt - 18970) * 0.37) + 5901) * self.UVT_2024
        else:
            return (((base_uvt - 31000) * 0.39) + 10352) * self.UVT_2024
    
    def calcular_anticipo(self, impuesto_neto: float, impuesto_neto_anterior: float,
                         retenciones: float, anios: int) -> Tuple[float, float, float]:
        """Calcula el anticipo para el año siguiente según Art. 807"""
        porcentaje = 0.25 if anios == 1 else (0.50 if anios == 2 else 0.75)
        
        # Método 1: (Impuesto neto actual * % anticipo) - Retenciones
        metodo1_calculo = (impuesto_neto * porcentaje) - retenciones
        metodo1 = max(0, metodo1_calculo)  # Si es negativo, se iguala a $0
        
        # Método 2: (((Impuesto actual + Impuesto anterior) / 2) * % anticipo) - Retenciones
        promedio = (impuesto_neto + impuesto_neto_anterior) / 2
        metodo2_calculo = (promedio * porcentaje) - retenciones
        metodo2 = max(0, metodo2_calculo)  # Si es negativo, se iguala a $0
        
        # Tomar el menor de los dos métodos
        anticipo_final = min(metodo1, metodo2)
        
        return metodo1, metodo2, anticipo_final
    
    def calcular_beneficio_auditoria(self, impuesto_neto: float, 
                                    impuesto_neto_anterior: float) -> Dict:
        """Calcula el beneficio de auditoría según Art. 689-3"""
        limite_minimo = 71 * self.UVT_2024
        
        if impuesto_neto_anterior < limite_minimo:
            return {
                "tiene_beneficio": False,
                "firmeza": 36,
                "mensaje": "No tiene beneficio de auditoría (impuesto anterior < 71 UVT)"
            }
        
        if impuesto_neto_anterior == 0:
            return {
                "tiene_beneficio": False,
                "firmeza": 36,
                "mensaje": "No tiene beneficio de auditoría (sin impuesto año anterior)"
            }
        
        incremento = ((impuesto_neto - impuesto_neto_anterior) / impuesto_neto_anterior) * 100
        
        if incremento >= 30:
            return {
                "tiene_beneficio": True,
                "firmeza": 6,
                "mensaje": "Tiene beneficio de auditoría - Firmeza: 6 meses",
                "incremento": incremento
            }
        elif incremento >= 20:
            return {
                "tiene_beneficio": True,
                "firmeza": 12,
                "mensaje": "Tiene beneficio de auditoría - Firmeza: 12 meses",
                "incremento": incremento
            }
        else:
            return {
                "tiene_beneficio": False,
                "firmeza": 36,
                "mensaje": "No tiene beneficio de auditoría - Firmeza: 36 meses",
                "incremento": incremento
            }
    
    def calcular(self):
        """Realiza el cálculo completo del impuesto de renta"""
        datos = self.obtener_datos()
        if datos is None:
            return
        
        # 1. Ingresos laborales totales
        ingresos_laborales = (datos["salarios"] + datos["cesantias"] + 
                             datos["prestaciones"] + datos["otros_pagos"])
        
        # 2. INCR
        incr = datos["incr_salud"] + datos["incr_pensiones"]
        
        # 3. Ingreso neto
        ingreso_neto = ingresos_laborales - incr
        
        # 4. Cesantías exentas
        cesantias_exentas = self.calcular_cesantias_exentas(
            datos["cesantias"],
            datos["ingreso_mensual_promedio"]
        )
        
        # 5. Deducción dependientes Parte 1 (10% sobre ingresos totales, no netos)
        deduccion_dep_parte1_valor = ingresos_laborales * 0.10
        deduccion_dep_parte1 = min(deduccion_dep_parte1_valor, 384 * self.UVT_2024)
        
        # 6. Deducciones limitadas
        intereses_vivienda_lim = min(datos["intereses_vivienda"], 1200 * self.UVT_2024)
        medicina_prepagada_lim = min(datos["medicina_prepagada"], 192 * self.UVT_2024)
        
        # 7. Pensión voluntaria y AFC
        suma_pension_afc = datos["pension_voluntaria"] + datos["renta_exenta_afc"]
        limite_pension_afc = min(
            suma_pension_afc,
            min(ingresos_laborales * 0.30, 3800 * self.UVT_2024)
        )
        
        # 8. Base para renta exenta 25%
        base_renta_exenta_25 = (ingreso_neto - cesantias_exentas - deduccion_dep_parte1 -
                                intereses_vivienda_lim - medicina_prepagada_lim - limite_pension_afc)
        
        # 9. Renta exenta 25%
        renta_exenta_25_calculada = base_renta_exenta_25 * 0.25
        renta_exenta_25 = min(renta_exenta_25_calculada, 790 * self.UVT_2024)
        
        # 10. Suma deducciones y rentas exentas (INCLUYE cesantías exentas)
        suma_deducciones_rentas = (cesantias_exentas + deduccion_dep_parte1 + intereses_vivienda_lim +
                                   medicina_prepagada_lim + limite_pension_afc + renta_exenta_25)
        
        # 11. Límite Art. 336
        limite_40_porciento = ingreso_neto * 0.40
        limite_1340_uvt = 1340 * self.UVT_2024
        limite_articulo_336 = min(limite_40_porciento, limite_1340_uvt)
        
        # 12. Deducciones aplicadas
        deducciones_rentas_aplicadas = min(suma_deducciones_rentas, limite_articulo_336)
        
        # 13. Deducción dependientes Parte 2
        num_dep = min(int(datos["num_dependientes"]), 4)
        deduccion_dep_parte2 = num_dep * 72 * self.UVT_2024
        
        # 14. Descuentos adicionales
        compras_factura_desc = min(datos["compras_factura"] * 0.01, 240 * self.UVT_2024)
        gmf_descuento = datos["gmf"] * 0.50
        
        # 15. Renta líquida - CORRECCIÓN: Se resta deducciones_rentas_aplicadas que YA incluye cesantías
        renta_liquida = (ingreso_neto - deducciones_rentas_aplicadas -
                        deduccion_dep_parte2 - compras_factura_desc - gmf_descuento)
        
        # 16. Base gravable
        base_gravable = max(0, renta_liquida)
        
        # 17. Impuesto neto
        impuesto_neto = self.aplicar_tabla_articulo_241(base_gravable)
        
        # 18. Subtotal
        subtotal = (impuesto_neto - datos["retenciones_anterior"] -
                   datos["saldo_favor_anterior"] - datos["anticipo_anterior"])
        
        # 19. Anticipo
        anticipo_m1, anticipo_m2, anticipo = self.calcular_anticipo(
            impuesto_neto,
            datos["impuesto_neto_anterior"],
            datos["retenciones_anterior"],
            datos["anios_declarando"]
        )
        
        # 20. Saldo final
        saldo_final = subtotal + anticipo
        
        # 21. Beneficio auditoría
        beneficio_auditoria = self.calcular_beneficio_auditoria(
            impuesto_neto,
            datos["impuesto_neto_anterior"]
        )
        
        # Mostrar resultados
        self.mostrar_resultados({
            "ingresos_laborales": ingresos_laborales,
            "incr": incr,
            "ingreso_neto": ingreso_neto,
            "cesantias_exentas": cesantias_exentas,
            "deduccion_dep_parte1": deduccion_dep_parte1,
            "intereses_vivienda_lim": intereses_vivienda_lim,
            "medicina_prepagada_lim": medicina_prepagada_lim,
            "limite_pension_afc": limite_pension_afc,
            "renta_exenta_25": renta_exenta_25,
            "suma_deducciones_rentas": suma_deducciones_rentas,
            "limite_articulo_336": limite_articulo_336,
            "deducciones_rentas_aplicadas": deducciones_rentas_aplicadas,
            "deduccion_dep_parte2": deduccion_dep_parte2,
            "compras_factura_desc": compras_factura_desc,
            "gmf_descuento": gmf_descuento,
            "renta_liquida": renta_liquida,
            "base_gravable": base_gravable,
            "impuesto_neto": impuesto_neto,
            "subtotal": subtotal,
            "anticipo_m1": anticipo_m1,
            "anticipo_m2": anticipo_m2,
            "anticipo": anticipo,
            "saldo_final": saldo_final,
            "beneficio_auditoria": beneficio_auditoria,
            "datos": datos
        })
    
    def formatear_pesos(self, valor: float) -> str:
        """Formatea un valor en pesos colombianos"""
        return "${:,.0f}".format(valor).replace(",", ".")
    
    def mostrar_resultados(self, resultados: Dict):
        """Muestra los resultados del cálculo"""
        # Limpiar frame de resultados
        for widget in self.resultados_frame.winfo_children():
            widget.destroy()
        
        # Título de resultados
        titulo_res = tk.Frame(self.resultados_frame, bg="#1565C0", pady=10)
        titulo_res.pack(fill=tk.X, padx=5, pady=(0, 10))
        
        tk.Label(
            titulo_res,
            text="RESULTADOS DEL CÁLCULO",
            font=("Arial", 16, "bold"),
            bg="#1565C0",
            fg="white"
        ).pack()
        
        # Frame principal
        main_res_frame = tk.Frame(self.resultados_frame, bg="#E3F2FD")
        main_res_frame.pack(fill=tk.BOTH, expand=True, padx=5)
        
        # Columna izquierda - Depuración
        frame_izq = tk.Frame(main_res_frame, bg="white", relief=tk.RAISED, borderwidth=2)
        frame_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        tk.Label(
            frame_izq,
            text="DEPURACIÓN DE LA RENTA",
            font=("Arial", 12, "bold"),
            bg="#1976D2",
            fg="white",
            pady=8
        ).pack(fill=tk.X)
        
        depuracion = [
            ("Ingresos laborales totales:", resultados["ingresos_laborales"]),
            ("(-) INCR:", resultados["incr"]),
            ("= Ingreso neto:", resultados["ingreso_neto"], True),
            ("(-) Cesantías exentas:", resultados["cesantias_exentas"]),
            ("(-) Deducción dependientes Parte 1:", resultados["deduccion_dep_parte1"]),
            ("(-) Intereses vivienda:", resultados["intereses_vivienda_lim"]),
            ("(-) Medicina prepagada:", resultados["medicina_prepagada_lim"]),
            ("(-) Pensión voluntaria y AFC:", resultados["limite_pension_afc"]),
            ("(-) Renta exenta 25%:", resultados["renta_exenta_25"]),
            ("", None),
            ("Suma deducciones y rentas:", resultados["suma_deducciones_rentas"]),
            ("Límite Art. 336 aplicable:", resultados["limite_articulo_336"], True),
            ("Deducciones aplicadas (con límite):", resultados["deducciones_rentas_aplicadas"]),
            ("", None),
            ("(-) Deducción dependientes Parte 2:", resultados["deduccion_dep_parte2"]),
            ("(-) Desc. factura electrónica 1%:", resultados["compras_factura_desc"]),
            ("(-) Desc. GMF 50%:", resultados["gmf_descuento"]),
            ("", None),
            ("= RENTA LÍQUIDA:", resultados["renta_liquida"], True),
        ]
        
        for item in depuracion:
            if item[1] is None:
                tk.Frame(frame_izq, height=5, bg="white").pack()
                continue
            
            frame_item = tk.Frame(frame_izq, bg="white")
            frame_item.pack(fill=tk.X, padx=10, pady=2)
            
            es_resaltado = len(item) > 2 and item[2]
            
            tk.Label(
                frame_item,
                text=item[0],
                font=("Arial", 9, "bold" if es_resaltado else "normal"),
                bg="white",
                fg="#0D47A1" if es_resaltado else "#424242",
                anchor="w"
            ).pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            tk.Label(
                frame_item,
                text=self.formatear_pesos(item[1]),
                font=("Arial", 9, "bold" if es_resaltado else "normal"),
                bg="white",
                fg="#0D47A1" if es_resaltado else "#424242",
                anchor="e"
            ).pack(side=tk.RIGHT)
        
        # Columna derecha
        frame_der = tk.Frame(main_res_frame, bg="#E3F2FD")
        frame_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Base gravable
        frame_base = tk.Frame(frame_der, bg="#4CAF50", relief=tk.RAISED, borderwidth=2)
        frame_base.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            frame_base,
            text="BASE GRAVABLE",
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            pady=5
        ).pack()
        
        tk.Label(
            frame_base,
            text=self.formatear_pesos(resultados["base_gravable"]),
            font=("Arial", 16, "bold"),
            bg="#4CAF50",
            fg="white",
            pady=5
        ).pack()
        
        tk.Label(
            frame_base,
            text="{:,.2f} UVT".format(resultados['base_gravable'] / self.UVT_2024),
            font=("Arial", 10),
            bg="#4CAF50",
            fg="white",
            pady=5
        ).pack()
        
        # Impuesto neto
        frame_impuesto = tk.Frame(frame_der, bg="#9C27B0", relief=tk.RAISED, borderwidth=2)
        frame_impuesto.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            frame_impuesto,
            text="IMPUESTO NETO DE RENTA",
            font=("Arial", 12, "bold"),
            bg="#9C27B0",
            fg="white",
            pady=5
        ).pack()
        
        tk.Label(
            frame_impuesto,
            text=self.formatear_pesos(resultados["impuesto_neto"]),
            font=("Arial", 16, "bold"),
            bg="#9C27B0",
            fg="white",
            pady=5
        ).pack()
        
        # Liquidación final
        frame_liq = tk.Frame(frame_der, bg="white", relief=tk.RAISED, borderwidth=2)
        frame_liq.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            frame_liq,
            text="LIQUIDACIÓN FINAL",
            font=("Arial", 11, "bold"),
            bg="#7B1FA2",
            fg="white",
            pady=6
        ).pack(fill=tk.X)
        
        liquidacion = [
            ("Impuesto neto de renta:", resultados["impuesto_neto"]),
            ("(-) Retenciones:", resultados["datos"]["retenciones_anterior"]),
            ("(-) Saldo a favor año anterior:", resultados["datos"]["saldo_favor_anterior"]),
            ("(-) Anticipo año anterior:", resultados["datos"]["anticipo_anterior"]),
            ("= SUBTOTAL:", resultados["subtotal"], True),
            ("(+) Anticipo año siguiente:", resultados["anticipo"]),
        ]
        
        for item in liquidacion:
            frame_item = tk.Frame(frame_liq, bg="white")
            frame_item.pack(fill=tk.X, padx=10, pady=2)
            
            es_resaltado = len(item) > 2 and item[2]
            
            tk.Label(
                frame_item,
                text=item[0],
                font=("Arial", 9, "bold" if es_resaltado else "normal"),
                bg="white",
                fg="#0D47A1" if es_resaltado else "#424242",
                anchor="w"
            ).pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            tk.Label(
                frame_item,
                text=self.formatear_pesos(item[1]),
                font=("Arial", 9, "bold" if es_resaltado else "normal"),
                bg="white",
                fg="#0D47A1" if es_resaltado else "#424242",
                anchor="e"
            ).pack(side=tk.RIGHT)
        
        # Saldo final
        es_a_pagar = resultados["saldo_final"] >= 0
        color_fondo = "#F44336" if es_a_pagar else "#4CAF50"
        texto_tipo = "SALDO A PAGAR" if es_a_pagar else "SALDO A FAVOR"
        
        frame_saldo = tk.Frame(frame_der, bg=color_fondo, relief=tk.RAISED, borderwidth=3)
        frame_saldo.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            frame_saldo,
            text=texto_tipo,
            font=("Arial", 14, "bold"),
            bg=color_fondo,
            fg="white",
            pady=8
        ).pack()
        
        tk.Label(
            frame_saldo,
            text=self.formatear_pesos(abs(resultados["saldo_final"])),
            font=("Arial", 20, "bold"),
            bg=color_fondo,
            fg="white",
            pady=10
        ).pack()
        
        # Anticipo detalle
        frame_anticipo = tk.Frame(frame_der, bg="white", relief=tk.RAISED, borderwidth=2)
        frame_anticipo.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(
            frame_anticipo,
            text="ANTICIPO AÑO SIGUIENTE",
            font=("Arial", 11, "bold"),
            bg="#FF9800",
            fg="white",
            pady=6
        ).pack(fill=tk.X)
        
        porcentaje_anticipo = {1: "25%", 2: "50%", 3: "75%"}[resultados["datos"]["anios_declarando"]]
        
        anticipo_info = [
            ("Método 1 ({}):".format(porcentaje_anticipo), resultados["anticipo_m1"]),
            ("Método 2 ({}):".format(porcentaje_anticipo), resultados["anticipo_m2"]),
            ("ANTICIPO DEFINITIVO (menor):", resultados["anticipo"], True),
        ]
        
        for item in anticipo_info:
            frame_item = tk.Frame(frame_anticipo, bg="white")
            frame_item.pack(fill=tk.X, padx=10, pady=2)
            
            es_resaltado = len(item) > 2 and item[2]
            
            tk.Label(
                frame_item,
                text=item[0],
                font=("Arial", 9, "bold" if es_resaltado else "normal"),
                bg="white",
                fg="#E65100" if es_resaltado else "#424242",
                anchor="w"
            ).pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            tk.Label(
                frame_item,
                text=self.formatear_pesos(item[1]),
                font=("Arial", 9, "bold" if es_resaltado else "normal"),
                bg="white",
                fg="#E65100" if es_resaltado else "#424242",
                anchor="e"
            ).pack(side=tk.RIGHT)
        
        # Beneficio auditoría
        frame_auditoria = tk.Frame(self.resultados_frame, bg="#FFF3E0", relief=tk.RAISED, borderwidth=2)
        frame_auditoria.pack(fill=tk.X, padx=5, pady=10)
        
        tk.Label(
            frame_auditoria,
            text="BENEFICIO DE AUDITORÍA (Art. 689-3)",
            font=("Arial", 12, "bold"),
            bg="#FF6F00",
            fg="white",
            pady=8
        ).pack(fill=tk.X)
        
        beneficio = resultados["beneficio_auditoria"]
        
        tk.Label(
            frame_auditoria,
            text=beneficio["mensaje"],
            font=("Arial", 11, "bold"),
            bg="#FFF3E0",
            fg="#E65100",
            pady=5,
            wraplength=1000
        ).pack(padx=10)
        
        tk.Label(
            frame_auditoria,
            text="Término de firmeza de la declaración: {} meses".format(beneficio['firmeza']),
            font=("Arial", 10),
            bg="#FFF3E0",
            fg="#424242",
            pady=5
        ).pack(padx=10)
        
        if "incremento" in beneficio:
            tk.Label(
                frame_auditoria,
                text="Incremento del impuesto: {:.2f}%".format(beneficio['incremento']),
                font=("Arial", 9),
                bg="#FFF3E0",
                fg="#666666",
                pady=5
            ).pack(padx=10)
        
        # Información adicional
        frame_info = tk.Frame(self.resultados_frame, bg="white", relief=tk.RAISED, borderwidth=2)
        frame_info.pack(fill=tk.X, padx=5, pady=(0, 10))
        
        tk.Label(
            frame_info,
            text="INFORMACIÓN ADICIONAL",
            font=("Arial", 11, "bold"),
            bg="#546E7A",
            fg="white",
            pady=6
        ).pack(fill=tk.X)
        
        info_text = """
UVT 2024: {}
Base gravable en UVT: {:,.2f} UVT
Límite Art. 336 aplicado: {}
Límite en UVT: {:,.2f} UVT
        """.format(
            self.formatear_pesos(self.UVT_2024),
            resultados['base_gravable'] / self.UVT_2024,
            self.formatear_pesos(resultados["limite_articulo_336"]),
            resultados['limite_articulo_336'] / self.UVT_2024
        )
        
        tk.Label(
            frame_info,
            text=info_text,
            font=("Arial", 9),
            bg="white",
            fg="#424242",
            justify=tk.LEFT,
            pady=5
        ).pack(padx=10)
        
        # Nota legal
        frame_nota = tk.Frame(self.resultados_frame, bg="#E1F5FE", relief=tk.SOLID, borderwidth=1)
        frame_nota.pack(fill=tk.X, padx=5, pady=(0, 10))
        
        tk.Label(
            frame_nota,
            text="Nota: Este cálculo se basa en el Estatuto Tributario Colombiano y la Ley 2277 de 2022. "
                 "Los resultados son referenciales y deben ser verificados por un contador público.",
            font=("Arial", 8, "italic"),
            bg="#E1F5FE",
            fg="#01579B",
            wraplength=1000,
            justify=tk.LEFT,
            pady=8,
            padx=10
        ).pack()
    
    def ejecutar(self):
        """Inicia la aplicación"""
        self.ventana.mainloop()


def main():
    """Función principal para ejecutar la Calculadora de Impuesto de Renta"""
    print("=" * 70)
    print("CALCULADORA IMPUESTO DE RENTA - AÑO GRAVABLE 2024")
    print("Personas Naturales Residentes Fiscales en Colombia")
    print("Basada en el Estatuto Tributario y Ley 2277 de 2022")
    print("=" * 70)
    print("\nIniciando aplicación...")
    
    app = CalculadoraRentaColombia()
    app.ejecutar()


if __name__ == "__main__":
    main()