from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os
import time

app = Flask(__name__)

load_dotenv()

BITRIX_WEBHOOK_URL = os.getenv("BITRIX_WEBHOOK_URL")
URL_VPS = os.getenv("URL_VPS")

BITRIX_WEBHOOK_URL = f"{BITRIX_WEBHOOK_URL}"


def log_erro(mensagem, e=None):
    """Função de log de erro para registrar exceções"""
    import traceback

    erro_detalhado = traceback.format_exc()
    print(f"\n[ERRO] {mensagem}")
    if e:
        print(f"[DETALHES] {str(e)}")
    print(f"[TRACEBACK] {erro_detalhado}\n")


# CIDADES DA OPERADORA VERO - INTERNET
CITIES_API_VERO_OURO = [
    "ALVORADA - RS",
    "ANDRADINA - SP",
    "ARACATUBA - SP",
    "BARÃO DE COCAIS - MG",
    "BARBACENA - MG",
    "BARROSO - MG",
    "BAURU - SP",
    "BIRIGUI - SP",
    "CACHOEIRINHA - RS",
    "CAPÃO DA CANOA - RS",
    "CAXAMBU - MG",
    "CHARQUEADAS - RS",
    "CRISTIANO OTONI - MG",
    "DIVINÓPOLIS - MG",
    "ESTEIO - RS",
    "FRANCISCO BELTRÃO - PR",
    "FREDERICO WESTPHALEN - RS",
    "GOIANIRA - GO",
    "GOVERNADOR VALADARES - MG",
    "GRAVATAÍ - RS",
    "ITAPEMA - SC",
    "ITAQUI - RS",
    "LAVRAS - MG",
    "MARIANA - MG",
    "NOVO HAMBURGO - RS",
    "PATO BRANCO - PR",
    "PEDERNEIRAS - SP",
    "PONTE NOVA - MG",
    "RIO VERDE - GO",
    "SABARÁ - MG",
    "SANTIAGO - RS",
    "SÃO JERÔNIMO - RS",
    "SÃO JOÃO DEL REI - MG",
    "SÃO LEOPOLDO - RS",
    "SÃO LOURENÇO - MG",
    "SÃO LUIZ GONZAGA - RS",
    "SAPUCAIA DO SUL - RS",
    "TIJUCAS - SC",
    "TRES LAGOAS - MS",
    "UBERLANDIA - MG",
    "URUGUAIANA - RS",
    "VENÂNCIO AIRES - RS",
    "VIÇOSA - MG",
    "XANXERÊ - SC"
]

CITIES_API_VERO_PADRAO = [
    "ARROIO DO SAL - RS",
    "CONSELHEIRO LAFAIETE - MG",
    "IMBÉ - RS",
    "LIMA DUARTE - MG",
    "MATIAS BARBOSA - MG",
    "PARÁ DE MINAS - MG",
    "SÃO JOSÉ DO CEDRO - SC",
    "SÃO MIGUEL DO OESTE - SC",
    "TEÓFILO OTONI - MG",
    "TRAMANDAÍ - RS",
    "ALFREDO VASCONCELOS - MG",
    "ANCHIETA - SC",
    "ANTÔNIO CARLOS - MG",
    "BALNEÁRIO PINHAL - RS",
    "BANDEIRANTE - SC",
    "BARRACÃO - PR",
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
    "ITAGUARA - MG",
    "ITATIAIUÇU - MG",
    "ITAÚNA - MG",
    "JECEABA - MG",
    "JUIZ DE FORA - MG",
    "JUPIÁ - SC",
    "MAQUINÉ - RS",
    "MAR DE ESPANHA - MG",
    "MARATÁ - RS",
    "MARIÓPOLIS - PR",
    "MARMELEIRO - PR",
    "MARTINHO CAMPOS - MG",
    "MONTENEGRO - RS",
    "NOVA SANTA RITA - RS",
    "NOVA SERRANA - MG",
    "NOVO HORIZONTE - SC",
    "OLIVEIRA - MG",
    "OSÓRIO - RS",
    "OURO BRANCO - MG",
    "PALMA SOLA - SC",
    "PANAMBI - RS",
    "PARECI NOVO - RS",
    "PERDÕES - MG",
    "PORTO ALEGRE - RS",
    "PRINCESA - SC",
    "RENASCENÇA - PR",
    "RESSAQUINHA - MG",
    "RIBEIRÃO VERMELHO - MG",
    "SANTA CRUZ DE MINAS - MG",
    "SANTA LUZIA - MG",
    "SANTO ÂNGELO - RS",
    "SANTO ANTÔNIO DA PATRULHA - RS",
    "SANTO ANTÔNIO DO AMPARO - MG",
    "SÃO BRÁS DO SUAÇUÍ - MG",
    "SÃO DOMINGOS - SC",
    "SÃO FRANCISCO DE PAULA - MG",
    "SÃO JOSÉ DO SUL - RS",
    "SÃO LOURENÇO DO OESTE - SC",
    "TERRA DE AREIA - RS",
    "TIRADENTES - MG",
    "TORRES - RS",
    "TRÊS CACHOEIRAS - RS",
    "TRIUNFO - RS",
    "VIAMÃO - RS",
    "VITORINO - PR",
    "XANGRI-LA - RS"
]

