

def kitten(**kwargs):
    if len(kwargs):
        for k in kwargs:
            print('kwargs k: {}  val: {}'.format(k, kwargs[k]))
    else: print('end.')

def main():
    kitten(x_i = 'xx', y_i = 'yy', z_i = 'zz')


if __name__ == '__main__': main()
