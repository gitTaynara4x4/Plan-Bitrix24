from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os


app = Flask(__name__)

load_dotenv()

CODIGO_BITRIX = os.getenv('CODIGO_BITRIX')
CODIGO_BITRIX_STR = os.getenv('CODIGO_BITRIX_STR')
PROFILE = os.getenv('PROFILE')
BASE_URL_API_BITRIX = os.getenv('BASE_URL_API_BITRIX')

BITRIX_WEBHOOK_URL = f"{BASE_URL_API_BITRIX}/{PROFILE}/{CODIGO_BITRIX}/"

# Listas de cidades para definir qual API chamar
CITIES_API_OURO = [
    "ALVORADA - RS",
    "BARÃO DE COCAIS - MG",
    "BARBACENA - MG",
    "BARROSO - MG",
    "CACHOEIRINHA - RS",
    "BELO HORIZONTE - MG",
    "CAPÃO DA CANOA - RS",
    "CAXAMBU - MG",
    "CHARQUEADAS - RS",
    "DIVINÓPOLIS - MG",
    "ESTEIO - RS",
    "FRANCISCO BELTRÃO - PR",
    "FREDERICO WESTPHALEN - RS",
    "GOVERNADOR VALADARES - MG",
    "GRAVATAÍ - RS",
    "ITAQUI - RS",
    "LAVRAS - MG",
    "MARIANA - MG",
    "NOVO HAMBURGO - RS",
    "NOVO HAMBURGO - SINOS - RS",
    "PATO BRANCO - PR",
    "PONTE NOVA - MG",
    "RIBEIRÃO DAS NEVES - MG",
    "SABARÁ - MG",
    "SANTIAGO - RS",
    "SÃO JERÔNIMO - RS",
    "SÃO LEOPOLDO - RS",
    "SÃO LEOPOLDO - SINOS - RS",
    "SÃO LOURENÇO - MG",
    "SÃO LUIZ GONZAGA - RS",
    "SAPUCAIA DO SUL - RS",
    "URUGUAIANA - RS",
    "VENÂNCIO AIRES - RS",
    "VIÇOSA - MG",
    "XANXERÊ - SC",
    "BAURU - SP",
    "TRES LAGOAS - MS",
    "ARACATUBA - SP",
    "RIO VERDE - GO",
    "UBERLANDIA - MG",
    "JAU - SP",
    "BIRIGUI - SP",
    "GOIANIA - GO",
    "GOIANIRA - GO",
    "PEDERNEIRAS - SP",
    "ANDRADINA - SP",
    "DOIS CORREGOS - SP",
    "TRINDADE - GO",
    "APARECIDA DE GOIANIA - GO",
    "SENADOR CANEDO - GO",
    "ITAPEMA - SC",
    "TIJUCAS - SC",
    "SÃO JOÃO DEL REI - MG"
]