CITIES_API_VERO_PRATA = [
    "AGUDOS - SP",
    "ALFREDO MARCONDES - SP",
    "AMERICANA - SP",
    "APARECIDA - SP",
    "ARARAS - SP",
    "ARUJA - SP",
    "AVANHANDAVA - SP",
    "BARRA BONITA - SP",
    "BENTO DE ABREU - SP",
    "BOTUCATU - SP",
    "BROTAS - SP",
    "CACAPAVA - SP",
    "CACHOEIRA PAULISTA - SP",
    "CAIEIRAS - SP",
    "CAIUA - SP",
    "CAJAMAR - SP",
    "CALDAS NOVAS - GO",
    "CANAS - SP",
    "CARAPICUIBA - SP",
    "CARATINGA - MG",
    "CASTILHO - SP",
    "CORDEIROPOLIS - SP",
    "CORONEL FABRICIANO - MG",
    "CRUZEIRO - SP",
    "DOIS IRMÃOS - RS",
    "EMILIANOPOLIS - SP",
    "FERNANDOPOLIS - SP",
    "FRANCISCO MORATO - SP",
    "FRANCO DA ROCHA - SP",
    "GOIATUBA - GO",
    "GOVERNADOR CELSO RAMOS - SC",
    "GUAICARA - SP",
    "GUARACAI - SP",
    "GUARARAPES - SP",
    "IACANGA - SP",
    "IGARACU DO TIETE - SP",
    "ILHA SOLTEIRA - SP",
    "INHUMAS - GO",
    "IPATINGA - MG",
    "IRACEMAPOLIS - SP",
    "ITAPEVI - SP",
    "ITAPURA - SP",
    "ITAQUAQUECETUBA - SP",
    "ITU - SP",
    "JALES - SP",
    "JANDIRA - SP",
    "JARINU - SP",
    "LAVINIA - SP",
    "LAVRINHAS - SP",
    "LEME - SP",
    "LIMEIRA - SP",
    "LINS - SP",
    "LORENA - SP",
    "MACATUBA - SP",
    "MAIRINQUE - SP",
    "MARTINOPOLIS - SP",
    "MIRANDOPOLIS - SP",
    "MURUTINGA DO SUL - SP",
    "NOVA INDEPENDENCIA - SP",
    "NOVA ODESSA - SP",
    "PEREIRA BARRETO - SP",
    "PIEDADE - SP",
    "PINDAMONHANGABA - SP",
    "PIQUEROBI - SP",
    "PIRACICABA - SP",
    "PIRAJUI - SP",
    "PIRAPORA DO BOM JESUS - SP",
    "PIRASSUNUNGA - SP",
    "PIRATININGA - SP",
    "POA - SP",
    "PORTO FERREIRA - SP",
    "POTIM - SP",
    "PRESIDENTE BERNARDES - SP",
    "PRESIDENTE EPITACIO - SP",
    "PRESIDENTE PRUDENTE - SP",
    "PRESIDENTE VENCESLAU - SP",
    "PROMISSAO - SP",
    "RIBEIRAO DOS INDIOS - SP",
    "RIBEIRAO PIRES - SP",
    "RUBIACEA - SP",
    "RUBINEIA - SP",
    "SANTA CRUZ DA CONCEICAO - SP",
    "SANTA FE DO SUL - SP",
    "SANTA HELENA DE GOIAS - GO",
    "SANTA ISABEL - SP",
    "SANTA MARIA DA SERRA - SP",
    "SANTA SALETE - SP",
    "SANTANA DA PONTE PENSA - SP",
    "SANTANA DE PARNAIBA - SP",
    "SANTANA DO PARAÍSO - MG",
    "SANTO ANASTACIO - SP",
    "SANTO EXPEDITO - SP",
    "SAO JOAO DA BOA VISTA - SP",
    "SAO JOSE DO RIO PRETO - SP",
    "SAO JOSE DOS CAMPOS - SP",
    "SAO ROQUE - SP",
    "SOROCABA - SP",
    "TANABI - SP",
    "TATUI - SP",
    "TIMÓTEO - MG",
    "TORRINHA - SP",
    "TRES FRONTEIRAS - SP",
    "URANIA - SP",
    "VALPARAISO - SP",
    "VARGEM GRANDE PAULISTA - SP",
    "VOTORANTIM - SP",
    "ABADIA DE GOIAS - GO",
    "ACREUNA - GO",
    "ÁGUAS MORNAS - SC",
    "ALTO HORIZONTE - GO",
    "AMARALINA - GO",
    "ANAURILANDIA - MS",
    "ANGELINA - SC",
    "ANTÔNIO CARLOS - SC - SC",
    "BARUERI - SP",
    "BATAGUASSU - MS",
    "BATAYPORA - MS",
    "BELA VISTA DE GOIAS - GO",
    "BIGUAÇU - SC",
    "BOA ESPERANÇA - MG",
    "BOM PRINCÍPIO - RS",
    "BRASÍLIA - DF",
    "BRUMADINHO - MG",
    "BURITI ALEGRE - GO",
    "CACHOEIRA ALTA - GO",
    "CAETÉ - MG",
    "CAMPINORTE - GO",
    "CAMPO BELO - MG",
    "CAMPO GRANDE - MS",
    "CANELINHA - SC",
    "CANOAS - RS",
    "CATALAO - GO",
    "CEZARINA - GO",
    "COTIA - SP",
    "CROMINIA - GO",
    "DOURADOS - MS",
    "EDEALINA - GO",
    "EDEIA - GO",
    "ESTÂNCIA VELHA - RS",
    "FATIMA DO SUL - MS",
    "FELIZ - RS",
    "FERRAZ DE VASCONCELOS - SP",
    "FIRMINOPOLIS - GO",
    "FLORIANÓPOLIS - SC",
    "GUAPO - GO",
    "HIDROLANDIA - GO",
    "IBIUNA - SP",
    "IGARAPÉ - MG",
    "INDIARA - GO",
    "IPAMERI - GO",
    "IPERO - SP",
    "ITABIRITO - MG",
    "ITAUCU - GO",
    "IVOTI - RS",
    "JANDAIA - GO",
    "JOÃO MONLEVADE - MG",
    "JUNDIAI - SP",
    "LEOPOLDINA - MG",
    "LINDOLFO COLLOR - RS",
    "LUZIÂNIA - GO",
    "MAJOR GERCINO - SC",
    "MANHUAÇU - MG",
    "MARA ROSA - GO",
    "MARZAGAO - GO",
    "MATOZINHOS - MG",
    "MORRO REUTER - RS",
    "NEPOMUCENO - MG",
    "NOVA ANDRADINA - MS",
    "NOVA IGUACU DE GOIAS - GO",
    "NOVA TRENTO - SC",
    "NOVO GAMA - GO",
    "OSASCO - SP",
    "OURO PRETO - MG",
    "PALHOÇA - SC",
    "PALMEIRAS DE GOIAS - GO",
    "PARAUNA - GO",
    "PEDRO LEOPOLDO - MG",
    "PEQUERI - MG",
    "PETROLINA DE GOIAS - GO",
    "PICADA CAFÉ - RS",
    "PIRACANJUBA - GO",
    "PONTALINA - GO",
    "PORANGATU - GO",
    "PORTÃO - RS",
    "PORTO BELO - SC",
    "PRESIDENTE LUCENA - RS",
    "RANCHO QUEIMADO - SC",
    "RIO GRANDE DA SERRA - SP",
    "RIO QUENTE - GO",
    "SANTA BÁRBARA - MG",
    "SANTA BARBARA D OESTE - SP",
    "SANTA MARIA DO HERVAL - RS",
    "SANTA TEREZA DE GOIAS - GO",
    "SANTO AMARO DA IMPERATRIZ - SC",
    "SANTO AUGUSTO - RS",
    "SANTOS DUMONT - MG",
    "SÃO BORJA - RS",
    "SÃO JOÃO BATISTA - SC",
    "SAO JOAO DA PARAUNA - GO",
    "SÃO JOAQUIM DE BICAS - MG",
    "SÃO JOSÉ - SC",
    "SÃO JOSÉ DA LAPA - MG",
    "SÃO JOSÉ DO HORTÊNCIO - RS",
    "SAO LUIS DE MONTES BELOS - GO",
    "SAO PAULO - SP",
    "SÃO PEDRO DE ALCÂNTARA - SC",
    "SÃO SEBASTIÃO DO CAÍ - RS",
    "SAPIRANGA - RS",
    "SUZANO - SP",
    "TURVELANDIA - GO",
    "URUAÇU - GO",
    "VALPARAÍSO DE GOIAS - GO",
    "VESPASIANO - MG",
    "VICENTINA - MS",
    "VISCONDE DO RIO BRANCO - MG",
    ]

CITIES_API_VERO_REDE_NEUTRA = [
    "APARECIDA DE GOIANIA - GO",
    "BELO HORIZONTE - MG",
    "CONTAGEM - MG",
    "GOIANIA - GO",
    "RIBEIRÃO DAS NEVES - MG",
    "SENADOR CANEDO - GO",
    "SETE LAGOAS - MG",
    "TRINDADE - GO",
    "UBÁ - MG",
]

CITIES_API_VERO_SAFIRA = [
    "BARBACENA - MG",
    "BAURU - SP",
    "DIVINÓPOLIS - MG",
    "PEDERNEIRAS - SP",
    "SABARÁ - MG",
    "TRES LAGOAS - MS",
    "UBERLANDIA - MG",
    "AGUDOS - SP",
    "BARUERI - SP",
    "CORDEIROPOLIS - SP",
    "COTIA - SP",
    "FERRAZ DE VASCONCELOS - SP",
    "IBIUNA - SP",
    "IPATINGA - MG",
    "IPERO - SP",
    "IRACEMAPOLIS - SP",
    "ITAQUAQUECETUBA - SP",
    "JUNDIAI - SP",
    "LIMEIRA - SP",
    "MANHUAÇU - MG",
    "OSASCO - SP",
    "PIRATININGA - SP",
    "PRESIDENTE PRUDENTE - SP",
    "RIO GRANDE DA SERRA - SP",
    "SANTA BARBARA D OESTE - SP",
    "SAO JOSE DOS CAMPOS - SP",
    "SAO PAULO - SP",
    "SUZANO - SP",
    "VALPARAÍSO DE GOIAS - GO",
    "JUIZ DE FORA - MG",
    "MAQUINÉ - RS",
    "TRAMANDAÍ - RS",
]

CITIES_API_VERO_GRAFENO_75 = [
    "AGUDOS - SP",
    "AMERICANA - SP",
    "CALDAS NOVAS - GO",
    "CORONEL FABRICIANO - MG",
    "DOIS IRMÃOS - RS",
    "GOIATUBA - GO",
    "GOVERNADOR CELSO RAMOS - SC",
    "GUARARAPES - SP",
    "INHUMAS - GO",
    "IPATINGA - MG",
    "LEME - SP",
    "LIMEIRA - SP",
    "PIEDADE - SP",
    "PIRASSUNUNGA - SP",
    "PRESIDENTE PRUDENTE - SP",
    "SANTA HELENA DE GOIAS - GO",
    "SAO JOSE DOS CAMPOS - SP",
    "SOROCABA - SP",
    "TATUI - SP",
    "TIMÓTEO - MG",
    "VOTORANTIM - SP",
    "ANDRADINA - SP",
    "ARROIO DO SAL - RS",
    "IMBÉ - RS",
    "LIMA DUARTE - MG",
    "MATIAS BARBOSA - MG",
    "PARÁ DE MINAS - MG",
    "SÃO JOSÉ DO CEDRO - SC",
    "SÃO MIGUEL DO OESTE - SC",
    "TRAMANDAÍ - RS",
    "BIRIGUI - SP",
    "FRANCISCO BELTRÃO - PR",
    "TRES LAGOAS - MS",
]

