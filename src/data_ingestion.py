import sqlite3
import pandas as pd
import numpy as np
import os

def setup_database():
    """Simula a carga de dados no banco de produção da empresa"""
    os.makedirs('data', exist_ok=True)
    
    conn = sqlite3.connect('data/enterprise.db')
    
    np.random.seed(42)
    df_fake = pd.DataFrame({
        'user_id': range(1000),
        'tenure': np.random.randint(1, 72, 1000),
        'monthly_charges': np.random.uniform(20, 120, 1000),
        'total_charges': np.random.uniform(100, 5000, 1000),
        'contract_type': np.random.choice(['Month-to-month', 'One year', 'Two year'], 1000),
        'churn': np.random.choice([0, 1], 1000, p=[0.7, 0.3])
    })
    
    df_fake.to_sql('customers', conn, if_exists='replace', index=False)
    conn.close()
    print("✅ Banco de dados SQLite criado com sucesso em data/enterprise.db")

def extract_data():
    """Executa a query SQL de nível sênior com Feature Engineering"""
    conn = sqlite3.connect('data/enterprise.db')
    
    query = """
    SELECT 
        *,
        (total_charges / tenure) as ltv_ratio,
        CASE WHEN contract_type = 'Month-to-month' THEN 1 ELSE 0 END as is_flexible
    FROM customers
    """
    
    df = pd.read_sql(query, conn)
    conn.close()
    
    df.to_csv('data/processed_data.csv', index=False)
    print(f"✅ Extração concluída. {len(df)} linhas prontas para o treino.")
    return df

if __name__ == "__main__":
    setup_database()
    extract_data()