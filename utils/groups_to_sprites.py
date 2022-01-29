from .flatten import flatten


def groups_to_sprites(group_list):
    return flatten([group.sprites() for group in group_list])
