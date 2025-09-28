import random
import json
import os
from collections import defaultdict, Counter
from datetime import datetime
import statistics

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("⚠️  Matplotlib no está disponible. Las gráficas estarán deshabilitadas.")
    print("   Instala con: pip install matplotlib")

class LightningStormAnalyzer:
    def __init__(self):
        """Inicializa el analizador del juego Lightning Storm"""
        # Configuración del juego según la descripción
        self.numeros_principales = list(range(1, 21))  # 1-20
        self.casillas_leaf = 19  # 19 casillas leaf (1:1)
        
        # Historial de rondas: lista de diccionarios
        # Cada entrada: {'numero': int, 'es_leaf': bool, 'bonus': bool, 'multiplicador': float, 'timestamp': str}
        self.historial = []
        
        # Estadísticas calculadas
        self.stats = {
            'total_rondas': 0,
            'conteo_numeros': defaultdict(int),
            'conteo_leaf': 0,
            'bonus_por_numero': defaultdict(int),
            'multiplicadores_por_numero': defaultdict(list),
            'total_bonus': 0,
            'racha_actual_sin_bonus': 0,
            'racha_maxima_sin_bonus': 0
        }
        
        # Archivo para persistencia
        self.archivo_datos = 'lightning_storm_data.json'
        self.cargar_datos()
    
    def cargar_datos(self):
        """Carga datos guardados anteriormente"""
        if os.path.exists(self.archivo_datos):
            try:
                with open(self.archivo_datos, 'r', encoding='utf-8') as f:
                    datos = json.load(f)
                    self.historial = datos.get('historial', [])
                    self.recalcular_estadisticas()
                print(f"✅ Datos cargados: {len(self.historial)} rondas anteriores")
            except Exception as e:
                print(f"⚠️  Error cargando datos: {e}")
    
    def guardar_datos(self):
        """Guarda los datos actuales"""
        try:
            datos = {
                'historial': self.historial,
                'fecha_guardado': datetime.now().isoformat()
            }
            with open(self.archivo_datos, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️  Error guardando datos: {e}")
    
    def recalcular_estadisticas(self):
        """Recalcula todas las estadísticas basadas en el historial"""
        # Resetear estadísticas
        self.stats = {
            'total_rondas': 0,
            'conteo_numeros': defaultdict(int),
            'conteo_leaf': 0,
            'bonus_por_numero': defaultdict(int),
            'multiplicadores_por_numero': defaultdict(list),
            'total_bonus': 0,
            'racha_actual_sin_bonus': 0,
            'racha_maxima_sin_bonus': 0
        }
        
        racha_sin_bonus = 0
        
        for ronda in self.historial:
            self.stats['total_rondas'] += 1
            
            if ronda.get('es_leaf', False):
                self.stats['conteo_leaf'] += 1
            else:
                numero = ronda['numero']
                self.stats['conteo_numeros'][numero] += 1
                
                if ronda.get('bonus', False):
                    self.stats['bonus_por_numero'][numero] += 1
                    self.stats['total_bonus'] += 1
                    racha_sin_bonus = 0
                else:
                    racha_sin_bonus += 1
                
                if ronda.get('multiplicador', 1) > 1:
                    self.stats['multiplicadores_por_numero'][numero].append(ronda['multiplicador'])
        
        self.stats['racha_actual_sin_bonus'] = racha_sin_bonus
        # Calcular racha máxima sin bonus
        racha_temp = 0
        racha_maxima = 0
        for ronda in self.historial:
            if ronda.get('bonus', False):
                racha_temp = 0
            else:
                racha_temp += 1
                racha_maxima = max(racha_maxima, racha_temp)
        self.stats['racha_maxima_sin_bonus'] = racha_maxima
    
    def agregar_ronda(self, numero=None, es_leaf=False, bonus=False, multiplicador=1.0):
        """Agrega una nueva ronda al historial"""
        if es_leaf:
            numero = None  # Las casillas leaf no tienen número específico
        elif numero is None or not (1 <= numero <= 20):
            print("❌ Número debe estar entre 1 y 20 para casillas numéricas")
            return False
        
        ronda = {
            'numero': numero,
            'es_leaf': es_leaf,
            'bonus': bonus,
            'multiplicador': multiplicador,
            'timestamp': datetime.now().isoformat()
        }
        
        self.historial.append(ronda)
        
        # Actualizar estadísticas incrementalmente
        self.stats['total_rondas'] += 1
        
        if es_leaf:
            self.stats['conteo_leaf'] += 1
            self.stats['racha_actual_sin_bonus'] += 1
        else:
            self.stats['conteo_numeros'][numero] += 1
            
            if bonus:
                self.stats['bonus_por_numero'][numero] += 1
                self.stats['total_bonus'] += 1
                self.stats['racha_actual_sin_bonus'] = 0
            else:
                self.stats['racha_actual_sin_bonus'] += 1
            
            if multiplicador > 1:
                self.stats['multiplicadores_por_numero'][numero].append(multiplicador)
        
        # Actualizar racha máxima si es necesario
        self.stats['racha_maxima_sin_bonus'] = max(
            self.stats['racha_maxima_sin_bonus'], 
            self.stats['racha_actual_sin_bonus']
        )
        
        self.guardar_datos()
        return True
    
    def calcular_probabilidades(self):
        """Calcula probabilidades actuales basadas en el historial"""
        if self.stats['total_rondas'] == 0:
            return None
        
        total_rondas = self.stats['total_rondas']
        
        # Probabilidades de números (1-20)
        prob_numeros = {}
        total_numericos = sum(self.stats['conteo_numeros'].values())
        
        if total_numericos > 0:
            for numero in self.numeros_principales:
                conteo = self.stats['conteo_numeros'][numero]
                prob_numeros[numero] = conteo / total_numericos if total_numericos > 0 else 1/20
        else:
            # Si no hay datos, asumir distribución uniforme
            for numero in self.numeros_principales:
                prob_numeros[numero] = 1/20
        
        # Probabilidad de leaf
        prob_leaf = self.stats['conteo_leaf'] / total_rondas
        
        # Probabilidad de bonus
        prob_bonus = self.stats['total_bonus'] / total_rondas if total_rondas > 0 else 0
        
        # Probabilidades de bonus por número
        prob_bonus_por_numero = {}
        for numero in self.numeros_principales:
            apariciones = self.stats['conteo_numeros'][numero]
            bonus_count = self.stats['bonus_por_numero'][numero]
            if apariciones > 0:
                prob_bonus_por_numero[numero] = bonus_count / apariciones
            else:
                prob_bonus_por_numero[numero] = prob_bonus  # Usar probabilidad general
        
        # Multiplicadores promedio por número
        mult_promedio_por_numero = {}
        for numero in self.numeros_principales:
            multiplicadores = self.stats['multiplicadores_por_numero'][numero]
            if multiplicadores:
                mult_promedio_por_numero[numero] = statistics.mean(multiplicadores)
            else:
                mult_promedio_por_numero[numero] = 1.0
        
        return {
            'probabilidades_numeros': prob_numeros,
            'probabilidad_leaf': prob_leaf,
            'probabilidad_bonus_general': prob_bonus,
            'probabilidades_bonus_por_numero': prob_bonus_por_numero,
            'multiplicadores_promedio': mult_promedio_por_numero,
            'total_rondas': total_rondas
        }
    
    def sugerir_mejores_numeros(self, top_n=5):
        """Sugiere los mejores números para apostar"""
        probabilidades = self.calcular_probabilidades()
        if not probabilidades:
            return []
        
        # Calcular "valor esperado" de cada número
        # Considera: probabilidad de salir * (1 + prob_bonus * valor_bonus + multiplicador_promedio - 1)
        valores_esperados = {}
        
        for numero in self.numeros_principales:
            prob_salir = probabilidades['probabilidades_numeros'][numero]
            prob_bonus = probabilidades['probabilidades_bonus_por_numero'][numero]
            mult_promedio = probabilidades['multiplicadores_promedio'][numero]
            
            # Valor esperado simplificado (ajustable según reglas exactas del juego)
            valor_base = prob_salir * 20  # Pago base estimado (20:1 para números específicos)
            bonus_extra = prob_bonus * 10  # Bonus estimado
            mult_extra = (mult_promedio - 1) * 5  # Valor extra por multiplicador
            
            valor_total = valor_base + bonus_extra + mult_extra
            valores_esperados[numero] = valor_total
        
        # Ordenar por valor esperado
        mejores = sorted(valores_esperados.items(), key=lambda x: x[1], reverse=True)
        
        return mejores[:top_n]
    
    def simular_rondas_futuras(self, num_simulaciones=1000, num_rondas=10):
        """Simula rondas futuras basadas en probabilidades actuales"""
        probabilidades = self.calcular_probabilidades()
        if not probabilidades:
            return None
        
        resultados_simulacion = {
            'conteo_numeros': defaultdict(int),
            'conteo_leaf': 0,
            'total_bonus': 0,
            'rondas_con_bonus': 0,
            'multiplicadores_aplicados': 0
        }
        
        for _ in range(num_simulaciones):
            bonus_en_simulacion = False
            
            for _ in range(num_rondas):
                # Decidir si sale leaf o número
                if random.random() < probabilidades['probabilidad_leaf']:
                    resultados_simulacion['conteo_leaf'] += 1
                else:
                    # Seleccionar número basado en probabilidades históricas
                    numeros = list(probabilidades['probabilidades_numeros'].keys())
                    probs = list(probabilidades['probabilidades_numeros'].values())
                    numero = random.choices(numeros, weights=probs)[0]
                    
                    resultados_simulacion['conteo_numeros'][numero] += 1
                    
                    # Simular bonus
                    prob_bonus = probabilidades['probabilidades_bonus_por_numero'][numero]
                    if random.random() < prob_bonus:
                        resultados_simulacion['total_bonus'] += 1
                        bonus_en_simulacion = True
                    
                    # Simular multiplicador
                    mult_promedio = probabilidades['multiplicadores_promedio'][numero]
                    if mult_promedio > 1 and random.random() < 0.3:  # 30% chance de multiplicador
                        resultados_simulacion['multiplicadores_aplicados'] += 1
            
            if bonus_en_simulacion:
                resultados_simulacion['rondas_con_bonus'] += 1
        
        # Calcular promedios
        for key in resultados_simulacion:
            if key != 'rondas_con_bonus':
                resultados_simulacion[key] = resultados_simulacion[key] / num_simulaciones
        
        resultados_simulacion['prob_bonus_en_X_rondas'] = resultados_simulacion['rondas_con_bonus'] / num_simulaciones
        
        return resultados_simulacion
    
    def mostrar_estadisticas(self):
        """Muestra estadísticas actuales detalladas"""
        print("\n" + "="*60)
        print("📊 ESTADÍSTICAS LIGHTNING STORM")
        print("="*60)
        
        if self.stats['total_rondas'] == 0:
            print("❌ No hay datos históricos disponibles")
            return
        
        # Resumen general
        print(f"🎮 Total de rondas: {self.stats['total_rondas']}")
        print(f"🍃 Casillas leaf: {self.stats['conteo_leaf']} ({self.stats['conteo_leaf']/self.stats['total_rondas']*100:.1f}%)")
        print(f"🔥 Total bonus: {self.stats['total_bonus']} ({self.stats['total_bonus']/self.stats['total_rondas']*100:.1f}%)")
        print(f"⚡ Racha actual sin bonus: {self.stats['racha_actual_sin_bonus']}")
        print(f"📈 Racha máxima sin bonus: {self.stats['racha_maxima_sin_bonus']}")
        
        # Números más frecuentes
        print(f"\n🎯 NÚMEROS MÁS FRECUENTES:")
        if self.stats['conteo_numeros']:
            numeros_ordenados = sorted(self.stats['conteo_numeros'].items(), 
                                     key=lambda x: x[1], reverse=True)
            for i, (numero, conteo) in enumerate(numeros_ordenados[:10]):
                porcentaje = conteo / sum(self.stats['conteo_numeros'].values()) * 100
                bonus_count = self.stats['bonus_por_numero'][numero]
                mult_count = len(self.stats['multiplicadores_por_numero'][numero])
                print(f"  {i+1:2d}. Número {numero:2d}: {conteo:3d} veces ({porcentaje:5.1f}%) "
                      f"| Bonus: {bonus_count} | Mult: {mult_count}")
        
        # Números con más bonus
        print(f"\n🎁 NÚMEROS CON MÁS BONUS:")
        if self.stats['bonus_por_numero']:
            bonus_ordenados = sorted([(num, count) for num, count in self.stats['bonus_por_numero'].items() if count > 0], 
                                   key=lambda x: x[1], reverse=True)
            for i, (numero, bonus_count) in enumerate(bonus_ordenados[:5]):
                apariciones = self.stats['conteo_numeros'][numero]
                prob_bonus = bonus_count / apariciones if apariciones > 0 else 0
                print(f"  {i+1}. Número {numero:2d}: {bonus_count} bonus ({prob_bonus*100:.1f}% cuando sale)")
        
        # Probabilidades actuales
        probabilidades = self.calcular_probabilidades()
        if probabilidades:
            print(f"\n📈 MEJORES APUESTAS (Top 5):")
            mejores = self.sugerir_mejores_numeros(5)
            for i, (numero, valor) in enumerate(mejores):
                prob = probabilidades['probabilidades_numeros'][numero] * 100
                prob_bonus = probabilidades['probabilidades_bonus_por_numero'][numero] * 100
                mult_prom = probabilidades['multiplicadores_promedio'][numero]
                print(f"  {i+1}. Número {numero:2d}: Valor {valor:.2f} "
                      f"| Prob: {prob:.1f}% | Bonus: {prob_bonus:.1f}% | Mult: {mult_prom:.1f}x")
    
    def mostrar_grafico(self, tipo='frecuencias'):
        """Muestra gráficos de análisis"""
        if not MATPLOTLIB_AVAILABLE:
            print("❌ Matplotlib no está disponible para mostrar gráficos")
            return
        
        if self.stats['total_rondas'] == 0:
            print("❌ No hay datos para mostrar en gráficos")
            return
        
        plt.style.use('dark_background')
        
        if tipo == 'frecuencias':
            # Gráfico de frecuencias de números
            numeros = []
            frecuencias = []
            
            for numero in sorted(self.numeros_principales):
                numeros.append(numero)
                frecuencias.append(self.stats['conteo_numeros'][numero])
            
            plt.figure(figsize=(12, 6))
            plt.bar(numeros, frecuencias, color='cyan', alpha=0.7, edgecolor='white')
            plt.title('🎯 Frecuencia de Números (1-20)', fontsize=16, color='white')
            plt.xlabel('Número', color='white')
            plt.ylabel('Frecuencia', color='white')
            plt.grid(True, alpha=0.3)
            
            # Línea de frecuencia esperada (uniforme)
            total_numericos = sum(frecuencias)
            if total_numericos > 0:
                esperado = total_numericos / 20
                plt.axhline(y=esperado, color='yellow', linestyle='--', 
                           label=f'Esperado (uniforme): {esperado:.1f}')
                plt.legend()
            
            plt.tight_layout()
            plt.show()
            
        elif tipo == 'bonus':
            # Gráfico de bonus por número
            numeros = []
            bonus_counts = []
            
            for numero in sorted(self.numeros_principales):
                if self.stats['conteo_numeros'][numero] > 0:  # Solo números que han salido
                    numeros.append(numero)
                    bonus_counts.append(self.stats['bonus_por_numero'][numero])
            
            if numeros:
                plt.figure(figsize=(12, 6))
                plt.bar(numeros, bonus_counts, color='gold', alpha=0.7, edgecolor='white')
                plt.title('🎁 Bonus por Número', fontsize=16, color='white')
                plt.xlabel('Número', color='white')
                plt.ylabel('Cantidad de Bonus', color='white')
                plt.grid(True, alpha=0.3)
                plt.tight_layout()
                plt.show()
        
        elif tipo == 'timeline':
            # Gráfico de timeline de bonus
            if len(self.historial) < 10:
                print("❌ Necesitas al menos 10 rondas para el gráfico de timeline")
                return
            
            rondas = []
            bonus_acumulado = 0
            bonus_timeline = []
            
            for i, ronda in enumerate(self.historial[-50:]):  # Últimas 50 rondas
                rondas.append(i + 1)
                if ronda.get('bonus', False):
                    bonus_acumulado += 1
                bonus_timeline.append(bonus_acumulado)
            
            plt.figure(figsize=(12, 6))
            plt.plot(rondas, bonus_timeline, color='lime', linewidth=2, marker='o', markersize=3)
            plt.title('📈 Timeline de Bonus (Últimas 50 rondas)', fontsize=16, color='white')
            plt.xlabel('Ronda', color='white')
            plt.ylabel('Bonus Acumulados', color='white')
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            plt.show()
    
    def menu_principal(self):
        """Menú principal interactivo"""
        while True:
            print("\n" + "⚡"*50)
            print("🎰 LIGHTNING STORM ANALYZER")
            print("⚡"*50)
            print("1. ➕ Agregar nueva ronda")
            print("2. 📊 Ver estadísticas actuales")
            print("3. 🎯 Simular rondas futuras")
            print("4. 📈 Mostrar gráficos")
            print("5. 🗑️  Limpiar historial")
            print("6. 💾 Exportar datos")
            print("7. ❌ Salir")
            print("⚡"*50)
            
            try:
                opcion = input("Selecciona una opción (1-7): ").strip()
                
                if opcion == "1":
                    self.menu_agregar_ronda()
                elif opcion == "2":
                    self.mostrar_estadisticas()
                elif opcion == "3":
                    self.menu_simulacion()
                elif opcion == "4":
                    self.menu_graficos()
                elif opcion == "5":
                    self.limpiar_historial()
                elif opcion == "6":
                    self.exportar_datos()
                elif opcion == "7":
                    print("👋 ¡Gracias por usar Lightning Storm Analyzer!")
                    break
                else:
                    print("❌ Opción inválida")
                    
            except KeyboardInterrupt:
                print("\n👋 ¡Hasta luego!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def menu_agregar_ronda(self):
        """Menú para agregar una nueva ronda"""
        print("\n🎮 AGREGAR NUEVA RONDA")
        print("-" * 30)
        
        try:
            # Preguntar tipo de resultado
            print("¿Qué tipo de resultado fue?")
            print("1. Número específico (1-20)")
            print("2. Casilla Leaf (1:1)")
            
            tipo = input("Tipo (1-2): ").strip()
            
            if tipo == "1":
                # Número específico
                numero = int(input("Número que salió (1-20): "))
                if not (1 <= numero <= 20):
                    print("❌ El número debe estar entre 1 y 20")
                    return
                
                # Preguntar por bonus
                bonus_input = input("¿Hubo bonus? (s/n): ").strip().lower()
                bonus = bonus_input in ['s', 'sí', 'si', 'yes', 'y']
                
                # Preguntar por multiplicador
                mult_input = input("Multiplicador (enter para 1.0): ").strip()
                if mult_input:
                    multiplicador = float(mult_input)
                else:
                    multiplicador = 1.0
                
                if self.agregar_ronda(numero=numero, bonus=bonus, multiplicador=multiplicador):
                    print(f"✅ Ronda agregada: Número {numero}")
                    if bonus:
                        print("   🎁 Con bonus")
                    if multiplicador > 1:
                        print(f"   ⚡ Multiplicador: {multiplicador}x")
                
            elif tipo == "2":
                # Casilla leaf
                if self.agregar_ronda(es_leaf=True):
                    print("✅ Ronda agregada: Casilla Leaf (1:1)")
            else:
                print("❌ Opción inválida")
                
        except ValueError:
            print("❌ Error: Ingresa números válidos")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def menu_simulacion(self):
        """Menú para simulaciones"""
        print("\n🎯 SIMULACIÓN DE RONDAS FUTURAS")
        print("-" * 35)
        
        try:
            num_rondas = int(input("¿Cuántas rondas simular? (default: 10): ") or "10")
            num_sims = int(input("¿Cuántas simulaciones? (default: 1000): ") or "1000")
            
            print(f"\n⚡ Simulando {num_sims} secuencias de {num_rondas} rondas...")
            
            resultados = self.simular_rondas_futuras(num_sims, num_rondas)
            
            if resultados:
                print(f"\n📊 RESULTADOS DE SIMULACIÓN:")
                print(f"🍃 Casillas leaf esperadas: {resultados['conteo_leaf']:.1f}")
                print(f"🎁 Bonus esperados: {resultados['total_bonus']:.1f}")
                print(f"⚡ Multiplicadores esperados: {resultados['multiplicadores_aplicados']:.1f}")
                print(f"📈 Probabilidad de al menos 1 bonus en {num_rondas} rondas: {resultados['prob_bonus_en_X_rondas']*100:.1f}%")
                
                print(f"\n🎯 NÚMEROS MÁS PROBABLES:")
                numeros_sim = sorted(resultados['conteo_numeros'].items(), 
                                   key=lambda x: x[1], reverse=True)
                for i, (numero, freq) in enumerate(numeros_sim[:8]):
                    print(f"  {i+1}. Número {numero:2d}: {freq:.1f} veces esperadas")
            
        except ValueError:
            print("❌ Error: Ingresa números válidos")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def menu_graficos(self):
        """Menú para mostrar gráficos"""
        if not MATPLOTLIB_AVAILABLE:
            print("❌ Matplotlib no está disponible para mostrar gráficos")
            return
        
        print("\n📈 GRÁFICOS DISPONIBLES")
        print("-" * 25)
        print("1. Frecuencias de números")
        print("2. Bonus por número") 
        print("3. Timeline de bonus")
        
        try:
            opcion = input("Selecciona gráfico (1-3): ").strip()
            
            if opcion == "1":
                self.mostrar_grafico('frecuencias')
            elif opcion == "2":
                self.mostrar_grafico('bonus')
            elif opcion == "3":
                self.mostrar_grafico('timeline')
            else:
                print("❌ Opción inválida")
                
        except Exception as e:
            print(f"❌ Error mostrando gráfico: {e}")
    
    def limpiar_historial(self):
        """Limpia todo el historial"""
        confirmacion = input("⚠️  ¿Estás seguro de limpiar todo el historial? (escribe 'CONFIRMAR'): ")
        if confirmacion == "CONFIRMAR":
            self.historial = []
            self.recalcular_estadisticas()
            self.guardar_datos()
            print("✅ Historial limpiado completamente")
        else:
            print("❌ Operación cancelada")
    
    def exportar_datos(self):
        """Exporta datos a un archivo de texto"""
        try:
            archivo = f"lightning_storm_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(archivo, 'w', encoding='utf-8') as f:
                f.write("LIGHTNING STORM - EXPORT DE DATOS\n")
                f.write("="*50 + "\n\n")
                f.write(f"Total de rondas: {self.stats['total_rondas']}\n")
                f.write(f"Fecha de export: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                f.write("HISTORIAL DE RONDAS:\n")
                f.write("-" * 20 + "\n")
                for i, ronda in enumerate(self.historial, 1):
                    if ronda.get('es_leaf'):
                        f.write(f"{i:3d}. Leaf (1:1)\n")
                    else:
                        bonus_str = " +BONUS" if ronda.get('bonus') else ""
                        mult_str = f" x{ronda.get('multiplicador', 1)}" if ronda.get('multiplicador', 1) > 1 else ""
                        f.write(f"{i:3d}. Número {ronda['numero']:2d}{bonus_str}{mult_str}\n")
                
            print(f"✅ Datos exportados a: {archivo}")
        except Exception as e:
            print(f"❌ Error exportando: {e}")


def main():
    """Función principal"""
    print("🎰 Bienvenido al Lightning Storm Analyzer!")
    print("Este programa te ayuda a analizar patrones y probabilidades")
    print("en el juego Lightning Storm para mejorar tus estrategias.\n")
    
    analyzer = LightningStormAnalyzer()
    analyzer.menu_principal()

if __name__ == "__main__":
    main()
