from dadata import DadataAsync
from config.settings import settings

async def get_lpr_by_inn(inn: str) -> dict:
    """
    Ищет компанию или ИП по ИНН через официальный метод findById/party.
    Возвращает словарь с названием, ФИО и должностью ЛПР.
    """
    lpr_data = {
        "company_name": "",
        "surname": "",
        "name": "",
        "patronymic": "",
        "position": ""
    }
    
    async with DadataAsync(settings.dadata_token) as dadata:
        # branch_type="MAIN" гарантирует получение головной организации
        results = await dadata.find_by_id("party", inn, branch_type="MAIN")
        
        if not results:
            return lpr_data
            
        data = results[0].get("data", {})
        
        # 1. Название компании
        name_block = data.get("name", {})
        lpr_data["company_name"] = name_block.get("short_with_opf") or results[0].get("value", "")

        # 2. Если это Юридическое лицо (ООО, АО и т.д.)
        if data.get("type") == "LEGAL":
            # Приоритет 1: забираем из структурированного блока managers
            managers = data.get("managers")
            if managers and len(managers) > 0:
                manager = managers[0]
                fio = manager.get("fio", {})
                lpr_data["surname"] = fio.get("surname", "")
                lpr_data["name"] = fio.get("name", "")
                lpr_data["patronymic"] = fio.get("patronymic", "")
                lpr_data["position"] = manager.get("post", "")
            
            # Приоритет 2: запасной вариант через блок management
            elif data.get("management"):
                mgmt = data["management"]
                lpr_data["position"] = mgmt.get("post", "")
                full_name = mgmt.get("name", "").split()
                if len(full_name) >= 3:
                    lpr_data["surname"] = full_name[0]
                    lpr_data["name"] = full_name[1]
                    lpr_data["patronymic"] = full_name[2]
                elif len(full_name) == 2:
                    lpr_data["surname"] = full_name[0]
                    lpr_data["name"] = full_name[1]

        # 3. Если это ИП (Индивидуальный предприниматель)
        elif data.get("type") == "INDIVIDUAL":
            fio = data.get("fio", {})
            lpr_data["surname"] = fio.get("surname", "")
            lpr_data["name"] = fio.get("name", "")
            lpr_data["patronymic"] = fio.get("patronymic", "")
            lpr_data["position"] = "Индивидуальный предприниматель"

    return lpr_data