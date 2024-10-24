import matplotlib
matplotlib.use('TkAgg')
import pandas as pd
import matplotlib.pyplot as plt
import re
import re
import pandas as pd

def load_chat(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        chat_data = file.readlines()

    messages = []
    for line in chat_data:
        match = re.match(r'\[(\d{2}/\d{2}/\d{2,4}) (\d{2}:\d{2}:\d{2})\] (.+?): (.+)', line)
        if match:
            date, time, sender, message = match.groups()
            messages.append({'data': date, 'hora': time, 'remetente': sender, 'mensagem': message})
        else:
            print(f"Linha fora do padrão: {line}")

    return pd.DataFrame(messages)


def summary_of_conversations(df):
    df.columns = df.columns.map(str)

    if 'remetente' not in df.columns:
        print("Erro: A coluna 'remetente' não foi encontrada!")
        print("Colunas disponíveis:", df.columns)
        return
    
    summary = df['remetente'].value_counts().reset_index()
    summary.columns = ['Remetente', 'Total de Mensagens']
    print(summary)

def history_by_sender(df, sender_name):
    history = df[df['remetente'] == sender_name]
    print(history[['data', 'hora', 'mensagem']])

def plot_daily_messages(df):
    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%y', dayfirst=True)
    daily_count = df.groupby(['data', 'remetente']).size().unstack(fill_value=0)
    daily_count.plot(kind='bar', stacked=True, figsize=(10, 6))
    plt.title('Quantidade de Mensagens por Dia')
    plt.xlabel('Data')
    plt.ylabel('Número de Mensagens')
    plt.legend(title='Remetente')
    plt.show()


def pie_chart_by_sender(df):
    sender_counts = df['remetente'].value_counts()
    sender_counts.plot(kind='pie', autopct='%1.1f%%', figsize=(8, 8))
    plt.title('Percentual de Mensagens por Remetente')
    plt.ylabel('')
    plt.show()

def line_chart_over_time(df):
    df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
    line_data = df.groupby(['data', 'remetente']).size().unstack(fill_value=0)
    line_data.plot(kind='line', marker='o', figsize=(12, 6))
    plt.title('Mensagens ao Longo do Tempo')
    plt.xlabel('Data')
    plt.ylabel('Número de Mensagens')
    plt.legend(title='Remetente')
    plt.show()

def main():
    file_path = input("Digite o caminho do arquivo de conversa do WhatsApp: ")
    df = load_chat(file_path)
    
    print("Tabela de Dados:")
    print(df)
    
    while True:
        print("\nEscolha uma opção:")
        print("1. Resumo das conversas")
        print("2. Histórico do remetente")
        print("3. Gráfico do histórico do remetente")
        print("4. Gráfico de pizza")
        print("5. Gráfico de linhas")
        print("6. Sair")
        
        choice = input("Opção: ")
        
        if choice == '1':
            summary_of_conversations(df)
        elif choice == '2':
            sender_name = input("Digite o nome do remetente: ")
            history_by_sender(df, sender_name)
        elif choice == '3':
            plot_daily_messages(df)
        elif choice == '4':
            pie_chart_by_sender(df)
        elif choice == '5':
            line_chart_over_time(df)
        elif choice == '6':
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()

