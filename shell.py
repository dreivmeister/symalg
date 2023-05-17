import symalg

"""
der expr -> derivative of expr
eval expr var val -> expression where var is evaluated at val
simp expr -> return full simplify of expr

"""



fn = '<stdin>'
while True:
    expr = input('symalg> ')
    result, error = symalg.run(fn, expr)
    
    if error:
        print(error.as_string())
    else:
        print(result)