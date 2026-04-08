# =================================================================================================================================

# Atividade Avaliativa - Uso de GitHub Actions para execução de Testes Automatizados (2,0)
O objetivo desta atividade avaliativa será:

Crie um repositório para registrar sua aplicação no Github. Lembre-se de manter o repositório público e/ou compartilhar com seu professor através da conta no github (neutonmelo-neutonmelo@gmail.com).
Seu grupo deverá desenvolver um CRUD (CREATE READ UPDATE DELETE) para gerenciar disciplinas oferecidas em uma instituição de ensino. Cada disciplina deverá registrar, obrigatoriamente, título, data de início, data de término, número de vagas e se a disciplina é de verão.

A partir disto você irá desenvolver testes funcionais para cada um das operações disponíveis no CRUD criado, para desenvolver os testes utilize a metodologia BDD (Behavior-Driven Development), tenham atenção para criar cenários quanto forem necessários para cada função.

Configure seu repositório para conter os arquivos necessários para ativar uma esteira automatizada que irá validar pull request abertos de qualquer branch para main. A esterira deverá validar se há pelo menos 75% de cobertura de testes em cada PR aberto.
# =================================================================================================================================
Segundo passo:

Instruções
TEXTO BASE
Você faz parte de uma equipe responsável pelo desenvolvimento de um sistema de marketplace semelhante a Amazon.

O sistema possui:

múltiplos vendedores
controle de estoque distribuído
cálculo de frete
pagamento via gateway externo
regras complexas de negócio 
Recentemente, o sistema apresentou:

falhas na finalização de pedidos
inconsistência de estoque
pedidos duplicados 
A liderança técnica decidiu:
“A partir de agora, toda funcionalidade deve ser definida primeiro por testes.”

CONTEXTO DO PROBLEMA

Nova funcionalidade:
Reserva de estoque durante checkout 

Regras:

produto deve ter estoque disponível
reserva expira em 5 minutos
não pode reservar mais que o disponível
concorrência entre usuários
ESCREVER TESTES (PSEUDOCÓDIGO)
Você deve criar:

3 cenários de sucesso
3 cenários de falha