CITIES_API_VERO_GRAFENO_80 = [
    "ALFREDO MARCONDES - SP",
    "APARECIDA - SP",
    "ARARAS - SP",
    "ARUJA - SP",
    "AVANHANDAVA - SP",
    "BARRA BONITA - SP",
    "BENTO DE ABREU - SP",
    "BOTUCATU - SP",
    "BROTAS - SP",
    "CACAPAVA - SP",
    "CACHOEIRA PAULISTA - SP",
    "CAIEIRAS - SP",
    "CAIUA - SP",
    "CAJAMAR - SP",
    "CANAS - SP",
    "CARAPICUIBA - SP",
    "CARATINGA - MG",
    "CASTILHO - SP",
    "CORDEIROPOLIS - SP",
    "CRUZEIRO - SP",
    "EMILIANOPOLIS - SP",
    "FERNANDOPOLIS - SP",
    "FRANCISCO MORATO - SP",
    "FRANCO DA ROCHA - SP",
    "GUAICARA - SP",
    "GUARACAI - SP",
    "IACANGA - SP",
    "IGARACU DO TIETE - SP",
    "ILHA SOLTEIRA - SP",
    "IRACEMAPOLIS - SP",
    "ITAPEVI - SP",
    "ITAPURA - SP",
    "ITAQUAQUECETUBA - SP",
    "ITU - SP",
    "JALES - SP",
    "JANDIRA - SP",
    "JARINU - SP",
    "LAVINIA - SP",
    "LAVRINHAS - SP",
    "LINS - SP",
    "LORENA - SP",
    "MACATUBA - SP",
    "MAIRINQUE - SP",
    "MARTINOPOLIS - SP",
    "MIRANDOPOLIS - SP",
    "MURUTINGA DO SUL - SP",
    "NOVA INDEPENDENCIA - SP",
    "NOVA ODESSA - SP",
    "PEREIRA BARRETO - SP",
    "PINDAMONHANGABA - SP",
    "PIQUEROBI - SP",
    "PIRACICABA - SP",
    "PIRAJUI - SP",
    "PIRAPORA DO BOM JESUS - SP",
    "PIRATININGA - SP",
    "POA - SP",
    "PORTO FERREIRA - SP",
    "POTIM - SP",
    "PRESIDENTE BERNARDES - SP",
    "PRESIDENTE EPITACIO - SP",
    "PRESIDENTE VENCESLAU - SP",
    "PROMISSAO - SP",
    "RIBEIRAO DOS INDIOS - SP",
    "RIBEIRAO PIRES - SP",
    "RUBIACEA - SP",
    "RUBINEIA - SP",
    "SANTA CRUZ DA CONCEICAO - SP",
    "SANTA FE DO SUL - SP",
    "SANTA ISABEL - SP",
    "SANTA MARIA DA SERRA - SP",
    "SANTA SALETE - SP",
    "SANTANA DA PONTE PENSA - SP",
    "SANTANA DE PARNAIBA - SP",
    "SANTANA DO PARAÍSO - MG",
    "SANTO ANASTACIO - SP",
    "SANTO EXPEDITO - SP",
    "SAO JOAO DA BOA VISTA - SP",
    "SAO JOSE DO RIO PRETO - SP",
    "SAO ROQUE - SP",
    "TANABI - SP",
    "TORRINHA - SP",
    "TRES FRONTEIRAS - SP",
    "URANIA - SP",
    "VALPARAISO - SP",
    "VARGEM GRANDE PAULISTA - SP",
    "ARACATUBA - SP",
    "CONSELHEIRO LAFAIETE - MG",
    "TEÓFILO OTONI - MG",
    "BARBACENA - MG",
    "BAURU - SP",
    "DIVINÓPOLIS - MG",
    "GOVERNADOR VALADARES - MG",
    "PEDERNEIRAS - SP",
]


# CIDADES DA OPERADORA GIGA+ - INTERNET

CITIES_API_GIGA_TERRITORIO_T1_a_T9 = [
    "CAMARGO - PR",
    "ENGENHEIRO BELTRÃO - PR",
    "JANDAIA DO SUL - PR",
    "JUSSARA - PR",
    "MANDAGUARI - PR",
    "MARIALVA - PR",
    "MARINGÁ - PR",
    "PAIÇANDU - PR",
    "PEABIRU - PR",
    "ROLÂNDIA - PR",
    "TELÊMACO BORBA - PR",
    "UBIRATÃ - PR",
    "CAMPO GRANDE - MS",
    "DOURADOS - MS",
    "DIADEMA - SP",
    "FERRAZ DE VASCONCELOS - SP",
    "GUARULHOS - SP",
    "ITAQUAQUECETUBA - SP",
    "MAUÁ - SP",
    "MOGI DAS CRUZES - SP",
    "POÁ - SP",
    "RIBEIRÃO PIRES - SP",
    "RIO GRANDE DA SERRA - SP",
    "SANTO ANDRÉ - SP",
    "SÃO BERNARDO DO CAMPO - SP",
    "SÃO PAULO - SP",
    "SUZANO - SP",
    "BERTIOGA - SP",
    "CAÇAPAVA - SP",
    "CARAGUATATUBA - SP",
    "CUBATÃO - SP",
    "GUARUJÁ - SP",
    "ILHABELA - SP",
    "ITANHAÉM - SP",
    "JACAREÍ - SP",
    "MONGAGUÁ - SP",
    "PERUÍBE - SP",
    "PRAIA GRANDE - SP",
    "SANTOS - SP",
    "SÃO JOSÉ DOS CAMPOS - SP",
    "SÃO SEBASTIÃO - SP",
    "SÃO VICENTE - SP",
    "TAUBATÉ - SP",
    "TREMEMBÉ - SP",
    "UBATUBA - SP",
    "ARARUAMA - RJ",
    "ARMAÇÃO DOS BÚZIOS - RJ",
    "ARRAIAL DO CABO - RJ",
    "CABO FRIO - RJ",
    "CASIMIRO DE ABREU - RJ",
    "IGUABA GRANDE - RJ",
    "MACAÉ - RJ",
    "RIO DAS OSTRAS - RJ",
    "SÃO PEDRO DA ALDEIRA - RJ",
    "SAQUAREMA - RJ",
    "ALÉM PARAÍBA - RJ",
    "BARRA DO PIRAÍ - RJ",
    "BARRA MANSA - RJ",
    "BOM JARDIM - RJ",
    "CACHOEIRAS DE MACACU - RJ",
    "CARMO - RJ",
    "COMENDADOR LEVY GASPARIAN - RJ",
    "GUAPIMIRIM - RJ",
    "ITAIPAVA - RJ",
    "ITATIAIA - RJ",
    "MAGÉ - RJ",
    "MIGUEL PEREIRA - RJ",
    "NOVA FRIBURGO - RJ",
    "PARAÍBA DO SUL - RJ",
    "PATY DO ALFERES - RJ",
    "PETRÓPOLIS - RJ",
    "PINHEIRAL - RJ",
    "PORTO REAL - RJ",
    "RESENDE - RJ",
    "SAPUCAIA - RJ",
    "SILVA JARDIM - RJ",
    "SUMIDOURO - RJ",
    "TERESÓPOLIS - RJ",
    "TRÊS RIOS - RJ",
    "VALENÇA - RJ",
    "VASSOURAS - RJ",
    "VOLTA REDONDA - RJ",
    "ANCHIETA - ES",
    "APERIBÉ - ES",
    "CACHOEIRO DE ITAPEMIRIM - RJ",
    "CAMBUCI - RJ",
    "CAMPOS DOS GOYTACAZES - RJ",
    "CANTAGALO - RJ",
    "CARIACICA - ES",
    "CATAGUASES - MG",
    "CORDEIRO - RJ",
    "DUAS BARRAS - RJ",
    "GUARAPARI - ES",
    "ITAOCARA - RJ",
    "ITAPEMIRIM - ES",
    "ITAPERUNA - RJ",
    "LAJE DO MURIAÉ - RJ",
    "MACUCO - RJ",
    "MARATAÍZES - ES",
    "MIRACEMA - RJ",
    "MURIAÉ - MG",
    "PIÚMA - ES",
    "SANTO ANTÔNIO DE PÁDUA - RJ",
    "SÃO FIDÉLIS - RJ",
    "SÃO JOSÉ DE UBÁ - RJ",
    "SERRA - ES",
    "VILA VELHA - ES",
    "VITÓRIA - ES",
    "AGUANIL - MG",
    "ALPINÓPOLIS - MG",
    "ARAXÁ - MG",
    "BOA ESPERANÇA - MG",
    "CAMPO DO MEIO - MG",
    "CAMPOS ALTOS - MG",
    "CAMPOS GERAIS - MG",
    "CARMO DO RIO CLARO - MG",
    "CONQUISTA - MG",
    "COQUEIRAL - MG",
    "COROMANDEL - MG",
    "CRISTAIS - MG",
    "DELTA - MG",
    "FORTALEZA DE MINAS - MG",
    "GUAPÉ - MG",
    "GUARANÉSIA - MG",
    "GUAXUPÉ - MG",
    "IBIÁ - MG",
    "ILICÍNEA - MG",
    "JACUÍ - MG",
    "MONTE SANTO DE MINAS - MG",
    "NEPOMUCENO - MG",
    "NOVA PONTE - MG",
    "PASSOS - MG",
    "PEDRINÓPOLIS - MG",
    "PERDIZES - MG",
    "PRATÁPOLIS - MG",
    "PRATINHA - MG",
    "SACRAMENTO - MG",
    "SANTA JULIANA - MG",
    "SANTANA DA VARGEM - MG",
    "SÃO GOTARDO - MG",
    "SÃO JOSÉ DA BARRA - MG",
    "SÃO SEBASTIÃO DO PARAÍSO - MG",
    "SÃO TOMÁS DE AQUINO - MG",
    "SERRA DO SALITRE - MG",
    "TAPIRA - MG",
    "UBERABA - MG",
    "UBERLÂNDIA - MG",
    "ALTINÓPOLIS - SP",
    "ARAMINA - SP",
    "BRASILIA - DF",
    "FRANCA - SP",
    "GUARÁ - SP",
    "IGARAPAVA - SP",
    "IPUÃ - SP",
    "ITIRAPUÃ - SP",
    "ITUVERAVA - SP",
    "MORRO AGUDO - SP",
    "ORLÂNDIA - SP",
    "PATROCÍNIO PAULISTA - SP",
    "RIBEIRÃO PRETO - SP",
    "SÃO JOAQUIM DA BARRA - SP",
    "SÃO JOSÉ DA BELA VISTA - SP",
]


