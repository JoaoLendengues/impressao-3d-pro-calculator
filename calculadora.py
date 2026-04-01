"""
Lógica de cálculo para impressão 3D
"""
class Calculadora3D:
    """Classe responsável pelos cálculos de precificação"""
    
    def __init__(self):
        self.resultados = {}
    
    def calcular(self, dados):
        """
        Calcula o custo total e valor de venda
        
        Args:
            dados: dicionário com os dados de entrada
                - peso_g: peso em gramas
                - horas: horas de impressão
                - minutos: minutos de impressão
                - custo_material_kg: custo do material por kg
                - consumo_watts: consumo da impressora em watts
                - custo_energia_kwh: custo da energia por kWh
                - taxa_horaria: taxa horária de impressão
                - custo_design: custo de design
                - margem_lucro: margem de lucro em %
        
        Returns:
            dicionário com os resultados calculados
        """
        try:
            # Converter dados
            peso_g = float(dados.get('peso_g', 0))
            horas = float(dados.get('horas', 0))
            minutos = float(dados.get('minutos', 0))
            custo_material_kg = float(dados.get('custo_material_kg', 0))
            consumo_watts = float(dados.get('consumo_watts', 0))
            custo_energia_kwh = float(dados.get('custo_energia_kwh', 0))
            taxa_horaria = float(dados.get('taxa_horaria', 0))
            custo_design = float(dados.get('custo_design', 0))
            margem_lucro = float(dados.get('margem_lucro', 0)) / 100
            
            # Converter unidades
            peso_kg = peso_g / 1000
            tempo_total = horas + (minutos / 60)
            
            # Cálculos
            custo_material = peso_kg * custo_material_kg
            consumo_kwh = (consumo_watts * tempo_total) / 1000
            custo_eletricidade = consumo_kwh * custo_energia_kwh
            custo_tempo = tempo_total * taxa_horaria
            
            # Custos totais
            custo_total_sem_lucro = custo_material + custo_eletricidade + custo_tempo + custo_design
            lucro = custo_total_sem_lucro * margem_lucro
            valor_venda = custo_total_sem_lucro + lucro
            
            # Armazenar resultados
            self.resultados = {
                'peso_g': peso_g,
                'peso_kg': peso_kg,
                'tempo_total': tempo_total,
                'custo_material': round(custo_material, 2),
                'custo_eletricidade': round(custo_eletricidade, 2),
                'custo_tempo': round(custo_tempo, 2),
                'custo_design': round(custo_design, 2),
                'custo_total': round(custo_total_sem_lucro, 2),
                'lucro': round(lucro, 2),
                'valor_venda': round(valor_venda, 2),
                'margem_percentual': margem_lucro * 100
            }
            
            return self.resultados
            
        except Exception as e:
            raise Exception(f"Erro no cálculo: {str(e)}")
    
    def validar_dados(self, dados):
        """Valida os dados de entrada"""
        campos_obrigatorios = ['peso_g', 'custo_material_kg', 'consumo_watts', 
                               'custo_energia_kwh', 'taxa_horaria', 'margem_lucro']
        
        for campo in campos_obrigatorios:
            valor = dados.get(campo, '')
            if not valor or valor == '0':
                return False, f"Campo {campo.replace('_', ' ')} é obrigatório!"
        
        # Validar peso
        try:
            peso = float(dados['peso_g'])
            if peso <= 0:
                return False, "Peso deve ser maior que zero!"
        except:
            return False, "Peso inválido!"
        
        # Validar tempo
        horas = dados.get('horas', '0')
        minutos = dados.get('minutos', '0')
        try:
            h = float(horas) if horas else 0
            m = float(minutos) if minutos else 0
            if h == 0 and m == 0:
                return False, "Informe o tempo de impressão!"
        except:
            return False, "Tempo inválido!"
        
        return True, "OK"
    