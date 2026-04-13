from repos.application_repo import create_application, get_application_by_id_for_user_repo, update_application_for_user_repo, delete_application_for_user_repo, list_applications_by_user_with_filters_repo, get_application_stats_for_user_repo
from repos.company_repo import get_company_by_id_for_user
from datetime import datetime, UTC
from utils.logger import logger

ALLOWED_STATUSES = {"applied", "under_review", "interview", "offer", "rejected"}

def create_application_for_user(user_id, company_id, job_title, notes=None, status=None, applied_at=None):
    if company_id is None:
        logger.warning("Company id is required")
        raise ValueError("Company id is required")
    
    try:
        company_id = int(company_id)
    except (TypeError, ValueError):
        raise ValueError("Company id must be a valid integer")
    
    if not job_title or not str(job_title).strip():
        raise ValueError("Job title is required")
    
    job_title = str(job_title).strip()
    notes = (notes or "").strip()

    company = get_company_by_id_for_user(user_id, company_id)
    if not company:
        logger.warning(f"Company not found company_id={company_id}")
        raise ValueError("Company not found")
    
    if not status:
        status = "applied"
    else:
        status = str(status).strip().lower()

    if status not in ALLOWED_STATUSES:
        logger.warning(f"Invalid application status status={status}")
        raise ValueError("Invalid application status")
    
    if not applied_at:
        applied_at = datetime.now(UTC).isoformat()

    created_at = datetime.now(UTC).isoformat()

    create_application(user_id, company_id, job_title, notes, status, applied_at, created_at)
    logger.info(f"Application created successfully job_title={job_title} status={status} user_id={user_id}")

    return {
        "company_id": company_id,
        "job_title": job_title,
        "status": status
    }

def get_applications_for_user(user_id, status=None, company_id=None):
    if status is not None:
        status = str(status).strip().lower()
        if status not in ALLOWED_STATUSES:
            logger.warning(f"Invalid application status status={status}")
            raise ValueError("Invalid application status")
    
    if company_id is not None:
        try:
            company_id = int(company_id)
        except (TypeError, ValueError):
            raise ValueError("Company id must be a valid integer")
        
        company = get_company_by_id_for_user(user_id, company_id)
        if company is None:
            logger.warning(f"Company not found company_id={company_id}")
            raise ValueError("Company not found")
    
    rows = list_applications_by_user_with_filters_repo(user_id, status, company_id)

    applications = [
        {
            "id": row[0],
            "user_id": row[1],
            "company_id": row[2],
            "company_name": row[3],
            "job_title": row[4],
            "notes": row[5],
            "status": row[6],
            "applied_at": row[7],
            "created_at": row[8]

        }
        for row in rows
    ]
    logger.info(
        f"Applications fetched user_id={user_id} status={status} company_id={company_id} count={len(applications)}"
    )

    return applications

def get_applications_by_id(user_id, application_id):
    try:
        application_id = int(application_id)
    except (TypeError, ValueError):
        raise ValueError("Application id must be a valid integer")

    row = get_application_by_id_for_user_repo(user_id, application_id)

    if row is None:
        logger.warning(f"Application not found application_id={application_id} user_id={user_id}")
        raise ValueError("Application not found")

    application = {
        "id": row[0],
        "user_id": row[1],
        "company_id": row[2],
        "company_name": row[3],
        "job_title": row[4],
        "notes": row[5],
        "status": row[6],
        "applied_at": row[7],
        "created_at": row[8]
    }
    
    logger.info(f"Application retrieved application_id={application_id} user_id={user_id}")
    return application

def update_application_for_user(user_id, application_id, company_id=None, job_title=None, notes=None, status=None, applied_at=None):
    row = get_application_by_id_for_user_repo(user_id, application_id)

    if row is None:
        logger.warning(f"Application not found application_id={application_id} user_id={user_id}")
        raise ValueError("Application not found")
    
    try:
        application_id = int(application_id)
    except (TypeError, ValueError):
        raise ValueError("Application id must be a valid integer")
    
    current_company_id = row[2]
    current_job_title = row[4]
    current_notes = row[5]
    current_status = row[6]
    current_applied_at = row[7]

    if company_id is not None:
        try:
            company_id = int(company_id)
        except (TypeError, ValueError):
            raise ValueError("Company id must be a valid integer")
    
        company = get_company_by_id_for_user(user_id, company_id)

        if not company:
            logger.warning(f"Company not found company_id={company_id} user_id={user_id}")
            raise ValueError("Company not found")
    else:
        company_id = current_company_id

    if job_title is not None:
        job_title = str(job_title).strip()
        if not job_title:
            raise ValueError("Job title can not be empty")
    else:
        job_title = current_job_title

    if notes is not None:
        notes = str(notes).strip()
    else:
        notes = current_notes

    if status is not None:
        status = str(status).strip().lower()
        if status not in ALLOWED_STATUSES:
            logger.warning(f"Invalid application status status={status} user_id={user_id}")
            raise ValueError("Invalid application status")
    else:
        status = current_status

    if applied_at is None:
        applied_at = current_applied_at

    update_application_for_user_repo(
        user_id,
        application_id,
        company_id,
        job_title,
        notes,
        status,
        applied_at
    )

    logger.info(f"Application updated application_id={application_id} company_id={company_id} user_id={user_id}")
    return {"message": "Application updated successfully"}

def delete_application_for_user_service(user_id, application_id):
    row = get_application_by_id_for_user_repo(user_id, application_id)

    if row is None:
        logger.warning(f"Application not found application_id={application_id} user_id={user_id}")
        raise ValueError("Application not found")
    
    delete_application_for_user_repo(user_id, application_id)

    logger.info(f"Application deleted application_id={application_id} user_id={user_id}")
    return {"application_id": application_id}

def get_application_stats_for_user_service(user_id):
    rows = get_application_stats_for_user_repo(user_id)

    stats = {
        "applied": 0,
        "under_review": 0,
        "interview": 0,
        "offer": 0,
        "rejected": 0
    }

    for row in rows:
        status = row[0]
        count = row[1]
        stats[status] = count
    
    logger.info(f"Application stats retrieved user_id={user_id}")
    return stats