CITIES_API_PADRAO = [
    "ALFREDO VASCONCELOS - MG",
    "ANCHIETA - RS",
    "ANTÔNIO CARLOS - MG",
    "ARROIO DO SAL - RS",
    "BALNEÁRIO PINHAL - RS",
    "BANDEIRANTE - RS",
    "BARRACÃO - RS",
    "BICAS - MG",
    "BOM DESPACHO - MG",
    "BOM SUCESSO - MG",
    "CAMPO ERÊ - SC",
    "CAPELA DE SANTANA - RS",
    "CARAÁ - RS",
    "CARANDAÍ - MG",
    "CARMO DA MATA - MG",
    "CARMÓPOLIS DE MINAS - MG",
    "CIDREIRA - RS",
    "CLÁUDIO - MG",
    "CONCEIÇÃO DA BARRA DE MINAS - MG",
    "CONGONHAS - MG",
    "CONSELHEIRO LAFAIETE - MG",
    "CRUZ ALTA - RS",
    "DESCANSO - SC",
    "DIONÍSIO CERQUEIRA - SC",
    "DORES DE CAMPOS - MG",
    "ENTRE RIOS DE MINAS - MG",
    "FLOR DA SERRA DO SUL - PR",
    "GALVÃO - SC",
    "GLORINHA - RS",
    "GUARACIABA - SC",
    "GUARARÁ - MG",
    "GUARUJÁ DO SUL - SC",
    "IJUÍ - RS",
    "IMBÉ - RS",
    "ITAGUARA - MG",
    "ITATIAIUÇU - MG",
    "ITAÚNA - MG",
    "JECEABA - MG",
    "JUIZ DE FORA - MG",
    "JUPIÁ - SP",
    "LIMA DUARTE - MG",
    "MAQUINÉ - RS",
    "MAR DE ESPANHA - MG",
    "MARATÁ - RS",
    "MARIÓPOLIS - RS",
    "MARMELEIRO - PR",
    "MARTINHO CAMPOS - MG",
    "MATIAS BARBOSA - MG",
    "MONTENEGRO - RS",
    "NOVA SANTA RITA - RS",
    "NOVA SERRANA - MG",
    "NOVO HORIZONTE - RS",
    "OLIVEIRA - MG",
    "OSÓRIO - RS",
    "OURO BRANCO - MG",
    "PALMA SOLA - SC",
    "PANAMBI - RS",
    "PARÁ DE MINAS - MG",
    "PARECI NOVO - RS",
    "PERDÕES - MG",
    "PORTO ALEGRE - RS",
    "PRINCESA - SC",
    "RENASCENÇA - SC",
    "RESSAQUINHA - MG",
    "RIBEIRÃO VERMELHO - MG",
    "SANTA CRUZ DE MINAS - MG",
    "SANTA LUZIA - MG",
    "SANTO ÂNGELO - RS",
    "SANTO ANTÔNIO DA PATRULHA - RS",
    "SANTO ANTÔNIO DO AMPARO - MG",
    "SÃO BRÁS DO SUAÇUÍ - MG",
    "SÃO DOMINGOS - RS",
    "SÃO FRANCISCO DE PAULA - RS",
    "SÃO JOSÉ DO CEDRO - SC",
    "SÃO JOSÉ DO SUL - RS",
    "SÃO LOURENÇO DO OESTE - SC",
    "SÃO MIGUEL DO OESTE - SC",
    "TEÓFILO OTONI - MG",
    "TERRA DE AREIA - RS",
    "TIRADENTES - MG",
    "TORRES - RS",
    "TRAMANDAÍ - RS",
    "TRÊS CACHOEIRAS - RS",
    "TRIUNFO - RS",
    "VIAMÃO - RS",
    "VITORINO - PR",
    "XANGRI-LÁ - RS"

]

