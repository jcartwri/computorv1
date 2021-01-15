def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def get_argument(polynom):
    flag_plus = False
    flag_minus = False
    flag_number = False
    flag_star = False
    flag_equal = False
    flag_begin = True
    number = 0
    error_polynom = {'mas' :[], 'k' : 0}

    dict_x = {'X^0': [], 'X^1': [], 'X^2': []}

    for i in polynom.split():
        if i == '=' and not flag_star:
            flag_equal = True if not flag_equal else exit()
            if flag_number:
                dict_x['X^0'].append(number)
            flag_minus = False
            flag_plus = True
            flag_number = False
            flag_begin = True
            continue
        if i == '+' and not flag_star:
            if flag_number:
                dict_x['X^0'].append(-number if flag_equal else number)
                flag_plus = False
                flag_minus = False
                flag_number = False
            elif flag_minus or flag_plus:
                print("Error, Cann't to be 2 sign in a row")
                exit()
            flag_plus = True if not flag_plus else exit()
            flag_begin = False
            continue
        if i == '-' and not flag_star:
            if flag_number:
                dict_x['X^0'].append(-number if flag_equal else number)
                flag_plus = False
                flag_minus = False
                flag_number = False
            elif flag_minus or flag_plus:
                print("Error, Cann't to be 2 sign in a row")
                exit()
            flag_minus = True if not flag_plus and not flag_minus else exit()
            flag_begin = False
            continue
        if isfloat(i) and (flag_plus or flag_minus or flag_begin):
            if i[0] == '-':
                print('Error <{}>, must not be minus, enter space between minus and number'.format(i))
                exit()
            var = (-1) * float(i) if flag_minus else float(i)
            if flag_number:
                number *= var
                flag_star = False
            else:
                number = var
            flag_number = True
            flag_begin = False
            continue
        if i == '*' and flag_number:
            flag_star = True
            continue
        if i and ((i[0:2] and i[0:2] == 'X^') or i == 'X') and (flag_number or flag_plus or flag_minus or flag_begin):
            if not i[2:].isdigit():
                print('Error with <{}>'.format(i))
            if flag_number:
                if not flag_star:
                    exit()
            if not flag_number:
                number = 1
            number = -number if flag_equal else number
            if i == 'X^0':
                dict_x['X^0'].append(number)
            elif i == 'X^1' or i == 'X':
                dict_x['X^1'].append(number)
            elif i == 'X^2':
                dict_x['X^2'].append(number)
            else:
                if i in dict_x.keys():
                    dict_x[i].append(number)
                else:
                    dict_x[i] = [number]
                if error_polynom['k'] < int(i[2:]):
                    error_polynom['k'] = int(i[2:])
                error_polynom['mas'].append(i[2:])

            flag_minus = False
            flag_plus = False
            flag_number = False
            flag_star = False
            flag_begin = False
            number = 1
            continue

        print('Error with <{}>'.format(i))
        exit()
    if flag_number:
        dict_x['X^0'].append(-number if flag_equal else number)

    n = 0
    reduced = 'Reduced form: '
    for i in dict_x.keys():
        dict_x[i] = sum(dict_x[i])
        if (dict_x[i] < 0) and dict_x[i] != 0:
            reduced = reduced[:-3] + ' - ' + str(-dict_x[i]) + ' * ' + i + ' + '
        elif dict_x[i] != 0:
            reduced += str(dict_x[i]) + ' * ' + i + ' + '
        if dict_x[i] != 0:
            n = int(i[2:])
    if sum(dict_x.values()) != 0:
        reduced = reduced[:-2] + '= 0'
        print(reduced)
    else:
        print('Reduced form: 0 * X^0 = 0')


    if error_polynom['mas']:
        if error_polynom['k'] > n:
            print('Polynomial degree: {}'.format(error_polynom['k']))
            print("The polynomial degree is strictly greater than 2, I can't solve.")
        else:
            print('Polynomial degree: {}'.format(n))
            print("The polynomial I can't solve.")
            print('error degree is:')
            print(error_polynom['mas'])
        exit()
    else:
        print('Polynomial degree: {}'.format(n))

    return dict_x

def get_decision(argument):
    if (argument['X^0'] == 0 and argument['X^1'] == 0 and argument['X^2'] == 0):
        print('Infinitely many solutions')
    elif (argument['X^0'] != 0 and argument['X^1'] == 0 and argument['X^2'] == 0):
        print('There is no solution!')
        print('Error: {} != 0'.format(argument['X^0']))
    elif (argument['X^0'] == 0 and argument['X^1'] != 0 and argument['X^2'] == 0):
        print('The solution is:\n0.0')
    elif (argument['X^0'] == 0 and argument['X^1'] == 0 and argument['X^2'] != 0):
        print('The solution is\n0.0')
    elif (argument['X^0'] != 0 and argument['X^1'] != 0 and argument['X^2'] == 0):
        print('The solution is\n{}'.format(-argument['X^0']/argument['X^1']))
    elif (argument['X^0'] != 0 and argument['X^1'] == 0 and argument['X^2'] != 0):
        res = -argument['X^0']/argument['X^2']
        if (res >= 0):
            print('The solution is\n{}'.format(res ** 0.5))
        else:
            print('There is no solution!')
            print("Error, can't sqrt < 0\n x != sqrt({})".format(res))
    elif (argument['X^0'] == 0 and argument['X^1'] != 0 and argument['X^2'] != 0):
        print('Discriminant is strictly positive, the two solutions are:')
        print('0.0\n{}'.format(-argument['X^1']/argument['X^2']))
    else:
        a = 1
        b = argument['X^1']/argument['X^2']
        c = argument['X^0']/argument['X^2']
        D = b ** 2 - 4 * a * c
        print('a = {} b = {} c = {} D = {}'.format(a,b,c,D))
        if (D == 0):
            print('Discriminant is null, the one solutions are:\n{}'.format(-b/(2*a)))
        elif (D > 0):
            print('Discriminant is strictly positive, the two solutions are:')
            print('{}\n{}'.format((-b + D ** 0.5) / (2 * a), (-b - D ** 0.5) / (2 * a)))
        else:
            print("Discriminant is strictly negative, the two solutions are:")
            print('{} + {} * i'.format((-b / (2 * a)), ((-D) ** 0.5) / (2 * a)))
            print('{} - {} * i'.format((-b / (2 * a)), ((-D) ** 0.5) / (2 * a)))






if __name__ == "__main__":
    try:
        polynom = input()
        argument = get_argument(polynom)
        get_decision(argument)
    except ValueError:
        print('Error!')


