from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os
import time

app = Flask(__name__)

load_dotenv()

CODIGO_BITRIX = os.getenv('CODIGO_BITRIX')
CODIGO_BITRIX_STR = os.getenv('CODIGO_BITRIX_STR')
PROFILE = os.getenv('PROFILE')
BASE_URL_API_BITRIX = os.getenv('BASE_URL_API_BITRIX')

BITRIX_WEBHOOK_URL = f"{BASE_URL_API_BITRIX}/{PROFILE}/{CODIGO_BITRIX}/"




def log_erro(mensagem, e=None):
    """ Função de log de erro para registrar exceções """
    import traceback
    erro_detalhado = traceback.format_exc()
    print(f"\n[ERRO] {mensagem}")
    if e:
        print(f"[DETALHES] {str(e)}")
    print(f"[TRACEBACK] {erro_detalhado}\n")

# CIDADES DA OPERADORA VERO - INTERNET 
CITIES_API_OURO = [
    "ALVORADA - RS", "BARÃO DE COCAIS - MG", "BARBACENA - MG", "BARROSO - MG", 
    "CACHOEIRINHA - RS", "BELO HORIZONTE - MG", "CAPÃO DA CANOA - RS", "CAXAMBU - MG", 
    "CHARQUEADAS - RS", "DIVINÓPOLIS - MG", "ESTEIO - RS", "FRANCISCO BELTRÃO - PR", 
    "FREDERICO WESTPHALEN - RS", "GOVERNADOR VALADARES - MG", "GRAVATAÍ - RS", 
    "ITAQUI - RS", "LAVRAS - MG", "MARIANA - MG", "NOVO HAMBURGO - RS", 
    "NOVO HAMBURGO - SINOS - RS", "PATO BRANCO - PR", "PONTE NOVA - MG", 
    "RIBEIRÃO DAS NEVES - MG", "SABARÁ - MG", "SANTIAGO - RS", "SÃO JERÔNIMO - RS", 
    "SÃO LEOPOLDO - RS", "SÃO LEOPOLDO - SINOS - RS", "SÃO LOURENÇO - MG", 
    "SÃO LUIZ GONZAGA - RS", "SAPUCAIA DO SUL - RS", "URUGUAIANA - RS", 
    "VENÂNCIO AIRES - RS", "VIÇOSA - MG", "XANXERÊ - SC", "BAURU - SP", 
    "TRES LAGOAS - MS", "ARACATUBA - SP", "RIO VERDE - GO", "UBERLANDIA - MG", 
    "JAU - SP", "BIRIGUI - SP", "GOIANIA - GO", "GOIANIRA - GO", "PEDERNEIRAS - SP", 
    "ANDRADINA - SP", "DOIS CORREGOS - SP", "TRINDADE - GO", 
    "APARECIDA DE GOIANIA - GO", "SENADOR CANEDO - GO", "ITAPEMA - SC", 
    "TIJUCAS - SC", "SÃO JOÃO DEL REI - MG"
]
CITIES_API_PADRAO = [
    "ALFREDO VASCONCELOS - MG", "ANCHIETA - RS", "ANTÔNIO CARLOS - MG", "ARROIO DO SAL - RS", 
    "BALNEÁRIO PINHAL - RS", "BANDEIRANTE - RS", "BARRACÃO - RS", "BICAS - MG", 
    "BOM DESPACHO - MG", "BOM SUCESSO - MG", "CAMPO ERÊ - SC", "CAPELA DE SANTANA - RS", 
    "CARAÁ - RS", "CARANDAÍ - MG", "CARMO DA MATA - MG", "CARMÓPOLIS DE MINAS - MG", 
    "CIDREIRA - RS", "CLÁUDIO - MG", "CONCEIÇÃO DA BARRA DE MINAS - MG", "CONGONHAS - MG", 
    "CONSELHEIRO LAFAIETE - MG", "CRUZ ALTA - RS", "DESCANSO - SC", "DIONÍSIO CERQUEIRA - SC", 
    "DORES DE CAMPOS - MG", "ENTRE RIOS DE MINAS - MG", "FLOR DA SERRA DO SUL - PR", 
    "GALVÃO - SC", "GLORINHA - RS", "GUARACIABA - SC", "GUARARÁ - MG", 
    "GUARUJÁ DO SUL - SC", "IJUÍ - RS", "IMBÉ - RS", "ITAGUARA - MG", 
    "ITATIAIUÇU - MG", "ITAÚNA - MG", "JECEABA - MG", "JUIZ DE FORA - MG", 
    "JUPIÁ - SP", "LIMA DUARTE - MG", "MAQUINÉ - RS", "MAR DE ESPANHA - MG", 
    "MARATÁ - RS", "MARIÓPOLIS - RS", "MARMELEIRO - PR", "MARTINHO CAMPOS - MG", 
    "MATIAS BARBOSA - MG", "MONTENEGRO - RS", "NOVA SANTA RITA - RS", "NOVA SERRANA - MG", 
    "NOVO HORIZONTE - RS", "OLIVEIRA - MG", "OSÓRIO - RS", "OURO BRANCO - MG", 
    "PALMA SOLA - SC", "PANAMBI - RS", "PARÁ DE MINAS - MG", "PARECI NOVO - RS", 
    "PERDÕES - MG", "PORTO ALEGRE - RS", "PRINCESA - SC", "RENASCENÇA - SC", 
    "RESSAQUINHA - MG", "RIBEIRÃO VERMELHO - MG", "SANTA CRUZ DE MINAS - MG", 
    "SANTA LUZIA - MG", "SANTO ÂNGELO - RS", "SANTO ANTÔNIO DA PATRULHA - RS", 
    "SANTO ANTÔNIO DO AMPARO - MG", "SÃO BRÁS DO SUAÇUÍ - MG", "SÃO DOMINGOS - RS", 
    "SÃO FRANCISCO DE PAULA - RS", "SÃO JOSÉ DO CEDRO - SC", "SÃO JOSÉ DO SUL - RS", 
    "SÃO LOURENÇO DO OESTE - SC", "SÃO MIGUEL DO OESTE - SC", "TEÓFILO OTONI - MG", 
    "TERRA DE AREIA - RS", "TIRADENTES - MG", "TORRES - RS", "TRAMANDAÍ - RS", 
    "TRÊS CACHOEIRAS - RS", "TRIUNFO - RS", "VIAMÃO - RS", "VITORINO - PR", 
    "XANGRI-LÁ - RS"
]
CITIES_API_PRATA = [
  "BOM PRINCÍPIO - RS", "BRASÍLIA - DF", "BRUMADINHO - MG", "CAETÉ - MG", 
  "CAMPO BELO - MG", "CANOAS - RS", "CARATINGA - MG", "CORONEL FABRICIANO - MG", "DOIS IRMÃOS - RS", "ESTÂNCIA VELHA - RS", "FELIZ - RS", "IGARAPÉ - MG", 
  "IPATINGA - MG", "ITABIRITO - MG", "IVOTI - RS", "JOÃO MONLEVADE - MG", 
  "LEOPOLDINA - MG", "LINDOLFO COLLOR - RS", "LUZIÂNIA - GO", "MANHUAÇU - MG", 
  "MATOZINHOS - MG", "MORRO REUTER - RS", "NEPOMUCENO - MG", "NOVO GAMA - GO", 
  "OURO PRETO - MG", "PEDRO LEOPOLDO - MG", "PEQUERI - MG", "PICADA CAFÉ - RS", 
  "PORTÃO - RS", "PORTÃO - SINOS - RS", "PRESIDENTE LUCENA - RS", "SANTA BÁRBARA - MG", 
  "SANTA MARIA DO HERVAL - RS", "SANTANA DO PARAÍSO - MG", "SANTO AUGUSTO - RS", 
  "SANTOS DUMONT - MG", "SÃO BORJA - RS", "SÃO JOAQUIM DE BICAS - MG", 
  "SÃO JOSÉ DA LAPA - MG", "SÃO JOSÉ DO HORTÊNCIO - RS", "SÃO SEBASTIÃO DO CAÍ - RS", 
  "SAPIRANGA - RS", "TIMÓTEO - MG", "VALPARAÍSO DE GOIÁS - GO", "VESPASIANO - MG", 
  "VISCONDE DO RIO BRANCO - MG", "LIMEIRA - SP", "CAMPO GRANDE - SP", "POA - SP", 
  "CALDAS NOVAS - GO", "PRESIDENTE PRUDENTE - SP", "SAO JOSE DO RIO PRETO - SP", 
  "PIRASSUNUNGA - SP", "ITAQUAQUECETUBA - SP", "SANTA BARBARA D OESTE - SP", 
  "LEME - SP", "MAIRINQUE - SP", "VOTORANTIM - SP", "CATALÃO - GO", 
  "RIBEIRÃO PIRES - SP", "INHUMAS - GO", "PINDAMONHANGABA - SP", "SAO ROQUE - SP", 
  "NOVA ANDRADINA - SP", "SAO JOSE DOS CAMPOS - SP", "PIRACICABA - SP", 
  "PORANGATU - GO", "TATUI - SP", "LINS - SP", "PRESIDENTE EPITÁCIO - SP", 
  "BOTUCATU - SP", "PALMEIRAS DE GOIÁS - GO", "SOROCABA - SP", "ACREÚNA - GO", 
  "ITU - SP", "CRUZEIRO - SP", "GOIATUBA - GO", "PEREIRA BARRETO - SP", 
  "ARUJA - SP", "GUAPÓ - GO", "BARRA BONITA - SP", "MARTINÓPOLIS - SP", 
  "FERNANDÓPOLIS - SP", "BATAGUASSU - SP", "IGARACU DO TIETE - SP", 
  "AMERICANA - SP", "SANTO ANASTÁCIO - SP", "IPAMERI - GO", "LORENA - SP", 
  "BATAYPORA - SP", "PONTALINA - GO", "ILHA SOLTEIRA - SP", "CASTILHO - SP", "MINEIROS DO TIETÊ - SP", "PRESIDENTE VENCESLAU - SP", 
  "SANTA ISABEL - SP", "SAO LUIS DE MONTES BELOS - GO", "VALPARAISO - SP", "MARA ROSA - GO", 
  "SANTA HELENA DE GOIAS - GO", "EDEIA - GO", "FRANCO DA ROCHA - SP", "APARECIDA - SP", 
  "CORDEIROPOLIS - SP", "JALES - SP", "MIRANDÓPOLIS - SP", "PRESIDENTE BERNARDES - SP", 
  "SANTA FE DO SUL - SP", "GUARARAPES - SP", "IRACEMÁPOLIS - SP", "PROMISSÃO - SP", 
  "CACAPAVA - SP", "ITAPURA - SP", "PIEDADE - SP", "NOVA IGUACU DE GOIAS - GO", 
  "ANAURILANDIA - MS", "BELA VISTA DE GOIAS - GO", "CACHOEIRA PAULISTA - SP", "FATIMA DO SUL - MS", 
  "CAIEIRAS - SP", "HIDROLÂNDIA - GO", "PARAÚNA - GO", "SAO JOAO DA BOA VISTA - SP", 
  "POTIM - SP", "AGUDOS - SP", "CAJAMAR - SP", "INDIARA - GO", "MACATUBA - SP", "ALTO HORIZONTE - GO", 
  "PIRACANJUBA - GO", "IACANGA - SP", "SANTA CRUZ DA CONCEIÇÃO - SP", "SAO PAULO - SP", "TORRINHA - SP", 
  "RUBINEIA - SP", "TRES FRONTEIRAS - SP", "ABADIA DE GOIAS - GO", "IPERO - SP", "NOVA INDEPENDENCIA - SP", 
  "PIRATININGA - SP", "BURITI ALEGRE - GO", "FIRMINÓPOLIS - GO", "ITAPEVI - SP", "RIO GRANDE DA SERRA - SP", 
  "SANTA MARIA DA SERRA - SP", "URÂNIA - SP", "GUAICARA - SP", "GUARACAI - SP", "JARINU - SP", "BROTAS - SP", 
  "MURUTINGA DO SUL - SP", "PETROLINA DE GOIAS - GO", "CARAPICUÍBA - SP", "PIQUEROBI - SP", "ALFREDO MARCONDES - SP", 
  "AMARALINA - GO", "AVANHANDAVA - SP", "CANAS - SP", "PORTO FERREIRA - SP", "RIBEIRÃO DOS ÍNDIOS - SP", 
  "VICENTINA - SP", "CAIÚA - SP", "EMILIANÓPOLIS - SP", "IBIÚNA - SP", "PIRAJUÍ - SP", "RUBIÁCEA - SP", 
  "SANTANA DA PONTE PENSA - SP", "CROMÍNIA - GO", "FRANCISCO MORATO - SP", "ITÁUCU - GO", "LAVÍNIA - SP", 
  "LAVRINHAS - SP", "PIRAPORA DO BOM JESUS - SP", "SANTA SALETE - SP", "SANTA TEREZA DE GOIAS - GO", 
  "SAO JOAO DA PARAUNA - GO", "TANABI - SP", "VARGEM GRANDE PAULISTA - SP", "BARUERI - SP", 
  "CACHOEIRA ALTA - GO", "CEZARINA - GO", "FERRAZ DE VASCONCELOS - SP", "JANDAIA - GO", "JUNDIAI - SP", 
  "NOVA ODESSA - SP", "RIO QUENTE - GO", "SANTO EXPEDITO - SP", "TURVELÂNDIA - GO", "BENTO DE ABREU - SP", 
  "EDEALINA - GO", "MARZAGÃO - GO", "SANTANA DE PARNAÍBA - SP", "ARARAS - SP", "URUAÇU - GO", 
  "COTIA - SP", "SUZANO - SP", "OSASCO - SP", "CAMPINORTE - GO", "JANDIRA - SP", "ÁGUAS MORNAS - SC", 
  "ANGELINA - SC", "CANELINHA - SC", "NOVA TRENTO - SC", "PORTO BELO - SC", "ANTÔNIO CARLOS - SC", 
  "RANCHO QUEIMADO - SC", "SÃO JOÃO BATISTA - SC", "BIGUÁÇU - SC", "FLORIANÓPOLIS - SC", 
  "GOVERNADOR CELSO RAMOS - SC", "MAJOR GERCINO - SC", "PALHOÇA - SC", "SANTO AMARO DA IMPERATRIZ - SC", 
  "SÃO JOSÉ - SC", "SÃO PEDRO DE ALCÂNTARA - SC", "DOURADOS - MS"
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
    "RIBEIRÃO DAS NEVES - MG",
    "BETIM - MG"
]