CITIES_API_PRATA = [  "BOA ESPERANÇA - MG",
  "BOM PRINCÍPIO - RS",
  "BRASÍLIA - DF",
  "BRUMADINHO - MG",
  "CAETÉ - MG",
  "CAMPO BELO - MG",
  "CANOAS - RS",
  "CARATINGA - MG",
  "CORONEL FABRICIANO - MG",
  "DOIS IRMÃOS - RS",
  "ESTÂNCIA VELHA - RS",
  "FELIZ - RS",
  "IGARAPÉ - MG",
  "IPATINGA - MG",
  "ITABIRITO - MG",
  "IVOTI - RS",
  "JOÃO MONLEVADE - MG",
  "LEOPOLDINA - MG",
  "LINDOLFO COLLOR - RS",
  "LUZIÂNIA - GO",
  "MANHUAÇU - MG",
  "MATOZINHOS - MG",
  "MORRO REUTER - RS",
  "NEPOMUCENO - MG",
  "NOVO GAMA - GO",
  "OURO PRETO - MG",
  "PEDRO LEOPOLDO - MG",
  "PEQUERI - MG",
  "PICADA CAFÉ - RS",
  "PORTÃO - RS",
  "PORTÃO - SINOS - RS",
  "PRESIDENTE LUCENA - RS",
  "SANTA BÁRBARA - MG",
  "SANTA MARIA DO HERVAL - RS",
  "SANTANA DO PARAÍSO - MG",
  "SANTO AUGUSTO - RS",
  "SANTOS DUMONT - MG",
  "SÃO BORJA - RS",
  "SÃO JOAQUIM DE BICAS - MG",
  "SÃO JOSÉ DA LAPA - MG",
  "SÃO JOSÉ DO HORTÊNCIO - RS",
  "SÃO SEBASTIÃO DO CAÍ - RS",
  "SAPIRANGA - RS",
  "TIMÓTEO - MG",
  "VALPARAÍSO DE GOIÁS - GO",
  "VESPASIANO - MG",
  "VISCONDE DO RIO BRANCO - MG",
  "LIMEIRA - SP",
  "CAMPO GRANDE - SP",
  "POA - SP",
  "CALDAS NOVAS - GO",
  "PRESIDENTE PRUDENTE - SP",
  "SAO JOSE DO RIO PRETO - SP",
  "PIRASSUNUNGA - SP",
  "ITAQUAQUECETUBA - SP",
  "SANTA BARBARA D OESTE - SP",
  "LEME - SP",
  "MAIRINQUE - SP",
  "VOTORANTIM - SP",
  "CATALÃO - GO",
  "RIBEIRÃO PIRES - SP",
  "INHUMAS - GO",
  "PINDAMONHANGABA - SP",
  "SAO ROQUE - SP",
  "NOVA ANDRADINA - SP",
  "SAO JOSE DOS CAMPOS - SP",
  "PIRACICABA - SP",
  "PORANGATU - GO",
  "TATUI - SP",
  "LINS - SP",
  "PRESIDENTE EPITÁCIO - SP",
  "BOTUCATU - SP",
  "PALMEIRAS DE GOIÁS - GO",
  "SOROCABA - SP",
  "ACREÚNA - GO",
  "ITU - SP",
  "CRUZEIRO - SP",
  "GOIATUBA - GO",
  "PEREIRA BARRETO - SP",
  "ARUJA - SP",
  "GUAPÓ - GO",
  "BARRA BONITA - SP",
  "MARTINÓPOLIS - SP",
  "FERNANDÓPOLIS - SP",
  "BATAGUASSU - SP",
  "IGARACU DO TIETE - SP",
  "AMERICANA - SP",
  "SANTO ANASTÁCIO - SP",
  "IPAMERI - GO",
  "LORENA - SP",
  "BATAYPORA - SP",
  "PONTALINA - GO",
  "ILHA SOLTEIRA - SP",
  "CASTILHO - SP",
  "MINEIROS DO TIETÊ - SP",
  "PRESIDENTE VENCESLAU - SP",
  "SANTA ISABEL - SP",
  "SAO LUIS DE MONTES BELOS - GO",
  "VALPARAISO - SP",
  "MARA ROSA - GO",
  "SANTA HELENA DE GOIAS - GO",
  "EDEIA - GO",
  "FRANCO DA ROCHA - SP",
  "APARECIDA - SP",
  "CORDEIROPOLIS - SP",
  "JALES - SP",
  "MIRANDÓPOLIS - SP",
  "PRESIDENTE BERNARDES - SP",
  "SANTA FE DO SUL - SP",
  "GUARARAPES - SP",
  "IRACEMÁPOLIS - SP",
  "PROMISSÃO - SP",
  "CACAPAVA - SP",
  "ITAPURA - SP",
  "PIEDADE - SP",
  "NOVA IGUACU DE GOIAS - GO",
  "ANAURILANDIA - MS",
  "BELA VISTA DE GOIAS - GO",
  "CACHOEIRA PAULISTA - SP",
  "FATIMA DO SUL - MS",
  "CAIEIRAS - SP",
  "HIDROLÂNDIA - GO",
  "PARAÚNA - GO",
  "SAO JOAO DA BOA VISTA - SP",
  "POTIM - SP",
  "AGUDOS - SP",
  "CAJAMAR - SP",
  "INDIARA - GO",
  "MACATUBA - SP",
  "ALTO HORIZONTE - GO",
  "PIRACANJUBA - GO",
  "IACANGA - SP",
  "SANTA CRUZ DA CONCEIÇÃO - SP",
  "SAO PAULO - SP",
  "TORRINHA - SP",
  "RUBINEIA - SP",
  "TRES FRONTEIRAS - SP",
  "ABADIA DE GOIAS - GO",
  "IPERO - SP",
  "NOVA INDEPENDENCIA - SP",
  "PIRATININGA - SP",
  "BURITI ALEGRE - GO",
  "FIRMINÓPOLIS - GO",
  "ITAPEVI - SP",
  "RIO GRANDE DA SERRA - SP",
  "SANTA MARIA DA SERRA - SP",
  "URÂNIA - SP",
  "GUAICARA - SP",
  "GUARACAI - SP",
  "JARINU - SP",
  "BROTAS - SP",
  "MURUTINGA DO SUL - SP",
  "PETROLINA DE GOIAS - GO",
  "CARAPICUÍBA - SP",
  "PIQUEROBI - SP",
  "ALFREDO MARCONDES - SP",
  "AMARALINA - GO",
  "AVANHANDAVA - SP",
  "CANAS - SP",
  "PORTO FERREIRA - SP",
  "RIBEIRÃO DOS ÍNDIOS - SP",
  "VICENTINA - SP",
  "CAIÚA - SP",
  "EMILIANÓPOLIS - SP",
  "IBIÚNA - SP",
  "PIRAJUÍ - SP",
  "RUBIÁCEA - SP",
  "SANTANA DA PONTE PENSA - SP",
  "CROMÍNIA - GO",
  "FRANCISCO MORATO - SP",
  "ITÁUCU - GO",
  "LAVÍNIA - SP",
  "LAVRINHAS - SP",
  "PIRAPORA DO BOM JESUS - SP",
  "SANTA SALETE - SP",
  "SANTA TEREZA DE GOIAS - GO",
  "SAO JOAO DA PARAUNA - GO",
  "TANABI - SP",
  "VARGEM GRANDE PAULISTA - SP",
  "BARUERI - SP",
  "CACHOEIRA ALTA - GO",
  "CEZARINA - GO",
  "FERRAZ DE VASCONCELOS - SP",
  "JANDAIA - GO",
  "JUNDIAI - SP",
  "NOVA ODESSA - SP",
  "RIO QUENTE - GO",
  "SANTO EXPEDITO - SP",
  "TURVELÂNDIA - GO",
  "BENTO DE ABREU - SP",
  "EDEALINA - GO",
  "MARZAGÃO - GO",
  "SANTANA DE PARNAÍBA - SP",
  "ARARAS - SP",
  "URUAÇU - GO",
  "COTIA - SP",
  "SUZANO - SP",
  "OSASCO - SP",
  "CAMPINORTE - GO",
  "JANDIRA - SP",
  "ÁGUAS MORNAS - SC",
  "ANGELINA - SC",
  "CANELINHA - SC",
  "NOVA TRENTO - SC",
  "PORTO BELO - SC",
  "ANTÔNIO CARLOS - SC",
  "RANCHO QUEIMADO - SC",
  "SÃO JOÃO BATISTA - SC",
  "BIGUÁÇU - SC",
  "FLORIANÓPOLIS - SC",
  "GOVERNADOR CELSO RAMOS - SC",
  "MAJOR GERCINO - SC",
  "PALHOÇA - SC",
  "SANTO AMARO DA IMPERATRIZ - SC",
  "SÃO JOSÉ - SC",
  "SÃO PEDRO DE ALCÂNTARA - SC",
  "DOURADOS - MS"
]

