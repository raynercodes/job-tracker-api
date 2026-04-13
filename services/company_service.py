from repos.company_repo import list_companies_by_users, get_company_by_name_for_user, create_company
from datetime import datetime, UTC
from utils.logger import logger

def create_company_for_user(user_id, company_name):
    company_name = (company_name or "").strip().lower()

    if not company_name:
        raise ValueError("Company name cannot be empty")
    
    if len(company_name) < 3:
        raise ValueError("Company name must be at least 3 characters")
    
    existing = get_company_by_name_for_user(user_id, company_name)

    if existing:
        logger.warning(f"Company already exists company_name={company_name} user_id={user_id}")
        raise ValueError("Company already exists")

    created_at = datetime.now(UTC).isoformat()

    create_company(user_id, company_name, created_at)
    logger.info(f"Company created user_id={user_id} company_name={company_name}")

def get_companies_for_user(user_id):
    rows = list_companies_by_users(user_id)

    companies = [
        {
            "id": row[0],
            "user_id": row[1],
            "company_name": row[2],
            "created_at": row[3]
        }
        for row in rows
    ]

    logger.info(f"Companies retrieved successfully user_id={user_id}")
    return companies