# CIDADES DA OPERADORA GIGA+ - INTERNET

CITIES_API_TERRITORIO_T1_T3_T4 = [
    "APUCARANA - PR", "ARAPONGAS - PR", "ARARUNA - PR", "CAMPO MOURÃO - PR", "CIANORTE - PR", "DOUTOR CAMARGO - PR", "ENGENHEIRO BELTRÃO - PR", "JANDAIA DO SUL - PR", "JUSSARA - PR", "MANDAGUARI - PR", "MARIALVA - PR", "MARINGÁ - PR", "PAIÇANDU - PR", "PEABIRU - PR", "ROLÂNDIA - PR", "TELÊMACO BORBA - PR", "UBIRATÃ - PR",
    "DIADEMA - SP", "FERRAZ DE VASCONCELOS - SP", "GUARULHOS - SP", "ITAQUAQUECETUBA - SP", "MAUÁ - SP", "MOGI DAS CRUZES - SP", "POÁ - SP", "RIBEIRÃO PIRES - SP", "RIO GRANDE DA SERRA - SP", "SANTO ANDRÉ - SP", "SÃO BERNARDO DO CAMPO - SP", "SÃO PAULO - SP", "SUZANO - SP",
    "BERTIOGA - SP", "CAÇAPAVA - SP", "CARAGUATATUBA - SP", "CUBATÃO - SP", "GUARUJÁ - SP", "ILHABELA - SP", "ITANHAÉM - SP", "JACAREÍ - SP", "MONGAGUÁ - SP", "PERUÍBE - SP", "PRAIA GRANDE - SP", "SANTOS - SP", "SÃO JOSÉ DOS CAMPOS - SP", "SÃO SEBASTIÃO - SP", "SÃO VICENTE - SP", "TAUBATÉ - SP", "TREMEMBÉ - SP", "UBATUBA - SP"
    ]
