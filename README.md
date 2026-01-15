# 🚀 Churn Prediction Service - End-to-End MLOps

Este projeto implementa um ecossistema completo de Machine Learning para predição de rotatividade de clientes (Churn), focando em práticas de **MLOps** e escalabilidade.

## 🛠️ Tecnologias e Arquitetura
- **Ingestão de Dados:** SQL para extração e processamento.
- **Tracking de Experimentos:** **MLflow** para versionamento de modelos, métricas e artefatos.
- **Serving (API):** **FastAPI** provendo endpoints de predição em tempo real com baixa latência.
- **Monitoramento:** **Evidently AI** para detecção de Data Drift e monitoramento de saúde do modelo.

## 🏗️ Destaques da Implementação
- **Modelo via Run ID:** Implementação de carregamento dinâmico de artefatos via MLflow Tracking, eliminando dependências de caminhos locais (hardcoded).
- **Validação de Dados:** Uso de **Pydantic** para garantir a integridade dos inputs na API.
- **Governança:** Separação clara entre o pipeline de treinamento e o ambiente de serviço (serving).
