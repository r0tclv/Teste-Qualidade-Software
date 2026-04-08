# language: pt
Funcionalidade: Gerenciamento de Disciplinas
    Como um usuario do sistema
    Eu quero gerenciar as disciplinas da instituicao
    Para ter controle sobre cursos oferecidos

    Cenario: Listar todas as disciplinas
        Dado que existe uma disciplina cadastrada
        E existe uma segunda disciplina cadastrada
        Quando eu faco uma requisicao GET para "/disciplinas"
        Entao o status code deve ser 200
        E a resposta deve conter 2 disciplinas

    Cenario: Criar uma nova disciplina
        Dados os dados da disciplina com titulo "Matematica", data_inicio "2026-01-15", data_termino "2026-06-30", vagas 40 e verao "False"
        Quando eu faco uma requisicao POST para "/disciplinas"
        Entao o status code deve ser 201
        E a mensagem "Disciplina criada com sucesso" deve estar presente na resposta

    Cenario: Criar uma nova disciplina de verao
        Dados os dados da disciplina com titulo "Fisica de Verao", data_inicio "2026-12-01", data_termino "2027-02-28", vagas 30 e verao "True"
        Quando eu faco uma requisicao POST para "/disciplinas"
        Entao o status code deve ser 201
        E a resposta deve conter o campo "verao" como verdadeiro

    Cenario: Criar uma disciplina com dados incompletos
        Dados os dados incompletos com titulo "Quimica"
        Quando eu faco uma requisicao POST para "/disciplinas"
        Entao o status code deve ser 400

    Cenario: Buscar uma disciplina por ID
        Dado que existe uma disciplina cadastrada com titulo "Historia"
        Quando eu faco uma requisicao GET para "/disciplinas/1"
        Entao o status code deve ser 200
        E a resposta deve conter o titulo "Historia"

    Cenario: Buscar uma disciplina inexistente
        Quando eu faco uma requisicao GET para "/disciplinas/999"
        Entao o status code deve ser 404

    Cenario: Atualizar uma disciplina existente
        Dado que existe uma disciplina cadastrada com titulo "Portugues"
        Quando eu faco uma requisicao PUT para "/disciplinas/1" com dados atualizados
        Entao o status code deve ser 200
        E a resposta deve conter a mensagem "Disciplina atualizada com sucesso"
        E a disciplina deve ter o titulo "Portugues Avancado"

    Cenario: Atualizar uma disciplina inexistente
        Quando eu faco uma requisicao PUT para "/disciplinas/999" com dados atualizados
        Entao o status code deve ser 404

    Cenario: Deletar uma disciplina existente
        Dado que existe uma disciplina cadastrada com titulo "Biologia"
        Quando eu faco uma requisicao DELETE para "/disciplinas/1"
        Entao o status code deve ser 200
        E a resposta deve conter a mensagem "Disciplina removida com sucesso"
        E a disciplina nao deve mais existir no banco

    Cenario: Deletar uma disciplina inexistente
        Quando eu faco uma requisicao DELETE para "/disciplinas/999"
        Entao o status code deve ser 404

    Cenario: Verificar health check da API
        Quando eu faco uma requisicao GET para "/health"
        Entao o status code deve ser 200
        E a resposta deve conter status "ok"