CITIES_API_GIGA_TERRITORIO_T10_a_T14 = [
    "CARNAÍBA - PE",
    "CARPINA - PE",
    "CARUARU - PE",
    "FLORES - PE",
    "GOIANÁ - PE",
    "ILHA DE ITAMARACÁ - PE",
    "IPOJUCA - PE",
    "ITAPISSUMA - PE",
    "LIMOEIRO - PE",
    "MIRANDIBA - PE",
    "NAZARÉ DA MATA - PE",
    "OLINDA - PE",
    "PARNAMIRIM - PE",
    "PAUDALHO - PE",
    "PAULISTA - PE",
    "SALGUEIRO - PE",
    "SANTA CRUZ DO CAPIBARIBE - PE",
    "SERRA TALHADA - PE",
    "SURUBIM - PE",
    "TERRA NOVA - PE",
    "TIMBAÚBA - PE",
    "TORITAMA - PE",
    "VERDEJANTE - PE",
    "ARACAJU - SE",
    "BARRA DOS COQUEIROS - SE",
    "CEDRO DE SÃO JOÃO - SE",
    "DIVINA PASTORA - SE",
    "ITAPORANGA D´AJUDA - SE",
    "JAPOATÃ - SE",
    "LAGARTO - SE",
    "LARANJEIRAS - SE",
    "NOSSA SENHORA DO SOCORRO - SE",
    "PACATUBA - SE",
    "PROPRIÁ - SE",
    "ROSÁRIO DO CATETE - SE",
    "SÃO CRISTÓVÃO - SE",
    "SIRIRI - SE",
    "TELHA - SE",
    "ACOPIARA - CE",
    "AIUABA - CE",
    "ANTONINA DO NORTE - CE",
    "ARARIPE - CE",
    "ARNEIROZ - CE",
    "ASSARÉ - CE",
    "BARBALHA - CE",
    "BREJO SANTO - CE",
    "CAMPOS SALES - CE",
    "CARIÚS - CE",
    "CATARINA - CE",
    "CEDRO - CE",
    "CRATEÚS - CE",
    "CRATO - CE",
    "FARIAS BRITO - CE",
    "ICÓ - CE",
    "IGUATU - CE",
    "INDEPENDÊNCIA - CE",
    "JATI - CE",
    "JUAZEIRO DO NORTE - CE",
    "JUCÁS - CE",
    "LAVRAS DA MANGABEIRA - CE",
    "MAURITI - CE",
    "MISSÃO - CE",
    "VELHA - CE",
    "MOMBAÇA - CE",
    "ORÓS - CE",
    "PARAMBU - CE",
    "PIQUET CARNEIRO - CE",
    "PORTEIRAS - CE",
    "QUIXELÔ - CE",
    "SALITRE - CE",
    "TARRAFAS - CE",
    "TAUÁ - CE",
    "VÁRZEA ALEGRE - CE",
    "CAXIAS - MA",
    "PARAUAPEBAS - PA",
    "TIMON - MA",
    "CAUCAIA - CE",
    "FORTALEZA - CE",
    "MARACANAÚ - CE",
    "ACARAÚ - CE",
    "AQUIRAZ - CE",
    "BEBERIBE - CE",
    "CAMOCIM - CE",
    "CASCAVEL - CE",
    "CRUZ - CE",
    "EUSÉBIO - CE",
    "FORTIM - CE",
    "FRECHEIRINHA - CE",
    "GRAÇA - CE",
    "GRANJA - CE",
    "IBIAPINA - CE",
    "ITAITINGA - CE",
    "ITAPIPOCA - CE",
    "ITAREMA - CE",
    "JIJOCA DE JERICOACOARA - CE",
    "LIMOEIRO DO NORTE - CE",
    "MARANGUAPE - CE",
    "MORADA NOVA - CE",
    "MUCAMBO - CE",
    "PACAJUS - CE",
    "PACATUBA - CE",
    "PACUJÁ - CE",
    "PARACURU - CE",
    "PARAIPABA - CE",
    "PENTECOSTE - CE",
    "PINDORETAMA - CE",
    "QUIXADÁ - CE",
    "RUSSAS - CE",
    "SÃO BENEDITO - CE",
    "SÃO GONÇALO DO AMARANTE - CE",
    "SÃO LUÍS DO CURU - CE",
    "SOBRAL - CE",
    "TABULEIRO DO NORTE - CE",
    "TIANGUÁ - CE",
    "TRAIRI - CE",
    "UBAJARA - CE",
]

CITIES_API_GIGA_TERRITORIO_CIDADES_ESPECIAIS = [
    "SÃO JOÃO BATISTA DO GLÓRIA - MG",
    "ITAÚ DE MINAS - MG",
    "ALTOS - PI",
    "PARNAÍBA - PI",
    "TERESINA - PI",
]

# CIDADES DA OPERADORA DESKTOP - INTERNET

