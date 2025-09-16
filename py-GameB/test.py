# import Account

# res = Account.CheckuserIdNotRepeat('13987654320')
# print(res)

def application(env,start_response):
    start_response('200 OK',[('Content-Type','text/html')])
    return [b"Hello World"]