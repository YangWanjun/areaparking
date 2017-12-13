from master.models import Company


def get_company_context():
    """テンプレートに出力する自社情報

    :return:
    """
    company = Company.get_company()
    if company:
        return {
            'company_name': company.name,
            'company_post_code': company.post_code or '',
            'company_address1': company.address1 or '',
            'company_address2': company.address2 or '',
            'company_tel': company.tel or '',
            'company_fax': company.fax or '',
            'company_email': company.email or '',
        }
    else:
        return dict()


def get_parking_lot_context(parking_lot):
    if parking_lot:
        return {
            'parking_lot_name': parking_lot.name,
        }
    else:
        return dict()


def get_contractor_context(contractor):
    if contractor:
        return {
            'user_name': contractor.name,
            'user_tel': contractor.tel,
            'user_fax': contractor.fax,
            'user_email': contractor.email,
            'user_address1': contractor.address1,
            'user_address2': contractor.address2,
        }
    else:
        return dict()
