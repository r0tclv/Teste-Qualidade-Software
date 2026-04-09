# =================================================================================================================================

# Atividade Avaliativa - Uso de GitHub Actions para execução de Testes Automatizados (2,0)
O objetivo desta atividade avaliativa será:

Crie um repositório para registrar sua aplicação no Github. Lembre-se de manter o repositório público e/ou compartilhar com seu professor através da conta no github (neutonmelo-neutonmelo@gmail.com).
Seu grupo deverá desenvolver um CRUD (CREATE READ UPDATE DELETE) para gerenciar disciplinas oferecidas em uma instituição de ensino. Cada disciplina deverá registrar, obrigatoriamente, título, data de início, data de término, número de vagas e se a disciplina é de verão.

A partir disto você irá desenvolver testes funcionais para cada um das operações disponíveis no CRUD criado, para desenvolver os testes utilize a metodologia BDD (Behavior-Driven Development), tenham atenção para criar cenários quanto forem necessários para cada função.

Configure seu repositório para conter os arquivos necessários para ativar uma esteira automatizada que irá validar pull request abertos de qualquer branch para main. A esterira deverá validar se há pelo menos 75% de cobertura de testes em cada PR aberto.






# =========================================================================================

Instruções
Nessa atividade você irá evoluir sua aplicação construída na atividade avaliativa com a capacidade de gerenciar disciplinas de uma instituição de ensino. Entretanto, antes da atividade principal, você precisará evoluir sua aplicação.

Comece transformando sua aplicação em uma API que faz uso do Flask, todas as disciplinas devem ser gravadas em um banco de dados Postgres rodando um container Docker. 

Feito isso você deverá criar um novo CRUD para sua aplicação, dessa vez para o gerenciamento de alunos. Cada aluno deve conter os seguintes dados, nome, data de nascimento, e-mail, CPF, telefone sexo, naturalidade. Mas, ao invés de iniciar a implementação das regras de negócio você deverá começar pela construção de testes usando a estratégia TDD. 

Sua entrega deverá ser um PR (Pull Request) aberto em seu repositório com dois commits, o primeiro contendo os testes desenvolvidos e, o segundo commit com a implementação das regras de negócio para cada um das funções do CRUD.

Para ajuda-lo. Algumas possíveis regras de negócio seriam:

Um aluno deve ser sempre maior de idade
Deve existir apenas um aluno por CPF, E-mail ou Telefone
Apenas números nacionais são aceitos
O cadastro de alunos de alunos fora de capitais devem ser vetados.