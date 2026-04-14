# language: pt
Funcionalidade: Gerenciamento de Alunos
    Como um usuario do sistema
    Eu quero gerenciar os alunos da instituicao
    Para ter controle sobre os estudantes matriculados

    Cenario: Listar todos os alunos
        Dado que existe um aluno cadastrado
        E existe um segundo aluno cadastrado
        Quando eu faco uma requisicao GET para "/alunos"
        Entao o status code deve ser 200
        E a resposta deve conter 2 alunos

    Cenario: Criar um novo aluno valido
        Dados os dados do aluno com nome "João Silva", data_nascimento "2000-01-15", email "joao@email.com", cpf "123.456.789-00", telefone "(11) 98765-4321", sexo "Masculino" e naturalidade "São Paulo"
        Quando eu faco uma requisicao POST para "/alunos"
        Entao o status code deve ser 201
        E a mensagem "Aluno criado com sucesso" deve estar presente na resposta

    Cenario: Criar um aluno menor de idade
        Dados os dados do aluno com nome "Pedro Oliveira", data_nascimento "2010-01-15", email "pedro@email.com", cpf "987.654.321-00", telefone "(11) 91234-5678", sexo "Masculino" e naturalidade "São Paulo"
        Quando eu faco uma requisicao POST para "/alunos"
        Entao o status code deve ser 400
        E a mensagem "Aluno deve ser maior de idade" deve estar presente na resposta

    Cenario: Criar aluno com CPF duplicado
        Dado que existe um aluno cadastrado com CPF "111.222.333-44"
        Quando eu faco uma requisicao POST para "/alunos" com os dados do aluno com nome "Maria Santos", data_nascimento "2000-05-20", email "maria@email.com", cpf "111.222.333-44", telefone "(21) 99999-9999", sexo "Feminino" e naturalidade "Rio de Janeiro"
        Entao o status code deve ser 400
        E a mensagem "Ja existe um aluno com este CPF" deve estar presente na resposta

    Cenario: Criar aluno com email duplicado
        Dado que existe um aluno cadastrado com email "existente@email.com"
        Quando eu faco uma requisicao POST para "/alunos" com os dados do aluno com nome "Carlos Souza", data_nascimento "1995-08-10", email "existente@email.com", cpf "555.666.777-88", telefone "(31) 98765-4321", sexo "Masculino" e naturalidade "Belo Horizonte"
        Entao o status code deve ser 400
        E a mensagem "Ja existe um aluno com este e-mail" deve estar presente na resposta

    Cenario: Criar aluno com telefone duplicado
        Dado que existe um aluno cadastrado com telefone "(11) 91234-5678"
        Quando eu faco uma requisicao POST para "/alunos" com os dados do aluno com nome "Ana Pereira", data_nascimento "1998-12-03", email "ana@email.com", cpf "999.888.777-66", telefone "(11) 91234-5678", sexo "Feminino" e naturalidade "Campinas"
        Entao o status code deve ser 400
        E a mensagem "Ja existe um aluno com este telefone" deve estar presente na resposta

    Cenario: Criar aluno com telefone internacional
        Dados os dados do aluno com nome "Fernanda Lima", data_nascimento "1999-03-22", email "fernanda@email.com", cpf "111.222.333-44", telefone "+1 (555) 123-4567", sexo "Feminino" e naturalidade "Nova York"
        Quando eu faco uma requisicao POST para "/alunos"
        Entao o status code deve ser 400
        E a mensagem "Apenas numeros nacionais sao aceitos para telefone" deve estar presente na resposta

    Cenario: Criar aluno fora da capital
        Dados os dados do aluno com nome "Roberto Costa", data_nascimento "1997-07-14", email "roberto@email.com", cpf "222.333.444-55", telefone "(19) 99999-9999", sexo "Masculino" e naturalidade "Interior"
        Quando eu faco uma requisicao POST para "/alunos"
        Entao o status code deve ser 400
        E a mensagem "Cadastro de alunos fora de capitais eh proibido" deve estar presente na resposta

    Cenario: Criar aluno com dados incompletos
        Dados os dados incompletos com nome "Jose"
        Quando eu faco uma requisicao POST para "/alunos"
        Entao o status code deve ser 400

    Cenario: Buscar um aluno por ID
        Dado que existe um aluno cadastrado com nome "Lucas Alves"
        Quando eu faco uma requisicao GET para "/alunos/1"
        Entao o status code deve ser 200
        E a resposta deve conter o nome "Lucas Alves"

    Cenario: Buscar um aluno inexistente
        Quando eu faco uma requisicao GET para "/alunos/999"
        Entao o status code deve ser 404

    Cenario: Atualizar um aluno existente
        Dado que existe um aluno cadastrado com nome "Rafael Gomes"
        Quando eu faco uma requisicao PUT para "/alunos/1" com dados atualizados
        Entao o status code deve ser 200
        E a resposta deve conter a mensagem "Aluno atualizado com sucesso"
        E o aluno deve ter o nome "Rafael Gomes Senior"

    Cenario: Atualizar um aluno inexistente
        Quando eu faco uma requisicao PUT para "/alunos/999" com dados atualizados
        Entao o status code deve ser 404

    Cenario: Deletar um aluno existente
        Dado que existe um aluno cadastrado com nome "Fernanda Dias"
        Quando eu faco uma requisicao DELETE para "/alunos/1"
        Entao o status code deve ser 200
        E a resposta deve conter a mensagem "Aluno removido com sucesso"
        E o aluno nao deve mais existir no banco

    Cenario: Deletar um aluno inexistente
        Quando eu faco uma requisicao DELETE para "/alunos/999"
        Entao o status code deve ser 404

    Cenario: Verificar health check da API
        Quando eu faco uma requisicao GET para "/health"
        Entao o status code deve ser 200
        E a resposta deve conter status "ok"