# CITIES_API_DESKTOP_BRONZE = ["MOGI GUAÇU - SP", "SÃO JOSÉ DOS CAMPOS - SP", "AGUAÍ - SP", "ÁGUAS DE SANTA BÁRBARA - SP", "AGUDOS - SP", "ALUMÍNIO - SP", "AMERICANA - SP", "AMÉRICO BRASILIENSE - SP", "AMPARO - SP", "ANGATUBA - SP", "ARAÇARIGUAMA - SP", "ARAÇOIABA DA SERRA - SP", "ARANDU - SP", "ARARAQUARA - SP", "ARARAS - SP", "AREALVA - SP", "AREIÓPOLIS - SP", "ATIBAIA - SP", "AVAÍ - SP", "AVARÉ - SP", "BARRA BONITA - SP", "BAURU - SP", "BIRITIBA MIRIM - SP", "BIRITIBA-MIRIM - SP", "BOA ESPERANÇA DO SUL - SP", "BOCAINA - SP", "BOFETE - SP", "BOITUVA - SP", "BOM JESUS DOS PERDÕES - SP", "BORBOREMA - SP", "BOREBI - SP", "BOTUCATU - SP", "BRAGANÇA PAULISTA - SP", "CABREÚVA - SP", "CAÇAPAVA - SP", "CAIEIRAS - SP", "CAMPINA DO MONTE ALEGRE - SP", "CAMPINAS - SP", "CAMPO LIMPO PAULISTA - SP", "CÂNDIDO RODRIGUES - SP", "CAPELA DO ALTO - SP", "CAPIVARI - SP", "CERQUEIRA CÉSAR - SP", "CERQUILHO - SP", "CESÁRIO LANGE - SP", "COLINA - SP", "CONCHAL - SP", "CONCHAS - SP", "CORDEIRÓPOLIS - SP", "CRISTAIS PAULISTA - SP", "DOBRADA - SP", "DOIS CÓRREGOS - SP", "DOURADO - SP", "ELIAS FAUSTO - SP", "ENGENHEIRO COELHO - SP", "FERNANDO PRESTES - SP", "FRANCA - SP", "FRANCISCO MORATO - SP", "FRANCO DA ROCHA - SP", "GAVIÃO PEIXOTO - SP", "GUAÍRA - SP", "GUARANTÃ - SP", "GUARAREMA - SP", "GUARIBA - SP", "GUARUJÁ - SP", "GUATAPARÁ - SP", "HOLAMBRA - SP", "HORTOLÂNDIA - SP", "LARAS - SP", "IBATÉ - SP", "IBITINGA - SP", "IGARAÇU DO TIETÊ - SP", "IGARATÁ - SP", "IPERÓ - SP", "IRACEMÁPOLIS - SP", "ITAÍ - SP", "ITAJOBI - SP", "ITAJU - SP", "ITANHAÉM - SP", "ITAPUÍ - SP", "ITATINGA - SP", "ITIRAPUÃ - SP", "ITU - SP", "JABORANDI - SP", "JABOTICABAL - SP", "JACAREÍ - SP", "JAGUARIÚNA - SP", "JARINU - SP", "JAÚ - SP", "JUMIRIM - SP", "JUNDIAÍ - SP", "LARANJAL PAULISTA - SP", "LENÇÓIS PAULISTA - SP", "LINDÓIA - SP", "LOUVEIRA - SP", "MACATUBA - SP", "MAIRIPORÃ - SP", "MANDURI - SP", "MATÃO - SP", "MINEIROS DO TIETÊ - SP", "MOGI DAS CRUZES - SP", "MONTE MOR - SP", "MOTUCA - SP", "NAZARÉ PAULISTA - SP", "NOVA EUROPA - SP", "NOVA ODESSA - SP", "ÓLEO - SP", "PARANAPANEMA - SP", "PARDINHO - SP", "PATROCÍNIO PAULISTA - SP", "PAULÍNIA - SP", "PEDERNEIRAS - SP", "PEDREIRA - SP", "PEREIRAS - SP", "PINDORAMA - SP", "PIRACAIA - SP", "PIRACICABA - SP", "PIRATININGA - SP", "PITANGUEIRAS - SP", "PORANGABA - SP", "PRAIA GRANDE - SP", "PRATÂNIA - SP", "PRESIDENTE ALVES - SP", "QUADRA - SP", "RAFARD - SP", "RIBEIRÃO BONITO - SP", "RIBEIRÃO CORRENTE - SP", "RIBEIRÃO PRETO - SP", "RINCÃO - SP", "RIO CLARO - SP", "RIO DAS PEDRAS - SP", "SALESÓPOLIS - SP", "SALTINHO - SP", "SALTO DE PIRAPORA - SP", "SANTA ADÉLIA - SP", "SANTA BÁRBARA D’OESTE - SP", "ITAPETININGA - SP", "ITÁPOLIS - SP", "SANTA ERNESTINA - SP", "SANTA GERTRUDES - SP", "SANTA LÚCIA - SP", "SANTO ANTÔNIO DE POSSE - SP", "SANTOS - SP", "SÃO CARLOS - SP", "SÃO MANUEL - SP", "SÃO VICENTE - SP", "SARAPUÍ - SP", "SERRA AZUL - SP", "SERRA NEGRA - SP", "SOROCABA - SP", "SUMARÉ - SP", "TABATINGA - SP", "TATUÍ - SP", "TAUBATÉ - SP", "TIETÊ - SP", "TRABIJU - SP", "TREMEMBÉ - SP", "VALINHOS - SP", "VÁRZEA PAULISTA - SP", "VINHEDO - SP", "VOTORANTIM - SP",  "MONGAGUÁ - SP"]
# CITIES_API_DESKTOP_PRATA = ["BÁLSAMO - SP", "BARRETOS - SP", "OLÍMPIA - SP"]
# CITIS_API_DESKTOP_OURO = ["BEBEDOURO - SP"]
# CITIS_API_DESKTOP_PLATINA = ["SANTA CRUZ DAS PALMEIRAS - SP", "CAFELÂNDIA - SP", "CASA BRANCA - SP", "COSMÓPOLIS - SP", "ESTIVA GERBI - SP", "INDAIATUBA - SP", "ITUPEVA - SP", "LINS - SP", "CEDRAL - SP", "ARTUR NOGUEIRA - SP", "CRAVINHOS - SP", "CUBATÃO - SP", "DESCALVADO - SP", "LEME - SP", "LIMEIRA - SP", "MIRASSOL - SP", "MOGI-MIRIM - SP", "MONTE ALEGRE DO SUL - SP", "MONTE ALTO - SP", "PERUÍBE - SP", "PILAR DO SUL - SP", "PIRASSUNUNGA - SP", "PORTO FERREIRA - SP", "SANTA RITA DO PASSA QUATRO - SP", "SÃO JOSÉ DO RIO PRETO - SP",  "TAMBAÚ - SP"]
# CITIS_API_DESKTOP_DIAMANTE = ["SÃO PAULO - SP"]
# CITIS_API_DESKTOP_ASCENDENTE = ["SANTA BRANCA - SP"]

CITIES_API_DESKTOP_PADRAO = [
    "AMPARO - SP",
    "CAMPINAS - SP",
    "HOLAMBRA - SP",
    "HORTOLÂNDIA - SP",
    "JAGUARIÚNA - SP",
    "LINDÓIA - SP",
    "MONTE MOR - SP",
    "PEDREIRA - SP",
    "SANTO ANTÔNIO DE POSSE - SP",
    "SERRA NEGRA - SP",
    "ALUMÍNIO - SP",
    "NOVA ODESSA - SP",
    "PAULÍNIA - SP",
    "PIRACICABA - SP",
    "SANTA BÁRBARA D'OESTE - SP",
    "SANTA GERTRUDES - SP",
    "SANTA RITA DO PASSA QUATRO - SP",
    "SUMARÉ - SP",
    "SERRA AZUL - SP",
    "AVAÍ - SP",
    "GUARANTÃ - SP",
    "PIRAJUÍ - SP",
    "PRESIDENTE ALVES - SP",
    "AMÉRICO BRASILIENSE - SP",
    "ARARAQUARA - SP",
    "BOA ESPERANÇA DO SUL - SP",
    "BORBOREMA - SP",
    "DESCALVADO - SP",
    "DOBRADA - SP",
    "DOURADO - SP",
    "GAVIÃO PEIXOTO - SP",
    "GUARIBA - SP",
    "GUATAPARÁ - SP",
    "IBATÉ - SP",
    "IBITINGA - SP",
    "ITÁPOLIS - SP",
    "MATÃO - SP",
    "MOTUCA - SP",
    "NOVA EUROPA - SP",
    "RIBEIRÃO BONITO - SP",
    "RINCÃO - SP",
    "SANTA LÚCIA - SP",
    "SÃO CARLOS - SP",
    "TABATINGA - SP",
    "COLINA - SP",
    "FERNANDO PRESTES - SP",
    "GUAÍRA - SP",
    "ITAJOBI - SP",
    "JABORANDI - SP",
    "JABOTICABAL - SP",
    "MONTE ALTO - SP",
    "PINDORAMA - SP",
    "PITANGUEIRAS - SP",
    "SANTA ADÉLIA - SP",
    "BAURU - SP",
    "BOTUCATU - SP",
    "LENÇÓIS PAULISTA - SP",
    "PIRATININGA - SP",
    "ARAÇARIGUAMA - SP",
    "ATIBAIA - SP",
    "BOM JESUS DOS PERDÕES - SP",
    "BRAGANÇA PAULISTA - SP",
    "CABREÚVA - SP",
    "CAIEIRAS - SP",
    "CAMPO LIMPO PAULISTA - SP",
    "FRANCISCO MORATO - SP",
    "FRANCO DA ROCHA - SP",
    "JARINU - SP",
    "LOUVEIRA - SP",
    "MAIRIPORÃ - SP",
    "NAZARÉ PAULISTA - SP",
    "PIRACAIA - SP",
    "VÁRZEA PAULISTA - SP",
    "VINHEDO - SP",
    "CUBATÃO - SP",
    "GUARUJÁ - SP",
    "ITANHAÉM - SP",
    "MONGAGUÁ - SP",
    "PRAIA GRANDE - SP",
    "SANTOS - SP",
    "SÃO BERNARDO DO CAMPO - SP",
    "SÃO VICENTE - SP",
    "BIRITIBA-MIRIM - SP",
    "CAÇAPAVA - SP",
    "GUARAREMA - SP",
    "IGARATÁ - SP",
    "JACAREÍ - SP",
    "MOGI DAS CRUZES - SP",
    "SALESÓPOLIS - SP",
    "SANTA BRANCA - SP",
    "SÃO JOSÉ DOS CAMPOS - SP",
    "TAUBATÉ - SP",
    "TREMEMBÉ - SP",
]

CITIES_API_DESKTOP_BARRETOS = ["BARRETOS - SP", "BEBEDOURO - SP", "OLÍMPIA - SP"]

CITIES_API_DESKTOP_TIO_SAM = [
    "CAPIVARI - SP",
    "ELIAS FAUSTO - SP",
    "RAFARD - SP",
    "SOROCABA - SP",
    "VOTORANTIM - SP",
    "AGUAÍ - SP",
    "AMERICANA - SP",
    "ARARAS - SP",
    "ARTUR NOGUEIRA - SP",
    "CASA BRANCA - SP",
    "CONCHAL - SP",
    "CORDEIRÓPOLIS - SP",
    "COSMÓPOLIS - SP",
    "ENGENHEIRO COELHO - SP",
    "ESTIVA GERBI - SP",
    "IRACEMÁPOLIS - SP",
    "LEME - SP",
    "LIMEIRA - SP",
    "MOGI GUAÇU - SP",
    "MOGI MIRIM - SP",
    "PIRASSUNUNGA - SP",
    "PORTO FERREIRA - SP",
    "SANTA CRUZ DAS PALMEIRAS - SP",
    "SANTA ROSA DE VITERBO - SP",
    "TAMBAÚ - SP",
    "CEDRAL - SP",
    "GUAPIAÇU - SP",
    "UCHOA - SP",
    "CAFELÂNDIA - SP",
    "CRAVINHOS - SP",
    "BADY BASSITT - SP",
    "MIRASSOL - SP",
    "SÃO JOSÉ DO RIO PRETO - SP",
    "LINS - SP",
    "INDAIATUBA - SP",
    "ITUPEVA - SP",
    "JUNDIAÍ - SP",
    "VALINHOS - SP",
    "PERUÍBE - SP",
]