CITIES_API_TERRITORIO_T5_T6_T7 = [
    "ARARUAMA - RJ", "ARMAÇÃO DOS BÚZIOS - RJ", "ARRAIAL DO CABO - RJ", "CABO FRIO - RJ", "CASIMIRO DE ABREU - RJ", "IGUABA GRANDE - RJ", "MACAÉ - RJ", "RIO DAS OSTRAS - RJ", "SÃO PEDRO DA ALDEIA - RJ", "SAQUAREMA - RJ",
    "ALÉM PARAÍBA - RJ", "BARRA DO PIRAÍ - RJ", "BARRA MANSA - RJ", "BOM JARDIM - RJ", "CACHOEIRAS DE MACACU - RJ", "CARMO - RJ", "COMENDADOR LEVY GASPARIAN - RJ", "GUAPIMIRIM - RJ", "ITAIPAVA - RJ", "ITATIAIA - RJ", "MAGÉ - RJ", "MIGUEL PEREIRA - RJ", "NOVA FRIBURGO - RJ", "PARAÍBA DO SUL - RJ", "PATY DO ALFERES - RJ", "PETRÓPOLIS - RJ", "PINHEIRAL - RJ", "PORTO REAL - RJ", "RESENDE - RJ", "SAPUCAIA - RJ", "SILVA JARDIM - RJ", "SUMIDOURO - RJ", "TERESÓPOLIS - RJ", "TRÊS RIOS - RJ", "VALENÇA - RJ", "VASSOURAS - RJ", "VOLTA REDONDA - RJ",
    "ANCHIETA - ES", "APERIBÉ - ES", "CACHOEIRO DE ITAPEMIRIM - ES", "CAMBUCI - ES", "CAMPOS DOS GOYTACAZES - ES", "CANTAGALO - ES", "CARIACICA - ES", "CATAGUASES - ES", "CORDEIRO - ES", "DUAS BARRAS - ES", "GUARAPARI - ES", "ITAOCARA - ES", "ITAPEMIRIM - ES", "ITAPERUNA - ES", "LAJE DO MURIAÉ - MG", "MACUCO - ES", "MARATAÍZES - ES", "MIRACEMA - ES", "MURIAÉ - ES", "PIÚMA - ES", "SANTO ANTÔNIO DE PÁDUA - ES", "SÃO FIDÉLIS - ES", "SÃO JOSÉ DE UBÁ - ES", "SERRA - ES", "VILA VELHA - ES", "VITÓRIA - ES"
]
CITIES_API_TERRITORIO_T8_T9 = [
    "AGUANIL - MG", "ALPINÓPOLIS - MG", "ARAXÁ - MG", "BOA ESPERANÇA - MG", "CAMPO DO MEIO - MG", "CAMPOS ALTOS - MG", "CAMPOS GERAIS - MG", "CARMO DO RIO CLARO - MG", "CONQUISTA - MG", "COQUEIRAL - MG", "COROMANDEL - MG", "CRISTAIS - MG", "DELTA - MG", "FORTALEZA DE MINAS - MG", "GUAPÉ - MG", "GUARANÉSIA - MG", "GUAXUPÉ - MG", "IBIÁ - MG", "ILICÍNEA - MG", "ITAÚ DE MINAS - MG", "JACUÍ - MG", "MONTE SANTO DE MINAS - MG", "NEPOMUCENO - MG", "NOVA PONTE - MG", "PASSOS - MG", "PEDRINÓPOLIS - MG", "PERDIZES - MG", "PRATÁPOLIS - MG", "PRATINHA - MG", "SACRAMENTO - MG", "SANTA JULIANA - MG", "SANTANA DA VARGEM - MG", "SÃO GOTARDO - MG", "SÃO JOÃO BATISTA DO GLÓRIA - MG", "SÃO JOSÉ DA BARRA - MG", "SÃO SEBASTIÃO DO PARAÍSO - MG", "SÃO TOMÁS DE AQUINO - MG", "SERRA DO SALITRE - MG", "TAPIRA - MG", "UBERABA - MG", "UBERLÂNDIA - MG",
    "ILTINÓPOLIS - SP", "ARAMINA - SP", "BRASÍLIA - DF", "FRANCA - SP", "GUARÁ - SP", "IGARAPAVA - SP", "IPUÃ - SP", "ITIRAPUÃ - SP", "ITUVERAVA - SP", "MORRO AGUDO - SP", "ORLÂNDIA - SP", "PATROCÍNIO PAULISTA - SP", "RIBEIRÃO PRETO - SP", "SÃO JOAQUIM DA BARRA - SP", "SÃO JOSÉ DA BELA VISTA - SP"
]
CITIES_API_TERRITORIO_T10_T12 = [
    "CARNAÍBA - PE", "CARPINA - PE", "CARUARU - PE", "FLORES - PE", "GOIANÁ - PE", "ILHA DE ITAMARACÁ - PE", "IPOJUCA - PE", "ITAPISSUMA - PE", "LIMOEIRO - PE", "MIRANDIBA - PE", "NAZARÉ DA MATA - PE", "OLINDA - PE", "PARNAMIRIM - PE", "PAUDALHO - PE", "PAULISTA - PE", "SALGUEIRO - PE", "SANTA CRUZ DO CAPIBARIBE - PE", "SERRA TALHADA - PE", "SURUBIM - PE", "TERRA NOVA - PE", "TIMBAÚBA - PE", "TORITAMA - PE", "VERDEJANTE - PE",
    "ACOPIARA - CE", "AIUABA - CE", "ANTONINA DO NORTE - CE", "ARARIPE - CE", "ARNEIROZ - CE", "ASSARÉ - CE", "BARBALHA - CE", "BREJO SANTO - CE", "CAMPOS SALES - CE", "CARIÚS - CE", "CATARINA - CE", "CEDRO - CE", "CRATEÚS - CE", "CRATO - CE", "FARIAS BRITO - CE", "ICÓ - CE", "IGUATU - CE", "INDEPENDÊNCIA - CE", "JATI - CE", "JUAZEIRO DO NORTE - CE", "JUCÁS - CE", "LAVRAS DA MANGABEIRA - CE", "MAURITI - CE", "MISSÃO VELHA - CE", "MOMBAÇA - CE", "ORÓS - CE", "PARAMBU - CE", "PIQUET CARNEIRO - CE", "PORTEIRAS - CE", "QUIXELÔ - CE", "SALITRE - CE", "TARRAFAS - CE", "TAUÁ - CE", "VÁRZEA ALEGRE - CE"
]
CITIES_API_TERRITORIO_T2_T11_T13_T14 = [
    "CAMPO GRANDE - MS", "DOURADOS - MS", 
    "ARACAJU - SE", "BARRA DOS COQUEIROS - SE", "CEDRO DE SÃO JOÃO - SE", "DIVINA PASTORA - SE", "ITAPORANGA D´AJUDA - SE", "JAPOATÃ - SE", "LAGARTO - SE", "LARANJEIRAS - SE", "NOSSA SENHORA DO SOCORRO - SE", "PACATUBA - SE", "PROPRIÁ - SE", "ROSÁRIO DO CATETE - SE", "SÃO CRISTÓVÃO - SE", "SIRIRI - SE", "TELHA - SE",
    "ALTOS - PI", "CAXIAS - MA", "PARAUAPEBAS - PA", "TERESINA - PI", "TIMON - MA",
    "CAUCAIA - CE", "FORTALEZA - CE", "MARACANAÚ - CE", "CARAÚ - CE", "AQUIRAZ - CE", "BEBERIBE - CE", "CAMOCIM - CE", "CASCAVEL - CE", "CRUZ - CE", "EUSÉBIO - CE", "FORTIM - CE", "FRECHEIRINHA - CE", "GRAÇA - CE", "GRANJA - CE", "IBIAPINA - CE", "ITAITINGA - CE", "ITAPIPOCA - CE", "ITAREMA - CE", "JIJOCA DE JERICOACOARA - CE", "LIMOEIRO DO NORTE - CE", "MARANGUAPE - CE", "MORADA NOVA - CE", "MUCAMBO - CE", "PACAJUS - CE", "PACATUBA - CE", "PACUJÁ - CE", "PARACURU - CE", "PARAIPABA - CE", "PARNAÍBA - CE", "PENTECOSTE - CE", "PINDORETAMA - CE", "QUIXADÁ - CE", "RUSSAS - CE", "SÃO BENEDITO - CE", "SÃO GONÇALO DO AMARANTE - CE", "SÃO LUÍS DO CURU - CE", "SOBRAL - CE", "TABULEIRO DO NORTE - CE", "TIANGUÁ - CE", "TRAIRI - CE", "UBAJARA - CE"
]
CITIES_API_TERRITORIO_ALTOS_PARNAIBA_TERESINA = [
    "ALTOS - PI", "PARNAÍBA - PI", "TERESINA - PI"
]
CITIES_API_TERRITORIO_CIDADES_ESPECIAIS_1 = [
    "SÃO JOÃO BATISTA DO GLÓRIA - MG"    
]
CITIES_API_TERRITORIO_CIDADES_ESPECIAIS_2 = [
    "ITAÚ DE MINAS - MG", "SÃO JOÃO BATISTA DO GLÓRIA - MG"
]
CITIES_API_TERRITORIO_CIDADES_ESPECIAIS_3 = [
    "ITAÚ DE MINAS - MG"
]

