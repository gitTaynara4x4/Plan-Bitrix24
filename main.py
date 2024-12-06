from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import os



app = Flask(__name__)
app = Flask(__name__)



load_dotenv()
CODIGO_BITRIX = os.getenv('CODIGO_BITRIX')
CODIGO_BITRIX_STR = os.getenv('CODIGO_BITRIX_STR')
PROFILE = os.getenv('PROFILE')
BASE_URL_API_BITRIX = os.getenv('BASE_URL_API_BITRIX')



BITRIX_WEBHOOK_URL = f"{BASE_URL_API_BITRIX}/{PROFILE}/{CODIGO_BITRIX}/"


@app.route('/update-plan/<string:entity_id>', methods=['GET'])
def update_plan(entity_id):
    try:
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

        update_url = f"{BITRIX_WEBHOOK_URL}/crm.deal.update"
        update_response = requests.post(update_url, json={
            "id": entity_id,
            "fields": {
                "UF_CRM_1733493949": value_to_update
            }
        })
        
        update_data = update_response.json()

        if update_data.get("result") == True:
            return jsonify({"message": "Campo atualizado com sucesso!", "value": value_to_update}), 200
        else:
            return jsonify({"error": "Falha ao atualizar o campo", "details": update_data}), 400

    except Exception as e:
        return jsonify({"error": "Erro interno", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=57)
