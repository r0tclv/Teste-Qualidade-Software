import json
from datetime import date


@given('que existe um aluno cadastrado')
def existe_aluno(context):
    payload = {
        'nome': 'João Silva',
        'data_nascimento': '2000-01-15',
        'email': 'joao@email.com',
        'cpf': '123.456.789-00',
        'telefone': '(11) 98765-4321',
        'sexo': 'Masculino',
        'naturalidade': 'São Paulo'
    }
    context.client.post('/alunos', json=payload)


@given('existe um segundo aluno cadastrado')
def existe_segundo_aluno(context):
    payload = {
        'nome': 'Maria Oliveira',
        'data_nascimento': '1995-03-22',
        'email': 'maria@email.com',
        'cpf': '987.654.321-00',
        'telefone': '(21) 99999-9999',
        'sexo': 'Feminino',
        'naturalidade': 'Rio de Janeiro'
    }
    context.client.post('/alunos', json=payload)


@given('que existe um aluno cadastrado com nome "{nome}"')
def existe_aluno_com_nome(context, nome):
    payload = {
        'nome': nome,
        'data_nascimento': '1990-05-10',
        'email': f'{nome.lower().replace(" ", ".")}@email.com',
        'cpf': '111.111.111-11',
        'telefone': '(11) 91234-5678',
        'sexo': 'Masculino',
        'naturalidade': 'São Paulo'
    }
    context.client.post('/alunos', json=payload)


@given('que existe um aluno cadastrado com CPF "{cpf}"')
def existe_aluno_com_cpf(context, cpf):
    payload = {
        'nome': 'Usuario Existente',
        'data_nascimento': '1990-01-01',
        'email': 'existente@email.com',
        'cpf': cpf,
        'telefone': '(11) 91234-5678',
        'sexo': 'Masculino',
        'naturalidade': 'São Paulo'
    }
    context.client.post('/alunos', json=payload)


@given('que existe um aluno cadastrado com email "{email}"')
def existe_aluno_com_email(context, email):
    payload = {
        'nome': 'Usuario Existente',
        'data_nascimento': '1990-01-01',
        'email': email,
        'cpf': '111.111.111-11',
        'telefone': '(11) 91234-5678',
        'sexo': 'Masculino',
        'naturalidade': 'São Paulo'
    }
    context.client.post('/alunos', json=payload)


@given('que existe um aluno cadastrado com telefone "{telefone}"')
def existe_aluno_com_telefone(context, telefone):
    payload = {
        'nome': 'Usuario Existente',
        'data_nascimento': '1990-01-01',
        'email': 'existente@email.com',
        'cpf': '111.111.111-11',
        'telefone': telefone,
        'sexo': 'Masculino',
        'naturalidade': 'São Paulo'
    }
    context.client.post('/alunos', json=payload)


@given('os dados do aluno com nome "{nome}", data_nascimento "{data_nasc}", email "{email}", cpf "{cpf}", telefone "{telefone}", sexo "{sexo}" e naturalidade "{naturalidade}"')
def dados_aluno(context, nome, data_nasc, email, cpf, telefone, sexo, naturalidade):
    context.aluno_data = {
        'nome': nome,
        'data_nascimento': data_nasc,
        'email': email,
        'cpf': cpf,
        'telefone': telefone,
        'sexo': sexo,
        'naturalidade': naturalidade
    }


@given('os dados incompletos com nome "{nome}"')
def dados_incompletos(context, nome):
    context.aluno_data = {'nome': nome}


@when('eu faco uma requisicao GET para "{url}"')
def requisicao_get(context, url):
    context.response = context.client.get(url)


@when('eu faco uma requisicao POST para "/alunos"')
def requisicao_post(context):
    context.response = context.client.post(
        '/alunos',
        json=vars(context).get('aluno_data', {})
    )


@when('eu faco uma requisicao PUT para "/alunos/{id}" com dados atualizados')
def requisicao_put(context, id):
    context.aluno_id = int(id)
    context.response = context.client.put(
        f'/alunos/{id}',
        json={'nome': 'Rafael Gomes Senior'}
    )


@when('eu faco uma requisicao DELETE para "/alunos/{id}"')
def requisicao_delete(context, id):
    context.aluno_id = int(id)
    context.response = context.client.delete(f'/alunos/{id}')


@when('eu faco uma requisicao GET para "/health"')
def requisicao_health(context):
    context.response = context.client.get('/health')


@then('o status code deve ser {codigo}')
def status_code_eh(context, codigo):
    assert context.response.status_code == int(codigo), \
        f'Esperado {codigo}, recebido {context.response.status_code}'


@then('a resposta deve conter {quantidade} alunos')
def resposta_contem_alunos(context, quantidade):
    data = json.loads(context.response.data)
    assert len(data) == int(quantidade), \
        f'Esperado {quantidade} alunos, recebido {len(data)}'


@then('a mensagem "{msg}" deve estar presente na resposta')
def mensagem_na_resposta(context, msg):
    data = json.loads(context.response.data)
    assert data['mensagem'] == msg, \
        f"Esperado '{msg}', recebido '{data.get('mensagem')}'"


@then('a resposta deve conter o nome "{nome}"')
def resposta_contem_nome(context, nome):
    data = json.loads(context.response.data)
    assert data['nome'] == nome, \
        f"Esperado nome '{nome}', recebido '{data.get('nome')}'"


@then('o aluno deve ter o nome "{nome}"')
def aluno_nome_atualizado(context, nome):
    resp = context.client.get(f'/alunos/{context.aluno_id}')
    data = json.loads(resp.data)
    assert data['nome'] == nome, \
        f"Esperado nome '{nome}', recebido '{data.get('nome')}'"


@then('o aluno nao deve mais existir no banco')
def aluno_removido(context):
    if hasattr(context, 'aluno_id'):
        resp = context.client.get(f'/alunos/{context.aluno_id}')
        assert resp.status_code == 404, 'Aluno deveria ter sido removido'


@then('a resposta deve conter status "ok"')
def resposta_health(context):
    data = json.loads(context.response.data)
    assert data.get('status') == 'ok', \
        f"Esperado status 'ok', recebido '{data.get('status')}'"