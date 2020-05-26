from backend.db_grps import get_groupinfo_db
from const.con_classes import STATUS


def valid_open_regstr(grps: list):
	for grp in grps:
		if get_groupinfo_db(grp)['status'] in (STATUS.LIST_PUBLISHED, STATUS.REGISTRATION_OPEN):
			return False
	return True


def valid_create_list(grps: list):
	for grp in grps:
		if get_groupinfo_db(grp)['status'] in (STATUS.LIST_PUBLISHED, STATUS.LIST_DELETED, STATUS.NEW):
			return False
	return True


def valid_del_list(grps: list):
	for grp in grps:
		if get_groupinfo_db(grp)['status'] in (STATUS.LIST_DELETED, STATUS.NEW, STATUS.REGISTRATION_OPEN):
			return False
	return True