# CIDADES DA OPERADORA DESKTOP - INTERNET

CITIES_API_DESKTOP_FERRO = ["SANTA CRUZ DAS PALMEIRAS - SP", "AGUAÍ - SP", "ARTHUR NOGUEIRA - SP", "CAFELÂNDIA - SP", "CASA BRANCA - SP", "COSMÓPOLIS - SP", "ESTIVA GERBI - SP", "INDAIATUBA - SP", "ITUPEVA - SP", "LINS - SP"]
CITIES_API_DESKTOP_BRONZE = ["SÃO JOSÉ DOS CAMPOS - SP","ÁGUAS DE SANTA BÁRBARA - SP", "AGUDOS - SP", "ALUMÍNIO - SP", "AMERICANA - SP", "AMÉRICO BRASILIENSE - SP", "AMPARO - SP", "ANGATUBA - SP", "ARAÇARIGUAMA - SP", "ARAÇOIABA DA SERRA - SP", "ARANDU - SP", "ARARAQUARA - SP", "ARARAS - SP", "AREALVA - SP", "AREIÓPOLIS - SP", "ATIBAIA - SP", "AVAÍ - SP", "AVARÉ - SP", "BARRA BONITA - SP", "BAURU - SP", "BIRITIBA-MIRIM - SP", "BOA ESPERANÇA DO SUL - SP", "BOCAINA - SP", "BOFETE - SP", "BOITUVA - SP", "BOM JESUS DOS PERDÕES - SP", "BORBOREMA - SP", "BOREBI - SP", "BOTUCATU - SP", "BRAGANÇA PAULISTA - SP", "CABREÚVA - SP", "CAÇAPAVA - SP", "CAIEIRAS - SP", "CAMPINA DO MONTE ALEGRE - SP", "CAMPINAS - SP", "CAMPO LIMPO PAULISTA - SP", "CÂNDIDO RODRIGUES - SP", "CAPELA DO ALTO - SP", "CAPIVARI - SP", "CERQUEIRA CÉSAR - SP", "CERQUILHO - SP", "CESÁRIO LANGE - SP", "COLINA - SP", "CONCHAL - SP", "CONCHAS - SP", "CORDEIRÓPOLIS - SP", "CRISTAIS PAULISTA - SP", "DOBRADA - SP", "DOIS CÓRREGOS - SP", "DOURADO - SP", "ELIAS FAUSTO - SP", "ENGENHEIRO COELHO - SP", "FERNANDO PRESTES - SP", "FRANCA - SP", "FRANCISCO MORATO - SP", "FRANCO DA ROCHA - SP", "GAVIÃO PEIXOTO - SP", "GUAÍRA - SP", "GUARANTÃ - SP", "GUARAREMA - SP", "GUARIBA - SP", "GUARUJÁ - SP", "GUATAPARÁ - SP", "HOLAMBRA - SP", "HORTOLÂNDIA - SP", "LARAS - SP", "IBATÉ - SP", "IBITINGA - SP", "IGARAÇU DO TIETÊ - SP", "IGARATÁ - SP", "IPERÓ - SP", "IRACEMÁPOLIS - SP", "ITAÍ - SP", "ITAJOBI - SP", "ITAJU - SP", "ITANHAÉM - SP", "ITAPUÍ - SP", "ITATINGA - SP", "ITIRAPUÃ - SP", "ITU - SP", "JABORANDI - SP", "JABOTICABAL - SP", "JACAREÍ - SP", "JAGUARIÚNA - SP", "JARINU - SP", "JAÚ - SP", "JUMIRIM - SP", "JUNDIAÍ - SP", "LARANJAL PAULISTA - SP", "LENÇÓIS PAULISTA - SP", "LINDÓIA - SP", "LOUVEIRA - SP", "MACATUBA - SP", "MAIRIPORÃ - SP", "MANDURI - SP", "MATÃO - SP", "MINEIROS DO TIETÊ - SP", "MOGI DAS CRUZES - SP", "MONTE MOR - SP", "MOTUCA - SP", "NAZARÉ PAULISTA - SP", "NOVA EUROPA - SP", "NOVA ODESSA - SP", "ÓLEO - SP", "PARANAPANEMA - SP", "PARDINHO - SP", "PATROCÍNIO PAULISTA - SP", "PAULÍNIA - SP", "PEDERNEIRAS - SP", "PEDREIRA - SP", "PEREIRAS - SP", "PINDORAMA - SP", "PIRACAIA - SP", "PIRACICABA - SP", "PIRATININGA - SP", "PITANGUEIRAS - SP", "PORANGABA - SP", "PRAIA GRANDE - SP", "PRATÂNIA - SP", "PRESIDENTE ALVES - SP", "QUADRA - SP", "RAFARD - SP", "RIBEIRÃO BONITO - SP", "RIBEIRÃO CORRENTE - SP", "RIBEIRÃO PRETO - SP", "RINCÃO - SP", "RIO CLARO - SP", "RIO DAS PEDRAS - SP", "SALESÓPOLIS - SP", "SALTINHO - SP", "SALTO DE PIRAPORA - SP", "SANTA ADÉLIA - SP", "SANTA BÁRBARA D’OESTE - SP", "ITAPETININGA - SP", "ITÁPOLIS - SP", "SANTA ERNESTINA - SP", "SANTA GERTRUDES - SP", "SANTA LÚCIA - SP", "SANTO ANTÔNIO DE POSSE - SP", "SANTOS - SP", "SÃO CARLOS - SP", "SÃO MANUEL - SP", "SÃO VICENTE - SP", "SARAPUÍ - SP", "SERRA AZUL - SP", "SERRA NEGRA - SP", "SOROCABA - SP", "SUMARÉ - SP", "TABATINGA - SP", "TATUÍ - SP", "TAUBATÉ - SP", "TIETÊ - SP", "TRABIJU - SP", "TREMEMBÉ - SP", "VALINHOS - SP", "VÁRZEA PAULISTA - SP", "VINHEDO - SP", "VOTORANTIM - SP"]
CITIES_API_DESKTOP_PRATA = ["BÁLSAMO - SP", "BARRETOS - SP", "OLÍMPIA - SP"]
CITIS_API_DESKTOP_OURO = ["BEBEDOURO - SP"]
CITIS_API_DESKTOP_PLATINA = ["CEDRAL - SP", "CRAVINHOS - SP", "CUBATÃO - SP", "DESCALVADO - SP", "LEME - SP", "LIMEIRA - SP", "MIRASSOL - SP", "MOGI GUAÇU - SP", "MOGI MIRIM - SP", "MONGAGUÁ - SP", "MONTE ALEGRE DO SUL - SP", "MONTE ALTO - SP", "PERUÍBE - SP", "PILAR DO SUL - SP", "PIRASSUNUNGA - SP", "PORTO FERREIRA - SP", "SANTA RITA DO PASSA QUATRO - SP", "SÃO JOSÉ DO RIO PRETO - SP",  "TAMBAÚ - SP"]
CITIS_API_DESKTOP_DIAMANTE = ["SÃO PAULO - SP"]
CITIS_API_DESKTOP_ASCENDENTE = ["SANTA BRANCA - SP"]


