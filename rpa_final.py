import requests
import sqlite3
from datetime import datetime

def coletar_dados_api():
    url = "https://api.adviceslip.com/advice"
    print("\n[1] Realizando requisição para a API...")

    try:
        resposta = requests.get(url, timeout=10)
        dados = resposta.json()

        print("[OK] Dados recebidos com sucesso!")

        return {
            'id': dados['slip']['id'],
            'conselho': dados['slip']['advice'],
            'data_coleta': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    except Exception as e:
        print(f"[ERRO] Falha ao acessar a API: {e}")
        return None

def criar_banco():
    print("\n[2] Criando/verificando banco de dados...")

    conn = sqlite3.connect('projeto_rpa.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS conselhos (
            id INTEGER PRIMARY KEY,
            conselho TEXT UNIQUE,
            data_coleta TEXT
        )
    ''')

    conn.commit()
    conn.close()

    print("[OK] Banco de dados pronto!")

def salvar_dados(dados):
    if not dados:
        print("[ERRO] Nenhum dado para salvar.")
        return False

    print("\n[3] Salvando dados no banco...")

    conn = sqlite3.connect('projeto_rpa.db')
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT OR IGNORE INTO conselhos 
            VALUES (?, ?, ?)
        ''', (dados['id'], dados['conselho'], dados['data_coleta']))
        
        conn.commit()
        
        if cursor.rowcount > 0:
            print("[OK] Novo conselho inserido com sucesso!")
            inserido = True
        else:
            print("[INFO] Conselho já existe no banco (não duplicado).")
            inserido = False
            
    except sqlite3.IntegrityError as e:
        print(f"[ERRO] Erro de integridade: {e}")
        inserido = False
    finally:
        conn.close()
    
    return inserido

def processar_dados():
    print("\n[4] Processando dados...")
    
    conn = sqlite3.connect('projeto_rpa.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('SELECT COUNT(*) FROM conselhos')
        total_conselhos = cursor.fetchone()[0]
        
        cursor.execute('SELECT conselho, data_coleta FROM conselhos ORDER BY data_coleta DESC')
        todos_conselhos = cursor.fetchall()
        
        conselhos_longos = [c[0] for c in todos_conselhos if len(c[0]) > 50]
        conselhos_curtos = [c[0] for c in todos_conselhos if len(c[0]) <= 50]
        
        print(f"[PROCESSAMENTO] Total de conselhos no banco: {total_conselhos}")
        print(f"[PROCESSAMENTO] Conselhos longos (>50 chars): {len(conselhos_longos)}")
        print(f"[PROCESSAMENTO] Conselhos curtos (≤50 chars): {len(conselhos_curtos)}")
        
        if todos_conselhos:
            print(f"\n[PROCESSAMENTO] Todos os conselhos armazenados:")
            for i, (conselho, data) in enumerate(todos_conselhos, 1):
                print(f"  {i}. '{conselho}' - {data}")
                
    except Exception as e:
        print(f"[ERRO] Erro ao processar dados: {e}")
    finally:
        conn.close()

def main():
    print("PROJETO RPA - SISTEMA DE CONSELHOS ALEATÓRIOS")
    print("=" * 50)

    dados = coletar_dados_api()

    if dados:
        print(f"\nConselho recebido da API:\n>>> {dados['conselho']}\n")

        criar_banco()
        salvar_dados(dados)
        processar_dados()

        print("\n" + "=" * 50)
        print("[OK] Processo concluído com sucesso!")
    else:
        print("\n[ERRO] Falha ao coletar dados da API.")

if __name__ == "__main__":
    main()