lim_inf = -10
lim_sup = 0


def ecuacion(x, y):
    return 2**x + 3**y


def valor_absoluto(valor):
    return abs(1 - valor)


def get_x_y():
    x = 0
    y = 0
    actual = ecuacion(x, y)
    anterior = 99999

    while (
        valor_absoluto(actual) < valor_absoluto(anterior)
        and x >= lim_inf
        and x <= lim_sup
    ):
        x -= 0.001
        y -= 0.001
        aux = ecuacion(x, y)
        anterior = actual
        actual = aux

    return x, y


def get_x(x=0, y=0):
    actual = ecuacion(x, y)
    anterior = 99999

    while (
        valor_absoluto(actual) < valor_absoluto(anterior)
        and x >= lim_inf
        and x <= lim_sup
    ):
        x -= 0.001
        aux = ecuacion(x, y)
        anterior = actual
        actual = aux
    x += 0.001

    return x


def get_y(x=0, y=0):
    actual = ecuacion(x, y)
    anterior = 99999

    while (
        valor_absoluto(actual) < valor_absoluto(anterior)
        and y >= lim_inf
        and y <= lim_sup
    ):
        y -= 0.001
        aux = ecuacion(x, y)
        anterior = actual
        actual = aux

    return y


if __name__ == "__main__":
    x, y = get_x_y()
    y = get_y(x, y)
    print("El mejor valor para x es: ", x)

    print("El mejor valor para y es: ", y)