def get_api_url_desktop(cidade):
    if cidade in CITIES_API_DESKTOP_FERRO:
        return "https://falasolucoes-workflow-solucoes.ywsa8i.easypanel.host/webhook/workflow_desktop_ferro"
    elif cidade in CITIES_API_DESKTOP_BRONZE:
        return "https://falasolucoes-workflow-solucoes.ywsa8i.easypanel.host/webhook/workflow_desktop_bronze"
    elif cidade in CITIES_API_DESKTOP_PRATA:
        return "https://falasolucoes-workflow-solucoes.ywsa8i.easypanel.host/webhook/workflow_desktop_prata"
    elif cidade in CITIS_API_DESKTOP_OURO:
        return "https://falasolucoes-workflow-solucoes.ywsa8i.easypanel.host/webhook/workflow_desktop_ouro"
    elif cidade in CITIS_API_DESKTOP_PLATINA:
        return "https://falasolucoes-workflow-solucoes.ywsa8i.easypanel.host/webhook/workflow_desktop_platina"
    elif cidade in CITIS_API_DESKTOP_DIAMANTE:
        return "https://falasolucoes-workflow-solucoes.ywsa8i.easypanel.host/webhook/workflow_desktop_diamante"
    elif cidade in CITIS_API_DESKTOP_ASCENDENTE:
        return "https://falasolucoes-workflow-solucoes.ywsa8i.easypanel.host/webhook/workflow_desktop_ascedente"
    else: 
        return None


