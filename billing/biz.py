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