CITIES_API_REDE_NEUTRA = [
    "APARECIDA DE GOIANIA - GO",
    "BELO HORIZONTE - MG",
    "CONTAGEM - MG",
    "GOIANIA - MG",
    "SENADOR CANEDO - GO",
    "SETE LAGOAS - MG",
    "TRINDADE - GO",
    "UBÁ - MG",
    "RIBEIRÃO DAS NEVES - MG"
]

# Função para obter a URL da API com base na cidade
def get_api_url(cidade):
    if cidade in CITIES_API_OURO:
        return "https://falasolucoes-workflow-solucoes.ywsa8i.easypanel.host/webhook/workflowouro"
    elif cidade in CITIES_API_PADRAO:
        return "https://falasolucoes-workflow-solucoes.ywsa8i.easypanel.host/webhook/workflowpadrao"
    elif cidade in CITIES_API_REDE_NEUTRA:
        return "https://falasolucoes-workflow-solucoes.ywsa8i.easypanel.host/webhook/workflowredeneutra"
    elif cidade in CITIES_API_PRATA:
        return "https://falasolucoes-workflow-solucoes.ywsa8i.easypanel.host/webhook/workflowprata"
    else:
        return None  # Cidade não mapeada

# Função para atualizar o campo no CRM
def atualizar_campo_no_crm(dados):
    # Aqui você coloca a lógica para atualizar o campo no CRM
    pass