def get_api_url_giga(cidade):
    if cidade in CITIES_API_TERRITORIO_T1_T3_T4:
        return "https://falasolucoes-workflow-solucoes.ywsa8i.easypanel.host/webhook/workflowt1_t3_t4"
    elif cidade in CITIES_API_TERRITORIO_T5_T6_T7:
        return "https://falasolucoes-workflow-solucoes.ywsa8i.easypanel.host/webhook/workflowt5_t6_t7"
    elif cidade in CITIES_API_TERRITORIO_T8_T9:
        return "https://falasolucoes-workflow-solucoes.ywsa8i.easypanel.host/webhook/workflowt8_t9"
    elif cidade in CITIES_API_TERRITORIO_T10_T12:
        return "https://falasolucoes-workflow-solucoes.ywsa8i.easypanel.host/webhook/workflowt10_t12"
    elif cidade in CITIES_API_TERRITORIO_T2_T11_T13_T14:
        return "https://falasolucoes-workflow-solucoes.ywsa8i.easypanel.host/webhook/workflowt2_t11_t13_t14"
    elif cidade in CITIES_API_TERRITORIO_ALTOS_PARNAIBA_TERESINA:
        return "https://falasolucoes-workflow-solucoes.ywsa8i.easypanel.host/webhook/workflowt_ALTOS_PARNAIBA_TERESINA"
    elif cidade in CITIES_API_TERRITORIO_CIDADES_ESPECIAIS_1:
        return "https://falasolucoes-workflow-solucoes.ywsa8i.easypanel.host/webhook/workflowt_CIDADES_ESPECIAIS_1"
    elif cidade in CITIES_API_TERRITORIO_CIDADES_ESPECIAIS_2:
        return "https://falasolucoes-workflow-solucoes.ywsa8i.easypanel.host/webhook/workflowt_CIDADES_ESPECIAIS_2"
    elif cidade in CITIES_API_TERRITORIO_CIDADES_ESPECIAIS_3:
        return "https://falasolucoes-workflow-solucoes.ywsa8i.easypanel.host/webhook/workflowt_CIDADES_ESPECIAIS_3"
    else: 
        return None

