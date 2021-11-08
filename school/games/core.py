def is_ce1(user):
    return user.groups.filter(name='CE1').exists()


def is_ce2(user):
    return user.groups.filter(name='CE2').exists()


def is_cm1(user):
    return user.groups.filter(name='CM1').exists()


def is_cm2(user):
    return user.groups.filter(name='CM2').exists()


def is_eleve(user):
    return user.groups.filter(name='ELEVE').exists()


def is_enseignant(user):
    return user.groups.filter(name='ENSEIGNANT').exists()


def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()