CITIES_API_DESK_FASTERNET_PADRAO = [
    "MONTE ALEGRE DO SUL - SP",
    "ANGATUBA - SP",
    "ARAÇOIABA DA SERRA - SP",
    "RIO CLARO - SP",
    "CRISTAIS PAULISTA - SP",
    "ITIRAPUÃ - SP",
    "PATROCÍNIO PAULISTA - SP",
    "RIBEIRÃO CORRENTE - SP",
]

CITIES_API_DESK_FASTERNET_TIO_SAM = [
    "BOFETE - SP",
    "BOITUVA - SP",
    "CAMPINA DO MONTE ALEGRE - SP",
    "CAPELA DO ALTO - SP",
    "CERQUILHO - SP",
    "CESÁRIO LANGE - SP",
    "CONCHAS - SP",
    "IPERÓ - SP",
    "ITAPETININGA - SP",
    "ITÚ - SP",
    "JUMIRIM - SP",
    "LARANJAL PAULISTA - SP",
    "PEREIRAS - SP",
    "PILAR DO SUL - SP",
    "PORANGABA - SP",
    "QUADRA - SP",
    "RIO DAS PEDRAS - SP",
    "SALTINHO - SP",
    "SALTO - SP",
    "SALTO DE PIRAPORA - SP",
    "SARAPUÍ - SP",
    "TATUÍ - SP",
    "TIETÊ - SP",
    "FRANCA - SP",
]


CITIES_API_DESK_LPNET_PADRAO = [
    "BOCAINA - SP",
    "ITAJU - SP",
    "SANTA ERNESTINA - SP",
    "TRABIJU - SP",
    "CÂNDIDO RODRIGUES - SP",
    "AGUDOS - SP",
    "AREIÓPOLIS - SP",
    "BARRA BONITA - SP",
    "BOREBI - SP",
    "DOIS CÓRREGOS - SP",
    "IGARAÇU DO TIETÊ - SP",
    "ITAPUÍ - SP",
    "JAÚ - SP",
    "MACATUBA - SP",
    "MINEIROS DO TIETÊ - SP",
    "ÓLEO - SP",
    "PARANAPANEMA - SP",
    "PEDERNEIRAS - SP",
    "PRATÂNIA - SP",
    "SÃO MANUEL - SP",
]

CITIES_API_DESK_LPNET_TIO_SAM = [
    "ÁGUAS DE SANTA BÁRBARA - SP",
    "ARANDU - SP",
    "AVARÉ - SP",
    "CERQUEIRA CÉSAR - SP",
    "IARAS - SP",
    "ITAÍ - SP",
    "ITATINGA - SP",
    "MANDURI - SP",
    "PARDINHO - SP",
]

# CIDADES DA OPERADORA BL_FIBRA - INTERNET
CITIES_API_BL_FIBRA_PADRAO = ["BELO HORIZONTE - MG", "CONTAGEM - MG", "SABARÁ - MG", "SANTA LUZIA - MG"]

# CIDADES DA OPERADORA MASTER INTERNET

CITIES_API_MASTER_PADRAO = [
    "DIVINÓPOLIS - MG",
    "NOVA SERRANA - MG",
    "TAUBATÉ - SP",
    "PINDAMONHANGABA - SP",
    "LORENA - SP",
    "SÃO JOSÉ DOS CAMPOS - SP",
    "CAÇAPAVA - SP",
    "JACAREÍ - SP",
    "TREMEMBÉ - SP",
    "ITAJUBÁ - MG",
    "PIRANGUÇU - MG",
    "PIRANGUINHO - MG",
    "VARGINHA - MG",
    "TRÊS CORAÇÕES - MG",
    "POÇOS DE CALDAS - MG",
    "ITAÚNA - MG",
    "MATEUS LEME - MG",
    "LAVRAS - MG",
    "SETE LAGOAS - MG",
    "PASSOS - MG",
    "POUSO ALEGRE - MG",
    "UNAÍ - MG",
    "PARACATU - MG",
    "MONTES CLAROS - MG",
    "CAMPOS DO JORDÃO - SP"
]


# CIDADES DA OPERADORA BLINK INTERNET

CITIES_API_BLINK_PADRAO = [
    "BELO HORIZONTE - MG",
    "BETIM - MG",
    "BRUMADINHO - MG",
    "CONFINS - MG",
    "CONTAGEM - MG",
    "IGARAPÉ - MG",
    "LAGOA SANTA - MG",
    "MATOZINHOS - MG",
    "NOVA LIMA - MG",
    "PEDRO LEOPOLDO - MG",
    "RIBEIRÃO DAS NEVES - MG",
    "SANTA LUZIA - MG",
    "SÃO JOAQUIM DE BICAS - MG",
    "SÃO JOSÉ DA LAPA - MG",
    "VESPASIANO - MG",
]


# CIDADES DA OPERADORA IMPLANTAR INTERNET

CITIES_API_IMPLANTAR_PADRAO = [
    "BELO HORIZONTE - MG",
    "SABARÁ - MG", 
    "CONTAGEM - MG"
]



#FUNCÃO PARA VERO 
def get_api_url_vero(cidade):
    clusters = []
    if cidade in CITIES_API_VERO_OURO:
        clusters.append("VERO OURO")
    if cidade in CITIES_API_VERO_PADRAO:
        clusters.append("VERO PADRÃO")
    if cidade in CITIES_API_VERO_PRATA:
        clusters.append("VERO PRATA")    
    if cidade in CITIES_API_VERO_REDE_NEUTRA:
        clusters.append("VERO REDE NEUTRA")
    if cidade in CITIES_API_VERO_GRAFENO_80:
        clusters.append("VERO GRAFENO_80")
    if cidade in CITIES_API_VERO_GRAFENO_75:
        clusters.append("VERO GRAFENO_75")
    if cidade in CITIES_API_VERO_SAFIRA:
        clusters.append("VERO SAFIRA")
    return clusters

#FUNÇÃO PARA DESKTOP
def get_api_url_desktop(cidade):
    clusters = []
    if cidade in CITIES_API_DESKTOP_PADRAO:
        clusters.append("DESKTOP PADRÃO")
    if cidade in CITIES_API_DESKTOP_BARRETOS:
        clusters.append("DESKTOP BARRETOS")
    if cidade in CITIES_API_DESKTOP_TIO_SAM:
        clusters.append("DESKTOP TIOSAM")
    if cidade in CITIES_API_DESK_FASTERNET_PADRAO:
        clusters.append("FASTERNET PADRÃO")
    if cidade in CITIES_API_DESK_FASTERNET_TIO_SAM:
        clusters.append("FASTERNET TIOSAM")
    if cidade in CITIES_API_DESK_LPNET_PADRAO:
        clusters.append("LPNET PADRÃO")
    if cidade in CITIES_API_DESK_LPNET_TIO_SAM:
        clusters.append("LPNET TIOSAM")
    return clusters

#FUNÇÃO PARA GIGA+
def get_api_url_giga(cidade):
    clusters = []
    if cidade in CITIES_API_GIGA_TERRITORIO_T1_a_T9:
        clusters.append("GIGA T1_A_T9")
    if cidade in CITIES_API_GIGA_TERRITORIO_T10_a_T14:
        clusters.append("GIGA T10_A_T14")
    if cidade in CITIES_API_GIGA_TERRITORIO_CIDADES_ESPECIAIS:
        clusters.append("GIGA T_CIDADES_ESPECIAIS")
    return clusters

#FUNÇÃO PARA BL FIBRA
def get_api_url_blfibra(cidade):
    clusters = []
    if cidade in CITIES_API_BL_FIBRA_PADRAO:
        clusters.append("BL FIBRA PADRAO")
    return clusters

#FUNÇÃO PARA MASTER
def get_api_url_master(cidade):
    clusters = []
    if cidade in CITIES_API_MASTER_PADRAO:
        clusters.append("MASTER PADRAO")
    return clusters

#FUNÇÃO PARA BLINK 
def get_api_url_blink(cidade):
    clusters = []
    if cidade in CITIES_API_BLINK_PADRAO:
        clusters.append("BLINK PADRAO")
    return clusters

