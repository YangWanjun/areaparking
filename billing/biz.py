from django.db.models import ObjectDoesNotExist

from . import models


def load_transfer_data(data_bytes, user):
    header = None
    for line in data_bytes.splitlines():
        if line:
            line = line.decode('cp932')
            if header is None and models.TransferHeader.is_header(line):
                header = models.TransferHeader.parse_header(line, user)
                header.save()
            elif models.TransferHeader.is_detail(line):
                detail = header.parse_detail(line)
                detail.save()
    return header


def execute_transfer_details(selected_details):
    """入金データ読み込み後、完全一致した振込明細情報を入金済みと登録する。

    :param selected_details:
    :return:
    """
    detail_id_list = []
    for detail_id in selected_details:
        try:
            detail = models.VTransferDetail.objects.get(pk=detail_id)
            if detail.contractor and detail.detail:
                models.ContractorTransfer.objects.create(contractor=detail.contractor, transfer_detail=detail.detail)
                continue
        except ObjectDoesNotExist:
            pass
        detail_id_list.append(detail_id)
    return detail_id_list