def get_api_url_vero(cidade):
    if cidade in CITIES_API_OURO:
        return "https://falasolucoes-workflow-solucoes.ywsa8i.easypanel.host/webhook/workflowouro"
    elif cidade in CITIES_API_PADRAO:
        return "https://falasolucoes-workflow-solucoes.ywsa8i.easypanel.host/webhook/workflowpadrao"
    elif cidade in CITIES_API_REDE_NEUTRA:
        return "https://falasolucoes-workflow-solucoes.ywsa8i.easypanel.host/webhook/workflowredeneutra"
    elif cidade in CITIES_API_PRATA:
        return "https://falasolucoes-workflow-solucoes.ywsa8i.easypanel.host/webhook/workflowprata"
    else:
        return None  


def atualizar_campo_no_crm(dados):
    pass

def atualizar_campo_e_chamar_api_desktop(cidade, entity_id):

    atualizar_campo_no_crm(entity_id)

    url_api = get_api_url_desktop(cidade)
    
    if url_api:
        response = requests.post(f"{url_api}?deal_id={entity_id}", json={"cidade": cidade})
        return response.json()  
    else:
        return {"error": "Cidade não mapeada"}
        

def atualizar_campo_e_chamar_api_giga(cidade, entity_id):
    
    atualizar_campo_no_crm(entity_id)
    
    
    url_api = get_api_url_giga(cidade)
    
    if url_api:
        response = requests.post(f"{url_api}?deal_id={entity_id}", json={"cidade": cidade})
        return response.json() 
    else:
        return {"error": "Cidade não mapeada"}
        

def atualizar_campo_e_chamar_api_vero(cidade, entity_id):
    
    atualizar_campo_no_crm(entity_id)
    
    
    url_api = get_api_url_vero(cidade)
    
    if url_api:
        response = requests.post(f"{url_api}?deal_id={entity_id}", json={"cidade": cidade})
        return response.json()
    else:
        return {"error": "Cidade não mapeada"}



