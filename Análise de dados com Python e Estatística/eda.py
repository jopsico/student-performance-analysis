# Importação das bibliotecas necessárias
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

df = pd.read_csv(r"C:\Users\jpmpe\Documents\student_habits_performance.csv")

# Colunas numéricas
cols = [
    "study_hours_per_day",
    "social_media_hours",
    "netflix_hours",
    "sleep_hours",
    "attendance_percentage",
    "exercise_frequency",
    "mental_health_rating",
    "exam_score",
]

# Preparando dados fora do dashboard
# Avaliando notas médias por diferentes intervalos (bin) de períodos gastos em redes sociais
# ["0-2h", "2-4h", "4-6h", ">6h"]
df["social_media_bin"] = pd.cut(df["social_media_hours"]
                                , bins=[0, 2, 4, 6, float("inf")]
                                , labels=["0-2h", "2-4h", "4-6h", ">6h"]
                                          )

# Criando o Dashboard das visualizações (Painél Único)
sns.set_theme(style="whitegrid")

fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(20, 12))
fig.canvas.manager.set_window_title("Dashboard - Hábitos e Desempenho dos Estudantes")
fig.suptitle("Análise de Impacto: Hábitos vs. Desempenho", fontsize=20, fontweight='bold', y=0.98)

# Mapa de calor para correlação
sns.heatmap(df[cols].corr(), annot=True, fmt=".2f", cmap="coolwarm", 
            ax=axes[0, 0], vmin=-1, vmax=1, 
            annot_kws={"size": 8},
            cbar_kws={"shrink": .8})
axes[0, 0].set_title("Correlação Geral", fontsize=14)
axes[0, 0].set_xticklabels(axes[0, 0].get_xticklabels(), rotation=45, ha='right')

# Gráfico de dispersão com linha de regressão
sns.regplot(data=df, x="study_hours_per_day", y="exam_score", 
            ax=axes[0, 1], scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
axes[0, 1].set_title("Horas de Estudo x Nota", fontsize=14)

# Redes sociais: distribuição geral (Histograma)
sns.histplot(data=df, x="social_media_hours", ax=axes[0, 2], color="skyblue", bins=20)
axes[0, 2].set_title("Distribuição de tempo em redes sociais", fontsize=14)
axes[0, 2].set_xlabel("Horas em redes sociais")
axes[0, 2].set_ylabel("Frequência")

# Pilotar gráfico de caixa (boxplot) para comparar notas por bin de redes sociais
sns.boxplot(x="social_media_bin", y="exam_score", data=df, ax=axes[0, 3], palette="Blues", hue="social_media_bin", legend=False)
axes[0, 3].set_title("Impacto: Tempo Online", fontsize=14)
axes[0, 3].set_xlabel("Intervalo (Horas)")
axes[0, 3].set_ylabel("Nota Final")

# Frequência de exercícios físicos
factors = ["exercise_frequency", "mental_health_rating", "diet_quality"]
titulos_pt = ["Frequência de Exercícios", "Saúde Mental", "Qualidade da Dieta"]

for i, col in enumerate(factors):
    sns.boxplot(x=col, y="exam_score", data=df, ax=axes[1, i], palette="Set2", hue=col, legend=False)
    axes[1, i].set_title(f"Impacto: {titulos_pt[i]}", fontsize=14)
    axes[1, i].set_ylabel("Nota Final")
    axes[1, i].set_xlabel("")
# Esconder o gráfico vazio
axes[1, 3].axis('off')
# Arruma os espaços entre os gráficos
plt.tight_layout(rect=[0, 0, 1, 0.95])

# Estatísticas descritivas gerais pelo terminal
# Comparando médias: Quem estuda  >5h x <2h pelo terminal
filtro_estudo_alto = df["study_hours_per_day"] > 5
filtro_estudo_baixo = df["study_hours_per_day"] < 2

grupo_estudo_alto = df[filtro_estudo_alto]["exam_score"]
grupo_estudo_baixo = df[filtro_estudo_baixo]["exam_score"]

print("Nota média para quem estuda >5h/dia:", grupo_estudo_alto.mean())
print("Nota média para quem estuda <2h/dia:", grupo_estudo_baixo.mean())

    # Estatísticas por gênero (média e desvio de padrão) pelo terminal
print("\n--- ESTATÍSTICAS POR GÊNERO ---")
print(df.groupby(["gender"])["exam_score"].agg(["mean", "std"]).round(2))

    # Avaliar distribuição de gênero pelo terminal
print("\n--- DISTRIBUIÇÃO DE GÊNERO ---")
print(df["gender"].value_counts(normalize=True).round(3).to_string())

plt.show()