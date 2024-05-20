import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3


def open_db_incoming(file="D:\\PycharmProjects\\Finance\\data\\main.db") -> pd.DataFrame:
    con = sqlite3.connect(file)
    df = pd.read_sql(
        """SELECT IM.*, U.username 
           FROM IncomingMoney IM  
           JOIN Users U ON IM.created_by = U.id; """,
        con=con)
    df = df.T.drop_duplicates().T
    # df['create_at'] = pd.to_datetime(df['create_at'], errors='coerce')
    con.close()
    # Convert 'create_at' column to datetime
    # df['create_at'] = pd.to_datetime(df_date['create_at'])
    return df


def open_db_outgoing(file="D:\\PycharmProjects\\Finance\\data\\main.db") -> pd.DataFrame:
    con = sqlite3.connect(file)
    df = pd.read_sql(
        """SELECT OM.*, U.username 
           FROM OutgoingMoney OM  
           JOIN Users U ON OM.created_by = U.id; """,
        con=con)
    df = df.T.drop_duplicates().T
    # df['create_at'] = pd.to_datetime(df['create_at'], errors='coerce')
    con.close()
    # Convert 'create_at' column to datetime
    # df['create_at'] = pd.to_datetime(df_date['create_at'])
    return df


def pie_chart(name):
    df = open_db_incoming()
    # Plot pie chart
    plt.figure(figsize=(8, 8))
    df['username'].value_counts().plot.pie(autopct='%1.1f%%')
    plt.savefig(f"D:\\PycharmProjects\\Finance\\media\\analisis\\{name}.jpg")
    plt.close()

def bar_plot(name):
    df = open_db_incoming()
    # Plot bar plot
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x='create_at', y='menturement', hue='username')
    plt.savefig(f"D:\\PycharmProjects\\Finance\\media\\analisis\\{name}.jpg")
    plt.close()

def hist_plot(name):
    df = open_db_incoming()
    if df.empty:
        print("DataFrame is empty.")
        return
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x='create_at', y='menturement', hue='username', multiple="stack")
    plt.savefig(f"D:\\PycharmProjects\\Finance\\media\\analisis\\{name}.jpg")
    plt.close()  # Close the plot to release resources
    print("Histogram plot saved successfully.")


def pie_chart_outgoing(name):
    df = open_db_outgoing()
    # Plot pie chart
    plt.figure(figsize=(8, 8))
    df['username'].value_counts().plot.pie(autopct='%1.1f%%')
    plt.savefig(f"D:\\PycharmProjects\\Finance\\media\\analisis\\{name}.jpg")
    plt.close()

def bar_plot_outgoing(name):
    df = open_db_outgoing()

    # Plot bar plot
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x='create_at', y='menturement', hue='username')
    plt.savefig(f"D:\\PycharmProjects\\Finance\\media\\analisis\\{name}.jpg")
    plt.close()

def hist_plot_outgoing(name):
    df = open_db_outgoing()
    if df.empty:
        print("DataFrame is empty.")
        return
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x='create_at', y='menturement', hue='username', multiple="stack")
    plt.savefig(f"D:\\PycharmProjects\\Finance\\media\\analisis\\{name}.jpg")
    plt.close()  # Close the plot to release resources
    print("Histogram plot saved successfully.")





def all_line_graft(name):
    df_incoming = open_db_incoming()
    df_outgoing = open_db_outgoing()
    df =pd.concat([df_incoming, df_outgoing])
    plt.figure(figsize=(10, 6))
    plt.plot(df_incoming['create_at'], df_incoming['menturement'], color='red', label='Incoming')
    plt.plot(df_outgoing['create_at'], df_outgoing['menturement'], color='blue', label='Outgoing')
    plt.title('Incoming and Outgoing Money Over Time')
    plt.xlabel('Date')
    plt.ylabel('Amount')
    # Add a legend
    plt.legend()
    # Show the plot
    plt.savefig(f"D:\\PycharmProjects\\Finance\\media\\analisis\\{name}.jpg")
    plt.close()
