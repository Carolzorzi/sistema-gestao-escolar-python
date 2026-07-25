# Sistema de Gestão Escolar

> Aplicação web interativa desenvolvida em Python para o gerenciamento completo de instituições de ensino ou outras unidades profissionais, unindo controle de usuários cadastrados, controle de funcionários e acompanhamento financeiro em tempo real.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey)

---

## Sobre o Projeto
Este sistema foi desenvolvido para otimizar a rotina administrativa escolar. Ele resolve dores reais como o acompanhamento de matrículas ativas/inativas, o controle de turmas/professores e, principalmente, a **gestão financeira**, permitindo visualizar de forma clara o faturamento previsto, mensalidades recebidas e o controle de inadimplência.

---

## 🛠️ Tecnologias Utilizadas
* **Python:** Linguagem principal de lógica e manipulação de dados.
* **Streamlit:** Framework para criação da interface web interativa.
* **Pandas:** Biblioteca para tratamento, filtragem e estruturação de tabelas.
* **SQLite:** Banco de dados relacional leve e embutido para persistência segura dos registros.
* **Plotly:** Biblioteca para geração de gráficos analíticos dinâmicos (Visão Geral).

---

## Principais Funcionalidades
* **Visão Geral (Dashboard):** 
  * Indicadores-chave (KPIs) de total de alunos, faturamento previsto e atual.
  * Gráficos em pizza interativos mostrando a distribuição de alunos ativos/inativos e o status detalhado dos pagamentos.
* **Gestão de Alunos Ativos:** 
  * Cadastro, listagem e controle do status de matrícula (Ativo/Inativo).
* **Gestão de Faturamento:** 
  * Acompanhamento financeiro (Faturamento Previsto vs. Faturamento Atual).
  * Gestão de inadimplência com resumo por status (*Pago/Em dia*, *Pendente*, *Inadimplente*).
  * Atualização dinâmica de status de pagamento por aluno com persistência imediata no banco de dados.

---

## Como Executar o Projeto Localmente

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/seu-usuario/sistema-gestao-escolar.git](https://github.com/seu-usuario/sistema-gestao-escolar.git)