def make_request_with_retries(method, url, **kwargs):
    max_retries = 5  
    for attempt in range(max_retries):
        try:
            response = requests.request(method, url, **kwargs)
            if response.status_code in [200, 201]:  
                return response
            else:
                log_erro(f"Erro {response.status_code} na tentativa {attempt + 1}", response.text)
        except requests.exceptions.RequestException as e:
            log_erro("Erro de conexão", e)
        time.sleep(2)  
    return None


def handle_request_errors(response, error_message, details=None):
    if response is None or response.status_code >= 400:
        return jsonify({"error": error_message, "details": details or response.text if response else "Nenhuma resposta"}), 400



@app.route('/update-plan-desktop/<string:entity_id>', methods=['POST'])
def update_plan_desktop(entity_id):
    try:
        get_deal_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.get"
        get_deal_response = make_request_with_retries('GET', get_deal_url, params={"id": entity_id})
        handle_request_errors(get_deal_response, "Falha ao buscar os dados da negociação")
        get_deal_data = get_deal_response.json()

        field_id = get_deal_data['result'].get("UF_CRM_1709042046")
        if not field_id:
            return jsonify({"error": "Campo Cidade List está vazio"}), 400

        get_fields_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.fields"
        get_fields_response = make_request_with_retries('GET', get_fields_url)
        handle_request_errors(get_fields_response, "Falha ao buscar os campos disponíveis")
        get_fields_data = get_fields_response.json()

        fields_items = get_fields_data['result'].get("UF_CRM_1709042046", {}).get("items", [])
        matched_item = next((item for item in fields_items if item["ID"] == field_id), None)
        if not matched_item:
            return jsonify({"error": f"ID {field_id} não encontrado na lista de itens do campo"}), 400

        value_to_update = matched_item["VALUE"]

        update_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.update"
        update_response = make_request_with_retries('POST', update_url, json={
            "id": entity_id,
            "fields": {"UF_CRM_1733493949": value_to_update}
        })
        handle_request_errors(update_response, "Falha ao atualizar o campo")
        
        api_response = atualizar_campo_e_chamar_api_desktop(value_to_update, entity_id)
        return jsonify({"message": "Campo atualizado com sucesso!", "value": value_to_update, "api_response": api_response}), 200

    except Exception as e:
        log_erro("Erro interno", e)
        return jsonify({"error": "Erro interno no servidor", "details": str(e)}), 500


@app.route('/update-plan-giga/<string:entity_id>', methods=['POST'])
def update_plan_giga(entity_id):
    try:
        get_deal_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.get"
        get_deal_response = make_request_with_retries('GET', get_deal_url, params={"id": entity_id})
        handle_request_errors(get_deal_response, "Falha ao buscar os dados da negociação")
        get_deal_data = get_deal_response.json()

        field_id = get_deal_data['result'].get("UF_CRM_1709042046")
        if not field_id:
            return jsonify({"error": "Campo Cidade List está vazio"}), 400

        get_fields_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.fields"
        get_fields_response = make_request_with_retries('GET', get_fields_url)
        handle_request_errors(get_fields_response, "Falha ao buscar os campos disponíveis")
        get_fields_data = get_fields_response.json()

        fields_items = get_fields_data['result'].get("UF_CRM_1709042046", {}).get("items", [])
        matched_item = next((item for item in fields_items if item["ID"] == field_id), None)
        
        value_to_update = matched_item["VALUE"] if matched_item else None

        update_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.update"
        update_response = make_request_with_retries('POST', update_url, json={
            "id": entity_id,
            "fields": {"UF_CRM_1733493949": value_to_update}
        })
        handle_request_errors(update_response, "Falha ao atualizar o campo")
        
        api_response = atualizar_campo_e_chamar_api_giga(value_to_update, entity_id)
        return jsonify({"message": "Campo atualizado com sucesso!", "value": value_to_update, "api_response": api_response}), 200

    except Exception as e:
        log_erro("Erro interno", e)
        return jsonify({"error": "Erro interno no servidor", "details": str(e)}), 500


@app.route('/update-plan-vero/<string:entity_id>', methods=['POST'])
def update_plan_vero(entity_id):
    try:
        get_deal_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.get"
        get_deal_response = make_request_with_retries('GET', get_deal_url, params={"id": entity_id})
        handle_request_errors(get_deal_response, "Falha ao buscar os dados da negociação")
        get_deal_data = get_deal_response.json()

        field_id = get_deal_data['result'].get("UF_CRM_1709042046")
        if not field_id:
            return jsonify({"error": "Campo Cidade List está vazio"}), 400

        get_fields_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.fields"
        get_fields_response = make_request_with_retries('GET', get_fields_url)
        handle_request_errors(get_fields_response, "Falha ao buscar os campos disponíveis")
        get_fields_data = get_fields_response.json()

        fields_items = get_fields_data['result'].get("UF_CRM_1709042046", {}).get("items", [])
        matched_item = next((item for item in fields_items if item["ID"] == field_id), None)
        
        value_to_update = matched_item["VALUE"] if matched_item else None

        update_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.update"
        update_response = make_request_with_retries('POST', update_url, json={
            "id": entity_id,
            "fields": {"UF_CRM_1733493949": value_to_update}
        })
        handle_request_errors(update_response, "Falha ao atualizar o campo")
        
        api_response = atualizar_campo_e_chamar_api_vero(value_to_update, entity_id)
        return jsonify({"message": "Campo atualizado com sucesso!", "value": value_to_update, "api_response": api_response}), 200

    except Exception as e:
        log_erro("Erro interno", e)
        return jsonify({"error": "Erro interno no servidor", "details": str(e)}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5711)
