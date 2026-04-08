import json


@given('que existe uma disciplina cadastrada')
def existe_disciplina(context):
    payload = {
        'titulo': 'Matematica',
        'data_inicio': '2026-01-15',
        'data_termino': '2026-06-30',
        'vagas': 40,
        'verao': False
    }
    context.client.post('/disciplinas', json=payload)


@given('existe uma segunda disciplina cadastrada')
def existe_segunda_disciplina(context):
    payload = {
        'titulo': 'Fisica',
        'data_inicio': '2026-02-01',
        'data_termino': '2026-07-31',
        'vagas': 35,
        'verao': False
    }
    context.client.post('/disciplinas', json=payload)


@given(
    'que existe uma disciplina cadastrada com titulo "{titulo}"')
def existe_disciplina_com_titulo(context, titulo):
    payload = {
        'titulo': titulo,
        'data_inicio': '2026-03-01',
        'data_termino': '2026-08-30',
        'vagas': 50,
        'verao': False
    }
    context.client.post('/disciplinas', json=payload)


@given(
    'os dados da disciplina com titulo "{titulo}", data_inicio "{inicio}", data_termino "{termino}", vagas {vagas} e verao "{verao}"')
def dados_disciplina(context, titulo, inicio, termino, vagas, verao):
    context.disciplina_data = {
        'titulo': titulo,
        'data_inicio': inicio,
        'data_termino': termino,
        'vagas': int(vagas),
        'verao': verao.title() == 'True'
    }


@given('os dados incompletos com titulo "{titulo}"')
def dados_incompletos(context, titulo):
    context.disciplina_data = {'titulo': titulo}


@when('eu faco uma requisicao GET para "{url}"')
def requisicao_get(context, url):
    context.response = context.client.get(url)


@when('eu faco uma requisicao POST para "/disciplinas"')
def requisicao_post(context):
    context.response = context.client.post(
        '/disciplinas',
        json=vars(context).get('disciplina_data', {})
    )


@when('eu faco uma requisicao PUT para "/disciplinas/{id}" com dados atualizados')
def requisicao_put(context, id):
    context.disciplina_id = int(id)
    context.response = context.client.put(
        f'/disciplinas/{id}',
        json={'titulo': 'Portugues Avancado'}
    )


@when('eu faco uma requisicao DELETE para "/disciplinas/{id}"')
def requisicao_delete(context, id):
    context.disciplina_id = int(id)
    context.response = context.client.delete(f'/disciplinas/{id}')


@when('eu faco uma requisicao GET para "/health"')
def requisicao_health(context):
    context.response = context.client.get('/health')


@then('o status code deve ser {codigo}')
def status_code_eh(context, codigo):
    assert context.response.status_code == int(codigo), \
        f'Esperado {codigo}, recebido {context.response.status_code}'


@then('a resposta deve conter {quantidade} disciplinas')
def resposta_contem_disciplinas(context, quantidade):
    data = json.loads(context.response.data)
    assert len(data) == int(quantidade), \
        f'Esperado {quantidade} disciplinas, recebido {len(data)}'


@then('a resposta deve conter o campo "verao" como verdadeiro')
def resposta_verao_true(context):
    data = json.loads(context.response.data)
    assert data.get('verao') is True, 'Esperada disciplina de verao'


@then('a mensagem "{msg}" deve estar presente na resposta')
def mensagem_na_resposta(context, msg):
    data = json.loads(context.response.data)
    assert data['mensagem'] == msg, \
        f"Esperado '{msg}', recebido '{data.get('mensagem')}'"


@then('a resposta deve conter o titulo "{titulo}"')
def resposta_contem_titulo(context, titulo):
    data = json.loads(context.response.data)
    assert data['titulo'] == titulo, \
        f"Esperado titulo '{titulo}', recebido '{data.get('titulo')}'"


@then('a disciplina deve ter o titulo "{titulo}"')
def disciplina_titulo_atualizado(context, context_ref=None):
    resp = context.client.get(f'/disciplinas/{context.disciplina_id}')
    data = json.loads(resp.data)
    assert data['titulo'] == titulo, \
        f"Esperado titulo '{titulo}', recebido '{data.get('titulo')}'"


@then('a disciplina nao deve mais existir no banco')
def disciplina_removida(context):
    if hasattr(context, 'disciplina_id'):
        resp = context.client.get(f'/disciplinas/{context.disciplina_id}')
        assert resp.status_code == 404, 'Disciplina deveria ter sido removida'


@then('a resposta deve conter status "ok"')
def resposta_health(context):
    data = json.loads(context.response.data)
    assert data.get('status') == 'ok', \
        f"Esperado status 'ok', recebido '{data.get('status')}'"
