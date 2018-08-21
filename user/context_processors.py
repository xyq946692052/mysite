from .forms import LoginForm

def login_modal_form(request):    #参考request, 让login_form成为公共可用，
    return {'login_modal_form':LoginForm}