#FUNCÃO PARA IMPLANTAR
def get_api_url_implantar(cidade):
    clusters = []
    if cidade in CITIES_API_IMPLANTAR_PADRAO:
        clusters.append("IMPLANTAR PADRAO")
    return clusters



#FUNÇÃO UPDATE_CALL_WORKFLOW_VERO
def update_field_and_call_workflow_vero(cidade, entity_id):
    clusters = get_api_url_vero(cidade)

    if len(clusters) == 0:
        requests.post(
            f"{BITRIX_WEBHOOK_URL}/crm.deal.update?ID={entity_id}&FIELDS[UF_CRM_1741717512]={'CIDADE NÃO MAPEADA'}")
        return {"error": "Error"}

    clusters_to_string = ""
    for i in range(len(clusters)):
        clusters_to_string += (
            f"{clusters[i]}, " if i != len(clusters) - 1 else f"{clusters[i]}"
        )
    requests.post(
        f"{BITRIX_WEBHOOK_URL}/crm.deal.update?ID={entity_id}&FIELDS[UF_CRM_1741717512]={clusters_to_string}"
    )
    res2 = requests.post(
        f"{URL_VPS}/webhook/workflow_send_plans_geral?deal_id={entity_id}"
    )
    print(res2.json())
    return {"clusters": clusters_to_string}

#FUNÇÃO UPDATE_CALL_WORKFLOW_GIGA+
def update_field_and_call_workflow_giga(cidade, entity_id):
    clusters = get_api_url_giga(cidade)

    if len(clusters) == 0:
        requests.post(
            f"{BITRIX_WEBHOOK_URL}/crm.deal.update?ID={entity_id}&FIELDS[UF_CRM_1741717512]={'CIDADE NÃO MAPEADA'}"
        )
        return {"error": "Error"}

    clusters_to_string = ""
    for i in range(len(clusters)):
        clusters_to_string += (
            f"{clusters[i]}, " if i != len(clusters) - 1 else f"{clusters[i]}"
        )
    requests.post(
        f"{BITRIX_WEBHOOK_URL}/crm.deal.update?ID={entity_id}&FIELDS[UF_CRM_1741717512]={clusters_to_string}"
    )
    res2 = requests.post(
        f"{URL_VPS}/webhook/workflow_send_plans_geral?deal_id={entity_id}"
    )
    print(res2.json())
    return {"clusters": clusters_to_string}

#FUNÇÃO UPDATE_CALL_WORKFLOW_DESKTOP
def update_field_and_call_workflow_desktop(cidade, entity_id):
    clusters = get_api_url_desktop(cidade)

    if len(clusters) == 0:
        requests.post(
            f"{BITRIX_WEBHOOK_URL}/crm.deal.update?ID={entity_id}&FIELDS[UF_CRM_1741717512]={'CIDADE NÃO MAPEADA'}"
        )
        return {"error": "Error"}

    
    clusters_to_string = ""
    for i in range(len(clusters)):
        clusters_to_string += (
            f"{clusters[i]}, " if i != len(clusters) - 1 else f"{clusters[i]}"
        )
    requests.post(
        f"{BITRIX_WEBHOOK_URL}/crm.deal.update?ID={entity_id}&FIELDS[UF_CRM_1741717512]={clusters_to_string}"
    )
    res2 = requests.post(
        f"{URL_VPS}/webhook/workflow_send_plans_geral?deal_id={entity_id}"
    )
    print(res2.json())
    return {"clusters": clusters_to_string}

#FUNÇÃO UPDATE_CALL_WORKFLOW_MASTER
def update_field_and_call_workflow_master(cidade, entity_id):
    clusters = get_api_url_master(cidade)

    if len(clusters) == 0:
        requests.post(
            f"{BITRIX_WEBHOOK_URL}/crm.deal.update?ID={entity_id}&FIELDS[UF_CRM_1741717512]={'CIDADE NÃO MAPEADA'}"
        )
        return {"error": "Error"}

    clusters_to_string = ""
    for i in range(len(clusters)):
        clusters_to_string += (
            f"{clusters[i]}, " if i != len(clusters) - 1 else f"{clusters[i]}"
        )
    requests.post(
        f"{BITRIX_WEBHOOK_URL}/crm.deal.update?ID={entity_id}&FIELDS[UF_CRM_1741717512]={clusters_to_string}"
    )
    res2 = requests.post(
        f"{URL_VPS}/webhook/workflow_send_plans_geral?deal_id={entity_id}"
    )
    print(res2.json())
    return {"clusters": clusters_to_string}

#FUNÇÃO UPDATE_CALL_WORKFLOW_BL_FIBRA
def update_field_and_call_workflow_blfibra(cidade, entity_id):
    clusters = get_api_url_blfibra(cidade)

    if len(clusters) == 0:
        requests.post(
            f"{BITRIX_WEBHOOK_URL}/crm.deal.update?ID={entity_id}&FIELDS[UF_CRM_1741717512]={'CIDADE NÃO MAPEADA'}"
        )
        return {"error": "Error"}
    
    clusters_to_string = ""
    for i in range(len(clusters)):
        clusters_to_string += (
            f"{clusters[i]}, " if i != len(clusters) - 1 else f"{clusters[i]}"
        )
    requests.post(
        f"{BITRIX_WEBHOOK_URL}/crm.deal.update?ID={entity_id}&FIELDS[UF_CRM_1741717512]={clusters_to_string}"
    )
    res2 = requests.post(
        f"{URL_VPS}/webhook/workflow_send_plans_geral?deal_id={entity_id}"
    )
    print(res2.json())
    return {"clusters": clusters_to_string}

#FUNÇÃO UPDATE_CALL_WORKFLOW_BLINK
def update_field_and_call_workflow_blink(cidade, entity_id):
    clusters = get_api_url_blink(cidade)

    if len(clusters) == 0:
        requests.post(
            f"{BITRIX_WEBHOOK_URL}/crm.deal.update?ID={entity_id}&FIELDS[UF_CRM_1741717512]={'CIDADE NÃO MAPEADA'}"
        )
        return {"error": "Error"}
    

    clusters_to_string = ""
    for i in range(len(clusters)):
        clusters_to_string += (
            f"{clusters[i]}, " if i != len(clusters) - 1 else f"{clusters[i]}"
        )
    requests.post(
        f"{BITRIX_WEBHOOK_URL}/crm.deal.update?ID={entity_id}&FIELDS[UF_CRM_1741717512]={clusters_to_string}"
    )
    res2 = requests.post(
        f"{URL_VPS}/webhook/workflow_send_plans_geral?deal_id={entity_id}"
    )
    print(res2.json())
    return {"clusters": clusters_to_string}

#FUNÇÃO UPDATE_CALL_WORKFLOW_IMPLANTAR
def update_field_and_call_workflow_implantar(cidade, entity_id):
    clusters = get_api_url_implantar(cidade)

    if len(clusters) == 0:
        requests.post(
            f"{BITRIX_WEBHOOK_URL}/crm.deal.update?ID={entity_id}&FIELDS[UF_CRM_1741717512]={'CIDADE NÃO MAPEADA'}"
        )
        return {"error": "Error"}
        
    clusters_to_string = ""
    for i in range(len(clusters)):
        clusters_to_string += (
            f"{clusters[i]}, " if i != len(clusters) - 1 else f"{clusters[i]}"
        )
    requests.post(
        f"{BITRIX_WEBHOOK_URL}/crm.deal.update?ID={entity_id}&FIELDS[UF_CRM_1741717512]={clusters_to_string}"
    )
    res2 = requests.post(
        f"{URL_VPS}/webhook/workflow_send_plans_geral?deal_id={entity_id}"
    )
    print(res2.json())
    return {"clusters": clusters_to_string}

def make_request_with_retries(method, url, **kwargs):
    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = requests.request(method, url, **kwargs)
            if response.status_code in [200, 201]:
                return response
            else:
                log_erro(
                    f"Erro {response.status_code} na tentativa {attempt + 1}",
                    response.text,
                )
        except requests.exceptions.RequestException as e:
            log_erro("Erro de conexão", e)
        time.sleep(2)
    return None

def handle_request_errors(response, error_message, details=None):
    if response is None or response.status_code >= 400:
        return (
            jsonify(
                {
                    "error": error_message,
                    "details": (
                        details or response.text if response else "Nenhuma resposta"
                    ),
                }
            ),
            400,
        )

