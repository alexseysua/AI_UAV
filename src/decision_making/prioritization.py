
def prioritize(results):
    list_objects = results.names
    list_conf = results.boxes.conf
    l_afv = []
    l_car = []
    l_bike = []
    l_worm = []

    ind_prior_obj = 0

    for i in range(len(list_objects)):
        match list_objects[i][0]:
            case "AFV":
                l_afv.append([list_objects[i][0], i])
            case "CAR":
                l_car.append([list_objects[i][0], i])
            case "BIKE":
                l_bike.append([list_objects[i][0], i])
            case "WORM":
                l_worm.append([list_objects[i][0], i])

    prev_conf = 0
    if len(l_afv) != 0:
        for o in l_afv:
            if prev_conf == 0:
                prev_conf = list_conf[o[1]]
                ind_prior_obj = o[1]
            elif prev_conf < list_conf[o[1]]:
                ind_prior_obj = o[1]
    elif len(l_car) != 0:
        for o in l_car:
            if prev_conf == 0:
                prev_conf = list_conf[o[1]]
                ind_prior_obj = o[1]
            elif prev_conf < list_conf[o[1]]:
                ind_prior_obj = o[1]
    elif len(l_bike) != 0:
        for o in l_bike:
            if prev_conf == 0:
                prev_conf = list_conf[o[1]]
                ind_prior_obj = o[1]
            elif prev_conf < list_conf[o[1]]:
                ind_prior_obj = o[1]
    else:
        for o in l_worm:
            if prev_conf == 0:
                prev_conf = list_conf[o[1]]
                ind_prior_obj = o[1]
            elif prev_conf < list_conf[o[1]]:
                ind_prior_obj = o[1]

    return list_objects[ind_prior_obj]
