def output(username,results):
    final_output = f'''
    ┌───────────────────────────────────────────────────────────────────────────────────────────┐
    | Scanned Username: \033[1;49;96m{username+' '*int(71-len(str(username)))}\033[0m |
    |-------------------------------------------------------------------------------------------|
    | SITE                           | URL                                                      |
    |-------------------------------------------------------------------------------------------|'''
    for sitio, detalles in results.items():
        if detalles['status'] == "FOUND":
            sitio_str = str(sitio) + ' ' * int(30 - len(str(sitio)))
            url_user_str = str(detalles['url_user']) + ' ' * int(56 - len(str(detalles['url_user'])))
            final_output += f'''\n    | \033[1;49;97m{sitio_str}\033[0m | {url_user_str} |'''

    final_output += f'''\n    └───────────────────────────────────────────────────────────────────────────────────────────┘'''
    
    return final_output