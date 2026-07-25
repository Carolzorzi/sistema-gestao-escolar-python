# Sistema de Gestão Escolar

> Aplicação web interativa desenvolvida em Python para o gerenciamento completo de instituições de ensino ou outras unidades profissionais, unindo controle de usuários cadastrados, controle de funcionários e acompanhamento financeiro em tempo real.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey)

---

## Sobre o Projeto
Este sistema foi desenvolvido para otimizar a rotina administrativa escolar. Ele resolve dores reais como o acompanhamento de matrículas ativas/inativas, o controle de turmas/professores e, principalmente, a **gestão financeira**, permitindo visualizar de forma clara o faturamento previsto, mensalidades recebidas e o controle de inadimplência.

---

## Tecnologias Utilizadas
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
  <img width="1912" height="908" alt="Visão Geral" src="https://github.com/user-attachments/assets/1924ebee-7103-4fc0-b1c6-5282218b128e" />

* **Gestão de Alunos Ativos:** 
  * Cadastro, listagem e controle do status de matrícula (Ativo/Inativo).
   <img width="1917" height="908" alt="Alunos Ativos" src="https://github.com/user-attachments/assets/246942db-a348-4397-a936-14fd9d73bf20" />

* **Gestão de Professores:** 
  * Cadastro, listagem e controle de disciplinas.
    <img width="1917" height="910" alt="Base de Professores" src="https://github.com/user-attachments/assets/dfa4158a-b0b1-471f-8fa3-ae52a549e87a" />

* **Gestão de Faturamento:** 
  * Acompanhamento financeiro (Faturamento Previsto vs. Faturamento Atual).
  * Gestão de inadimplência com resumo por status (*Pago/Em dia*, *Pendente*, *Inadimplente*).
  * Atualização dinâmica de status de pagamento por aluno com persistência imediata no banco de dados.
  <img width="1917" height="912" alt="Gestão de Faturamento" src="https://github.com/user-attachments/assets/84f65da3-b4f4-442e-bce5-f38c482b7d64" />

* **Configurações do Sistema:** 
  * Efeito simples de ajuste de aparência dos botões do menu lateral (arredondamento).
  <img width="1917" height="920" alt="Configurações do Sistema" src="https://github.com/user-attachments/assets/ea678c6c-2920-45a4-ab88-484897710d7a" />

---

## Como Executar o Projeto Localmente

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/Carolzorzi/sistema_gestao_escolar.git](https://github.com/Carolzorzi/sistema_gestao_escolar.git)).