# Função principal para atualizar o campo e chamar a API
def atualizar_campo_e_chamar_api(cidade, entity_id):
    # Atualiza o campo no CRM
    atualizar_campo_no_crm(entity_id)
    
    # Obtém a URL da API para a cidade
    url_api = get_api_url(cidade)
    
    if url_api:
        # Chama a API correspondente à cidade
        response = requests.post(f"{url_api}?deal_id={entity_id}", json={"cidade": cidade})
        return response
    else:
        return "Cidade não mapeada."

# Ajuste na chamada da função
@app.route('/update-plan/<string:entity_id>', methods=['POST'])
def update_plan(entity_id):
    try:
        # URL para buscar os dados da negociação
        get_deal_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.get"
        get_deal_response = requests.get(get_deal_url, params={"id": entity_id})
        get_deal_data = get_deal_response.json()

        if 'result' not in get_deal_data:
            return jsonify({"error":"Falha ao buscar os dados da negociação", "details": get_deal_data}), 400
        
        field_id = get_deal_data['result'].get("UF_CRM_1709042046")
        if not field_id:
            return jsonify({"error": "Campo Cidade List está vazio"}), 400
        
        get_fields_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.fields"
        get_fields_response = requests.get(get_fields_url)
        get_fields_data = get_fields_response.json()

        if 'result' not in get_fields_data: 
            return jsonify({"error": "Falha ao buscar os campos disponíveis", "details": get_fields_data}), 400
        
        fields_items = get_fields_data['result'].get("UF_CRM_1709042046", {}).get("items", [])
        if not fields_items:
            return jsonify({"error": " O campo Cidade está Vazio"}), 400
        
        matched_item = next((item for item in fields_items if item["ID"] == field_id), None)
        if not matched_item: 
            return jsonify({"error": f"ID {field_id} não encontrado na lista de itens do campo"}), 400
        
        value_to_update = matched_item["VALUE"]

        # Atualiza o campo no CRM
        update_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.update"
        update_response = requests.post(update_url, json={
            "id": entity_id,
            "fields": {
                "UF_CRM_1733493949": value_to_update
            }
        })
        
        update_data = update_response.json()

        if update_data.get("result") == True:
            # Agora a função recebe o entity_id
            api_response = atualizar_campo_e_chamar_api(value_to_update, entity_id)
            return jsonify({"message": "Campo atualizado com sucesso!", "value": value_to_update, "api_response": api_response}), 200
        else:
            return jsonify({"error": "Falha ao atualizar o campo", "details": update_data}), 400

    except Exception as e:
        return jsonify({"error": "Erro interno", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5711)