@app.route("/update-plan-desktop/<string:entity_id>", methods=["POST"])
def update_plan_desktop(entity_id):
    try:
        get_deal_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.get"
        get_deal_response = make_request_with_retries(
            "GET", get_deal_url, params={"id": entity_id}
        )
        handle_request_errors(
            get_deal_response, "Falha ao buscar os dados da negociação"
        )
        get_deal_data = get_deal_response.json()

        cidade = get_deal_data["result"].get("UF_CRM_1731588487")
        uf = get_deal_data["result"].get("UF_CRM_1731589190")

        if not cidade or not uf:
            return jsonify({"error": "Campos Cidade e UF estão vazios"}), 400

        cidade_completa = f"{cidade.strip().upper()} - {uf.strip().upper()}"

        update_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.update"

        update_response = make_request_with_retries(
            "POST",
            update_url,
            json={"id": entity_id, "fields": {"UF_CRM_1733493949": cidade_completa}},
        )

        api_response = update_field_and_call_workflow_desktop(cidade_completa, entity_id)
        return (
            jsonify(
                {
                    "message": "Campo atualizado com sucesso!",
                    "cidade_completa": cidade_completa,
                    "api_response": api_response,
                }
            ),
            200,
        )

    except Exception as e:
        log_erro("Erro interno", e)
        return jsonify({"error": "Erro interno no servidor", "details": str(e)}), 500


@app.route("/update-plan-giga/<string:entity_id>", methods=["POST"])
def update_plan_giga(entity_id):
    try:
        get_deal_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.get"
        get_deal_response = make_request_with_retries(
            "GET", get_deal_url, params={"id": entity_id}
        )
        handle_request_errors(
            get_deal_response, "Falha ao buscar os dados da negociação"
        )
        get_deal_data = get_deal_response.json()

        cidade = get_deal_data["result"].get("UF_CRM_1731588487")
        uf = get_deal_data["result"].get("UF_CRM_1731589190")

        if not cidade or not uf:
            return jsonify({"error": "Campos Cidade e UF estão vazios"}), 400

        cidade_completa = f"{cidade.strip().upper()} - {uf.strip().upper()}"

        update_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.update"

        update_response = make_request_with_retries(
            "POST",
            update_url,
            json={"id": entity_id, "fields": {"UF_CRM_1733493949": cidade_completa}},
        )

        api_response = update_field_and_call_workflow_giga(cidade_completa, entity_id)
        return (
            jsonify(
                {
                    "message": "Campo atualizado com sucesso!",
                    "cidade_completa": cidade_completa,
                    "api_response": api_response,
                }
            ),
            200,
        )

    except Exception as e:
        log_erro("Erro interno", e)
        return jsonify({"error": "Erro interno no servidor", "details": str(e)}), 500


@app.route("/update-plan-vero/<string:entity_id>", methods=["POST"])
def update_plan_vero(entity_id):
    try:
        get_deal_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.get"
        get_deal_response = make_request_with_retries(
            "GET", get_deal_url, params={"id": entity_id}
        )
        handle_request_errors(
            get_deal_response, "Falha ao buscar os dados da negociação"
        )
        get_deal_data = get_deal_response.json()

        cidade = get_deal_data["result"].get("UF_CRM_1731588487")
        uf = get_deal_data["result"].get("UF_CRM_1731589190")

        if not cidade or not uf:
            return jsonify({"error": "Campos Cidade e UF estão vazios"}), 400

        cidade_completa = f"{cidade.strip().upper()} - {uf.strip().upper()}"

        update_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.update"

        update_response = make_request_with_retries(
            "POST",
            update_url,
            json={"id": entity_id, "fields": {"UF_CRM_1733493949": cidade_completa}},
        )

        api_response = update_field_and_call_workflow_vero(cidade_completa, entity_id)
        return (
            jsonify(
                {
                    "message": "Campo atualizado com sucesso!",
                    "cidade_completa": cidade_completa,
                    "api_response": api_response,
                }
            ),
            200,
        )

    except Exception as e:
        log_erro("Erro interno", e)
        return jsonify({"error": "Erro interno no servidor", "details": str(e)}), 500

@app.route("/update-plan-blfibra/<string:entity_id>", methods=["POST"])
def update_plan_blfibra(entity_id):
    try:
        get_deal_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.get"
        get_deal_response = make_request_with_retries(
            "GET", get_deal_url, params={"id": entity_id}
        )
        handle_request_errors(
            get_deal_response, "Falha ao buscar os dados da negociação"
        )
        get_deal_data = get_deal_response.json()

        cidade = get_deal_data["result"].get("UF_CRM_1731588487")
        uf = get_deal_data["result"].get("UF_CRM_1731589190")

        if not cidade or not uf:
            return jsonify({"error": "Campos Cidade e UF estão vazios"}), 400

        cidade_completa = f"{cidade.strip().upper()} - {uf.strip().upper()}"

        update_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.update"

        update_response = make_request_with_retries(
            "POST",
            update_url,
            json={"id": entity_id, "fields": {"UF_CRM_1733493949": cidade_completa}},
        )

        api_response = update_field_and_call_workflow_blfibra(cidade_completa, entity_id)
        return (
            jsonify(
                {
                    "message": "Campo atualizado com sucesso!",
                    "cidade_completa": cidade_completa,
                    "api_response": api_response,
                }
            ),
            200,
        )

    except Exception as e:
        log_erro("Erro interno", e)
        return jsonify({"error": "Erro interno no servidor", "details": str(e)}), 500

@app.route("/update-plan-master/<string:entity_id>", methods=["POST"])
def update_plan_master(entity_id):
    try:
        get_deal_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.get"
        get_deal_response = make_request_with_retries(
            "GET", get_deal_url, params={"id": entity_id}
        )
        handle_request_errors(
            get_deal_response, "Falha ao buscar os dados da negociação"
        )
        get_deal_data = get_deal_response.json()

        cidade = get_deal_data["result"].get("UF_CRM_1731588487")
        uf = get_deal_data["result"].get("UF_CRM_1731589190")

        if not cidade or not uf:
            return jsonify({"error": "Campos Cidade e UF estão vazios"}), 400

        cidade_completa = f"{cidade.strip().upper()} - {uf.strip().upper()}"

        update_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.update"

        update_response = make_request_with_retries(
            "POST",
            update_url,
            json={"id": entity_id, "fields": {"UF_CRM_1733493949": cidade_completa}},
        )

        api_response = update_field_and_call_workflow_master(cidade_completa, entity_id)
        return (
            jsonify(
                {
                    "message": "Campo atualizado com sucesso!",
                    "cidade_completa": cidade_completa,
                    "api_response": api_response,
                }
            ),
            200,
        )

    except Exception as e:
        log_erro("Erro interno", e)
        return jsonify({"error": "Erro interno no servidor", "details": str(e)}), 500


@app.route("/update-plan-blink/<string:entity_id>", methods=["POST"])
def update_plan_blink(entity_id):
    try:
        get_deal_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.get"
        get_deal_response = make_request_with_retries(
            "GET", get_deal_url, params={"id": entity_id}
        )
        handle_request_errors(
            get_deal_response, "Falha ao buscar os dados da negociação"
        )
        get_deal_data = get_deal_response.json()

        cidade = get_deal_data["result"].get("UF_CRM_1731588487")
        uf = get_deal_data["result"].get("UF_CRM_1731589190")

        if not cidade or not uf:
            return jsonify({"error": "Campos Cidade e UF estão vazios"}), 400

        cidade_completa = f"{cidade.strip().upper()} - {uf.strip().upper()}"

        update_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.update"

        update_response = make_request_with_retries(
            "POST",
            update_url,
            json={"id": entity_id, "fields": {"UF_CRM_1733493949": cidade_completa}},
        )

        api_response = update_field_and_call_workflow_blink(cidade_completa, entity_id)
        return (
            jsonify(
                {
                    "message": "Campo atualizado com sucesso!",
                    "cidade_completa": cidade_completa,
                    "api_response": api_response,
                }
            ),
            200,
        )

    except Exception as e:
        log_erro("Erro interno", e)
        return jsonify({"error": "Erro interno no servidor", "details": str(e)}), 500


@app.route("/update-plan-implantar/<string:entity_id>", methods=["POST"])
def update_plan_implantar(entity_id):
    try:
        get_deal_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.get"
        get_deal_response = make_request_with_retries(
            "GET", get_deal_url, params={"id": entity_id}
        )
        handle_request_errors(
            get_deal_response, "Falha ao buscar os dados da negociação"
        )
        get_deal_data = get_deal_response.json()

        cidade = get_deal_data["result"].get("UF_CRM_1731588487")
        uf = get_deal_data["result"].get("UF_CRM_1731589190")

        if not cidade or not uf:
            return jsonify({"error": "Campos Cidade e UF estão vazios"}), 400

        cidade_completa = f"{cidade.strip().upper()} - {uf.strip().upper()}"

        update_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.update"

        update_response = make_request_with_retries(
            "POST",
            update_url,
            json={"id": entity_id, "fields": {"UF_CRM_1733493949": cidade_completa}},
        )

        api_response = update_field_and_call_workflow_implantar(cidade_completa, entity_id)
        return (
            jsonify(
                {
                    "message": "Campo atualizado com sucesso!",
                    "cidade_completa": cidade_completa,
                    "api_response": api_response,
                }
            ),
            200,
        )

    except Exception as e:
        log_erro("Erro interno", e)
        return jsonify({"error": "Erro interno no servidor", "details": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0")
