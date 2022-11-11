__CPU__ = "CPU"
__MOTHERBOARD__ = "MB"
__RAM__ = "RAM"
__HDD__ = "HDD"
__SSD__ = "SSD"
__STORAGE__ = "STORAGE"
__GPU__ = "GPU"
__PSU__ = "PSU"
__CASE__ = "CASE"

def get_type(key):
    if key == 'processors': return __CPU__
    if key == 'cases': return __CASE__
    if key == 'graphics_cards': return __GPU__
    if key == 'storage': return __STORAGE__
    if key == 'motherboards': return __MOTHERBOARD__
    if key == 'power_supplies': return __PSU__
    if key == 'ram': return __RAM__
    if key == 'hard_drives': return __HDD__
    if key == 'solid_state_drives': return __SSD__

    return "UNKNOWN"